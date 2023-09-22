#!/bin/python3

# https://github.com/dropbox/dropbox-sdk-python/blob/main/example/updown.py

"""Sync files with Dropbox.

/OnlySnarf/post         -->     ~/.onlysnarf/uploads/post
/OnlySnarf/message      -->     ~/.onlysnarf/uploads/message

~/.onlysnarf/uploads/post       -->     /OnlySnarf/Uploads/post
~/.onlysnarf/uploads/message    -->     /OnlySnarf/Uploads/message


"""

from __future__ import print_function
from pathlib import Path

import argparse
import contextlib
import datetime
import os
import six
import sys
import time
import unicodedata

if sys.version.startswith('2'):
    input = raw_input  # noqa: E501,F821; pylint: disable=redefined-builtin,undefined-variable,useless-suppression

import dropbox
# from dropbox import DropboxOAuth2FlowNoRedirect

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

# OAuth2 access token.  TODO: login etc.
# TOKEN = str(os.getenv("DROPBOX_ACCESS_TOKEN"))

parser = argparse.ArgumentParser(description='Sync ~/.onlysnarf/uploads with Dropbox')
parser.add_argument('folder', nargs='?', default='Uploads', help='Folder name in your Dropbox')
parser.add_argument('rootdir', nargs='?', default='~/.onlysnarf/uploads', help='Local directory to sync with')
# parser.add_argument('--token', default=TOKEN, help='Access token (see https://www.dropbox.com/developers/apps)')
parser.add_argument('--yes', '-y', action='store_true', help='Answer yes to all questions')
parser.add_argument('--no', '-n', action='store_true', help='Answer no to all questions')
parser.add_argument('--default', '-d', action='store_true', help='Take default answer on all questions')

subparsers = parser.add_subparsers(help='Include a sub-command to run a corresponding action:', dest="action", required=True)
parser_config = subparsers.add_parser('download', help='> scan for downloads')
parser_config = subparsers.add_parser('upload', help='> scan for uploads')

def main():
    """Main program.

    Parse command line, then iterate over files and directories in 
    Dropbox rootdir and download all files. Skips some temporary files and
    directories, and avoids duplicate uploads by comparing size and
    mtime with the server.
    """
    args = parser.parse_args()
    if sum([bool(b) for b in (args.yes, args.no, args.default)]) > 1:
        print('At most one of --yes, --no, --default is allowed')
        sys.exit(2)
    # if not args.token:
    #     print('--token is mandatory')
    #     sys.exit(2)

    rootdir = os.path.expanduser(args["rootdir"])
    args["rootdir"] = rootdir
    print('Dropbox folder name:', args.folder)
    print('Local directory:', rootdir)
    if not os.path.exists(rootdir):
        print(rootdir, 'does not exist on your filesystem')
        sys.exit(1)
    elif not os.path.isdir(rootdir):
        print(rootdir, 'is not a folder on your filesystem')
        sys.exit(1)

    dbx = dropbox.Dropbox(
            app_key = str(os.getenv("DROPBOX_KEY")),
            app_secret = str(os.getenv("DROPBOX_SECRET")),
            oauth2_refresh_token = str(os.getenv("DROPBOX_REFRESH_TOKEN"))
        )

    if args.action == "download":
        sync_downloads(vars(args), dbx)
    elif args.action == "upload":
        sync_uploads(vars(args), dbx)

########################################################################################################################
########################################################################################################################
########################################################################################################################

def sync_downloads(args, dbx):
    listing = list_folder(dbx, args["folder"])
    downloadMe = []

    for list_ in listing:
        try:
            if isinstance(listing[list_], dropbox.files.FolderMetadata):
                pass
            elif isinstance(listing[list_], dropbox.files.FileMetadata) and listing[list_].is_downloadable:
                downloadMe.append(listing[list_])

        except Exception as e:
            if "has no attribute" not in str(e):
                print(e)

    for listing in downloadMe:
        path = os.path.join(args["rootdir"], args["folder"], listing.path_lower).replace("/uploads/Uploads", "/uploads") 
        path = (args["rootdir"] + path).replace("/uploads/uploads/", "/uploads/")
        if os.path.isfile(path):
            name = listing.name
            if not isinstance(name, six.text_type):
                name = name.decode('utf-8')
            nname = unicodedata.normalize('NFC', name)
            if name.startswith('.'):
                print('Skipping dot file:', name)
            elif name.startswith('@') or name.endswith('~'):
                print('Skipping temporary file:', name)
            elif name.endswith('.pyc') or name.endswith('.pyo'):
                print('Skipping generated file:', name)
            else:
                mtime = os.path.getmtime(path)
                mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                size = os.path.getsize(path)
                if (isinstance(listing, dropbox.files.FileMetadata) and
                        mtime_dt == listing.client_modified and size == listing.size):
                    print(name, 'is already synced [stats match]')
                else:
                    print(name, 'exists with different stats, downloading')
                    # res = download(dbx, folder, subfolder, name)
                    res = download_downloads(dbx, args["rootdir"], listing)
                    with open(path, 'rb') as f:
                        data = f.read()
                    if res == data:
                        print(name, 'is already synced [content match]')
                    else:
                        print(name, 'has changed since last sync')
                        if yesno('Refresh %s' % name, False, args):
                            upload_downloads(dbx, path, listing.path_display, overwrite=True)
        elif yesno('Download %s' % listing.name, True, args):
            download_downloads(dbx, args["rootdir"], listing)

            # # Then choose which subdirectories to traverse.
            # keep = []
            # for name in dirs:
            #     if name.startswith('.'):
            #         print('Skipping dot directory:', name)
            #     elif name.startswith('@') or name.endswith('~'):
            #         print('Skipping temporary directory:', name)
            #     elif name == '__pycache__':
            #         print('Skipping generated directory:', name)
            #     elif yesno('Descend into %s' % name, True, args):
            #         print('Keeping directory:', name)
            #         keep.append(name)
            #     else:
            #         print('OK, skipping directory:', name)
            # dirs[:] = keep

    dbx.close()
    return True # for tests

def sync_uploads(args, dbx):
    for dn, dirs, files in os.walk(args["rootdir"]):
        subfolder = dn[len(args["rootdir"]):].strip(os.path.sep)
        listing = list_folder(dbx, args["folder"], subfolder=subfolder)
        print('Descending into', subfolder, '...')

        # First do all the files.
        for name in files:
            fullname = os.path.join(dn, name)
            if not isinstance(name, six.text_type):
                name = name.decode('utf-8')
            nname = unicodedata.normalize('NFC', name)
            if name.startswith('.'):
                print('Skipping dot file:', name)
            elif name.startswith('@') or name.endswith('~'):
                print('Skipping temporary file:', name)
            elif name.endswith('.pyc') or name.endswith('.pyo'):
                print('Skipping generated file:', name)
            elif nname in listing:
                md = listing[nname]
                mtime = os.path.getmtime(fullname)
                mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                size = os.path.getsize(fullname)
                if (isinstance(md, dropbox.files.FileMetadata) and
                        mtime_dt == md.client_modified and size == md.size):
                    print(name, 'is already synced [stats match]')
                else:
                    print(name, 'exists with different stats, downloading')
                    res = download_uploads(dbx, args["folder"], subfolder, name)
                    with open(fullname, 'rb') as f:
                        data = f.read()
                    if res == data:
                        print(name, 'is already synced [content match]')
                    else:
                        print(name, 'has changed since last sync')
                        if yesno('Refresh %s' % name, False, args):
                            upload_uploads(dbx, fullname, args["folder"], subfolder, name,
                                   overwrite=True)
            elif yesno('Upload %s' % name, True, args):
                upload_uploads(dbx, fullname, args["folder"], subfolder, name)

        # Then choose which subdirectories to traverse.
        keep = []
        for name in dirs:
            if name.startswith('.'):
                print('Skipping dot directory:', name)
            elif name.startswith('@') or name.endswith('~'):
                print('Skipping temporary directory:', name)
            elif name == '__pycache__':
                print('Skipping generated directory:', name)
            elif yesno('Descend into %s' % name, True, args):
                print('Keeping directory:', name)
                keep.append(name)
            else:
                print('OK, skipping directory:', name)
        dirs[:] = keep

    dbx.close()
    return True # for tests

def list_folder(dbx, folder, subfolder=""):
    """List a folder.

    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """

    path = '/%s' % (folder)
    if subfolder:
        path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
    while '//' in path:
        path = path.replace('//', '/')
    path = path.rstrip('/')
    try:
        with stopwatch('list_folder'):
            res = dbx.files_list_folder(path, recursive=False if subfolder else True)
    except dropbox.exceptions.ApiError as err:
        print('Folder listing failed for', path, '-- assumed empty:', err)
        return {}
    else:
        rv = {}
        for entry in res.entries:
            rv[entry.name] = entry
        # print(rv)
        return rv

def download_downloads(dbx, folder, file):
    """Download a file.

    Return the bytes of the file, or None if it doesn't exist.
    """
    path = '/%s/%s' % (folder, file.path_lower.replace(os.path.sep, '/'))
    while "//" in path or "/uploads/uploads/" in path:
        path = path.replace("//", "/").replace("/uploads/uploads/", "/uploads/")
    Path(os.path.dirname(path)).mkdir(parents=True, exist_ok=True)
    # print("downloading: {}".format(file.path_display.replace("/Uploads","")))
    with stopwatch('download'):
        try:
            res = dbx.files_download_to_file(path, file.path_display)
            return res
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None
        except Exception as e:
            print(e)

def download_uploads(dbx, folder, subfolder, name):
    """Download a file.

    Return the bytes of the file, or None if it doesn't exist.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    with stopwatch('download'):
        try:
            md, res = dbx.files_download(path)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None
    data = res.content
    print(len(data), 'bytes; md:', md.path_display)
    return res

def upload_downloads(dbx, path, path_display, overwrite=False):
    """Upload a file.

    Return the request response, or None in case of error.
    """
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    mtime = os.path.getmtime(path)
    with open(path, 'rb') as f:
        data = f.read()
    with stopwatch('upload %d bytes' % len(data)):
        try:
            res = dbx.files_upload(
                data, path_display, mode,
                client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                mute=True)
        except dropbox.exceptions.ApiError as err:
            print('*** API error', err)
            return None
    print('uploaded as', res.name.encode('utf8'))
    return res

def upload_uploads(dbx, fullname, folder, subfolder, name, overwrite=False):
    """Upload a file.

    Return the request response, or None in case of error.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    mtime = os.path.getmtime(fullname)
    with open(fullname, 'rb') as f:
        data = f.read()
    with stopwatch('upload %d bytes' % len(data)):
        try:
            res = dbx.files_upload(
                data, path, mode,
                client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                mute=True)
        except dropbox.exceptions.ApiError as err:
            print('*** API error', err)
            return None
    print('uploaded as', res.name.encode('utf8'))
    return res

def yesno(message, default, args):
    """Handy helper function to ask a yes/no question.

    Command line arguments --yes or --no force the answer;
    --default to force the default answer.

    Otherwise a blank line returns the default, and answering
    y/yes or n/no returns True or False.

    Retry on unrecognized answer.

    Special answers:
    - q or quit exits the program
    - p or pdb invokes the debugger
    """
    if args["default"]:
        print(message + '? [auto]', 'Y' if default else 'N')
        return default
    if args["yes"]:
        print(message + '? [auto] YES')
        return True
    if args["no"]:
        print(message + '? [auto] NO')
        return False
    if default:
        message += '? [Y/n] '
    else:
        message += '? [N/y] '
    while True:
        answer = input(message).strip().lower()
        if not answer:
            return default
        if answer in ('y', 'yes'):
            return True
        if answer in ('n', 'no'):
            return False
        if answer in ('q', 'quit'):
            print('Exit')
            raise SystemExit(0)
        if answer in ('p', 'pdb'):
            import pdb
            pdb.set_trace()
        print('Please answer YES or NO.')

@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))

if __name__ == '__main__':
    main()
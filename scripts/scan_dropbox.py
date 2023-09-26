#!/bin/python3
# https://github.com/dropbox/dropbox-sdk-python/blob/main/example/updown.py

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

# if sys.version.startswith('2'):
#     input = raw_input  # noqa: E501,F821; pylint: disable=redefined-builtin,undefined-variable,useless-suppression

import dropbox

from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

parser = argparse.ArgumentParser(description='Sync ~/.onlysnarf/uploads with Dropbox')
parser.add_argument('folder', nargs='?', default='Uploads', help='Folder name in your Dropbox')
# parser.add_argument('--token', default=TOKEN, help='Access token (see https://www.dropbox.com/developers/apps)')
parser.add_argument('--yes', '-y', action='store_true', help='Answer yes to all questions')
parser.add_argument('--no', '-n', action='store_true', help='Answer no to all questions')
parser.add_argument('--default', '-d', action='store_true', help='Take default answer on all questions')

parser.add_argument('--directory', action='store_true', help='Prefer folders of files')

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
    print('Dropbox folder name:', args.folder)

    dbx = dropbox.Dropbox(
            app_key = str(os.getenv("DROPBOX_KEY")),
            app_secret = str(os.getenv("DROPBOX_SECRET")),
            oauth2_refresh_token = str(os.getenv("DROPBOX_REFRESH_TOKEN"))
        )

    scan(vars(args), dbx)

########################################################################################################################
########################################################################################################################
########################################################################################################################

def scan(args, dbx):
    dropbox_folders = list_folder(dbx, args["folder"])
    folders = []

    for list_ in dropbox_folders:
        try:
            if args["directory"] and isinstance(dropbox_folders[list_], dropbox.files.FolderMetadata):
                pass
            elif isinstance(dropbox_folders[list_], dropbox.files.FileMetadata) and dropbox_folders[list_].is_downloadable:
                folders.append(dropbox_folders[list_])
        except Exception as e:
            if "has no attribute" not in str(e):
                print(e)

    # MERGE SCAN PROCESSES / BEHAVIOR
    
    # find a config, files, or a folder to upload
    
    for listing in folders:
        path = os.path.join(args["folder"], listing.path_lower) 
        print(f"path: {path}")

    # check for a config near the located files or folder
    upload_config = ?

    # create a config or use one that was found
    upload_config = {}

    # update the config values to match pending upload 
    upload_object = {}

    # post / message
    # Post.create_post(upload_object).send()
    # Message.create_message(upload_object).send()

    dbx.close()
    
    # backup to dropbox backup folder / delete the files or folder (& config) 
    
    return True # for tests


# get share link that is capable of being downloaded
def get_share_link(dbx, path):
    try:
        shared_link_metadata = dbx.sharing_create_shared_link_with_settings(path)
        link = shared_link_metadata.url
        name = shared_link_metadata.name
    except Exception as e:
        shared_link_metadata = dbx.sharing_list_shared_links(path)
        link = shared_link_metadata.links[0]
        name = link.name
        link = link.url
    # formatting to allow downloads
    link = link.replace("dl=0", "dl=1")
    print(f"share link: {link}")
    return link

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
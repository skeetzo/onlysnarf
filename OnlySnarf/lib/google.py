#!/usr/bin/python3

# hide annoying google warning
import logging
logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)

import os
import shutil
import datetime
import json
import sys
import subprocess
import pathlib
import io
from subprocess import PIPE, Popen
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
# from moviepy.editor import VideoFileClip
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload,MediaIoBaseDownload
##
from ..util.settings import Settings

###################
##### Globals #####
###################

AUTH = False
CACHE = []
DRIVE = None
PYDRIVE = None
ONE_GIGABYTE = 1000000000
ONE_MEGABYTE = 1000000
FIFTY_MEGABYTES = 50000000
ONE_HUNDRED_KILOBYTES = 100000
OnlyFansFolder_ = None

# Video MimeTypes
# Flash   .flv    video/x-flv
# MPEG-4  .mp4    video/mp4
# iPhone Index    .m3u8   application/x-mpegURL
# iPhone Segment  .ts     video/MP2T
# 3GP Mobile  .3gp    video/3gpp
# QuickTime   .mov    video/quicktime
# A/V Interleave  .avi    video/x-msvideo
# Windows Media   .wmv    video/x-ms-wmv
MIMETYPES_IMAGES = "(mimeType contains 'image/jpeg' or mimeType contains 'image/jpg' or mimeType contains 'image/png')"
MIMETYPES_VIDEOS = "(mimeType contains 'video/mp4' or mimeType contains 'video/quicktime' or mimeType contains 'video/x-ms-wmv' or mimeType contains 'video/x-flv')"
MIMETYPES_ALL = "(mimeType contains 'image/jpeg' or mimeType contains 'image/jpg' or mimeType contains 'image/png' or mimeType contains 'video/mp4' or mimeType contains 'video/quicktime')"
MIMETYPE_FOLDER = "mimeType contains 'application/vnd.google-apps.folder'"

################
##### Auth #####
################

def authGoogle():
    """Authorizes Google Drive API"""

    Settings.dev_print("authenticating google")
    try:
        # PyDrive
        gauth = GoogleAuth()
        if os.path.exists("/opt/onlysnarf/settings.yaml"):
            gauth = GoogleAuth(settings_file="/opt/onlysnarf/settings.yaml")
        # Try to load saved client credentials
        gauth.LoadCredentialsFile(Settings.get_google_path())
        Settings.dev_print("loaded: google credentials")
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile(Settings.get_google_path())
        global PYDRIVE
        PYDRIVE = GoogleDrive(gauth)
        # Drive v3 API (alternative downloads)
        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = file.Storage(Settings.get_google_path())
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(Settings.get_secret_path(), SCOPES)
            creds = tools.run_flow(flow, store)
        global DRIVE
        DRIVE = build('drive', 'v3', http=creds.authorize(Http()))
    except Exception as e:
        Settings.dev_print(e)
        Settings.print('Error: Unable to Authenticate w/ Google')
        return False
    Settings.dev_print("authentication successful") 
    return True

def checkAuth():
    """Check if Google Drive is authorized, if not then authorize"""

    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    return AUTH

###########################################
##### Archiving / Creating / Deleting #####
###########################################

def backup_file(file):
    """
    Backs up file to Google Drive in OnlyFans/posted folder

    Parameters
    ----------
    file : Google File
        Google Drive file to backup

    """

    try:
        global PYDRIVE
        # get backup folder
        backupTo = get_folder_by_name("posted")
        # determine category of folder to backup into
        stri = "posted/{}".format(backupTo["title"])
        if file.category or Settings.get_category():
            category = file.category or Settings.get_category()
            # get the folder to back up to
            backupTo = get_posted_folder_by_name(category)
            # if performer, get the proper inner category folder
            if str(category) == "performers" and Settings.get_category_performer():
                backupTo = get_folder_by_name(Settings.get_category_performer(), parent=backupTo)
            stri = "posted/{}".format(backupTo["title"])

        # check posted for folder to backup with existing name
        file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and title='{}'".format(backupTo['id'], str(file.get_parent()["title"]))}).GetList()
        if len(file_list) == 0:
            parentFolder = PYDRIVE.CreateFile({'title':str(file.get_parent()["title"]), 'parents':[{"kind": "drive#fileLink", "id": str(backupTo['id'])}], 'mimeType':'application/vnd.google-apps.folder'})
        else:
            parentFolder = file_list[0]

        parentFolder.Upload()
        Settings.dev_print("moving to: {}".format(stri))
        # change parents of file to "move" it
        file.get_file()['parents'] = [{"kind": "drive#fileLink", "id": str(parentFolder['id'])}]
        file.get_file().Upload()
        Settings.print("File Backed Up: {}".format(file.get_title()))
    except Exception as e:
        Settings.dev_print(e)

def create_folders():
    """Create OnlySnarf category folders"""

    auth = checkAuth()
    if not auth: return
    Settings.print("Creating Folders: {}".format(Settings.get_drive_path()))
    # get root OnlySnarf folder in Drive
    OnlyFansFolder = get_folder_root()
    if OnlyFansFolder is None:
        Settings.err_print("unable to create category folders")
        return
    file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(OnlyFansFolder['id'])}).GetList()
    # create each missing folder
    for folder in Settings.get_categories():
        found = False
        for folder_ in file_list:
            if str(folder) == folder_['title']:
                Settings.maybe_print("found folder: {}".format(folder))
                found = True
        if not found:
            if not Settings.is_create_missing():
                Settings.maybe_print("skipping: create missing category folder - {}".format(folder))
                continue   
            Settings.maybe_print("created folder: {}".format(folder))
            contentFolder = PYDRIVE.CreateFile({"title": str(folder), "parents": [{"id": OnlyFansFolder['id']}], "mimeType": "application/vnd.google-apps.folder"})
            contentFolder.Upload()

def delete_folder(folder):
    """
    Delete folder

    Parameters
    ----------
    folder : Google Folder
        Google Drive folder to delete

    """

    if Settings.is_delete():
        try:
            Settings.print("Deleting folder: {}".format(folder["title"]))
            folder.Trash()
        except Exception as e: Settings.dev_print(e)

#################
##### Cache #####
#################

def cache_add(folders):
    """Add folder to local cache"""

    global CACHE
    for folder in folders:
        CACHE.append([folder['title'], folder])

def cache_check(folderName):
    """Check local cache for folder by name"""

    global CACHE
    for folder in CACHE:
        if str(CACHE[0]) == str(folderName):
            return CACHE[1]
    return False

####################
##### Download #####
####################

def download_file(file):
    """
    Download file using one of two methods

    1) PyDrive
    2) Google Drive - shows download %

    Parameters
    ----------
    file : Google File
        Google file to download

    Returns
    -------
    bool
        Whether or not the download was successful

    """

    Settings.maybe_print("downloading file: {}".format(file.get_title()))
    def method_one():
        try:
            with open(str(file.get_path()), 'w+b') as output:
                #Settings.print("8",end="",flush=True)
                request = DRIVE.files().get_media(fileId=file.get_id())
                downloader = MediaIoBaseDownload(output, request)
                #Settings.print("=",end="",flush=True)
                done = False
                while done is False:
                    #Settings.print("=",end="",flush=True)
                    status, done = downloader.next_chunk()
                    if int(Settings.get_verbosity()) >= 1:
                       Settings.print_same_line("Downloading: %d%%\r" % (status.progress() * 100))
                #Settings.print("D")
                Settings.maybe_print("download complete (1)")
        except Exception as e:
            Settings.dev_print(e)
            return False
        return True 
    def method_two():
        try:
            file.get_file().GetContentFile(file.get_path())
            Settings.maybe_print("download complete (2)")
        except Exception as e:
            Settings.dev_print(e)
            return False
        return True
    successful = method_one() or method_two()
    return successful

###############
##### Get #####
###############

def get_files_by_folder_id(folderID):
    """Get files of folder by id

    Parameters
    ----------
    folderID : str
        The folder id of the Google Folder to get the files of

    Returns
    -------
    list
        A list of Google Files in the matching folder

    """

    if not folderID:
        Settings.err_print("missing folder id")
        return
    auth = checkAuth()
    if not auth: return []
    return PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(folderID)}).GetList()
    
def get_file(id_):
    """Get file by id

    Parameters
    ----------
    id_ : str
        The id of the Google File to locate

    Returns
    -------
    Google File
        The located Google File

    """

    auth = checkAuth()
    if not auth: return
    myfile = PYDRIVE.CreateFile({'id': id_})
    # myfile.FetchMetadata()
    return myfile

def get_file_parent(id_):
    """
    Get parent file of file

    Parameters
    ----------
    id_ : str
        The id of the Google File to locate

    Returns
    -------
    Google Folder
        The located parent Google Folder

    """
    # auth = checkAuth()
    # if not auth: return
    # Settings.dev_print("getting file parent: {}".format(id_))
    parent = get_file(id_)["parents"][0]
    parent = PYDRIVE.CreateFile({'id': parent["id"]})
    return parent


def get_folder_by_name(folderName, parent=None):
    """
    Find folder by name with parent
    
    Parameters
    ----------
    folderName : str
        Name of folder to find
    parent : str
        Optional parent folder to search within 

    Returns
    -------
    Google Folder
        The located / created Google Folder

    """

    global CACHE
    if cache_check(folderName): return cache_check(folderName)
    auth = checkAuth()
    if not auth: return
    if str(folderName) in str(Settings.get_categories()) and not parent:
        parent = get_folder_root()
    if not parent: parent = get_folder_root()
    Settings.maybe_print("getting folder: {}".format(folderName))
    file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(parent['id'])}).GetList()
    for folder in file_list:
        if str(folder['title'])==str(folderName):
            Settings.maybe_print("found folder: {}".format(folderName))
            cache_add([folder])
            return folder
    if not Settings.is_create_missing():
        Settings.maybe_print("skipping: create missing folder - {}".format(folderName))
        return None
    # create if missing
    folder = PYDRIVE.CreateFile({"title": str(folderName), "mimeType": "application/vnd.google-apps.folder", "parents": [{"kind": "drive#fileLink", "id": parent["id"]}]})
    folder.Upload()
    Settings.maybe_print("created folder: {}".format(folderName))
    return folder

def get_images_of_folder(folder):
    """
    Get all image files of folder

    Parameters
    ----------
    folder : Google Folder
        The Google Folder to search for images

    Returns
    -------
    list
        The images located within the folder

    """

    image_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and {}".format(folder['id'], MIMETYPES_IMAGES)}).GetList()
    if len(image_list) > 0:
        Settings.dev_print("images: {}".format(len(image_list)))
    else:
        Settings.maybe_print("images folder (empty): {}".format(folder['title']))
        if Settings.is_delete_empty(): delete_folder(folder)
    return image_list

def get_videos_of_folder(folder):
    """
    Gets all video files of folder

    Parameters
    ----------
    folder : Google Folder
        The Google Folder to search for videos

    Returns
    -------
    list
        The videos located within the folder

    """

    video_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and {}".format(folder['id'], MIMETYPES_VIDEOS)}).GetList()
    if len(video_list) > 0:
        Settings.dev_print("videos: {}".format(len(video_list)))
    else:
        Settings.maybe_print("video folder (empty): {}".format(folder['title']))
        if Settings.is_delete_empty(): delete_folder(folder)
    return video_list

# returns first layer of files found
def get_folders_of_folder_by_keywords(folder):
    """
    Gets all folders in folder by the matching keywords

    Parameters
    ----------
    folder : Google Folder
        The Google Folder to search for keywords within

    Returns
    -------
    list
        The matching keyword folders located within folder

    """

    auth = checkAuth()
    if not auth: return []
    Settings.maybe_print("getting keywords in: {}".format(folder['title']))
    foundFolders = []
    folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and {}".format(folder['id'], MIMETYPE_FOLDER)}).GetList()
    for folder in folders:
        if Settings.get_drive_keyword() and str(folder['title']) != str(Settings.get_drive_keyword()):
            Settings.dev_print("{} -> not keyword".format(folder['title']))
            continue
        elif Settings.get_drive_ignore() and str(folder['title']) == str(Settings.get_drive_ignore()):
            Settings.dev_print("{} -> by not keyword".format(folder['title']))
            continue
        elif str(folder['title']) == str(Settings.get_drive_keyword):
            Settings.dev_print("{} -> by keyword".format(folder['title']))
        else:
            Settings.dev_print("{}".format(folder['title']))
        foundFolders.append(folder)
    if Settings.get_sort_method() == "ordered":
        foundFolders = sorted(foundFolders, key = lambda x: x["title"])
    return foundFolders

def get_posted_folder_by_name(folderName, parent=None):
    """
    Get folder in "posted" folders by name.

    Parameters
    ----------
    folderName : str
        Name of the folder to find
    parent : Google Folder
        Optional Google Folder to search in

    Returns
    -------
    Google Folder
        The Google Folder that matches the folderName

    """

    global CACHE
    if cache_check(folderName): return cache_check(folderName)
    auth = checkAuth()
    if not auth: return
    Settings.maybe_print("getting posted folder: {}".format(folderName))
    if parent is None:
        parent = get_folder_root()
    posted = None
    file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(parent['id'])}).GetList()
    for folder in file_list:
        if str(folder['title'])=="posted":
            Settings.maybe_print("found folder: posted")
            cache_add([folder])
            posted = folder
    if posted == None:
        if not Settings.is_create_missing():
            Settings.maybe_print("skipping: create missing folder - {}".format("posted"))
            return None        
        # create if missing
        posted = PYDRIVE.CreateFile({"title": str("posted"), "mimeType": "application/vnd.google-apps.folder", "parents": [{"kind": "drive#fileLink", "id": parent}]})
        posted.Upload()
        Settings.maybe_print("created folder: {}".format("posted"))
    folder= None
    file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(posted['id'])}).GetList()
    for folder_ in file_list:
        if str(folder_['title'])==str(folderName):
            Settings.maybe_print("found folder: {}".format(folderName))
            cache_add([folder_])
            return folder_
    if not Settings.is_create_missing():
        Settings.maybe_print("skipping: create missing folder - {}".format(folderName))
        return None
    # create if missing
    folder = PYDRIVE.CreateFile({"title": str(folderName), "mimeType": "application/vnd.google-apps.folder", "parents": [{"kind": "drive#fileLink", "id": posted['id']}]})
    folder.Upload()
    Settings.maybe_print("created folder: {}".format(folderName))
    cache_add([folder])
    return folder

def get_folders_of_folder(folder):
    """
    Get folders of folder.

    Parameters
    ----------
    folder : Google Folder
        The folder to get the folders of

    Returns
    -------
    list
        A list of the folders found

    """

    global CACHE
    if cache_check(folder): return cache_check(folder)
    auth = checkAuth()
    if not auth: return []
    Settings.maybe_print("getting folders of: {}".format(folder['title']))
    folders = []
    folder_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and {}".format(folder['id'], MIMETYPE_FOLDER)}).GetList()
    for folder in folder_list:
        file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(folder['id'])}).GetList()
        if len(file_list) > 0:
            Settings.maybe_print("found folder: {}".format(folder['title']))
            folders.append(folder)
        else:
            Settings.maybe_print("found folder (empty): {}".format(folder['title']))
            if Settings.is_delete_empty(): delete_folder(folder)
    cache_add(folders)
    return folders

# Creates the OnlyFans folder structure
def get_folder_root():
    """
    Gets the OnlySnarf root folder.

    Creates the OnlySnarf folder structure if missing.

    Returns
    -------
    Google Folder
        The root OnlySnarf folder

    """

    auth = checkAuth()
    if not auth: return
    global OnlyFansFolder_
    if OnlyFansFolder_ is not None:
        return OnlyFansFolder_
    OnlyFansFolder = None
    if Settings.get_drive_path() != "":
        mount_root = "root"
        root_folders = str(Settings.get_drive_path()).split("/")
        Settings.maybe_print("mount folders: {}".format("/".join(root_folders)))    
        for folder in root_folders:
            mount_root = get_folder_by_name(mount_root, parent=folder)
            if mount_root is None:
                mount_root = "root"
                Settings.warn_print("drive mount folder not found")
                break
        mount_root = get_folder_by_name(mount_root, parent=Settings.get_drive_root())
        if mount_root is None:
            mount_root = {"id":"root"}
            Settings.warn_print("drive mount folder not found")
        else:
            Settings.maybe_print("found root (alt): {}/{}".format(Settings.get_drive_path(), Settings.get_drive_root()))
        OnlyFansFolder = mount_root
    else:
        file_list = PYDRIVE.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for folder in file_list:
            if str(folder['title']) == str(Settings.get_drive_path()):
                OnlyFansFolder = folder
                Settings.maybe_print("found root: {}".format(Settings.get_drive_path()))
    if OnlyFansFolder is None:
        Settings.print("Creating Root: {}".format(Settings.get_drive_path()))
        OnlyFansFolder = PYDRIVE.CreateFile({"title": str(Settings.get_drive_path()), "mimeType": "application/vnd.google-apps.folder"})
        OnlyFansFolder.Upload()
    OnlyFansFolder_ = OnlyFansFolder
    return OnlyFansFolder_

##################
##### Upload #####
##################

def upload_file(file=None):
    """
    Upload file to Google Drive

    Parameters
    ----------
    file : Google File
        Google file to be uploaded

    Returns
    -------
    bool
        Whether or not the upload was successful

    """

    auth = checkAuth()
    if not auth: return False
    if not file:
        Settings.err_print("missing file")
        return False
    if Settings.is_debug():
        Settings.print("Skipping Google Upload (debug): {}".format(filename))
        return False
    elif not Settings.is_backup():
        Settings.print('Skipping Google Upload (disabled): {}'.format(filename))
        return False
    else:
        Settings.print('Google Upload (file): {}'.format(filename))
    uploadedFile = PYDRIVE.CreateFile({'title':str(file.get_title()), 'parents':[{"kind": "drive#fileLink", "id": str(file.get_parent()["id"])}],'mimeType':str(file.get_mimetype())})
    uploadedFile.SetContentFile(file.get_path())
    uploadedFile.Upload()
    return True

def upload_gallery(files=[]):
    """
    Upload files to folder.

    Parameters
    ----------
    files : list
        The list of files to upload

    Returns
    -------
    bool
        Whether or not the upload was successful

    """

    parent = get_folder_by_name("posted")
    if not parent:
        Settings.err_print("missing posted folder")
        return False
    if Settings.is_debug():
        Settings.print("Skipping Google Upload (debug): {}".format(path))
        return False
    elif not Settings.is_backup():
        Settings.print('Skipping Google Upload (disabled): {}'.format(path))
        return False
    else:
        Settings.print('Google Upload: {}'.format(path))
    tmp_folder = PYDRIVE.CreateFile({'title':str(datetime.datetime.now()), 'parents':[{"kind": "drive#fileLink", "id": str(parent['id'])}],'mimeType':'application/vnd.google-apps.folder'})
    tmp_folder.Upload()
    successful = False
    for file in files:
        setattr(file, "parent", tmp_folder)
        successful = upload_file(file=file)
    return successful

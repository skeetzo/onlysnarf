#!/usr/bin/python3
# 3/28/2019: Skeetzo

import random
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
from moviepy.editor import VideoFileClip
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload,MediaIoBaseDownload
##
from .settings import SETTINGS as settings
from .file import Google_File

###################
##### Globals #####
###################

AUTH = False
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

def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()

################
##### Auth #####
################

# Google Auth
def authGoogle():
    settings.maybePrint('Authenticating Google')
    try:
        # PyDrive
        gauth = GoogleAuth()
        # Try to load saved client credentials
        gauth.LoadCredentialsFile(settings.GOOGLE_PATH)
        settings.maybePrint('Loaded: Google Credentials')
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
        gauth.SaveCredentialsFile(settings.GOOGLE_PATH)
        global PYDRIVE
        PYDRIVE = GoogleDrive(gauth)
        # Drive v3 API
        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = file.Storage(settings.GOOGLE_PATH)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(settings.PATH_SECRET, SCOPES)
            creds = tools.run_flow(flow, store)
        global DRIVE
        DRIVE = build('drive', 'v3', http=creds.authorize(Http()))
    except Exception as e:
        # settings.maybePrint(e)
        print('Error: Unable to Authenticate w/ Google')
        # return False
    settings.maybePrint('Authentication Successful') 
    # return True

def checkAuth():
    global AUTH
    if not AUTH:
        AUTH = authGoogle()

################################
##### Archiving / Deleting #####
################################

# Deletes online file
def delete_file(file):
    try: file.get_file().Trash()
    except Exception as e: settings.devPrint(e)

# Archives posted file / folder by updating their parent id
# posted
# - [image, gallery, video, performer]
# -- [file / folders]
def backup_file(file):
    try:
        global PYDRIVE
        parentFolder = PYDRIVE.CreateFile({'title':str(file.get_folder_name()), 'parents':[{"kind": "drive#fileLink", "id": str(get_posted_folder_by_name(file.get_category())['id'])}],'mimeType':'application/vnd.google-apps.folder'})
        parentFolder.Upload()
        settings.devPrint("Moving To: posted/{}/{}".format(file.get_category(), file.get_folder_name()))
        file.get_file()['parents'] = [{"kind": "drive#fileLink", "id": str(parentFolder['id'])}]
        file.get_file().Upload()
        print("File Backed Up: {}".format(file['title']))
    except Exception as e:
        settings.maybePrint(e)

###################
##### Folders #####
###################

def create_folders():
    checkAuth()
    print("Creating Folders: {}".format(settings.ROOT_FOLDER))
    OnlyFansFolder = get_folder_root()
    if OnlyFansFolder is None:
        print("Error: Unable To Create Folders")
        return
    file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(OnlyFansFolder['id'])}).GetList()
    for folder in settings.DRIVE_FOLDERS:
        found = False
        for folder_ in file_list:
            if str(folder) == folder_['title']:
                settings.maybePrint("found: {}".format(folder))
                found = True
        if not found:
            settings.maybePrint("created: {}".format(folder))
            contentFolder = PYDRIVE.CreateFile({"title": str(folder), "parents": [{"id": OnlyFansFolder['id']}], "mimeType": "application/vnd.google-apps.folder"})
            contentFolder.Upload()

# def find_folder(parent, folderName):
#     checkAuth()
#     if str(parent) != "root":
#         parent = parent['id']
#     settings.maybePrint("Finding Folder: {}/{}".format(parent, folderName))
#     file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(parent)}).GetList()
#     for folder in file_list:
#         if str(folder['title']) == str(folderName):
#             return folder
#     print("Error: Unable to Find Folder - {}".format(folderName))
#     return None

def get_folder_by_name(folderName, parent=None):
    checkAuth()
    if str(parent) in str(settings.DRIVE_FOLDERS):
        parent = get_folder_by_name(parent)
    settings.maybePrint("Getting Folder: {}".format(folderName))
    if parent is None:
        parent = get_folder_root()
    file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(parent['id'])}).GetList()
    for folder in file_list:
        if str(folder['title'])==str(folderName):
            settings.maybePrint("Found Folder: {}".format(folderName))
            return folder
    if str(settings.CREATE_DRIVE) == "False":
        settings.maybePrint("Skipping: Create Missing Folder - {}".format(folderName))
        return None
    # create if missing
    folder = PYDRIVE.CreateFile({"title": str(folderName), "mimeType": "application/vnd.google-apps.folder", "parents": [{"kind": "drive#fileLink", "id": parent}]})
    folder.Upload()
    settings.maybePrint("Created Folder: {}".format(folderName))
    return folder

def get_posted_folder_by_name(folderName):
    checkAuth()
    settings.maybePrint("Getting Posted Folder: {}".format(folderName))
    if parent is None:
        parent = get_folder_root()
    posted = None
    file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(parent['id'])}).GetList()
    for folder in file_list:
        if str(folder['title'])=="posted":
            settings.maybePrint("Found Folder: posted")
            posted = folder
    if posted == None:
        if str(settings.CREATE_DRIVE) == "False":
            settings.maybePrint("Skipping: Create Missing Folder - {}".format("posted"))
            return None        
        # create if missing
        posted = PYDRIVE.CreateFile({"title": str("posted"), "mimeType": "application/vnd.google-apps.folder", "parents": [{"kind": "drive#fileLink", "id": parent}]})
        posted.Upload()
        settings.maybePrint("Created Folder: {}".format("posted"))
    folder= None
    file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(posted['id'])}).GetList()
    for folder_ in file_list:
        if str(folder_['title'])==str(folderName):
            settings.maybePrint("Found Folder: {}".format(folderName))
            return folder_
    if str(settings.CREATE_DRIVE) == "False":
        settings.maybePrint("Skipping: Create Missing Folder - {}".format(folderName))
        return None
    # create if missing
    folder = PYDRIVE.CreateFile({"title": str(folderName), "mimeType": "application/vnd.google-apps.folder", "parents": [{"kind": "drive#fileLink", "id": posted['id']}]})
    folder.Upload()
    settings.maybePrint("Created Folder: {}".format(folderName))
    return folder

def get_folders_of_folder(folderName, parent=None):
    checkAuth()
    settings.maybePrint("Getting Folders of: {}".format(folderName))
    folders = []
    folder_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name(folderName, parent=parent)['id'])}).GetList()
    for folder in folder_list:
        file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(folder['id'])}).GetList()
        if len(file_list) > 0:
            settings.maybePrint("Found Folder: {}".format(folder['title']))
            folders.append(folder)
        else:
            settings.maybePrint("Found Folder (empty): {}".format(folder['title']))
    return folders

# Creates the OnlyFans folder structure
def get_folder_root():
    checkAuth()
    global OnlyFansFolder_
    if OnlyFansFolder_ is not None:
        return OnlyFansFolder_
    OnlyFansFolder = None
    if settings.DRIVE_PATH is not None:
        mount_root = "root"
        root_folders = settings.DRIVE_PATH.split("/")
        settings.maybePrint("Mount Folders: {}".format("/".join(root_folders)))    
        for folder in root_folders:
            mount_root = get_folder_by_name(mount_root, parent=folder)
            # mount_root = find_folder(mount_root, folder)
            if mount_root is None:
                mount_root = "root"
                print("Warning: Drive Mount Folder Not Found")
                break
        mount_root = get_folder_by_name(mount_root, parent=settings.ROOT_FOLDER)
        # mount_root = find_folder(mount_root, settings.ROOT_FOLDER)
        if mount_root is None:
            mount_root = {"id":"root"}
            print("Warning: Drive Mount Folder Not Found")
        else:
            settings.maybePrint("Found Root (alt): {}/{}".format(settings.DRIVE_PATH, settings.ROOT_FOLDER))
        OnlyFansFolder = mount_root
    else:
        file_list = PYDRIVE.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for folder in file_list:
            if str(folder['title']) == str(settings.ROOT_FOLDER):
                OnlyFansFolder = folder
                settings.maybePrint("Found Root: {}".format(settings.ROOT_FOLDER))
    if OnlyFansFolder is None:
        print("Creating Root: {}".format(settings.ROOT_FOLDER))
        OnlyFansFolder = PYDRIVE.CreateFile({"title": str(settings.ROOT_FOLDER), "mimeType": "application/vnd.google-apps.folder"})
        OnlyFansFolder.Upload()
    OnlyFansFolder_ = OnlyFansFolder
    return OnlyFansFolder_

####################
##### Download #####
####################

def download_file(file):
    print("Downloading File: {}".format(file["title"]))
    # download file
    def method_two():
        file.GetContentFile(self.get_path())
        print("Download Complete (2)")
    def method_one():
        try:
            with open(str(self.get_path()), 'w+b') as output:
                # print("8",end="",flush=True)
                request = DRIVE.files().get_media(fileId=file["id"])
                downloader = MediaIoBaseDownload(output, request)
                # print("=",end="",flush=True)
                done = False
                while done is False:
                    # print("=",end="",flush=True)
                    status, done = downloader.next_chunk()
                    if str(settings.VERBOSE) == "True":
                        print("Downloading: %d%%\r" % (status.progress() * 100), end="")
                # print("D")
                print("Download Complete (1)")
        except Exception as e:
            settings.maybePrint(e)
            return False
        return True 
    successful = method_one() or method_two()
    return successful

###############
##### Get #####
###############

def get_files_by_folder_id(folderID):
    if not folderID:
        print("Error: Missing Folder ID")
        return
    checkAuth()
    global PYDRIVE
    file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(folderID)}).GetList()
    files = []
    for file in file_list:
        file_ = Google_File()
        setattr(file_, "id", file["id"])
        setattr(file_, "file", file)
        files.append(file_)
    return files

def get_file(id_):
    myfile = PYDRIVE.CreateFile({'id': id_})
    return myfile


















































# these need to be combined into this general top category
# but it also needs to check folder names for bykeyword/notkeyword 
# needs to return folders of content
# use def get_folders_of_folder(folderName, parent=None):


def get_files_by_category(category):
    print("Getting: {}".format(category))
    folder = get_folder_name(category)
    image_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()
    video_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_VIDEOS)}).GetList()
    file_list = []
    for i in image_list: file_list.append(i)
    for v in video_list: file_list.append(v)
    folder_size = len(file_list)
    settings.maybePrint('Images: {}'.format(len(image_list)))
    settings.maybePrint('Videos: {}'.format(len(video_list)))
    settings.maybePrint('Total: {}'.format(folder_size))
    files = []
    for file in file_list:
        file_ = File()
        setattr(file_, "file", file)
        setattr(file_, "parent", folder)
        files.append(file_)
    return files

# gets all the images in the images folders
def get_images():
    checkAuth()
    print('Getting Images')
    images_folder = get_folder_by_name("images")
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(images_folder['id'])}).GetList()
    images_list = []
    for folder in random_folders:
        if settings.BYKEYWORD != None and str(settings.BYKEYWORD) != str(folder['title']):
            settings.maybePrint('-> not keyword')
            continue
        elif settings.NOTKEYWORD != None and str(settings.NOTKEYWORD) != str(folder['title']):
            settings.maybePrint('-> by not keyword')
            continue
        images_list.append([images_folder, folder])
        settings.maybePrint("checking folder: {}".format(folder['title']))
        images_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()      
        for image_file in images_list_tmp:
            # images_list.append({"folder":folder['title'],"folder_id":folder['id'],"id":image_file['id'],"image":image_file['title']})
            file = Google_File()
            setattr(file, "parent", folder)
            setattr(file, "file", image_file)
            images_list.append(file)
    if len(images_list)==0:
        print('Warning: Missing Message Files')
        return []
    return images_list

def get_galleries():
    checkAuth()
    print('Getting Galleries')
    gallery_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("galleries")['id'])}).GetList()
    folder_list = []
    random_gallery = None
    folder_name = None
    if gallery_folders == None:
        print("Error: Unable to Connect to Google Drive")
        return []
    for folder in gallery_folders:
        if str(settings.VERBOSE) == "True":
            print('checking galleries: {}'.format(folder['title']),end="")
        gallery_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
        if settings.BYKEYWORD != None and str(settings.BYKEYWORD) != str(folder['title']):
            settings.maybePrint('-> not keyword')
            continue
        elif settings.NOTKEYWORD != None and str(settings.NOTKEYWORD) != str(folder['title']):
            settings.maybePrint('-> by not keyword')
            continue
        if len(gallery_list_tmp)>0:
            folder_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    galleries = []
    for folder in folder_list:
        if str(settings.VERBOSE) == "True":
            print('checking gallery: {}'.format(folder['title']),end="")
        gallery_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
        for folder_ in gallery_list_tmp:
            gallery_list_tmp_tmp = PYDRIVE.ListFile({'q': "'"+folder_['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()
            if len(gallery_list_tmp_tmp)>0:
                folder_name = folder['title']
                settings.maybePrint(" -> found")
                folder__ = Folder()
                setattr(folder__, "files", gallery_list_tmp_tmp)
                galleries.append(folder__)
            else:
                settings.maybePrint(" -> empty")
    print('Galleries: '+str(len(galleries)))
    return galleries

def get_videos():
    checkAuth()
    print('Getting Videos')
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("videos")['id'])}).GetList()
    video_list = []
    random_video = None
    folder_name = None
    if random_folders == None:
        print("Error: Unable to Connect to Google Drive")
        return video_list
    for folder in random_folders:
        if str(settings.VERBOSE) == "True":
            print("checking folder: {}".format(folder['title']),end="")
        video_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_VIDEOS)}).GetList()
        if settings.BYKEYWORD != None and str(settings.BYKEYWORD) != str(folder['title']):
            settings.maybePrint('-> not keyword')
            continue
        elif settings.NOTKEYWORD != None and str(settings.NOTKEYWORD) != str(folder['title']):
            settings.maybePrint('-> by not keyword')
            continue
        if len(video_list_tmp)>0:
            video_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    if len(video_list)==0: print('Warning: Missing Video File')
    folder_ = Folder()
    setattr(folder_, "files", video_list)
    return folder_

# gets all the images in the messages folders
def get_message_image(folderName):
    checkAuth()
    print('Getting Message Image: {}'.format(folderName))
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("messages")['id'])}).GetList()
    images_list = []
    random_image = None
    folder_name = None
    for folder in random_folders:
        if folder['title'] != str(folderName):
            continue
        if str(settings.VERBOSE) == "True":
            print("checking folder: {}".format(folder['title']),end="")
        images_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()      
        if settings.BYKEYWORD != None and str(settings.BYKEYWORD) != str(folder['title']):
            settings.maybePrint('-> not keyword')
            continue
        elif settings.NOTKEYWORD != None and str(settings.NOTKEYWORD) != str(folder['title']):
            settings.maybePrint('-> by not keyword')
            continue
        if len(images_list_tmp)>0:
            images_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    if len(images_list)==0:
        print('Error: Missing Image File')
        return {"file":"","keywords":""}
    random_image = random.choice(images_list)
    folder_name = random_image['title'];
    print('Messages Folder: '+random_image['title'])
    random_image = PYDRIVE.ListFile({'q': "'"+random_image['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()
    random_image = random.choice(random_image)
    print('Messages Image: '+random_image['title'])
    file = Google_File()
    setattr(file, "file", random_image)
    setattr(file, "keywords", str(folder_name))
    return file



























##################
##### Upload #####
##################

def upload_file(file=None):
    checkAuth()
    if not file:
        print("Error: Missing File")
        return False
    if str(settings.FORCE_BACKUP) == "True":
        print("Google Upload (forced): {}".format(filename))
    elif str(settings.DEBUG) == "True":
        print("Skipping Google Upload (debug): {}".format(filename))
        return
    elif str(settings.BACKUP) == "False":
        print('Skipping Google Upload (disabled): {}'.format(filename))
        return
    elif str(settings.SKIP_BACKUP) == "True":
        print('Skipping Backup: {}'.format(filename))
        return
    else:
        print('Google Upload (file): {}'.format(filename))
    # if not mimetype:
    #     print("Error: Missing Mimetype")
    #     return
    
    # file_metadata = {
    #     'name': str(filename),
    #     'mimeType': str(mimetype),
    #     'parents': [{"kind": "drive#fileLink", "id": str(parent['id'])}]
    # }
    # media = MediaFileUpload(path, mimetype=str(mimetype), resumable=True)
    # file = DRIVE.files().create(body=file_metadata, media_body=media, fields='id').execute()
    uploadedFile = PYDRIVE.CreateFile({'title':str(file.get_title()), 'parents':[{"kind": "drive#fileLink", "id": str(file.get_parent_id())}],'mimeType':str(file.get_mimetype())})
    uploadedFile.SetContentFile(file.get_path())
    uploadedFile.Upload()
    # print('File ID: {}'.format(file.get('id')))

def upload_gallery(files=[]):
    parent = get_folder_by_name("posted")
    if not parent:
        print("Error: Missing Posted Folder")
        return
    if str(settings.FORCE_BACKUP) == "True":
        print("Google Upload (forced): {}".format(path))
    elif str(settings.DEBUG) == "True":
        print("Skipping Google Upload (debug): {}".format(path))
        return
    elif str(settings.BACKUP) == "False":
        print('Skipping Google Upload (disabled): {}'.format(path))
        return
    elif str(settings.SKIP_BACKUP) == "True":
        print('Skipping Backup (gallery): {}'.format(path))
        return
    else:
        print('Google Upload: {}'.format(path))
    # file_metadata = {
    #     'name': str(datetime.datetime.now()),
    #     'mimeType': str("application/vnd.google-apps.folder"),
    #     'parents': [{"kind": "drive#fileLink", "id": str(parent['id'])}]
    # }
    # media = MediaFileUpload(path, mimetype="application/vnd.google-apps.folder", resumable=True)
    # parent = DRIVE.files().create(body=file_metadata, fields='id').execute()
    tmp_folder = PYDRIVE.CreateFile({'title':str(datetime.datetime.now()), 'parents':[{"kind": "drive#fileLink", "id": str(parent['id'])}],'mimeType':'application/vnd.google-apps.folder'})
    tmp_folder.Upload()
    for file in files:
        setattr(file, "parent", tmp_folder)
        upload_file(file=file)

def upload_input(path=None):
    if not path: path = settings.INPUT
    if os.path.isdir(path):
        upload_gallery(path=path)
    else:
        upload_file(path=path)

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
from .settings import SETTINGS as settings

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
        return False
    settings.maybePrint('Authentication Success') 
    return True

def checkAuth():
    global AUTH
    if not AUTH:
        AUTH = authGoogle()

################################
##### Archiving / Deleting #####
################################

# Deletes online file
def delete_file(file):
    checkAuth()
    if str(settings.SKIP_DOWNLOAD) == "True":
        print("Warning: Unable to Delete, skipped download")
        return True
    if str(settings.FORCE_DELETE) == "True":
        print("Deleting (Forced): {}".format(fileName))
    elif str(settings.DEBUG) == "True":
        print("Skipping Delete (Debug): {}".format(fileName))
        return
    elif str(settings.DELETE_GOOGLE) == "False":
        print('Skipping Delete (Disabled): {}'.format(fileName))
        return
    elif str(settings.SKIP_DELETE_GOOGLE) == "True":
        print('Skipping Delete: {}'.format(file['title']))
        return
    else:
        print('Deleting: {}'.format(fileName))
    file.Trash()

# Archives posted file / folder
def move_file(file):
    checkAuth()
    if str(settings.SKIP_DOWNLOAD) == "True":
        print("Warning: Unable to Backup, skipped download")
        return True
    if str(settings.FORCE_BACKUP) == "True":
        print("Backing Up (forced): {}".format(file['title']))
    elif str(settings.DEBUG) == "True":
        print("Skipping Backup (debug): {}".format(file['title']))
        return
    elif str(settings.BACKUP) == "False":
        print('Skipping Backup (disabled): {}'.format(file['title']))
        return
    elif str(settings.SKIP_BACKUP) == "True":
        print('Skipping Backup: {}'.format(file['title']))
        return
    else:
        print('Backing Up (file): {}'.format(file['title']))
    file['parents'] = [{"kind": "drive#fileLink", "id": str(get_folder_by_name("posted")['id'])}]
    file.Upload()
    print('Google File Backed Up: {}'.format(file['title']))

def move_files(fileName, files):
    checkAuth()
    if str(settings.SKIP_DOWNLOAD) == "True":
        print("Warning: Unable to Backup, skipped download")
        return True
    if str(settings.FORCE_BACKUP) == "True":
        print("Backing Up (forced): {}".format(fileName))
    elif str(settings.DEBUG) == "True":
        print("Skipping Backup (debug): {}".format(fileName))
        return
    elif str(settings.BACKUP) == "False":
        print('Skipping Backup (disabled): {}'.format(fileName))
        return
    elif str(settings.SKIP_BACKUP) == "True":
        print('Skipping Backup: {}'.format(file['title']))
        return
    else:
        print('Backing Up (gallery): {}'.format(fileName))
    title = fileName+" - "+datetime.datetime.now().strftime("%d-%m@%I-%M")
    settings.maybePrint('Moving To: '+title)
    global PYDRIVE
    tmp_folder = PYDRIVE.CreateFile({'title':str(title), 'parents':[{"kind": "drive#fileLink", "id": str(get_folder_by_name("posted")['id'])}],'mimeType':'application/vnd.google-apps.folder'})
    tmp_folder.Upload()
    settings.maybePrint("Backing Up:")
    for file in files:
        settings.maybePrint(" - {}".format(file['title']))
        file['parents'] = [{"kind": "drive#fileLink", "id": tmp_folder['id']}]
        file.Upload()
    print('Google Files Backed Up: {}'.format(title))

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

def find_folder(parent, folderName):
    checkAuth()
    global PYDRIVE
    if str(parent) != "root":
        parent = parent['id']
    settings.maybePrint("Finding Folder: {}/{}".format(parent, folderName))
    file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(parent)}).GetList()
    for folder in file_list:
        if str(folder['title']) == str(folderName):
            return folder
    print("Error: Unable to Find Folder - {}".format(folderName))
    return None

def get_files_of_folder(folderName, parent=None):
    folder = get_folder_by_name(folderName, parent=parent)
    global PYDRIVE
    files = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType != 'application/vnd.google-apps.folder'"}).GetList()      
    return files

def get_folder_by_name(folderName, parent=None):
    checkAuth()
    if str(parent) == "galleries" or str(parent) == "images" or str(parent) == "videos" or str(parent) == "performers":
        parent = get_folder_by_name(parent)
    settings.maybePrint("Getting Folder: {}".format(folderName))
    global PYDRIVE
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
    folder = PYDRIVE.CreateFile({"title": str(folderName), "mimeType": "application/vnd.google-apps.folder", "parents": [{"kind": "drive#fileLink", "id": OnlyFansFolder}]})
    folder.Upload()
    settings.maybePrint("Created Folder: {}".format(folderName))
    return folder

def get_folders_of_folder(folderName, parent=None):
    checkAuth()
    settings.maybePrint("Getting Folders of: {}".format(folderName))
    global PYDRIVE
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
    global PYDRIVE
    global OnlyFansFolder_
    if OnlyFansFolder_ is not None:
        return OnlyFansFolder_
    OnlyFansFolder = None
    if settings.DRIVE_PATH is not None:
        mount_root = "root"
        root_folders = settings.DRIVE_PATH.split("/")
        settings.maybePrint("Mount Folders: {}".format("/".join(root_folders)))    
        for folder in root_folders:
            mount_root = find_folder(mount_root, folder)
            if mount_root is None:
                mount_root = "root"
                print("Warning: Drive Mount Folder Not Found")
                break
        mount_root = find_folder(mount_root, settings.ROOT_FOLDER)
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

# Download File
def download_file(file, REPAIR=False):
    if not file:
        print("Error: Missing File")
        return
    tmp = settings.getTmp()
    if str(settings.SKIP_DOWNLOAD) == "True":
        print("Skipping Download (debug)")
        settings.update_value("input",tmp)
        return {"path":tmp}
    checkAuth()
    print('Downloading File: {}'.format(file['title']))
    # download file
    name = os.path.splitext(file['title'])[0]
    ext = os.path.splitext(file['title'])[1].lower()
    if not ext:
        ext = '.mp4'
        settings.maybePrint('ext (default): '+str(ext))
    else:
        settings.maybePrint('ext: '+str(ext))
    name = "{}{}".format(name, ext)
    tmp = os.path.join(tmp, name)
    settings.maybePrint("name: {}".format(name))
    settings.maybePrint('path: '+str(tmp))
    if str(ext).lower() == ".mp4":
        try:
            with open(tmp, 'w+b') as output:
                # print("8",end="",flush=True)
                file_id = file['id']
                request = DRIVE.files().get_media(fileId=file['id'])
                downloader = MediaIoBaseDownload(output, request)
                # print("=",end="",flush=True)
                done = False
                while done is False:
                    # print("=",end="",flush=True)
                    status, done = downloader.next_chunk()
                    if str(settings.VERBOSE) == "True":
                        print("Downloading: %d%%\r" % (status.progress() * 100),end="")
                # print("D")
                print("Download Complete: Regular")
        except Exception as e:
            settings.maybePrint(e)
            file.GetContentFile(tmp)
            print("Download Complete: Alternative")
        if REPAIR:
            tmp = repair(tmp)
        global FIFTY_MEGABYTES
        if int(os.stat(str(tmp)).st_size) >= FIFTY_MEGABYTES or settings.FORCE_REDUCTION: # greater than 1GB
            tmp = reduce(tmp)
        tmp = thumbnail_fix(tmp)
    else:
        file.GetContentFile(tmp)
        print("Download Complete: Alt")
    ### Finish ###
    if not os.path.isfile(str(tmp)):
        print("Error: Missing Downloaded File")
        return False
    size = os.path.getsize(tmp)
    settings.maybePrint("File Size: {}kb - {}mb".format(size/1000, size/1000000))
    global ONE_MEGABYTE
    if size <= ONE_MEGABYTE:
        settings.maybePrint("Warning: Small File Size")
    global ONE_HUNDRED_KILOBYTES
    if size <= ONE_HUNDRED_KILOBYTES:
        settings.maybePrint("Error: File Size Too Small")
        print("Error: Download Failure")
        return False
    settings.update_value("input",tmp)
    print('Downloaded: File')
    return {"path":tmp}

# Download Gallery
def download_gallery(folder):
    if not folder:
        print("Error: Missing Folder")
        return
    tmp = settings.getTmp()
    if str(settings.SKIP_DOWNLOAD) == "True":
        print("Skipping Download (debug)")
        settings.update_value("input",tmp)
        return {"path":tmp,"files":[]}
    checkAuth()
    print('Downloading Gallery: {}'.format(folder['title']))
    # download folder
    global PYDRIVE
    file_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()
    folder_size = len(file_list)
    settings.maybePrint('Folder size: '+str(folder_size))
    settings.maybePrint('Upload limit: '+str(settings.IMAGE_UPLOAD_LIMIT))
    if int(folder_size) == 0:
        print('Error: Empty Folder')
        return False
    random.shuffle(file_list)
    file_list = file_list[:int(settings.IMAGE_UPLOAD_LIMIT)]
    i = 1
    for file in sorted(file_list, key = lambda x: x['title']):
        print('Downloading: {} ({}/{})'.format(file['title'], i, folder_size))
        settings.maybePrint('filePath: '+os.path.join(tmp, str(file['title'])))
        file.GetContentFile(os.path.join(tmp, str(file['title'])))
        i+=1
    print('Downloaded: Gallery')
    settings.update_value("input",tmp)
    return {"path":tmp,"files":file_list}

def download_message_image(folderName="random"):
    print('Fetching Image')
    file = {}
    data = {}
    try:
        file = get_message_image(folderName)
        data = download_file(file.get("file"))
    except Exception as e:
        settings.maybePrint(e)
        return {}
    settings.update_value("input",data.get("path"))
    return {"path":data.get("path"), "file":file.get("file")}

def download_content(folder):
    if not folder:
        print("Error: Missing Folder")
        return
    checkAuth()
    print('Downloading Content: {}'.format(folder['title']))
    # mkdir /tmp
    global PYDRIVE
    content_title = folder['title']
    # download folder
    # file_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and (mimeType contains 'image/jpeg' or mimeType contains 'image/jpg' or mimeType contains 'image/png' or (mimeType contains 'video/mp4' or mimeType contains 'video/quicktime'))"}).GetList()
    image_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()
    video_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_VIDEOS)}).GetList()
    file_list = []
    for i in image_list: file_list.append(i)
    for v in video_list: file_list.append(v)
    folder_size = len(file_list)
    settings.maybePrint('Images: {}'.format(len(image_list)))
    settings.maybePrint('Videos: {}'.format(len(video_list)))
    settings.maybePrint('Total: {}'.format(folder_size))
    # settings.maybePrint("Files: {}".format(file_list))
    content = {}
    file = None
    # if it contains only 1 file, I want to download a file
    if int(folder_size) == 1:
        file = file_list[0]
        content = download_file(file)
    # if it contains multiple images, I want to download a gallery
    elif int(len(image_list)) > 1:
        file = content_found
        content = download_gallery(file)
    # if it contains only 1 image, I want to download a file
    elif int(len(image_list)) == 1:
        file = image_list[0]
        content = download_gallery(file)
    # if it contains at least 1 video, I want to download a random file
    elif int(len(video_list)) >= 1:
        file = file_list[0]
        content = download_file(file)
    elif int(folder_size) == 0:
        print("Warning: Missing Files")
    content["file"] = file
    content["keywords"] = content_title
    print('Downloaded: Content')
    return content

# Download Performer
def download_performer(folder):
    if not folder:
        print("Error: Missing Folder")
        return
    checkAuth()
    print('Downloading Performer: {}'.format(folder['title']))
    # mkdir /tmp
    tmp = settings.getTmp()
    global PYDRIVE
    content_folders = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    content_found = []
    random_content = None
    content_title = None
    for folder in content_folders:
        settings.maybePrint('content: '+folder['title'])
        content_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_ALL)}).GetList()
        # video_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and (mimeType contains 'image/jpeg' or mimeType contains 'image/jpg' or mimeType contains 'image/png')"}).GetList()
        # image_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'video/mp4'"}).GetList()
        if len(content_list) == 0:
            settings.maybePrint('- skipping empty content: '+folder['title'])
        if len(content_list) > 0:
            settings.maybePrint('- content galleries found: '+folder['title'])
            content_found.append(folder)
    if len(content_found)==0:
        print('Warning: Missing Content Folder')
        return {}
    content_found = random.choice(content_found)
    content_title = content_found['title']
    settings.maybePrint("Folder: {}".format(content_title))
    content = download_content(content_found)
    print('Downloaded: Performer')
    return content

# Download Scene
def download_scene(sceneFolder):
    checkAuth()
    print('Downloading Scene')
    tmp = settings.getTmp()
    global PYDRIVE
    content = None
    preview = None
    folder_list = PYDRIVE.ListFile({'q': "'"+sceneFolder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    for folder in folder_list:
        if folder['title'] == "content":
            content = folder
            settings.maybePrint("Content Folder: "+folder['id'])
        elif folder['title'] == "preview":
            preview = folder
            settings.maybePrint("Preview Folder: "+folder['id'])
    data = PYDRIVE.ListFile({'q': "'"+sceneFolder['id']+"' in parents and trashed=false and mimeType contains 'text/plain'"}).GetList()
    if len(data) == 0:
        print("Error: Missing Scene Data")
        return
    data = data[0]
    if data is None:
        print("Error: Missing Scene Data")
        return
    if content is None:
        print("Error: Missing Scene Content Folder")
        return
    if preview is None:
        print("Error: Missing Scene Preview Folder")
        return
    # tries to download as gallery first, then finds first video file
    content_ = None
    try:
        content_ = download_gallery(content)
    except Exception as e:
        print("1:" +str(e))
    if content_ is None:
        try:
            content_ = PYDRIVE.ListFile({'q': "'"+content['id']+"' in parents and trashed=false and mimeType != 'application/vnd.google-apps.folder'"}).GetList()
            content_ = download_file(content_[0])
        except Exception as e:
            print("2: "+str(e))
    content = content_
    if content is None:
        print("Error: Unable to Find Content")
        return
    # move content to tmp/content
    tmp_content = os.path.join(content[1], "content")
    settings.maybePrint("Old Content Path: {}".format(content[1]))
    settings.maybePrint("New Content Path: {}".format(tmp_content))
    os.mkdir(tmp_content)
    for file in os.listdir(content[1]):
        file = os.path.join(content[1], file) 
        settings.maybePrint("Moving: {}".format(file))
        shutil.move(file, tmp_content)
    data.GetContentFile(os.path.join(tmp, "data.json"))
    # read data.json    
    with open(os.path.join(tmp, "data.json"), 'r', encoding='utf-8') as f:
        data = json.load(f)
    settings.maybePrint("data.json: {}".format(data))
    preview = PYDRIVE.ListFile({'q': "'"+preview['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()
    if len(preview) == 0:
        print("Error: Missing Scene Preview")
        return
    preview = preview[0]
    preview = download_file(preview)
    if "mp4" in preview:
        preview = thumbnail_fix(preview)
    if data is None:
        print("Error: Missing Scene Data")
        return
    if content is None:
        print("Error: Missing Scene Content")
        return
    if preview is None:
        print("Error: Missing Scene Preview")
        return
    print('Downloaded: Scene')
    return {"path":tmp_content,"preview":preview,"data":data,"content":content}

###############
##### Get #####
###############

# gets all the images in the images folders
def get_images():
    checkAuth()
    print('Getting Images')
    global PYDRIVE
    images_folder = get_folder_by_name("images")
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(images_folder['id'])}).GetList()
    images_list = []
    for folder in random_folders:
        images_list.append([images_folder, folder])
        settings.maybePrint('checking folder: '+folder['title'])
        images_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()      
        for image_file in images_list_tmp:
            # images_list.append({"folder":folder['title'],"folder_id":folder['id'],"id":image_file['id'],"image":image_file['title']})
            images_list.append([folder, image_file])
    if len(images_list)==0:
        print('Warning: Missing Message Files')
        return
    return images_list

# gets all the images in the messages folders
def get_message_image(folderName):
    checkAuth()
    print('Getting Message Image: {}'.format(folderName))
    global PYDRIVE
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("messages")['id'])}).GetList()
    images_list = []
    random_image = None
    folder_name = None
    for folder in random_folders:
        if folder['title'] != str(folderName):
            continue
        if str(settings.VERBOSE) == "True":
            print('checking folder: '+folder['title'],end="")
        images_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()      
        if settings.BYKEYWORD != None and str(settings.BYKEYWORD) != str(folder['title']):
            settings.maybePrint('-> not keyword')
            continue
        elif settings.NOTKEYWORD != None and str(settings.NOTKEYWORD) == str(folder['title']):
            settings.maybePrint('-> by not keyword')
            continue
        if len(images_list_tmp)>0:
            images_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    if len(images_list)==0:
        print('Error: Missing Image File')
        return {}
    random_image = random.choice(images_list)
    folder_name = random_image['title'];
    print('Messages Folder: '+random_image['title'])
    random_image = PYDRIVE.ListFile({'q': "'"+random_image['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()
    random_image = random.choice(random_image)
    print('Messages Image: '+random_image['title'])
    return {"file":random_image}

# Downloads random image from Google Drive
def get_random_image():
    checkAuth()
    print('Getting Random Image')
    global PYDRIVE
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("images")['id'])}).GetList()
    images_list = []
    random_image = None
    folder_name = None
    for folder in random_folders:
        if str(settings.VERBOSE) == "True":
            print('checking folder: '+folder['title'],end="")
        images_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()      
        if settings.BYKEYWORD != None and str(settings.BYKEYWORD) != str(folder['title']):
            settings.maybePrint('-> not keyword')
            continue
        elif settings.NOTKEYWORD != None and str(settings.NOTKEYWORD) == str(folder['title']):
            settings.maybePrint('-> by not keyword')
            continue
        if len(images_list_tmp)>0:
            images_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    if len(images_list)==0:
        print('Error: Missing Image File')
        return {}
    random_image = random.choice(images_list)
    folder_name = random_image['title'];
    print('Random Folder: '+random_image['title'])
    random_image = PYDRIVE.ListFile({'q': "'"+random_image['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()
    random_image = random.choice(random_image)
    print('Random Image: '+random_image['title'])
    return {"file":random_image,"keywords":folder_name}

# Downloads random gallery from Google Drive
def get_random_gallery():
    checkAuth()
    print('Getting Random Gallery')
    global PYDRIVE
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("galleries")['id'])}).GetList()
    folder_list = []
    random_gallery = None
    folder_name = None
    for folder in random_folders:
        if str(settings.VERBOSE) == "True":
            print('checking galleries: {}'.format(folder['title']),end="")
        gallery_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
        if settings.BYKEYWORD != None and str(settings.BYKEYWORD) != str(folder['title']):
            settings.maybePrint('-> not keyword')
            continue
        elif settings.NOTKEYWORD != None and str(settings.NOTKEYWORD) == str(folder['title']):
            settings.maybePrint('-> by not keyword')
            continue
        if len(gallery_list_tmp)>0:
            folder_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    random.shuffle(folder_list)
    for folder in folder_list:
        if str(settings.VERBOSE) == "True":
            print('checking gallery: {}'.format(folder['title']),end="")
        gallery_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
        random_gallery_tmp = random.choice(gallery_list_tmp)
        gallery_list_tmp_tmp = PYDRIVE.ListFile({'q': "'"+random_gallery_tmp['id']+"' in parents and trashed=false and {}".format(MIMETYPES_IMAGES)}).GetList()
        if len(gallery_list_tmp_tmp)>0:
            folder_name = folder['title']
            random_gallery = random_gallery_tmp
            settings.maybePrint(" -> found")
        else:
            settings.maybePrint(" -> empty")
    if not random_gallery:
        print('Error: Missing Gallery Folder')
        return {}
    print('Random Gallery: '+random_gallery['title'])
    return {"file":random_gallery,"keywords":folder_name}

# Downloads random performer from Google Drive
def get_random_performer():
    checkAuth()
    print('Getting Random Performer')
    global PYDRIVE
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("performers")['id'])}).GetList()
    performer_list = []
    random_performer = None
    # print('random folders: '+str(random_folders))
    for folder in random_folders:
        # random_folder_folder = random.choice(random_folders)
        settings.maybePrint('random performer: '+folder['title'])
        performer_content_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
        # print('random folders: '+str(performer_list))
        if settings.BYKEYWORD != None and str(settings.BYKEYWORD) != str(folder['title']): 
            settings.maybePrint('- skipping nonkeyword: '+folder['title'])
            continue
        elif settings.NOTKEYWORD != None and str(settings.NOTKEYWORD) == str(folder['title']):
            settings.maybePrint('-> by not keyword')
            continue
        if len(performer_content_list)==0:
            settings.maybePrint('- skipping empty performer: '+folder['title'])
        elif len(performer_content_list)>0:
            settings.maybePrint('- performer found: '+folder['title'])
            performer_list.append(folder)
    if len(performer_list)==0:
        print('Error: Missing Performer Folder')
        return {}
    random_performer = random.choice(performer_list)
    print('Random Performer: '+random_performer['title'])
    return {"file":random_performer}

# Downloads random video from Google Drive
def get_random_video():
    checkAuth()
    print('Getting Random Video')
    global PYDRIVE
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("videos")['id'])}).GetList()
    video_list = []
    random_video = None
    folder_name = None
    for folder in random_folders:
        if str(settings.VERBOSE) == "True":
            print('checking folder: '+folder['title'],end="")
        video_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and {}".format(MIMETYPES_VIDEOS)}).GetList()
        if settings.BYKEYWORD != None and str(settings.BYKEYWORD) != str(folder['title']):
            settings.maybePrint('-> not keyword')
            continue
        elif settings.NOTKEYWORD != None and str(settings.NOTKEYWORD) == str(folder['title']):
            settings.maybePrint('-> by not keyword')
            continue
        if len(video_list_tmp)>0:
            video_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    if len(video_list)==0:
        print('Error: Missing Video File')
        return {}
    random_video = random.choice(video_list)
    folder_name = random_video['title'];
    print('Random Folder: '+random_video['title'])
    random_video = PYDRIVE.ListFile({'q': "'"+random_video['id']+"' in parents and trashed=false and {}".format(MIMETYPES_VIDEOS)}).GetList()
    random_video = random.choice(random_video)
    print('Random Video: '+random_video['title'])
    return {"file":random_video,"keywords":folder_name}

# Downloads random scene from Google Drive
def get_random_scene():
    checkAuth()
    print('Getting Random Scene')
    global PYDRIVE
    random_folders = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'".format(get_folder_by_name("scenes")['id'])}).GetList()
    folder_list = []
    random_scene = None
    folder_name = None
    for folder in random_folders:
        if str(settings.VERBOSE) == "True":
            print('checking scenes: '+folder['title'],end="")
        scene_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
        if settings.BYKEYWORD != None and str(settings.BYKEYWORD) != str(folder['title']):
            settings.maybePrint('-> not keyword')
            continue
        elif settings.NOTKEYWORD != None and str(settings.NOTKEYWORD) == str(folder['title']):
            settings.maybePrint('-> by not keyword')
            continue
        if len(scene_list_tmp)>0:
            folder_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    random.shuffle(folder_list)
    for folder in folder_list:
        if str(settings.VERBOSE) == "True":
            print('checking scene: '+folder['title'],end="")
        scene_list_tmp_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'text/plain'"}).GetList()
        if len(scene_list_tmp_tmp)>0:
            folder_name = folder['title']
            random_scene = folder
            settings.maybePrint(" -> found")
        else:
            settings.maybePrint(" -> empty")
    if not random_scene:
        print('Error: Missing Scene Folders')
        return {}
    print('Random Scene: '+random_scene['title'])
    return {"file":random_scene,"keywords":folder_name}

##################
##### Random #####
##################

def random_download(fileChoice):
    print('Random: {}'.format(fileChoice))
    file = None
    file_ = None
    data = None
    keywords = None
    performers = None
    try:
        if fileChoice == 'image':
            file = get_random_image()
            data = download_file(file.get("file"))
        elif fileChoice == 'gallery':
            file = get_random_gallery()
            data = download_gallery(file.get("file"))
        elif fileChoice == 'performer':
            file = get_random_performer()
            data = download_performer(file.get("file"))
            performers = file.get("file").get("title").split(" ")
            file_ = data.get("file")
            keywords = data.get("keywords")
        elif fileChoice == 'scene':
            file = get_random_scene()
            return download_scene(file.get("file"))
        elif fileChoice == 'video':
            file = get_random_video()
            data = download_file(file.get("file"))
        else:
            return print("Error: Missing File Choice")
        if file == None or data == None:
            print("Error: Missing Random File(s)")
            return {}
    except Exception as e:
        settings.maybePrint(e)
        return {}
    return {"path":data.get("path"), "file":file_ or file.get("file"), "files":data.get("files"), "keywords":keywords or file.get("keywords"), "performers":performers}

##################
##### Upload #####
##################

def upload_file(path=None, parent=None):
    checkAuth()
    file = os.path.basename(path)
    filename = os.path.splitext(file)[0]
    ext = os.path.splitext(file)[1].lower()
    mimetype = None
    print(settings.SKIP_BACKUP)
    if str(settings.FORCE_BACKUP) == "True":
        print("Google Upload (forced): {}".format(filename))
    elif str(settings.DEBUG) == "True":
        print("Skipping Google Upload (debug): {}".format(filename))
        return
    elif str(settings.BACKUP) == "False":
        print('Skipping Google Upload (disabled): {}'.format(filename))
        return
    elif str(settings.SKIP_BACKUP) == "True":
        print('Skipping Backup: {}'.format(file['title']))
        return
    else:
        print('Google Upload (file): {}'.format(filename))
    if "mov" in ext or "mp4" in ext:
        mimetype = "video/mp4"
    elif "jpg" in ext or "jpeg" in ext:
        mimetype = "image/jpeg"
    if not mimetype:
        print("Error: Missing Mimetype")
        return
    if not parent: parent = get_folder_by_name("posted")
    if not parent:
        print("Error: Missing Posted Folder")
        return
    # file_metadata = {
    #     'name': str(filename),
    #     'mimeType': str(mimetype),
    #     'parents': [{"kind": "drive#fileLink", "id": str(parent['id'])}]
    # }
    # media = MediaFileUpload(path, mimetype=str(mimetype), resumable=True)
    # file = DRIVE.files().create(body=file_metadata, media_body=media, fields='id').execute()
    file = PYDRIVE.CreateFile({'title':str(filename), 'parents':[{"kind": "drive#fileLink", "id": str(parent['id'])}],'mimeType':str(mimetype)})
    file.Upload()
    # print('File ID: {}'.format(file.get('id')))

def upload_gallery(path=None):
    parent = get_folder_by_name("posted")
    if not parent:
        print("Error: Missing Posted Folder")
        return
    print(settings.SKIP_BACKUP)
    if str(settings.FORCE_BACKUP) == "True":
        print("Google Upload (forced): {}".format(path))
    elif str(settings.DEBUG) == "True":
        print("Skipping Google Upload (debug): {}".format(path))
        return
    elif str(settings.BACKUP) == "False":
        print('Skipping Google Upload (disabled): {}'.format(path))
        return
    elif str(settings.SKIP_BACKUP) == "True":
        print('Skipping Backup (gallery): {}'.format(file['title']))
        return
    else:
        print('Google Upload: {}'.format(path))
    file_metadata = {
        'name': str(datetime.datetime.now()),
        'mimeType': str("application/vnd.google-apps.folder"),
        'parents': [{"kind": "drive#fileLink", "id": str(parent['id'])}]
    }
    tmp_folder = PYDRIVE.CreateFile({'title':str(datetime.datetime.now()), 'parents':[{"kind": "drive#fileLink", "id": str(parent['id'])}],'mimeType':'application/vnd.google-apps.folder'})
    tmp_folder.Upload()
    # media = MediaFileUpload(path, mimetype="application/vnd.google-apps.folder", resumable=True)
    # parent = DRIVE.files().create(body=file_metadata, fields='id').execute()
    files = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for file in files:
        upload_file(path=file, parent=tmp_folder)

def upload_input(path=None):
    if not path: path = settings.INPUT
    if os.path.isdir(path):
        upload_gallery(path=path)
    else:
        upload_file(path=path)

##################
##### FFMPEG #####
##################

def repair(path):
    if str(settings.SKIP_REPAIR) == "True":
        print("Warning: Skipping Repair")
        return path
    repairedPath = str(path).replace(".mp4", "_fixed.mp4")
    try:
        print("Repairing: {} <-> {}".format(path, settings.WORKING_VIDEO))
        if str(settings.VERBOSE) == "True":
            subprocess.call(['untrunc', str(settings.WORKING_VIDEO), str(path)]).communicate()
        else:
            subprocess.Popen(['untrunc', str(settings.WORKING_VIDEO), str(path)],stdin=FNULL,stdout=FNULL)
    except AttributeError:
        if os.path.isfile(str(path)+"_fixed.mp4"):
            shutil.move(str(path)+"_fixed.mp4", repairedPath)
            print("Repair Complete")
    except:
        settings.maybePrint(sys.exc_info()[0])
        print("Warning: Skipping Repair")
        return path
    print("Repair Successful")
    return str(repairedPath)

def reduce(path):
    if str(settings.SKIP_REDUCE) == "True":
        print("Warning: Skipping Reduction")
        return path
    reducedPath = str(path).replace(".mp4", "_reduced.mp4")
    try:
        settings.maybePrint("Reducing: {}".format(path))
        try:
            clip = VideoFileClip(str(path))
            settings.maybePrint("Length: {}".format(clip.duration))
            bitrate = 1000000000 / int(clip.duration)
            settings.maybePrint("Bitrate: {}".format(bitrate))
        except FileNotFoundError:
            print("Error: Missing File to Reduce")
            return path
        loglevel = "quiet"
        if str(settings.VERBOSE) == "True":
            loglevel = "debug"
        p = subprocess.call(['ffmpeg', '-loglevel', str(loglevel), '-err_detect', 'ignore_err', '-y', '-i', str(path), '-c', 'copy', '-c:v', 'libx264', '-c:a', 'aac', '-strict', '2', '-crf', '26', '-b:v', str(bitrate), str(reducedPath)])
        # p.communicate()
    except FileNotFoundError:
        print("Warning: Ignoring Fixed Video")
        return reduce(str(path).replace(".mp4", "_fixed.mp4"))
    except Exception as e:
        settings.maybePrint(e)
        if "Conversion failed!" in str(e):
            print("Error: Conversion Failure")
            return path                    
    print("Reduction Complete")
    originalSize = os.path.getsize(str(path))
    newSize = os.path.getsize(str(reducedPath))
    print("Original Size: {}kb - {}mb".format(originalSize/1000, originalSize/1000000))
    print("Reduced Size: {}kb - {}mb".format(newSize/1000, newSize/1000000))
    if int(originalSize) < int(newSize):
        print("Warning: Original Size Smaller")
        return path
    if int(newSize) == 0:
        print("Error: Missing Reduced File")
        return path
    return reducedPath

def thumbnail_fix(path):
    if str(settings.THUMBNAILING_PREVIEW) == "False":
        print("Warning: Preview Thumbnailing Disabled")
        return path
    try:
        print("Thumbnailing: {}".format(path))
        loglevel = "quiet"
        if str(settings.VERBOSE) == "True":
            loglevel = "debug"
        thumbnail_path = os.path.join(os.path.dirname(str(path)), 'thumbnail.png')
        settings.maybePrint("thumbnail path: {}".format(thumbnail_path))
        p = subprocess.call(['ffmpeg', '-loglevel', str(loglevel), '-i', str(path),'-ss', '00:00:00.000', '-vframes', '1', str(thumbnail_path)])
        p.communicate()
        print("Thumbnailing Complete")
        return thumbedPath
    except FileNotFoundError:
        print("Warning: Ignoring Thumbnail")
    except AttributeError:
        print("Thumbnailing: Captured PNG")
    except:
        settings.maybePrint(sys.exc_info()[0])
        print("Error: Thumbnailing Fuckup")    
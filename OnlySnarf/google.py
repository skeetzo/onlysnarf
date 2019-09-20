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
FOLDERS = None
OnlyFansFolder_ = None

################
##### Auth #####
################

# Google Auth
def authGoogle():
    print('Authenticating Google')
    try:
        # PyDrive
        gauth = GoogleAuth()
        # Try to load saved client credentials
        gauth.LoadCredentialsFile(settings.PATH_GOOGLE_CREDS)
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
        gauth.SaveCredentialsFile(settings.PATH_GOOGLE_CREDS)
        global PYDRIVE
        PYDRIVE = GoogleDrive(gauth)
        # Drive v3 API
        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = file.Storage(settings.PATH_GOOGLE_CREDS)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(settings.PATH_SECRET, SCOPES)
            creds = tools.run_flow(flow, store)
        global DRIVE
        DRIVE = build('drive', 'v3', http=creds.authorize(Http()))
    except:
        settings.maybePrint(sys.exc_info()[0])
        print('Error: Unable to Authenticate w/ Google')
        return False
    print('Authentication Success') 
    return True

################################
##### Archiving / Deleting #####
################################

# Deletes online file
def delete_file(file):
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    if str(settings.FORCE_DELETE_GOOGLE) == "True":
        print("Deleting (Forced): {}".format(fileName))
    elif str(settings.DEBUG) == "True":
        print("Skipping Delete (Debug): {}".format(fileName))
        return
    elif str(settings.DELETE_GOOGLE) == "False":
        print('Skipping Delete (Disabled): {}'.format(fileName))
        return
    else:
        print('Deleting: {}'.format(fileName))
    file.Trash()

# Archives posted file / folder
def move_file(file):
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    if str(settings.FORCE_BACKUP) == "True":
        print("Backing Up (Forced): {}".format(file['title']))
    elif str(settings.DEBUG) == "True":
        print("Skipping Backup (Debug): {}".format(file['title']))
        return
    elif str(settings.BACKUP) == "False":
        print('Skipping Backup (Disabled): {}'.format(file['title']))
        return
    else:
        print('Backing Up: {}'.format(file['title']))
    OnlyFans_POSTED_FOLDER = get_folder_by_name("posted")
    file['parents'] = [{"kind": "drive#fileLink", "id": str(OnlyFans_POSTED_FOLDER)}]
    file.Upload()
    print('Google File Backed Up: {}'.format(file['title']))

def move_files(fileName, files):
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    if str(settings.FORCE_BACKUP) == "True":
        print("Backing Up (Forced): {}".format(fileName))
    elif str(settings.DEBUG) == "True":
        print("Skipping Backup (Debug): {}".format(fileName))
        return
    elif str(settings.BACKUP) == "False":
        print('Skipping Backup (Disabled): {}'.format(fileName))
        return
    else:
        print('Backing Up: {}'.format(fileName))
    title = fileName+" - "+datetime.datetime.now().strftime("%d-%m@%I-%M")
    settings.maybePrint('Moving To: '+title)
    global PYDRIVE
    OnlyFans_POSTED_FOLDER = get_folder_by_name("posted")
    tmp_folder = PYDRIVE.CreateFile({'title':str(title), 'parents':[{"kind": "drive#fileLink", "id": str(OnlyFans_POSTED_FOLDER)}],'mimeType':'application/vnd.google-apps.folder'})
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
    print("Creating Folders: {}".format(settings.ROOT_FOLDER))
    OnlyFansFolder = get_folder_root()
    if OnlyFansFolder is None:
        print("Error: Unable To Create Folders")
        return
    file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(OnlyFansFolder)}).GetList()
    for folder in settings.DRIVE_FOLDERS:
        found = False
        for folder_ in file_list:
            if str(folder) == folder_['title']:
                settings.maybePrint("found: {}".format(folder))
                found = True
        if not found:
            settings.maybePrint("created: {}".format(folder))
            contentFolder = PYDRIVE.CreateFile({"title": str(folder), "parents": [{"id": OnlyFansFolder}], "mimeType": "application/vnd.google-apps.folder"})
            contentFolder.Upload()

def find_folder(parent, folderName):
    global PYDRIVE
    file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(parent)}).GetList()
    for folder in file_list:
        if str(folder['title']) == str(folderName):
            return folder['id']
    print("Error: Unable to Find Folder - {}".format(folderName))
    return None

def get_folder_by_name(folderName):
    settings.maybePrint("Getting Folder: {}".format(folderName))
    global PYDRIVE
    global FOLDERS
    if FOLDERS is not None:
        if FOLDERS.get(str(folderName)) is not None:
            return FOLDERS.get(str(folderName))
    else:
        FOLDERS = {}
    OnlyFansFolder = get_folder_root()
    if OnlyFansFolder is None:
        print("Error: Unable To Get Folder - {}".format(folderName))
        return None
    file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(OnlyFansFolder)}).GetList()
    for folder in file_list:
        if str(folder['title'])==str(folderName):
            FOLDERS[str(folderName)] = folder['id']
            settings.maybePrint("Found Folder: {}".format(folderName))
            return folder['id']
    if str(settings.DRIVE_CREATE_MISSING) == "False":
        settings.maybePrint("Skipping: Create Missing Folder - {}".format(folderName))
        return None
    # create if missing
    folder = PYDRIVE.CreateFile({"title": str(folderName), "mimeType": "application/vnd.google-apps.folder", "parents": [{"kind": "drive#fileLink", "id": OnlyFansFolder}]})
    folder.Upload()
    FOLDERS[str(folderName)] = folder['id']
    settings.maybePrint("Created Folder: {}".format(folderName))
    return folder['id']

# Creates the OnlyFans folder structure
def get_folder_root():
    global PYDRIVE
    global OnlyFansFolder_
    if OnlyFansFolder_ is not None:
        return OnlyFansFolder_
    OnlyFansFolder = None
    if settings.PATH_DRIVE is not None:
        mount_root = "root"
        root_folders = settings.PATH_DRIVE.split("/")
        settings.maybePrint("Mount Folders: {}".format(root_folders))    
        for folder in root_folders:
            mount_root = find_folder(mount_root, folder)
            if mount_root is None:
                mount_root = "root"
                print("Warning: Drive Mount Folder Not Found")
                break
        mount_root = find_folder(mount_root, settings.ROOT_FOLDER)
        if mount_root is None:
            mount_root = "root"
            print("Warning: Drive Mount Folder Not Found")
        else:
            print("Found Root (alt): {}/{}".format(settings.PATH_DRIVE, settings.ROOT_FOLDER))
        OnlyFansFolder = mount_root
    else:
        file_list = PYDRIVE.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        for folder in file_list:
            if str(folder['title']) == str(settings.ROOT_FOLDER):
                OnlyFansFolder = folder['id']
                print("Found Root: {}".format(settings.ROOT_FOLDER))
    if OnlyFansFolder is None:
        print("Creating Root: {}".format(settings.ROOT_FOLDER))
        OnlyFansFolder = PYDRIVE.CreateFile({"title": str(settings.ROOT_FOLDER), "mimeType": "application/vnd.google-apps.folder"})
        OnlyFansFolder.Upload()
        OnlyFansFolder = OnlyFansFolder['id']
    OnlyFansFolder_ = OnlyFansFolder
    return OnlyFansFolder_

####################
##### Download #####
####################

# Download File
def download_file(file, REPAIR=False):
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    print('Downloading File')
    tmp = settings.getTmp()
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
            print("Download Complete")
        if REPAIR:
            tmp = repair(tmp)
        global FIFTY_MEGABYTES
        if int(os.stat(str(tmp)).st_size) >= FIFTY_MEGABYTES or settings.FORCE_REDUCTION: # greater than 1GB
            tmp = reduce(tmp)
        tmp = thumbnail_fix(tmp)
    else:
        file.GetContentFile(tmp)
    ### Finish ###
    if not os.path.isfile(str(tmp)):
        print("Error: Missing Downloaded File")
        return
    size = os.path.getsize(tmp)
    settings.maybePrint("File Size: {}kb - {}mb".format(size/1000, size/1000000))
    global ONE_MEGABYTE
    if size <= ONE_MEGABYTE:
        settings.maybePrint("Warning: Small File Size")
    global ONE_HUNDRED_KILOBYTES
    if size <= ONE_HUNDRED_KILOBYTES:
        settings.maybePrint("Error: File Size Too Small")
        print("Error: Download Failure")
        return
    print('Downloaded: File')
    return tmp

# Download Gallery
def download_gallery(folder):
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    print('Downloading Gallery')
    tmp = settings.getTmp()
    # download folder
    global PYDRIVE
    file_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and (mimeType contains \'image/jpeg\' or mimeType contains \'image/jpg\' or mimeType contains \'image/png\')"}).GetList()
    folder_size = len(file_list)
    settings.maybePrint('Folder size: '+str(folder_size))
    settings.maybePrint('Upload limit: '+str(settings.IMAGE_UPLOAD_LIMIT))
    if int(folder_size) == 0:
        print('Error: Empty Folder')
        return
    random.shuffle(file_list)
    file_list = file_list[:int(settings.IMAGE_UPLOAD_LIMIT)]
    i = 1
    for file in sorted(file_list, key = lambda x: x['title']):
        print('Downloading: {} ({}/{})'.format(file['title'], i, folder_size))
        settings.maybePrint('filePath: '+os.path.join(tmp, str(file['title'])))
        file.GetContentFile(os.path.join(tmp, str(file['title'])))
        i+=1
    print('Downloaded: Gallery')
    return [file_list, tmp]

# Download Performer
def download_performer(folder):
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
        content_list = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
        if len(content_list)==0:
            settings.maybePrint('- skipping empty content: '+folder['title'])
        elif len(content_list)>0:
            settings.maybePrint('- content galleries found: '+folder['title'])
            for content in content_list:
                content_list_galleries = PYDRIVE.ListFile({'q': "'"+content['id']+"' in parents and trashed=false and (mimeType contains \'image/jpeg\' or mimeType contains \'image/jpg\' or mimeType contains \'image/png\' or mimeType contains \'video/mp4\')"}).GetList()
                if len(content_list_galleries)==0:
                    settings.maybePrint('- skipping empty content gallery: '+content['title'])
                elif len(content_list_galleries)>0 and len(content_list_galleries):
                    settings.maybePrint('- content gallery found: '+content['title'])
                    content_found.append(content)
    if len(content_found)==0:
        print('Warning: Missing Content Folder')
        return
    random_content = random.choice(content_found)
    content_title = random_content['title']
    settings.maybePrint("Folder: {}".format(content_title))
    # download folder
    file_list = PYDRIVE.ListFile({'q': "'"+random_content['id']+"' in parents and trashed=false and (mimeType contains \'image/jpeg\' or mimeType contains \'image/jpg\' or mimeType contains \'image/png\' or mimeType contains \'video/mp4\')"}).GetList()
    folder_size = len(file_list)
    settings.maybePrint('Folder size: {}'.format(folder_size))
    settings.maybePrint('Upload limit: {}'.format(settings.IMAGE_UPLOAD_LIMIT))
    # settings.maybePrint("Files: {}".format(file_list))
    if folder_size == 0:
        print("Error: Missing Files")
        return
    # get all images first then videos 1 at a time from folder
    videos = []
    images = []
    for file in file_list:
        if "mp4" in str(file['title']):
            videos.append(file)
        else:
            images.append(file)
    if len(images) > len(videos):
        settings.maybePrint("Found: Images")
        file_list_random = []
        for x in range(folder_size):
            random_file = random.choice(file_list)
            file_list.remove(random_file)
            file_list_random.append(random_file)
        file_list = file_list_random[:settings.IMAGE_UPLOAD_LIMIT]
    else:
        settings.maybePrint("Found: Videos")
        file_list = [random.choice(videos)]

    i = 1
    for file in sorted(file_list, key = lambda x: x['title']):
        print('Downloading: {} ({}/{})'.format(file['title'], i, folder_size))
        settings.maybePrint('filePath: '+tmp+"/"+str(file['title']))
        file.GetContentFile(tmp+"/"+str(file['title']))
        i+=1
    print('Downloaded: Performer')
    return [file_list, tmp, content_title]

# Download Scene
def download_scene(sceneFolder):
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
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
    content = download_gallery(content)
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
    preview = PYDRIVE.ListFile({'q': "'"+preview['id']+"' in parents and trashed=false and (mimeType contains \'image/jpeg\' or mimeType contains \'image/jpg\' or mimeType contains \'image/png\')"}).GetList()
    if len(preview) == 0:
        print("Error: Missing Scene Preview")
        return
    preview = preview[0]
    preview = download_file(preview)
    if "mp4" in preview:
        if str(settings.THUMBNAILING_PREVIEW) == "False":
            print("Error: Preview Thumbnailing Disabled")
            return
        preview = thumbnail_preview_fix(preview)
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
    return [tmp_content, preview, data, content]
    # return json.dumps({
    #     "content": content[0],
    #     "content_path": tmp_content,
    #     "preview": preview,
    #     "data": data
    # })

###############
##### Get #####
###############

# gets all the folders in the messages category
# gets all the images in the folders
# returns an array of json images w/ 
# [ 'image.folder' - 'image.title']
def get_images():
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    print('Getting Images')
    global PYDRIVE
    OnlyFans_Images_Folder = get_folder_by_name("images")
    if OnlyFans_Images_Folder is None:
        print("Error: Unable to get Images Folder")
        return None
    random_folders = PYDRIVE.ListFile({'q': "'"+OnlyFans_Images_Folder+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    images_list = []
    for folder in random_folders:
        settings.maybePrint('checking folder: '+folder['title'])
        images_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and (mimeType contains \'image/jpeg\' or mimeType contains \'image/jpg\' or mimeType contains \'image/png\')"}).GetList()      
        for image_file in images_list_tmp:
            # images_list.append({"folder":folder['title'],"folder_id":folder['id'],"id":image_file['id'],"image":image_file['title']})
            images_list.append([folder, image_file])
    if len(images_list)==0:
        print('Warning: Missing Message Files')
        return
    return images_list
    # menu.selectImage -> [] -> menu.selectImage

def get_message_image(folderName):
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    print('Getting Message Image: {}'.format(folderName))
    global PYDRIVE
    OnlyFans_Images_Folder = get_folder_by_name("messages")
    if OnlyFans_Images_Folder is None:
        print("Error: Unable to get Images Folder")
        return None
    random_folders = PYDRIVE.ListFile({'q': "'"+OnlyFans_Images_Folder+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    images_list = []
    random_image = None
    folder_name = None
    for folder in random_folders:
        if folder['title'] != str(folderName):
            continue
        if str(settings.VERBOSE) == "True":
            print('checking folder: '+folder['title'],end="")
        images_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and (mimeType contains \'image/jpeg\' or mimeType contains \'image/jpg\' or mimeType contains \'image/png\')"}).GetList()      
        if len(images_list_tmp)>0:
            images_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    if len(images_list)==0:
        print('Error: Missing Image File')
        return
    random_image = random.choice(images_list)
    folder_name = random_image['title'];
    print('Messages Folder: '+random_image['title'])
    random_image = PYDRIVE.ListFile({'q': "'"+random_image['id']+"' in parents and trashed=false and (mimeType contains \'image/jpeg\' or mimeType contains \'image/jpg\' or mimeType contains \'image/png\')"}).GetList()
    random_image = random.choice(random_image)
    print('Messages Image: '+random_image['title'])
    return [random_image, folder_name]

# Downloads random image from Google Drive
def get_random_image():
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    print('Getting Random Image')
    global PYDRIVE
    OnlyFans_Images_Folder = get_folder_by_name("images")
    if OnlyFans_Images_Folder is None:
        print("Error: Unable to get Images Folder")
        return None
    random_folders = PYDRIVE.ListFile({'q': "'"+OnlyFans_Images_Folder+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    images_list = []
    random_image = None
    folder_name = None
    for folder in random_folders:
        if str(settings.VERBOSE) == "True":
            print('checking folder: '+folder['title'],end="")
        images_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and (mimeType contains \'image/jpeg\' or mimeType contains \'image/jpg\' or mimeType contains \'image/png\')"}).GetList()      
        if len(images_list_tmp)>0:
            images_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    if len(images_list)==0:
        print('Error: Missing Image File')
        return
    random_image = random.choice(images_list)
    folder_name = random_image['title'];
    print('Random Folder: '+random_image['title'])
    random_image = PYDRIVE.ListFile({'q': "'"+random_image['id']+"' in parents and trashed=false and (mimeType contains \'image/jpeg\' or mimeType contains \'image/jpg\' or mimeType contains \'image/png\')"}).GetList()
    random_image = random.choice(random_image)
    print('Random Image: '+random_image['title'])
    return [random_image, folder_name]

# Downloads random gallery from Google Drive
def get_random_gallery():
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    print('Getting Random Gallery')
    global PYDRIVE
    OnlyFans_Galleries_Folder = get_folder_by_name("galleries")
    if OnlyFans_Galleries_Folder is None:
        print("Error: Unable to get Galleries Folder")
        return None
    random_folders = PYDRIVE.ListFile({'q': "'"+OnlyFans_Galleries_Folder+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    folder_list = []
    random_gallery = None
    folder_name = None
    for folder in random_folders:
        if str(settings.VERBOSE) == "True":
            print('checking galleries: {}'.format(folder['title']),end="")
        gallery_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
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
        gallery_list_tmp_tmp = PYDRIVE.ListFile({'q': "'"+random_gallery_tmp['id']+"' in parents and trashed=false and (mimeType contains \'image/jpeg\' or mimeType contains \'image/jpg\' or mimeType contains \'image/png\')"}).GetList()
        if len(gallery_list_tmp_tmp)>0:
            folder_name = folder['title']
            random_gallery = random_gallery_tmp
            settings.maybePrint(" -> found")
        else:
            settings.maybePrint(" -> empty")
    if not random_gallery:
        print('Error: Missing Gallery Folder')
        return
    print('Random Gallery: '+random_gallery['title'])
    return [random_gallery, folder_name]

# Downloads random performer from Google Drive
def get_random_performer():
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    print('Getting Random Performer')
    global PYDRIVE
    OnlyFans_Performers_Folder = get_folder_by_name("performers")
    if OnlyFans_Performers_Folder is None:
        print("Error: Unable to get Performers Folder")
        return None
    random_folders = PYDRIVE.ListFile({'q': "'"+OnlyFans_Performers_Folder+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    performer_list = []
    random_performer = None
    # print('random folders: '+str(random_folders))
    for folder in random_folders:
        random_folder_folder = random.choice(random_folders)
        settings.maybePrint('random performer: '+random_folder_folder['title'])
        performer_content_list = PYDRIVE.ListFile({'q': "'"+random_folder_folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
        # print('random folders: '+str(performer_list))
        if len(performer_content_list)==0:
            settings.maybePrint('- skipping empty performer: '+random_folder_folder['title'])
        elif len(performer_content_list)>0:
            settings.maybePrint('- performer found: '+random_folder_folder['title'])
            performer_list.append(random_folder_folder)
    if len(performer_list)==0:
        print('Error: Missing Performer Folder')
        return
    random_performer = random.choice(performer_list)
    print('Random Performer: '+random_performer['title'])
    return random_performer

# Downloads random video from Google Drive
def get_random_video():
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    print('Getting Random Video')
    global PYDRIVE
    OnlyFans_Videos_Folder = get_folder_by_name("videos")
    if OnlyFans_Videos_Folder is None:
        print("Error: Unable to get Videos Folder")
        return None
    random_folders = PYDRIVE.ListFile({'q': "'"+OnlyFans_Videos_Folder+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    video_list = []
    random_video = None
    folder_name = None
    for folder in random_folders:
        if str(settings.VERBOSE) == "True":
            print('checking folder: '+folder['title'],end="")
        video_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'video/mp4'"}).GetList()
        if len(video_list_tmp)>0:
            video_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    if len(video_list)==0:
        print('Error: Missing Video File')
        return
    random_video = random.choice(video_list)
    folder_name = random_video['title'];
    print('Random Folder: '+random_video['title'])
    random_video = PYDRIVE.ListFile({'q': "'"+random_video['id']+"' in parents and trashed=false and mimeType contains 'video/mp4'"}).GetList()
    random_video = random.choice(random_video)
    print('Random Video: '+random_video['title'])
    return [random_video, folder_name]

# Downloads random scene from Google Drive
def get_random_scene():
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    print('Getting Random Scene')
    global PYDRIVE
    OnlyFans_Scenes_Folder = get_folder_by_name("scenes")
    if OnlyFans_Scenes_Folder is None:
        print("Error: Unable to get Scenes Folder")
        return None
    random_folders = PYDRIVE.ListFile({'q': "'"+OnlyFans_Scenes_Folder+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    folder_list = []
    random_scene = None
    folder_name = None
    for folder in random_folders:
        if str(settings.VERBOSE) == "True":
            print('checking scenes: '+folder['title'],end="")
        scene_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
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
        return
    print('Random Scene: '+random_scene['title'])
    return [random_scene, folder_name]

##################
##### Upload #####
##################

def upload_file(filename=None, mimetype="video/mp4"):
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    if filename == None:
        print("Error: Missing Filename")
        return
    file_metadata = {
        'name': str(filename),
        'mimeType': str(mimetype)
    }
    media = MediaFileUpload(str(filename), mimetype=str(mimetype), resumable=True)
    file = DRIVE.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print('File ID: %s' % file.get('id'))

##################
##### FFMPEG #####
##################

def repair(path):
    if (settings.SKIP_REPAIR):
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
    if (settings.SKIP_REDUCE):
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
        p.communicate()
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
    if (settings.SKIP_THUMBNAIL):
        print("Warning: Skipping Thumbnail")
        return path
    thumbedPath = str(path).replace(".mp4", "_thumbed.mp4")
    try:
        print("Thumbnailing: {}".format(path))
        loglevel = "quiet"
        if str(settings.VERBOSE) == "True":
            loglevel = "debug"
        thumbnail_path = os.path.join(os.path.dirname(str(path)), 'thumbnail.png')
        settings.maybePrint("thumbnail path: {}".format(thumbnail_path))
        p = subprocess.call(['ffmpeg', '-loglevel', str(loglevel), '-i', str(path),'-ss', '00:00:00.000', '-vframes', '1', str(thumbnail_path)])
        p.communicate()
    except FileNotFoundError:
        print("Warning: Ignoring Thumbnail")
        return path
    except AttributeError:
        print("Thumbnailing: Captured PNG")
    except:
        settings.maybePrint(sys.exc_info()[0])
        print("Error: Thumbnailing Fuckup")
        return path
    try:
        p = subprocess.call(['ffmpeg', '-loglevel', str(loglevel), '-y', '-i', str(path), '-i', str(thumbnail_path), '-pix_fmt', 'rgb24', '-c', 'copy', '-acodec', 'copy', '-vcodec', 'copy', '-map', '0', '-map', '1', '-c:v:1', 'png', '-disposition:v:1', 'attached_pic', str(thumbedPath)])
        p.communicate()
    except AttributeError:
        print("Thumbnailing: Added PNG")
    except:
        settings.maybePrint(sys.exc_info()[0])
        print("Error: Thumbnailing Adding Fuckup")
        return path
    print("Thumbnailing Complete")
    originalSize = os.path.getsize(str(path))
    newSize = os.path.getsize(str(thumbedPath))
    print("Original Size: {}kb - {}mb".format(originalSize/1000, originalSize/1000000))
    print("Thumbed Size: {}kb - {}mb".format(newSize/1000, newSize/1000000))
    if int(originalSize) < int(newSize):
        print("Warning: Original Size Smaller")
        return path
    if int(newSize) == 0:
        print("Error: Missing Thumbnailed File")
        return path
    return thumbedPath

def thumbnail_preview_fix(path):
    # if (settings.SKIP_THUMBNAIL):
        # print("Warning: Skipping Thumbnail")
        # return
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
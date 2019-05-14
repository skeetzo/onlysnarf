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
INITIALIZED = False
FOLDERS = None
OnlyFansFolder_ = None
##################
##### Config #####
##################

def initialize():
    try:
        # settings.maybePrint("Initializing OnlySnarf")
        global INITIALIZED
        if INITIALIZED:
            # settings.maybePrint("Already Initialized, Skipping")
            return
        global OnlyFans_VIDEOS_FOLDER
        global OnlyFans_IMAGES_FOLDER
        global OnlyFans_GALLERIES_FOLDER
        global OnlyFans_POSTED_FOLDER
        global OnlyFans_SCENES_FOLDER
        global OnlyFans_PERFORMERS_FOLDER
        OnlyFans_VIDEOS_FOLDER = None
        OnlyFans_IMAGES_FOLDER = None
        OnlyFans_GALLERIES_FOLDER = None
        OnlyFans_POSTED_FOLDER = None
        OnlyFans_SCENES_FOLDER = None
        OnlyFans_PERFORMERS_FOLDER = None
        with open(settings.CONFIG_PATH) as config_file:    
            config = json.load(config_file)
        OnlyFans_VIDEOS_FOLDER = config['videos_folder']
        OnlyFans_IMAGES_FOLDER = config['images_folder']
        OnlyFans_GALLERIES_FOLDER = config['galleries_folder']
        OnlyFans_POSTED_FOLDER = config['posted_folder']
        OnlyFans_SCENES_FOLDER = config['scenes_folder']
        OnlyFans_PERFORMERS_FOLDER = config['performers_folder']
        # settings.maybePrint("Initialized OnlySnarf: Google")
        INITIALIZED = True
    except Exception as e:
        print('Error Initializing, run `onlysnarf-config`')
        print(e)
        sys.exit(0)
    except FileNotFoundError:
        print('Missing Config, run `onlysnarf-config`')
        sys.exit(0)

################
##### Auth #####
################

# Google Auth
def authGoogle():
    print('Authenticating Google...')
    try:
        # PyDrive
        gauth = GoogleAuth()
        # Try to load saved client credentials
        gauth.LoadCredentialsFile(settings.GOOGLE_CREDS_PATH)
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
        gauth.SaveCredentialsFile(settings.GOOGLE_CREDS_PATH)
        global PYDRIVE
        PYDRIVE = GoogleDrive(gauth)
        # Drive v3 API
        SCOPES = 'https://www.googleapis.com/auth/drive'
        store = file.Storage(settings.GOOGLE_CREDS_PATH)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(settings.SECRET_PATH, SCOPES)
            creds = tools.run_flow(flow, store)
        global DRIVE
        DRIVE = build('drive', 'v3', http=creds.authorize(Http()))
    except:
        settings.maybePrint(sys.exc_info()[0])
        print('...Authentication Failure!')
        return False
    print('...Authentication Success!') 
    return True

################################
##### Archiving / Deleting #####
################################

# Deletes online file
def delete_file(file):
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    if str(settings.DELETING_FORCED) == "True":
        print("Deleting (Forced): {}".format(fileName))
    elif str(settings.DEBUG) == "True":
        print("Skipping Delete (Debug): {}".format(fileName))
        return
    elif str(settings.DELETING) == "False":
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
    if str(settings.BACKING_UP_FORCE) == "True":
        print("Backing Up (Forced): {}".format(fileName))
    elif str(settings.DEBUG) == "True":
        print("Skipping Backup (Debug): {}".format(fileName))
        return
    elif str(settings.BACKING_UP) == "False":
        print('Skipping Backup (Disabled): {}'.format(fileName))
        return
    else:
        print('Backing Up: {}'.format(fileName))
    global OnlyFans_POSTED_FOLDER
    file['parents'] = [{"kind": "drive#fileLink", "id": str(OnlyFans_POSTED_FOLDER)}]
    file.Upload()
    print('Google File Backed Up: {}'.format(file['title']))

def move_files(fileName, files):
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    if str(settings.BACKING_UP_FORCE) == "True":
        print("Backing Up (Forced): {}".format(fileName))
    elif str(settings.DEBUG) == "True":
        print("Skipping Backup (Debug): {}".format(fileName))
        return
    elif str(settings.BACKING_UP) == "False":
        print('Skipping Backup (Disabled): {}'.format(fileName))
        return
    else:
        print('Backing Up: {}'.format(fileName))
    title = fileName+" - "+datetime.datetime.now().strftime("%d-%m@%I-%M")
    settings.maybePrint('Moving To: '+title)
    global PYDRIVE
    global OnlyFans_POSTED_FOLDER
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

# Creates the OnlyFans folder structure
def get_folder_OnlyFans():
    global PYDRIVE
    file_list = PYDRIVE.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    global OnlyFansFolder_
    if OnlyFansFolder_ is not None:
        return OnlyFansFolder_
    OnlyFansFolder = None
    if settings.MOUNT_DRIVE is not None:
        mount_root = None
        for file in file_list:
            if file['title'] == str(settings.MOUNT_DRIVE):
                print("Found Root (alt): {}".format(settings.MOUNT_DRIVE))
                mount_root = file
        if mount_root is None:
            print("Error: Drive Mount Folder Not Found")
            return
        file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(mount_root['id'])}).GetList()
    for file in file_list:
        if file['title'] == "OnlyFans":
            print("Found Root OnlyFans")
            OnlyFansFolder = file
    if OnlyFansFolder is None:
        print("Creating Root OnlyFans")
        OnlyFansFolder = PYDRIVE.CreateFile({"title": "OnlyFans", "mimeType": "application/vnd.google-apps.folder"})
        OnlyFansFolder.Upload()
    OnlyFansFolder_ = OnlyFansFolder
    return OnlyFansFolder_

def create_folders():
    print("Creating OnlyFans Folders")
    OnlyFansFolder = get_folder_OnlyFans()
    file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false".format(OnlyFansFolder)}).GetList()
    for folder in settings.DRIVE_FOLDERS:
        found = False
        for folder_ in file_list:
            if str(folder) == folder_['title']:
                print("found: {}".format(folder))
                found = True
        if not found:
            print("created")
            contentFolder = PYDRIVE.CreateFile({"title": str(folder), "parents": [{"id": OnlyFansFolder['id']}], "mimeType": "application/vnd.google-apps.folder"})
            contentFolder.Upload()

def get_folder_by_name(folderName):
    settings.maybePrint("Getting Folder: {}".format(folderName))
    try:
        global PYDRIVE
        global FOLDERS
        if FOLDERS is not None:
            if FOLDERS.get(str(folderName)) is not None:
                return FOLDERS.get(str(folderName))
        else:
            FOLDERS = {}
        OnlyFansFolder = get_folder_OnlyFans()
        file_list = PYDRIVE.ListFile({'q': "'{}' in parents and trashed=false"}.format(OnlyFansFolder['id'])).GetList()
        for folder in file_list:
            if str(folder['title']==str(folderName)):
                FOLDERS.set(str(folderName),folder)
                return folder
        if str(settings.CREATE_MISSING_FOLDERS) == "False":
            settings.maybePrint("Skipping: Create Missing Folder - "+str(folderName))
            return
        # create if missing
        folder = PYDRIVE.CreateFile({"title": str(folderName), "mimeType": "application/vnd.google-apps.folder", "parents": [{"kind": "drive#fileLink", "id": OnlyFansFolder}]})
        folder.Upload()
        FOLDERS.set(str(folderName),folder)
        return None
    except Exception as e:
        print(e)

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
    print("Downloading: {}".format(name))
    settings.maybePrint('path: '+str(tmp))
    if str(ext).lower() == ".mp4":
        with open(tmp, 'w+b') as output:
            file_id = file['id']
            request = DRIVE.files().get_media(fileId=file['id'])
            downloader = MediaIoBaseDownload(output, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print("<-- %d%%\r" % (status.progress() * 100),end="")
            print("Download Complete")
        if REPAIR:
            tmp = repair(tmp)
        global FIFTY_MEGABYTES
        if int(os.stat(str(tmp)).st_size) >= FIFTY_MEGABYTES or settings.FORCE_REDUCTION: # greater than 1GB
            tmp = reduce(tmp)
        tmp = fixThumbnail(tmp)
    else:
        file.GetContentFile(tmp)
    ### Finish ###
    if not os.path.isfile(str(tmp)):
        print("Error: Missing Downloaded File")
        return
    print('File Size: '+str(os.path.getsize(tmp)))
    global ONE_MEGABYTE
    if os.path.getsize(tmp) <= ONE_MEGABYTE:
        settings.maybePrint("Warning: Small File Size")
    global ONE_HUNDRED_KILOBYTES
    if os.path.getsize(tmp) <= ONE_HUNDRED_KILOBYTES:
        settings.maybePrint("Error: File Size Too Small")
        print("Download Failure")
        return
    print('Download Complete: File')
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
    print('Download Complete: Gallery')
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
                content_list_galleries = PYDRIVE.ListFile({'q': "'"+content['id']+"' in parents and trashed=false and mimeType contains 'image/jpeg'"}).GetList()
                if len(content_list_galleries)==0:
                    settings.maybePrint('- skipping empty content gallery: '+content['title'])
                elif len(content_list_galleries)>0 and len(content_list_galleries):
                    settings.maybePrint('- content gallery found: '+content['title'])
                    content_found.append(content)
    if len(content_found)==0:
        print('No content folder found!')
        return
    random_content = random.choice(content_found)
    content_title = random_content['title']
    settings.maybePrint("Folder: {}".format(content_title))
    # download folder
    file_list = PYDRIVE.ListFile({'q': "'"+random_content['id']+"' in parents and trashed=false and mimeType contains 'image/jpeg'"}).GetList()
    folder_size = len(file_list)
    settings.maybePrint('Folder size: {}'.format(folder_size))
    settings.maybePrint('Upload limit: {}'.format(settings.IMAGE_UPLOAD_LIMIT))
    # settings.maybePrint("Files: {}".format(file_list))
    if folder_size == 0:
        print("Error: Missing Files")
        return
    file_list_random = []
    for x in range(folder_size):
        random_file = random.choice(file_list)
        file_list.remove(random_file)
        file_list_random.append(random_file)
    file_list_random = file_list_random[:settings.IMAGE_UPLOAD_LIMIT]
    i = 1
    for file in sorted(file_list_random, key = lambda x: x['title']):
        print('Downloading {} from GDrive ({}/{})'.format(file['title'], i, folder_size))
        settings.maybePrint('filePath: '+tmp+"/"+str(file['title']))
        file.GetContentFile(tmp+"/"+str(file['title']))
        i+=1
    print('Download Complete')
    return [file_list_random, tmp, content_title]

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
    if data is None:
        print("Error: Missing Scene Data")
        return
    if content is None:
        print("Error: Missing Scene Content")
        return
    if preview is None:
        print("Error: Missing Scene Preview")
        return
    print('Download Complete: Scene')
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

# Downloads random image from Google Drive
def get_random_image():
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    print('Getting Random Image')
    global PYDRIVE
    OnlyFans_Images_Folder = get_folder_by_name("images")
    random_folders = PYDRIVE.ListFile({'q': "'"+OnlyFans_Images_Folder+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    images_list = []
    random_image = None
    folder_name = None
    for folder in random_folders:
        if str(settings.VERBAL) == "True":
            print('checking folder: '+folder['title'],end="")
        images_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and (mimeType contains \'image/jpeg\' or mimeType contains \'image/jpg\' or mimeType contains \'image/png\')"}).GetList()      
        if len(images_list_tmp)>0:
            images_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    if len(images_list)==0:
        print('No image file found!')
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
    random_folders = PYDRIVE.ListFile({'q': "'"+OnlyFans_Galleries_Folder+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    folder_list = []
    random_gallery = None
    folder_name = None
    for folder in random_folders:
        if str(settings.VERBAL) == "True":
            print('checking galleries: {}'.format(folder['title']),end="")
        gallery_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
        if len(gallery_list_tmp)>0:
            folder_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    random.shuffle(folder_list)
    for folder in folder_list:
        if str(settings.VERBAL) == "True":
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
        print('No gallery folders found!')
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
        print('No performer folder found!')
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
    random_folders = PYDRIVE.ListFile({'q': "'"+OnlyFans_Videos_Folder+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    video_list = []
    random_video = None
    folder_name = None
    for folder in random_folders:
        if str(settings.VERBAL) == "True":
            print('checking folder: '+folder['title'],end="")
        video_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'video/mp4'"}).GetList()
        if len(video_list_tmp)>0:
            video_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    if len(video_list)==0:
        print('No video file found!')
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
    random_folders = PYDRIVE.ListFile({'q': "'"+OnlyFans_Scenes_Folder+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
    folder_list = []
    random_scene = None
    folder_name = None
    for folder in random_folders:
        if str(settings.VERBAL) == "True":
            print('checking scenes: '+folder['title'],end="")
        scene_list_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'application/vnd.google-apps.folder'"}).GetList()
        if len(scene_list_tmp)>0:
            folder_list.append(folder)
            settings.maybePrint(" -> added")
        else:
            settings.maybePrint(" -> empty")
    random.shuffle(folder_list)
    for folder in folder_list:
        if str(settings.VERBAL) == "True":
            print('checking scene: '+folder['title'],end="")
        scene_list_tmp_tmp = PYDRIVE.ListFile({'q': "'"+folder['id']+"' in parents and trashed=false and mimeType contains 'text/plain'"}).GetList()
        if len(scene_list_tmp_tmp)>0:
            folder_name = folder['title']
            random_scene = folder
            settings.maybePrint(" -> found")
        else:
            settings.maybePrint(" -> empty")
    if not random_scene:
        print('No scene folders found!')
        return
    print('Random Scene: '+random_scene['title'])
    return [random_scene, folder_name]

def get_random_test():
    global AUTH
    if not AUTH:
        AUTH = authGoogle()
    print('Getting Random: Test')
    global PYDRIVE
    OnlyFans_Scenes_Folder = get_folder_by_name("test")

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
    repairedPath = str(path).replace(".mp4", "_fixed.mp4")
    try:
        print("Repairing: {} <-> {}".format(path, settings.WORKING_VIDEO))
        if str(settings.DEBUG) == "True":
            fixed = subprocess.call(['untrunc', str(settings.WORKING_VIDEO), str(path)])
        else:
            subprocess.Popen(['untrunc', str(settings.WORKING_VIDEO), str(path)],stdin=FNULL,stdout=FNULL)
        fixed.communicate()
    except AttributeError:
        if os.path.isfile(str(path)+"_fixed.mp4"):
            shutil.move(str(path)+"_fixed.mp4", repairedPath)
            print("Repair Successful")
    except:
        settings.maybePrint(sys.exc_info()[0])
        print("Warning: Skipping Repair")
        return path
    print("Repair Complete")
    return str(repairedPath)

def reduce(path):
    reducedPath = str(path).replace(".mp4", "_reduced.mp4")
    try:
        print("Reducing: {}".format(path))
        try:
            clip = VideoFileClip(str(path))
            print("Length: {}".format(clip.duration))
            bitrate = 1000000000 / int(clip.duration)
            print("Bitrate: {}".format(bitrate))
        except FileNotFoundError:
            print("Error: Missing File to Reduce")
            return path
        loglevel = "quiet"
        if str(settings.DEBUG) == "True":
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
    print("Original Size: {}".format(originalSize))
    print("Reduced Size: {}".format(newSize))
    if int(originalSize) < int(newSize):
        print("Warning: Original Size Smaller")
        return path
    if int(newSize) == 0:
        print("Error: Missing Reduced File")
        return path
    return reducedPath

def fixThumbnail(path):
    thumbedPath = str(path).replace(".mp4", "_thumbed.mp4")
    try:
        print("Thumbnailing: {}".format(path))
        loglevel = "quiet"
        if str(settings.DEBUG) == "True":
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
    print("Original Size: {}".format(originalSize))
    print("Thumbed Size: {}".format(newSize))
    if int(originalSize) < int(newSize):
        print("Warning: Original Size Smaller")
        return path
    if int(newSize) == 0:
        print("Error: Missing Thumbnailed File")
        return path
    return thumbedPath
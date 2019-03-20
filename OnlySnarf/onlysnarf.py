#!/usr/bin/python
# 9/22/2018 - Skeetzo
# 10/10/2018: args overhaul
# 10/20/2018: usability overhaul
# 1/21/2019: upload fix & hashtagging
# 2/3/2019: upload ext fix & tweeting
# 2/6/2019: menu
# 3/18/2019: file separation cleanup

import random
import os
import shutil
import datetime
import json
import sys
import pathlib

from . import google as Google
from . import driver as OnlySnarf
# from pprint import pprint

CONFIG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.json')
# MOUNT_PATH = "/var/mnt"
MOUNT_PATH = None
DEBUG = False
DEBUG_SKIP_DOWNLOAD = True
IMAGE_UPLOAD_LIMIT = 6
REMOVE_LOCAL = True
# selenium web browser
BROWSER = None
# backup uploaded content
BACKING_UP = True
# delete uploaded content
DELETING = False
# -v -> video
# -g -> gallery
# -i -> image
TYPE = None
# Twitter hashtags
HASHTAGGING = False
# -f -> force / ignore upload max wait
FORCE_UPLOAD = False
# -show -> shows window
SHOW_WINDOW = False
# -t -> text
TEXT = None
# -q -> quiet / no tweet
TWEETING = True
FOLDER_NAME = None

################
##### Args #####
################
i = 0
while i < len(sys.argv):
    if '-v' in str(sys.argv[i]):
        TYPE = "video"
    if '-g' in str(sys.argv[i]):
        TYPE = "gallery"
    if '-i' in str(sys.argv[i]):
        TYPE = "image"
    if '-t' in str(sys.argv[i]):
        TEXT = str(sys.argv[i+1])
    if '-d' in str(sys.argv[i]):
        DEBUG = True
    if '-h' in str(sys.argv[i]):
        HASHTAGGING = True
    if '-f' in str(sys.argv[i]):
        FORCE_UPLOAD = True
    if '-show' in str(sys.argv[i]):
        SHOW_WINDOW = True
    if '-q' in str(sys.argv[i]):
        TWEETING = False
    if '-delete' in str(sys.argv[i]):
        DELETING = False
    i += 1

def updateDefaults(args):
    for arg in args:
        if arg[0] == "Debug":
            global DEBUG
            DEBUG = arg[1]
        if arg[0] == "Debug Skip Download":
            global DEBUG_SKIP_DOWNLOAD
            DEBUG_SKIP_DOWNLOAD = arg[1]
        if arg[0] == "Image Upload Limit":
            global IMAGE_UPLOAD_LIMIT
            IMAGE_UPLOAD_LIMIT = arg[1]
        if arg[0] == "Backup":
            global BACKING_UP
            BACKING_UP = arg[1]
        if arg[0] == "Delete Google":
            global DELETING
            DELETING = arg[1]
        if arg[0] == "Delete Local":
            global REMOVE_LOCAL
            REMOVE_LOCAL = arg[1]
        if arg[0] == "Hashtag":
            global HASHTAGGING
            HASHTAGGING = arg[1]
        if arg[0] == "Force Upload":
            global FORCE_UPLOAD
            FORCE_UPLOAD = arg[1]
        if arg[0] == "Show Window":
            global SHOW_WINDOW
            SHOW_WINDOW = arg[1]
        if arg[0] == "Text":
            global TEXT
            TEXT = arg[1]
        if arg[0] == "Tweeting":
            global TWEETING        
            TWEETING = arg[1]
        if arg[0] == "Type":
            global TYPE        
            TYPE = arg[1]
        if arg[0] == "Mount":
            global MOUNT_PATH        
            MOUNT_PATH = arg[1]

def argsToArray():
    return [
        # [ "File Name", FILE_NAME],
        # [ "File Path", FILE_PATH],
        # [ "Location", LOCATION, ["Local","Google"]],
        [ "Backup", BACKING_UP, ["True","False"]],
        [ "Delete Google", DELETING, ["True","False"]],
        [ "Delete Local", REMOVE_LOCAL, ["True","False"]],
        [ "Hashtag", HASHTAGGING, ["True","False"]],
        [ "Force Upload", FORCE_UPLOAD, ["True","False"]],
        [ "Show Window", SHOW_WINDOW, ["True","False"]],
        [ "Text", TEXT],
        [ "Type", TYPE],
        [ "Tweeting", TWEETING, ["True","False"]],
        [ "Debug", DEBUG, ["True","False"]],
        # [ "Debug Skip Download", DEBUG_SKIP_DOWNLOAD, ["True","False"]]    
    ]
 
# debugging
def maybePrint(text):
    if DEBUG:
        print(text);

##################
##### Config #####
##################
try:
    with open(CONFIG_FILE) as config_file:    
        config = json.load(config_file)
except FileNotFoundError:
    print('Missing Config, run `onlysnarf-config`')
    sys.exit(0)
    # from . import config as CONFIG
    # CONFIG.main()
    # with open(CONFIG_FILE) as config_file:    
        # config = json.load(config_file)

##########################
##### MENU FUNCTIONS #####
##########################

def all(fileChoice, args):
    updateDefaults(args)
    global TYPE
    TYPE = str(fileChoice)
    main()

def download(fileChoice, args):
    updateDefaults(args)
    auth = Google.authGoogle()
    if not auth:
        return
    if fileChoice == 'image':
        return download_image_()
    elif fileChoice == 'gallery':
        return download_gallery_()
    elif fileChoice == 'video':
        return download_video_()

def download_image_():
    if DEBUG:
        print('Deleting Locals')
        remove_local()
    print('Fetching Content')
    random_file = Google.get_random_image(argsToArray())
    if random_file == None:
        print('Missing Random Image')
        return
    file_name = random_file['title']
    file_path = Google.download_file(argsToArray(), random_file)
    if random_file == None:
        print('Missing Random Image')
        return
    if file_path == None:
        print('Missing Random Image: Empty Download')
        return
    return [file_name, file_path]

def download_gallery_():
    if DEBUG:
        print('Deleting Locals')
        remove_local()
    print('Fetching Content')
    random_file = Google.get_random_gallery(argsToArray())
    if random_file == None:
        print('Missing Random Gallery')
        return
    file_name = random_file['title']
    file_path = Google.download_gallery(argsToArray(), random_file)
    if file_path == None:
        print('Missing Random Gallery: Empty Download')
        return
    return [file_name, file_path]

def download_video_():
    if DEBUG:
        print('Deleting Locals')
        remove_local()
    print('Fetching Content')
    random_file = Google.get_random_video()
    file_name = random_file['title']
    file_path = Google.download_file(random_file)
    if random_file == None:
        print('Missing Random Video')
        return
    if file_path == None:
        print('Missing Random Video: Empty Download')
        return
    return [file_name, file_path]

def upload(fileChoice, args):
    updateDefaults(args)
    file_name = None
    file_path = None
    for arg in args:
        if arg[0] == "file_name":
            file_name = arg[1]
        if arg[0] == "file_path":
            file_path = arg[1]
    print('file name: '+str(file_name))
    print('file path: '+str(file_path))
    if fileChoice == 'image':
        return upload_image_(file_name, file_path)
    elif fileChoice == 'gallery':
        return upload_gallery_(file_name, file_path)
    elif fileChoice == 'video':
        return upload_video_(file_name, file_path)
    else:
        print("Missing Upload Choice")

def upload_image_(file_name, file_path):
    print('Accessing OnlyFans')
    OnlySnarf.log_into_OnlyFans(SHOW_WINDOW)
    OnlySnarf.upload_file_to_OnlyFans(argsToArray(), file_name, file_path, FOLDER_NAME)
    print('Upload Complete')

def upload_gallery_(file_name, file_path):
    print('Accessing OnlyFans')
    OnlySnarf.log_into_OnlyFans(SHOW_WINDOW)
    OnlySnarf.upload_directory_to_OnlyFans(argsToArray(), file_name, file_path, FOLDER_NAME)
    print('Upload Complete')

def upload_video_(file_name, file_path):
    print('Accessing OnlyFans')
    OnlySnarf.log_into_OnlyFans(SHOW_WINDOW)
    OnlySnarf.upload_file_to_OnlyFans(argsToArray(), file_name, file_path, FOLDER_NAME)
    print('Upload Complete')

def backup(fileChoice, args):
    updateDefaults(args)
    print("Missing Feature: Backup")

#####################
##### FUNCTIONS #####
#####################

# Deletes local file
def remove_local():
    if REMOVE_LOCAL == False:
        print("Skipping Local Remove")
        return
    # print('Deleting Local File(s)')
    # delete /tmp
    tmp = os.getcwd()
    if MOUNT_PATH:
        tmp = MOUNT_PATH
    tmp += '/tmp'
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
        print('Local File(s) Removed')
    else:
        print('Local Files Not Found')

def main():
    ARGS = argsToArray()
    auth = Google.authGoogle(ARGS)
    if not auth:
        return
    if DEBUG:
        print('0/3 : Deleting Locals')
        remove_local()
    print('1/3 : Fetching Content')
    random_file = None
    file_name = None
    file_path = None
    folder_name = None
    if TYPE == "gallery":
        response = Google.get_random_gallery(ARGS)
        random_file = response[0]
        folder_name = response[1]
        if random_file == None:
            return
        file_name = random_file['title']
        results = Google.download_gallery(ARGS, random_file)
        gallery_files = results[0]
        file_path = results[1]
    elif TYPE == "video":
        response = Google.get_random_video(ARGS)
        random_file = response[0]
        folder_name = response[1]
        if random_file == None:
            return
        file_name = random_file['title']
        file_path = Google.download_file(ARGS, random_file)
    elif TYPE == "image":
        response = Google.get_random_image(ARGS)
        random_file = response[0]
        folder_name = response[1]
        if random_file == None:
            return
        file_name = random_file['title']
        file_path = Google.download_file(ARGS, random_file)
    else:
        print('Missing Args!')
        return
    if random_file == None:
        print('Missing Random File / Directory!')
        return
    if file_path == None:
        print('Missing Random Video: Empty Download')
        return
    sys.stdout.flush()
    #################################################
    print('2/3 : Accessing OnlyFans')
    OnlySnarf.log_into_OnlyFans(SHOW_WINDOW)
    if TYPE == "gallery":
        OnlySnarf.upload_directory_to_OnlyFans(ARGS, file_name, file_path, folder_name)
    elif TYPE == "video" or TYPE == "image":
        OnlySnarf.upload_file_to_OnlyFans(ARGS, file_name, file_path, folder_name)
    else:
        print('Missing OnlyFans Instructions!')
        return
    print('Upload Complete')
    sys.stdout.flush()
    #################################################
    print('3/3 : Cleaning Up Files')
    remove_local()
    if TYPE == "gallery":
        Google.move_files(ARGS, file_name, gallery_files)
    else:
        Google.move_file(ARGS, random_file)
    delete_file(random_file)
    print('Files Cleaned ')
    #################################################
    print('Google Drive to OnlyFans Upload Complete!')
    sys.stdout.flush()

################################################################################################################################################

if __name__ == "__main__":
    try:
        # os.system('clear')
        print('OnlySnarf Settings:')
        print(' - DEBUG = '+str(DEBUG))
        print(' - BACKING_UP = '+str(BACKING_UP))
        print(' - HASHTAGGING = '+str(HASHTAGGING))
        print(' - TWEETING = '+str(TWEETING))
        print(' - FORCE_UPLOAD = '+str(FORCE_UPLOAD))
        main()
    except:
        print(sys.exc_info()[0])
        print("Shnarf!")
    finally:
        sys.exit(0)
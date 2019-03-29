#!/usr/bin/python
# 3/28/2019 Skeetzo

import random
import os
import shutil
import datetime
import json
import sys
import pathlib
from . import settings
from . import google as Google
from . import driver as OnlySnarf
# from pprint import pprint

###################
##### Helpers #####
###################

# debugging
def maybePrint(text):
    if settings.DEBUG:
        print(text);

def getTmp():
    # mkdir /tmp
    tmp = os.getcwd()
    if settings.MOUNT_PATH:
        tmp = os.path.join(settings.MOUNT_PATH, "tmp")
    else:
        tmp = os.path.join(tmp, "tmp")
    if not os.path.exists(str(tmp)):
        os.mkdir(str(tmp))
    return tmp

##########################
##### MENU FUNCTIONS #####
##########################

def test(TYPE):
    settings.TYPE = TYPE
    # auth = Google.authGoogle()
    # if not auth:
        # return
    print('0/3 : Deleting Locals')
    remove_local()
    print('1/3 : Testing')
    # users = OnlySnarf.get_users()
    message_all(image=settings.IMAGE)

def all(TYPE):
    settings.TYPE = TYPE
    main()

def download(fileChoice):
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
    remove_local()
    print('Fetching Content')
    random_file = Google.get_random_image()
    if random_file == None:
        print('Missing Random Image')
        return
    file_name = random_file['title']
    file_path = Google.download_file(random_file)
    if random_file == None:
        print('Missing Random Image')
        return
    if file_path == None:
        print('Missing Random Image: Empty Download')
        return
    return [file_name, file_path]

def download_gallery_():
    remove_local()
    print('Fetching Content')
    random_file = Google.get_random_gallery()
    if random_file == None:
        print('Missing Random Gallery')
        return
    file_name = random_file['title']
    file_path = Google.download_gallery(random_file)
    if file_path == None:
        print('Missing Random Gallery: Empty Download')
        return
    return [file_name, file_path]

def download_video_():
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

def upload(fileChoice):
    if fileChoice == 'image':
        return upload_image_(settings.FILE_NAME, settings.FILE_PATH)
    elif fileChoice == 'gallery':
        return upload_gallery_(settings.FILE_NAME, settings.FILE_PATH)
    elif fileChoice == 'video':
        return upload_video_(settings.FILE_NAME, settings.FILE_PATH)
    else:
        print("Missing Upload Choice")

def upload_image_():
    print('Accessing OnlyFans')
    OnlySnarf.log_into_OnlyFans()
    OnlySnarf.upload_file_to_OnlyFans(settings.FILE_NAME, settings.FILE_PATH, FOLDER_NAME)
    print('Upload Complete')

def upload_gallery_():
    print('Accessing OnlyFans')
    OnlySnarf.log_into_OnlyFans()
    OnlySnarf.upload_directory_to_OnlyFans(settings.FILE_NAME, settings.FILE_PATH, FOLDER_NAME)
    print('Upload Complete')

def upload_video_():
    print('Accessing OnlyFans')
    OnlySnarf.log_into_OnlyFans()
    OnlySnarf.upload_file_to_OnlyFans(settings.FILE_NAME, settings.FILE_PATH, FOLDER_NAME)
    print('Upload Complete')

def backup(fileChoice, args):
    print("Missing Feature: Backup")

####################
##### Messages #####
####################

def message_all(message=":)", image=None, price="10.00"):
    print("Messaging: All")
    users = OnlySnarf.get_users()
    for user in users:
        user.sendMessage(message, image, price)

def message_recent(message=":)", image=None, price="10.00"):
    print("Messaging: Recent")
    users = OnlySnarf.get_recent_users()
    for user in users:
        user.sendMessage(message, image, price)

def message_by_username(username=None, message=":)", image=None, price="10.00"):
    print("Messaging: User - %s" % username)
    OnlySnarf.get_user_by_username(str(username)).sendMessage(message, image, price)

#################
##### Crons ##### -> move to onlysnarf.py
#################

# sends a message to all recent subscribers
def greet_new_subscribers():
    pass # needs to add OnlySnarf.searchNotificationsForNewSubscribers

#####################
##### FUNCTIONS #####
#####################

# Deletes local file
def remove_local():
    if settings.REMOVE_LOCAL == False:
        print("Skipping Local Remove")
        return
    # print('Deleting Local File(s)')
    # delete /tmp
    tmp = getTmp()
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
        print('Local File(s) Removed')
    else:
        print('Local Files Not Found')

def main():
    auth = Google.authGoogle()
    if not auth:
        return
    if settings.DEBUG:
        print('0/3 : Deleting Locals')
        remove_local()
    print('1/3 : Fetching Content')
    random_file = None
    file_name = None
    file_path = None
    folder_name = None
    if settings.TYPE == "gallery":
        response = Google.get_random_gallery()
        random_file = response[0]
        folder_name = response[1]
        if random_file == None:
            return
        file_name = random_file['title']
        results = Google.download_gallery(random_file)
        gallery_files = results[0]
        file_path = results[1]
    elif settings.TYPE == "video":
        response = Google.get_random_video()
        random_file = response[0]
        folder_name = response[1]
        if random_file == None:
            return
        file_name = random_file['title']
        file_path = Google.download_file(random_file)
    elif settings.TYPE == "image":
        response = Google.get_random_image()
        random_file = response[0]
        folder_name = response[1]
        if random_file == None:
            return
        file_name = random_file['title']
        file_path = Google.download_file(random_file)
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
    OnlySnarf.log_into_OnlyFans(settings.SHOW_WINDOW)
    if settings.TYPE == "gallery":
        OnlySnarf.upload_directory_to_OnlyFans(file_name, file_path, folder_name)
    elif settings.TYPE == "video" or settings.TYPE == "image":
        OnlySnarf.upload_file_to_OnlyFans(file_name, file_path, folder_name)
    else:
        print('Missing OnlyFans Instructions!')
        return
    print('Upload Complete')
    sys.stdout.flush()
    #################################################
    print('3/3 : Cleaning Up Files')
    remove_local()
    if settings.TYPE == "gallery":
        Google.move_files(file_name, gallery_files)
    else:
        Google.move_file(random_file)
    Google.delete_file(random_file)
    print('Files Cleaned ')
    #################################################
    print('Google Drive to OnlyFans Upload Complete!')
    sys.stdout.flush()

################################################################################################################################################

if __name__ == "__main__":
    try:
        # os.system('clear')
        print('OnlySnarf Settings:')
        print(' - DEBUG = '+str(settings.DEBUG))
        print(' - BACKING_UP = '+str(settings.BACKING_UP))
        print(' - HASHTAGGING = '+str(settings.HASHTAGGING))
        print(' - TWEETING = '+str(settings.TWEETING))
        print(' - FORCE_UPLOAD = '+str(settings.FORCE_UPLOAD))
        main()
    except:
        print(sys.exc_info()[0])
        print("Shnarf!")
    finally:
        sys.exit(0)
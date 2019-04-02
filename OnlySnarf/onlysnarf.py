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

AUTH = False

###################
##### Helpers #####
###################

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
    users = OnlySnarf.get_users()
    return
    response = download_random_image()
    if not response or response == None:
        print("Error: Missing Image")
        return
    # message_all(image=response[1])
    message_recent(image=response[1])
    Google.move_file(response[2])
    OnlySnarf.exit()

def all(TYPE):
    settings.TYPE = TYPE
    main()

# upload a file or gallery
# send a message to [recent, all, user] w/ a preview image
def upload_and_announce(fileChoice):
    settings.TYPE = fileChoice
    response = download_random_image()
    upload(fileChoice, filename=response[0], filepath=response[1])
    # uploads a file or gallery
    # sends a message to all users w/ a preview image
    

# 

def download(fileChoice):
    if fileChoice == 'image':
        return download_random_image()
    elif fileChoice == 'gallery':
        return download_random_gallery()
    elif fileChoice == 'video':
        return download_random_video()

def download_random_image():
    global AUTH
    if not AUTH:
        AUTH = Google.authGoogle()
    remove_local()
    print('Fetching Content')
    response = Google.get_random_image()
    random_file = response[0]
    folder_name = response[1]
    if random_file == None:
        return
    file_name = random_file['title']
    file_path = Google.download_file(random_file)
    if random_file == None:
        print('Missing Random Image')
        return
    if file_path == None:
        print('Missing Random Image: Empty Download')
        return
    return [file_name, file_path, random_file]

def download_random_gallery():
    global AUTH
    if not AUTH:
        AUTH = Google.authGoogle()
    remove_local()
    print('Fetching Content')
    response = Google.get_random_gallery()
    random_file = response[0]
    folder_name = response[1]
    if random_file == None:
        return
    file_name = random_file['title']
    results = Google.download_gallery(random_file)
    gallery_files = results[0]
    file_path = results[1]
    if file_path == None:
        print('Missing Random Gallery: Empty Download')
        return
    return [file_name, file_path, random_file]

def download_random_video():
    global AUTH
    if not AUTH:
        AUTH = Google.authGoogle()
    remove_local()
    print('Fetching Content')
    response = Google.get_random_video()
    random_file = response[0]
    folder_name = response[1]
    if random_file == None:
        return
    file_name = random_file['title']
    file_path = Google.download_file(random_file)
    if random_file == None:
        print('Missing Random Video')
        return
    if file_path == None:
        print('Missing Random Video: Empty Download')
        return
    return [file_name, file_path, random_file]

def upload(fileChoice, filename=settings.FILE_NAME, filepath=settings.FILE_PATH):
    if fileChoice == 'image':
        return upload_image(filename, filepath)
    elif fileChoice == 'gallery':
        return upload_gallery(filename, filepath)
    elif fileChoice == 'video':
        return upload_video(filename, filepath)
    else:
        print("Missing Upload Choice")

def upload_image(filename, filepath):
    print('Accessing OnlyFans')
    OnlySnarf.upload_file_to_OnlyFans(settings.FILE_NAME, settings.FILE_PATH, FOLDER_NAME)
    print('Upload Complete')

def upload_gallery(filename, filepath):
    print('Accessing OnlyFans')
    OnlySnarf.upload_directory_to_OnlyFans(settings.FILE_NAME, settings.FILE_PATH, FOLDER_NAME)
    print('Upload Complete')

def upload_video(filename, filepath):
    print('Accessing OnlyFans')
    OnlySnarf.upload_file_to_OnlyFans(settings.FILE_NAME, settings.FILE_PATH, FOLDER_NAME)
    print('Upload Complete')

def backup(fileChoice, args):
    print("Missing Feature: Backup")

####################
##### Messages #####
####################

def message_all(message=settings.DEFAULT_MESSAGE, image=settings.IMAGE, price=settings.DEFAULT_PRICE):
    print("Messaging: All")
    users = OnlySnarf.get_users()
    for user in users:
        user.sendMessage(message, image, price)

def message_recent(message=settings.DEFAULT_MESSAGE, image=settings.IMAGE, price=settings.DEFAULT_PRICE):
    print("Messaging: Recent")
    users = OnlySnarf.get_recent_users()
    for user in users:
        user.sendMessage(message, image, price)

def message_by_username(username=None, message=settings.DEFAULT_MESSAGE, image=settings.IMAGE, price=settings.DEFAULT_PRICE):
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
    global AUTH
    if not AUTH:
        AUTH = Google.authGoogle()
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
    OnlySnarf.log_into_OnlyFans()
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
    print('Google Drive to OnlyFans Upload Complete')
    sys.stdout.flush()
    OnlySnarf.exit()

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
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

#################
##### Crons #####
#################

# sends a message to all recent subscribers
def greet_new_subscribers():
    pass # needs to add OnlySnarf.searchNotificationsForNewSubscribers

# sends the image / message prepared for all users
def send_user_messages():
    pass

##########################
##### MENU FUNCTIONS #####
##########################

def all(TYPE):
    settings.TYPE = TYPE
    main()

####################
##### Download #####
####################

def download(fileChoice):
    if fileChoice == 'image':
        return download_random_image()
    elif fileChoice == 'gallery':
        return download_random_gallery()
    elif fileChoice == 'video':
        return download_random_video()
    elif fileChoice == 'scene':
        return download_random_scene()
    else:
        return print("Error: Missing File Choice")

def download_random_image():
    global AUTH
    if not AUTH:
        AUTH = Google.authGoogle()
    remove_local()
    print('Fetching Content')
    response = Google.get_random_image()
    google_file = response[0]
    folder_name = response[1]
    if google_file == None:
        return
    file_name = google_file['title']
    file_path = Google.download_file(google_file)
    if google_file == None:
        print('Missing Random Image')
        return
    if file_path == None:
        print('Missing Random Image: Empty Download')
        return
    return [file_name, file_path, google_file]

def download_random_gallery():
    global AUTH
    if not AUTH:
        AUTH = Google.authGoogle()
    remove_local()
    print('Fetching Content')
    response = Google.get_random_gallery()
    google_file = response[0]
    folder_name = response[1]
    if google_file == None:
        return
    file_name = google_file['title']
    results = Google.download_gallery(google_file)
    gallery_files = results[0]
    file_path = results[1]
    if file_path == None:
        print('Missing Random Gallery: Empty Download')
        return
    return [file_name, file_path, google_file]

def download_random_video():
    global AUTH
    if not AUTH:
        AUTH = Google.authGoogle()
    remove_local()
    print('Fetching Content')
    response = Google.get_random_video()
    google_file = response[0]
    folder_name = response[1]
    if google_file == None:
        return
    file_name = google_file['title']
    repair = False
    if str(folder_name) == "gopro":
        repair = True
    file_path = Google.download_file(google_file, REPAIR=repair)
    if google_file == None:
        print('Missing Random Video')
        return
    if file_path == None:
        print('Missing Random Video: Empty Download')
        return
    return [file_name, file_path, google_file]

def download_random_scene():
    global AUTH
    if not AUTH:
        AUTH = Google.authGoogle()
    remove_local()
    print('Fetching Content')
    response = Google.get_random_scene()
    google_file = response[0]
    folder_name = response[1]
    if google_file == None:
        return
    file_name = google_file['title']
    results = Google.download_scene(google_file)
    if results == None:
        print('Missing Random Scene: Empty Download')
        return
    return results

####################
##### Messages #####
####################

def message_all(message=None, image=None, price=None):
    print("Messaging: All")
    users = OnlySnarf.get_users()
    for user in users:
        user.sendMessage(message, image, price)

def message_recent(message=None, image=None, price=None):
    print("Messaging: Recent")
    users = OnlySnarf.get_recent_users()
    for user in users:
        user.sendMessage(message, image, price)

def message_favorites(message=None, image=None, price=None):
    print("Messaging: Recent")
    users = OnlySnarf.get_favorite_users()
    for user in users:
        user.sendMessage(message, image, price)

def message_by_username(username=None, message=None, image=None, price=None):
    print("Messaging: User - %s" % username)
    OnlySnarf.get_user_by_username(str(username)).sendMessage(message, image, price)

#################
##### Reset #####
#################

# Deletes local file
def remove_local():
    try:
        if settings.REMOVE_LOCAL == False:
            print("Skipping Local Remove")
            return
        # print('Deleting Local File(s)')
        # delete /tmp
        tmp = settings.getTmp()
        if os.path.exists(tmp):
            shutil.rmtree(tmp)
            print('Local File(s) Removed')
        else:
            print('Local Files Not Found')
    except OSError as e:
        print("Error: Missing Local Path")

#################
##### Scene #####
#################

# upload a file or gallery
# send a message to [recent, all, user] w/ a preview image
def release_scene(userChoice="all"):
    response = download("scene")
    print("Scene: {}".format(response))
    content = response[0]
    preview = response[1]
    data = response[2]
    # print("Data:\n{}".format(json.dumps(data, sort_keys=True, indent=4)))
    data = json.loads(data)
    # print("Data: {}".format(data))
    title = None
    message = None
    price = None
    try:
        title = data["title"]
        message = data["message"]
        price = data["price"]
    except Exception as e:
        settings.maybePrint(e)
    if title == None or message == None or price == None:
        return print("Error: Missing Scene Data")
    print("Scene:")
    print("- Title: {}".format(title))
    print("- Message: {}".format(message))
    print("- Price: {}".format(price))
    upload("scene", filename=title, filepath=content)
    if str(userChoice) == "all":
        message_all(message=message, image=preview, price=price)
    elif str(userChoice) == "recent":
        message_recent(message=message, image=preview, price=price)
    elif str(userChoice) == "favorite":
        message_favorites(message=message, image=preview, price=price)
    else:
        message_by_username(message=message, image=preview, price=price, username=userChoice)

##################
##### Upload #####
##################

def upload(fileChoice, filename=None, filepath=None):
    settings.TYPE = fileChoice
    if fileChoice == 'image':
        OnlySnarf.upload_file_to_OnlyFans(filename, filepath)
    elif fileChoice == 'gallery':
        OnlySnarf.upload_directory_to_OnlyFans(filename, filepath)
    elif fileChoice == 'video':
        OnlySnarf.upload_file_to_OnlyFans(filename, filepath)
    elif fileChoice == 'scene':
        OnlySnarf.upload_scene_to_OnlyFans(filename, filepath)
    else:
        print("Missing Upload Choice")
    print('Upload Complete')


def test(TYPE):
    settings.TYPE = TYPE
    # auth = Google.authGoogle()
    # if not auth:
        # return
    print('0/3 : Deleting Locals')
    remove_local()
    print('1/3 : Testing')

    ### Users ###
    # users = OnlySnarf.get_users()
    # return
    #####################
    OnlySnarf.update_chat_logs()
    
    ### Scene ###
    # release_scene(userChoice="all")
    # return
    #############

    ### Message ###
    # response = download_random_image()
    # if not response or response == None:
        # print("Error: Missing Image")
        # return
    # message_all(message="Creampie Clue :D", image=response[1], price="10.00")
    # message_recent(message=":)", image=response[1], price="50.00")
    # Google.move_file(response[2])
    ###############

    ### Exit Gracefully ###
    OnlySnarf.exit()
    #######################


#####################
##### FUNCTIONS #####
#####################



def main():
    global AUTH
    if not AUTH:
        AUTH = Google.authGoogle()
    print('0/3 : Deleting Locals')
    remove_local()
    print('1/3 : Fetching Content')
    google_file = None
    file_name = None
    file_path = None
    folder_name = None
    if settings.TYPE == "gallery":
        response = Google.get_random_gallery()
        google_file = response[0]
        folder_name = response[1]
        if google_file == None:
            return
        file_name = google_file['title']
        results = Google.download_gallery(google_file)
        # gallery_files = results[0]
        file_path = results[1]
    elif settings.TYPE == "video":
        response = Google.get_random_video()
        google_file = response[0]
        folder_name = response[1]
        if google_file == None:
            return
        file_name = google_file['title']
        repair = False
        if str(folder_name) == "gopro":
            repair = True
        file_path = Google.download_file(google_file, REPAIR=repair)
    elif settings.TYPE == "image":
        response = Google.get_random_image()
        google_file = response[0]
        folder_name = response[1]
        if google_file == None:
            return
        file_name = google_file['title']
        file_path = Google.download_file(google_file)
    elif settings.TYPE == "scene":
        response = Google.get_random_scene()
        google_file = response[0]
        folder_name = response[1]
        if google_file == None:
            return
        file_name = google_file['title']
        results = Google.download_scene(google_file)
        # scene_files = results[0]
        file_path = results[1]
    else:
        print('Missing Args!')
        return
    if google_file == None:
        print('Missing Random File / Directory!')
        return
    if file_path == None:
        print('Missing Random Video: Empty Download')
        return
    sys.stdout.flush()
    #################################################
    print('2/3 : Accessing OnlyFans')
    logged_in = OnlySnarf.log_into_OnlyFans()
    if logged_in == False:
        print("Error: Login Failure")
        return
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
        Google.move_file(google_file)
    Google.delete_file(google_file)
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
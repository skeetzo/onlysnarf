#!/usr/bin/python3
# 3/28/2019 Skeetzo

import random
import os
import shutil
import datetime
import json
import sys
import pathlib
import time
from .settings import SETTINGS as settings
from . import google as Google
from . import driver as OnlySnarf
# from pprint import pprint

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
    elif fileChoice == 'performer':
        return download_random_performer()
    elif fileChoice == 'scene':
        return download_random_scene()
    elif fileChoice == 'video':
        return download_random_video()
    else:
        return print("Error: Missing File Choice")

def download_random_image():
    remove_local()
    print('Fetching Image')
    response = Google.get_random_image()
    if response == None:
        print("Error: Missing Image Download")
        return
    google_file = response[0]
    folder_name = response[1]
    if google_file == None:
        return
    file_name = google_file['title']
    file_path = Google.download_file(google_file)
    if google_file == None:
        print('Error: Missing Random Image')
        return
    if file_path == None:
        print('Error: Empty Download')
        return
    return [file_name, file_path, google_file, folder_name]

def download_random_gallery():
    remove_local()
    print('Fetching Gallery')
    response = Google.get_random_gallery()
    if response == None:
        print("Error: Missing Gallery Download")
        return
    google_file = response[0]
    folder_name = response[1]
    if google_file == None:
        print("Error: Missing Google File")
        return
    file_name = google_file['title']
    results = Google.download_gallery(google_file)
    gallery_files = results[0]
    file_path = results[1]
    if file_path == None:
        print('Error: Missing Random Gallery')
        return
    return [file_name, file_path, google_file, gallery_files, folder_name]

def download_random_performer():
    remove_local()
    print('Fetching Performer')
    google_file = Google.get_random_performer()
    performer = google_file['title']
    results = Google.download_performer(google_file)
    if results == None:
        print("Error: Missing Performer Download")
        return
    gallery_files = results[0]
    file_path = results[1]
    gallery_name = results[2]
    if file_path == None:
        print('Error: Missing Content')
        return
    if gallery_files == None:
        print('Error: Missing Gallery Content')
        return
    if performer == None:
        print('Error: Missing Performer Name')
        return
    if gallery_name == None:
        print('Error: Missing Gallery Name')
        return
    return [file_path, google_file, performer, gallery_name, google_file]

def download_random_video():
    remove_local()
    print('Fetching Video')
    response = Google.get_random_video()
    if response == None:
        print("Error: Missing Video Download")
        return
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
        print('Error: Missing Random Video')
        return
    if file_path == None:
        print('Error: Empty Download')
        return
    return [file_name, file_path, google_file, folder_name]

def download_random_scene():
    remove_local()
    print('Fetching Scene')
    response = Google.get_random_scene()
    if response == None:
        print("Error: Missing Scene Download")
        return
    google_file = response[0]
    folder_name = response[1]
    if google_file == None:
        print("Error: Missing Google File")
        return
    file_name = google_file['title']
    results = Google.download_scene(google_file)
    if results == None:
        print('Error: Empty Download')
        return
    return results

####################
##### Messages #####
####################

def message(choice=None, message=None, image=None, price=None):
    print("Messaging: {}".format(choice))
    OnlySnarf.message(choice, message, image, price)

#################
##### Reset #####
#################

# Deletes local file
def remove_local():
    try:
        if str(settings.REMOVE_LOCAL) == "False":
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
    except Exception as e:
        print(e)

###################
##### Release #####
###################

def release_image():
    try:
        print("Releasing Image")
        response = download("image")
        if response == None:
            print("Error: Failure Releasing Image")
            return False
        # settings.maybePrint("Image: {}".format(response))
        text = None
        content = None
        file = None
        keywords = None
        try:
            text = response[0]
            content = response[1]
            file = response[2]
            keywords = response[3].split(" ")
        except Exception as e:
            settings.maybePrint(e)
        if str(keywords) == " " or str(keywords[0]) == " ":
            keywords = []
        if text == None:
            print("Error: Missing Image Title")
            return False
        if content == None:
            print("Error: Missing Image Content")
            return False
        if file == None:
            print("Error: Missing Image File")
            return False
        if keywords == None:
            print("Warning: Missing Image Keywords")
        print("Image:")
        print("- Title: {}".format(text)) # name of scene
        print("- Keywords: {}".format(keywords)) # text sent in messages
        print("- Content: {}".format(content)) # the file(s) to upload
        upload("image", path=content, text=text, keywords=keywords)
        Google.move_file(file)
        return True
    except Exception as e:
        settings.maybePrint(e)
        return False

def release_gallery():
    try:
        print("Releasing Gallery")
        response = download("gallery")
        if response == None:
            print("Error: Failure Releasing Gallery")
            return False
        # settings.maybePrint("Gallery: {}".format(response))
        text = None
        content = None
        google_file = None
        google_files = None
        keywords = None
        try:
            text = response[0]
            content = response[1]
            google_file = response[2]
            google_files = response[3]
            keywords = response[4].split(" ")
        except Exception as e:
            settings.maybePrint(e)
        if keywords == " " or str(keywords[0]) == " ":
            keywords = []
        if text == None:
            print("Error: Missing Gallery Title")
            return False
        if content == None:
            print("Error: Missing Gallery Content")
            return False
        if google_file == None:
            print("Error: Missing Gallery File")
            return False
        if google_files == None or len(google_files) == 0:
            print("Error: Missing Gallery Files")
            return False
        if str(keywords) == None:
            print("Warning: Missing Gallery Keywords")
        print("Gallery:")
        print("- Title: {}".format(text)) # name of scene
        print("- Keywords: {}".format(keywords)) # text sent in messages
        print("- Content: {}".format(content)) # the file(s) to upload
        files = os.listdir(content)
        file = files[0]
        ext = str(os.path.splitext(file)[1].lower())
        settings.maybePrint('ext: '+str(ext))
        upload("gallery", path=content, text=text, keywords=keywords)
        Google.move_files(google_file['title'], google_files)
        return True
    except Exception as e:
        settings.maybePrint(e)
        return False

def release_performer():
    try:
        print("Releasing Performer")
        response = download("performer")
        if response == None:
            print("Error: Failure Releasing Performer")
            return False
        # settings.maybePrint("Performer: {}".format(response))
        text = None
        performer = None
        content = None
        google_file = None
        folder_name = None
        try:
            content = response[0]
            google_file = response[1]
            performer = response[2]
            text = response[3]
            folder_name = response[4]
        except Exception as e:
            settings.maybePrint(e)
        if text == None:
            print("Error: Missing Performer Text")
            return False
        if performer == None:
            print("Error: Missing Performer Name")
            return False
        if content == None:
            print("Error: Missing Performer Content")
            return False
        text += " w/ @{}".format(performer)
        print("Performer:")
        print("- Performer: {}".format(performer)) # name of scene
        print("- Text: {}".format(text)) # name of scene
        print("- Content: {}".format(content)) # the file(s) to upload
        files = os.listdir(content)
        file = files[0]
        ext = str(os.path.splitext(file)[1].lower())
        settings.maybePrint('ext: '+str(ext))
        upload("gallery", path=content, text=text)
        Google.move_file(google_file)
        return True
    except Exception as e:
        settings.maybePrint(e)
        return False
    
# upload a file or gallery
# send a message to [recent, all, user] w/ a preview image
def release_scene():
    try:
        print("Releasing Scene")
        response = download("scene")
        if response == None:
            print("Error: Failure Releasing Scene")
            return False
        # settings.maybePrint("Scene: {}".format(response))
        content = response[0]
        preview = response[1]
        data = response[2]
        google_folder = response[3]
        # print("Data:\n{}".format(json.dumps(data, sort_keys=True, indent=4)))
        data = json.loads(json.dumps(data))
        settings.maybePrint("Data: {}".format(data))
        title = None
        message = None
        price = None
        text = None
        performers = None
        keywords = None
        users = None
        title = data["title"]
        message = data["message"]
        price = data["price"]
        text = data["text"]
        performers = data["performers"]
        keywords = data["keywords"]
        if str(keywords) == " " or str(keywords[0]) == " ":
            keywords = []
        users = data["users"]
        if title == None:
            print("Error: Missing Scene Title")
            return False
        if message == None:
            print("Error: Missing Scene Message")
            return False
        if price == None:
            print("Error: Missing Scene Price")
            return False
        if text == None:
            print("Error: Missing Scene Text")
            return False
        print("Scene:")
        print("- Title: {}".format(title)) # name of scene
        print("- Text: {}".format(text)) # text entered into file upload
        print("- Price: {}".format(price)) # price of messages sent
        print("- Message: {}".format(message)) # text sent in messages
        print("- Keywords: {}".format(keywords)) # text sent in messages
        print("- Performers: {}".format(performers)) # text sent in messages
        print("- Preview: {}".format(preview)) # image sent in messages
        print("- Content: {}".format(content)) # the file(s) to upload
        print("- Users: {}".format(users)) # the file(s) to upload 
        files = os.listdir(content)
        file = files[0]
        ext = str(os.path.splitext(file)[1].lower())
        settings.maybePrint('ext: '+str(ext))
        if not ext or ext == '.mp4':
            upload("video", path=content, text=text, keywords=keywords, performers=performers)
        elif ext == '.jpg' or ext == '.jpeg' and len(files) > 1:
            upload("gallery", path=content, text=text, keywords=keywords, performers=performers)
        elif ext == '.jpg' or ext == '.jpeg' and len(files) == 1:
            upload("image", path=content, text=text, keywords=keywords, performers=performers) 
        else:
            print("Error: Missing Scene Type")
        if str(users[0]) == "all" or str(users[0]) == str("recent") or str(users[0]) == str("favorites"):
            users = users[0]
        if not users or str(users).lower() == "none":
            print("Warning: Missing User Choice")
        elif str(users) == "all":
            message_all(message=message, image=preview, price=price)
        elif str(users) == "recent":
            message_recent(message=message, image=preview, price=price)
        elif str(users) == "favorites":
            message_favorites(message=message, image=preview, price=price)
        else:
            for user in users:
                message_by_username(message=message, image=preview, price=price, username=user)
        Google.move_file(google_folder)
        return True
    except Exception as e:
        settings.maybePrint(e)
        return False

def release_video():
    try:
        print("Releasing Video")
        response = download("video")
        if response == None:
            print("Error: Failure Releasing Video")
            return False
        # settings.maybePrint("Video: {}".format(response))
        text = None
        content = None
        file = None
        keywords = None
        try:
            text = response[0]
            content = response[1]
            file = response[2]
            keywords = response[3].split(" ")
        except Exception as e:
            settings.maybePrint(e)
        if str(keywords) == " " or str(keywords[0]) == " ":
            keywords = []
        ext = str(os.path.splitext(text)[1].lower())
        settings.maybePrint('ext: '+str(ext))
        if ext == '.mp4':
            settings.maybePrint("pruning extension")
            text = os.path.splitext(text)[0]
        if text == None:
            print("Error: Missing Video Title")
            return False
        if content == None:
            print("Error: Missing Video Content")
            return False
        if file == None:
            print("Error: Missing Video File")
            return False
        if keywords == None:
            print("Warning: Missing Video Keywords")
        print("Video:")
        print("- Title: {}".format(text)) # name of scene
        print("- Keywords: {}".format(keywords)) # text sent in messages
        print("- Content: {}".format(content)) # the file(s) to upload
        upload("video", path=content, text=text, keywords=keywords)
        Google.move_file(file)
        return True
    except Exception as e:
        settings.maybePrint(e)
        return False

##################
##### Upload #####
##################

def upload(fileChoice, path=None, text=None, keywords=None, performers=None):
    settings.maybePrint("Uploading: {} - {} - {}".format(fileChoice, path, text))
    try:
        settings.TYPE = fileChoice
        if fileChoice == 'image':
            OnlySnarf.upload_file_to_OnlyFans(path=path, text=text, keywords=keywords, performers=performers)
        elif fileChoice == 'gallery':
            OnlySnarf.upload_directory_to_OnlyFans(path=path, text=text, keywords=keywords, performers=performers)
        elif fileChoice == 'video':
            OnlySnarf.upload_file_to_OnlyFans(path=path, text=text, keywords=keywords, performers=performers)
        else:
            print("Missing Upload Choice")
    except TypeError as e:
        settings.maybePrint(e)
        print("Error: Upload Failure")
        return
    print('Upload Complete')

#####################
##### FUNCTIONS #####
#####################

def main():
    print("0/3 : Deleting Locals")
    remove_local()
    sys.stdout.flush()
    #################################################
    print("1/3 : Running - {}".format(settings.TYPE))
    if str(settings.TYPE) == "image":
        released = release_image()
    elif str(settings.TYPE) == "video":
        released = release_video()
    elif str(settings.TYPE) == "gallery":
        released = release_gallery()
    elif str(settings.TYPE) == "performer":
        released = release_performer()
    elif str(settings.TYPE) == "scene":
        released = release_scene()
    else:
        print('Missing Args!')
        return
    sys.stdout.flush()
    if released == False:
        print("Error: Missing Released Files")
        return
    #################################################
    print('2/3 : Cleaning Up Files')
    remove_local()
    print('Files Cleaned ')
    #################################################
    print('3/3 : Google Drive to OnlyFans Upload Complete')
    sys.stdout.flush()
    OnlySnarf.exit()


def test(TYPE):
    print('0/3 : Deleting Locals')
    remove_local()
    print('1/3 : Testing')

    ### Message ###
    response = download_random_image()
    if not response or response == None:
        print("Error: Missing Image")
        return
    message(choice="all", message="8=======D", image=response[1], price="0.00")
    # message(choice="recent", message="8=======D", image=response[1], price="50.00")
    Google.move_file(response[2])
    ##############

    #######################
    ### Exit Gracefully ###
    OnlySnarf.exit()
    return
    #######################

    ### Users ###
    # print('TESTING: Users')
    # users = OnlySnarf.get_users()
    # time.sleep(30)
    # reset = OnlySnarf.reset()
    # if not reset:
        # return print("Error: Failed to Reset")
    # return
    #####################
    print('TESTING: Chat Logs')
    OnlySnarf.update_chat_logs()
    time.sleep(30)
    reset = OnlySnarf.reset()
    if not reset:
        return print("Error: Failed to Reset")
    
    #######################
    ### Exit Gracefully ###
    OnlySnarf.exit()
    return
    #######################
    
    ### Image ###
    print('TESTING: Image')
    release_image()
    time.sleep(30)
    reset = OnlySnarf.reset()
    if not reset:
        return print("Error: Failed to Reset")
    ### Gallery ###
    print('TESTING: Gallery')
    release_gallery()
    time.sleep(30)
    reset = OnlySnarf.reset()
    if not reset:
        return print("Error: Failed to Reset")
    ### Performer ###
    print('TESTING: Performer')
    release_performer()
    time.sleep(30)
    reset = OnlySnarf.reset()
    if not reset:
        return print("Error: Failed to Reset")
    ### Scene ###
    print('TESTING: Scene')
    release_scene()
    time.sleep(30)
    reset = OnlySnarf.reset()
    if not reset:
        return print("Error: Failed to Reset")
    ### Video ###
    print('TESTING: Video')
    release_video()
    time.sleep(30)
    reset = OnlySnarf.reset()
    if not reset:
        return print("Error: Failed to Reset")
    # return

    #######################
    ### Exit Gracefully ###
    OnlySnarf.exit()
    #######################


################################################################################################################################################

if __name__ == "__main__":
    try:
        # os.system('clear')
        OnlySnarf.initialize()
        main()
    except:
        print(sys.exc_info()[0])
        print("Shnarf!")
    finally:
        sys.exit(0)
else:
    try:
        settings.initialize()
        OnlySnarf.initialize()
    except Exception as e:
        print(e)
        print("Shnnarf?")
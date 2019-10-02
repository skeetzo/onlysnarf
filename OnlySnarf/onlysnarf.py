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
from OnlySnarf.settings import SETTINGS as settings
from OnlySnarf import google as Google
from OnlySnarf import driver as OnlySnarf
from OnlySnarf.user import User
from OnlySnarf import cron as Cron

# from pprint import pprint
#################################################################
#################################################################
#################################################################

def main(opt):
    print("0/3 : Deleting Locals")
    remove_local()
    sys.stdout.flush()
    #################################################
    print("1/3 : Running - {}".format(opt))
    released = release(opt)
    if released == False: print("Error: Failed to release - {}".format(opt))
    sys.stdout.flush()
    #################################################
    print('2/3 : Cleaning Up Files')
    remove_local()
    print('Files Cleaned ')
    #################################################
    print('3/3 : Google Drive to OnlyFans Upload Complete')
    OnlySnarf.exit()
    sys.stdout.flush()

####################
##### Discount #####
####################

def discount(user, depth=1, discount=0, months=0):
    users = []
    skip = False
    if str(user) == "all":
        users = User.get_all_users()
        skip = True
    elif str(user) == "new":
        users = User.get_new_users()
        skip = True
    elif str(user) == "favorite":
        users = User.get_favorite_users()
        skip = True
    elif str(user) == "recent":
        users = User.get_recent_users()
        skip = True
    else:
        if isinstance(user, str):
            user = User.get_user_by_username(user)
        users.append(user)
    skip_ = False
    for user in users:
        try:
            OnlySnarf.discount_user(user.id, depth=depth, discount=discount, months=months, skip_reload=skip_)
        except Exception as e:
            settings.maybePrint(e)
        depth = int(depth) + 1
        if skip: # skips first False
            skip_ = skip

####################
##### Download #####
####################

def download(fileChoice, methodChoice="random", file=None):
    if methodChoice == "random":
        return Google.random_download(fileChoice)
    elif methodChoice == "choose" and file is not None:
        if fileChoice == 'image' or fileChoice == 'video':
            return Google.download_file(file)
        elif fileChoice == 'gallery':
            return Google.download_gallery(file)
        elif fileChoice == 'performer':
            if "folder" in file.get("mimeType"):
                return Google.download_content(file)
            else:          
                return Google.download_file(file)  
#################################################################
        elif fileChoice == 'scene':
            return Google.download_scene(file)
#################################################################
    else:
        print("Error: Unable to Download")
        return None

###################
##### Message #####
###################

def message(choice, message=None, image=None, price=None, username=None):
    if not image[0] or image[0] == None:
        print("Error: Missing Image")
        return False
    successful_message = OnlySnarf.message(choice=choice, message=message, image=image, price=price, username=username)
    return successful_message

#####################
##### Promotion #####
#####################

def give_trial(user):
    print("Applying Promotion: "+user)
    link = OnlySnarf.get_new_trial_link()
    text = "Here's your free trial link!\n"+link
    settings.maybePrint("Link: "+str(text))
    send_email(email, text)

def send_email(email, text):
    print("Sending Email: "+str(email))
    pass

#################
##### Reset #####
#################

# Deletes local file
def remove_local():
    try:
        if str(settings.SKIP_DELETE) == "True":
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

def release(opt, methodChoice="random", file=None, folderName=None, parent=None):
    print("0/3 : Deleting Locals")
    remove_local()
    sys.stdout.flush()
    #################################################
    print("1/3 : Running - {}".format(opt))
    released = release_(opt, methodChoice=methodChoice, file=file, folderName=folderName, parent=parent)
    if released == False: print("Error: Failed to release - {}".format(opt))
    sys.stdout.flush()
    #################################################
    print('2/3 : Cleaning Up Files')
    remove_local()
    print('Files Cleaned ')
    #################################################
    print('3/3 : Google Drive to OnlyFans Upload Complete')
    OnlySnarf.exit()
    sys.stdout.flush()

def release_(opt, methodChoice="random", file=None, folderName=None, parent=None):
    try:
        if not opt:
            print("Error: Missing Option")
            return False
        print("Releasing: {}".format(opt))
        data = download(opt, methodChoice=methodChoice, file=file)
        if data == None:
            print("Error: Missing Data")
            return False
        text = None
        path = None
        keywords = []
        performers = []
        files = None
        parent = parent.get("title")
        try:
            if file == None: file = data.get("file")
            text = file.get("title") or ""
            path = data.get("path")
            files = data.get("files")
            keywords = data.get("keywords") or parent
            performers = data.get("performers") or []
            # if parent: keywords = parent.split(" ")
            if isinstance(keywords, str): keywords = keywords.split(" ")
            if str(opt) == "performer":
                keywords = folderName or keywords
                if parent: performers = parent.split(" ")
            if isinstance(keywords, list): keywords = [n.strip() for n in keywords]
            if str(methodChoice) == "choose":
                text_ = input("Text ({}): ".format(text))
                if text_ != "":
                    text = text_
                keywords_ = input("Keywords ({}): ".format(keywords))
                if keywords_ != "":
                    keywords = keywords_.split(",")
                    keywords = [n.strip() for n in keywords]
                performers_ = input("Performers ({}): ".format(performers))
                if performers_ != "":
                    performers = performers_.split(",")
                    performers = [n.strip() for n in performers]
        except Exception as e:
            settings.maybePrint(e)
        if text == None: print("Warning: Missing Title")
        if path == None: print("Warning: Missing Content")
        if keywords == None or len(keywords) == 0: print("Warning: Missing Keywords")
        if performers == None or len(performers) == 0: print("Warning: Missing Performers")
        print("Data:")
        print("- Text: {}".format(text)) # name of scene
        print("- Keywords: {}".format(keywords)) # text sent in messages
        print("- Content: {}".format(path)) # the file(s) to upload
        print("- Performer(s): {}".format(performers)) # name of performers
        successful_upload = upload(path, text, keywords, performers)
        if not successful_upload:
            print("Error: Missing Data Type")
        elif files:
            Google.move_files(text, files)
        else:
            Google.move_file(file)
    except Exception as e:
        settings.maybePrint(e)
        return False
    
# upload a file or gallery
# send a message to [recent, all, user] w/ a preview image
def release_scene(methodChoice="random", file=None, folderName=None, parent=None):
    try:
        print("Releasing Scene")
        response = download("scene", methodChoice=methodChoice, file=file)
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
        successful_upload = upload(path, text, keywords, performers)
        if successful_upload:
            if str(users[0]) == "all" or str(users[0]) == str("recent") or str(users[0]) == str("favorites"):
                users = users[0]
            if not users or str(users).lower() == "none":
                print("Warning: Missing User Choice")
            elif str(users) == "all" or str(users) == "recent" or str(users) == "favorites":
                successful_message = OnlySnarf.message(choice=str(users), message=message, image=preview, price=price)
            else:
                for user in users:
                    successful_message = OnlySnarf.message(choice="user", message=message, image=preview, price=price, username=user)
            if successful_message:
                Google.move_file(google_folder)
            else:
                print("Error: Failure Messaging")
                return False
        else:
            print("Error: Failure Uploading")
            return False
        return True
    except Exception as e:
        settings.maybePrint(e)
        return False

##################
##### Upload #####
##################

def upload(path, text, keywords, performers):
    settings.maybePrint("Uploading: {}".format(path))
    successful = False
    try:
        successful = OnlySnarf.upload_to_OnlyFans(path=path, text=text, keywords=keywords, performers=performers)
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Unable to Upload")
        return False
    if successful:
        print("Upload Complete")
    else:
        print("Upload Failure")
    return successful

#################
##### Users #####
#################

def get_users():
    settings.maybePrint("Getting Users")
    try:
        return User.get_all_users()
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Unable to get users");
        return []

###############
##### Dev #####
###############

def test(TYPE):
    print('0/3 : Deleting Locals')
    remove_local()
    print('1/3 : Testing')

    # ### Promotion ###
    print('TESTING: Cron')
    response = Cron.test()
    if not response or response == None:
        print("Error: Failed to test crons")
    reset = OnlySnarf.reset()
    if not reset:
        return print("Error: Failed to Reset")
    return

################################################################################################################################################

if __name__ == "__main__":
    try:
        # os.system('clear')
        settings.initialize()
        OnlySnarf.initialize()
        main(settings.TYPE)
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
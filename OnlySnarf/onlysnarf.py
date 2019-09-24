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
from OnlySnarf import cron as Cron
# from pprint import pprint

##########################
##### MENU FUNCTIONS #####
##########################

def all(opt):
    main(opt)

####################
##### Download #####
####################

def download(fileChoice, methodChoice="random", file=None):
    if methodChoice == "random":
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
    elif methodChoice == "choose" and file is not None:
        if fileChoice == 'image':
            response = Google.download_file(file)
        elif fileChoice == 'gallery':
            response = Google.download_gallery(file)


        elif fileChoice == 'video':
            response = Google.download_file(file)

        # google_file = response[0]
        # folder_name = response[1]
        # if google_file == None:
        #     return
        # file_name = google_file['title']
        # file_path = Google.download_file(google_file)

        # return [file_name, file_path, google_file, folder_name]

    else:
        print("Error: Unable to Download")
        return None

def download_message_image(folderName="random"):
    remove_local()
    print('Fetching Image')
    response = Google.get_message_image(folderName)
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


########################
########################

########################

########################
########################

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

##
##
##

##################
##### Upload #####
##################

def upload(fileChoice, path=None, text=None, keywords=None, performers=None):
    settings.maybePrint("Uploading: {} - {} - {}".format(fileChoice, path, text))
    successful = False
    try:
        if fileChoice == 'image':
            successful = OnlySnarf.upload_to_OnlyFans(path=path, text=text, keywords=keywords, performers=performers)
        elif fileChoice == 'gallery':
            successful = OnlySnarf.upload_to_OnlyFans(path=path, text=text, keywords=keywords, performers=performers)
        elif fileChoice == 'video':
            successful = OnlySnarf.upload_to_OnlyFans(path=path, text=text, keywords=keywords, performers=performers)
        else:
            print("Missing Upload Choice")
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Unable to Upload")
        return
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
    successful = False
    try:
        successful = OnlySnarf.get_users()
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Unable to get users");
        return
    if successful:
        settings.maybePrint("Users Found")
    else:
        print("Warning: users not found")
        return []
    return successful

#####################
##### FUNCTIONS #####
#####################

def main(opt):
    print("0/3 : Deleting Locals")
    remove_local()
    sys.stdout.flush()
    #################################################
    print("1/3 : Running - {}".format(opt))
    if str(opt) == "image":
        released = release_image()
    elif str(opt) == "video":
        released = release_video()
    elif str(opt) == "gallery":
        released = release_gallery()
    elif str(opt) == "performer":
        released = release_performer()
    elif str(opt) == "scene":
        released = release_scene()
    else:
        print('Missing Args!')
        return
    sys.stdout.flush()
    if released == False:
        print("Error: Failed to release - {}".format(opt))
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
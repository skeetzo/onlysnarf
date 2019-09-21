#!/usr/bin/python3
# 3/28/2019 Skeetzo
# OnlySnarf.py menu system

### doesn't work:
# upload & backup (requires upload via local added to main script)
# settings menu -> "Incorrect Index"

import random
import os
import shutil
import datetime
import json
import sys
import pathlib
import pkg_resources
from OnlySnarf.settings import SETTINGS as settings
from OnlySnarf import onlysnarf as OnlySnarf
from OnlySnarf import google as Google

###################
##### Globals #####
###################

version = str(pkg_resources.get_distribution("onlysnarf").version)
header = "\n ________         .__          _________                     _____ \n \
\\_____  \\   ____ |  | ___.__./   _____/ ____ _____ ________/ ____\\\n \
 /   |   \\ /    \\|  |<   |  |\\_____  \\ /    \\\\__  \\\\_   _ \\   __\\ \n \
/    |    \\   |  \\  |_\\___  |/        \\   |  \\/ __ \\ |  |\\/| |   \n \
\\_______  /___|  /____/ ____/_______  /___|  (____  \\\\__|  |_|   \n \
        \\/     \\/     \\/            \\/     \\/     \\/              \n"

UPDATED = False
UPDATED_TO = False
INITIALIZED = False

colors = {
        'blue': '\033[94m',
        'header': '\033[48;1;34m',
        'teal': '\033[96m',
        'pink': '\033[95m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'menu': '\033[48;1;44m'
        }

menuItems = []
actionItems = []
messageItems = []
fileItems = []
locationItems = []
promotionItems = []
settingItems = []

def initialize():
    # print("Initializing Menu")
    global INITIALIZED
    if INITIALIZED:
        # print("Already Initialized, Skipping")
        return
    global settingItems
    # Settings Menu
    settingItems = sorted([
        [ "Backup", settings.BACKUP, ["True","False"],True],
        [ "Delete Google", settings.DELETE_GOOGLE, ["True","False"],False],
        [ "Skip Delete Local", settings.SKIP_DELETE, ["True","False"],False],
        [ "Force Backup", settings.FORCE_BACKUP, ["True","False"],False],
        [ "Force Upload", settings.FORCE_UPLOAD, ["True","False"],False],
        [ "Mount Path", settings.PATH_MOUNT,None,False],
        [ "Google: Root Folder Path", settings.PATH_DRIVE,None,False],
        [ "Users Path", settings.PATH_USERS,None,False],
        [ "Show Window", settings.SHOW_WINDOW, ["True","False"],False],
        [ "Google: Root Folder Name", settings.ROOT_FOLDER,None,False],
        [ "Google: Drive Folders", settings.DRIVE_FOLDERS,None,False],
        [ "Image Limit", settings.IMAGE_UPLOAD_LIMIT,None,True],
        [ "Image Max", settings.IMAGE_UPLOAD_MAX,None,False],
        [ "Tweeting", settings.TWEETING, ["True","False"],True],
        [ "Debug", settings.DEBUG, ["True","False"],False],
        [ "Skip Download", settings.SKIP_DOWNLOAD, ["True","False"],False],    
        [ "Create Missing Google Folders", settings.DRIVE_CREATE_MISSING, ["True","False"],False],    
        [ "Verbose", settings.VERBOSE, ["True","False"],True]    
    ])
    if str(settings.DEBUG) == "True":
        settingItems.append([ "Text", settings.TEXT,None,False])
        settingItems.append([ "Image", settings.IMAGE,None,False])
        settingItems.append([ "Prefer Local", settings.PREFER_LOCAL,["True","False"],True])
    settingItems.insert(0,[ "Back", "main"])

    global menuItems
    # Main Menu
    menuItems = [
        [ "Actions", "action"],
        [ "Settings", "set_settings"],
        [ "Exit", "exit"]
    ]

    global actionItems
    # Actions Menu
    actionItems = sorted([
        [ "Release", "release" ],
        [ "Download", "download" ],
        # [ "Promotion", "promotion" ],
        [ "Message", "message" ],
        [ "Reset", "reset" ]
    ])
    if str(settings.DEBUG) == "True":
        actionItems.append([ "Test", "test"])
        actionItems.append([ "Promotion", "promotion" ])
    actionItems.insert(0,[ "Back", "main"])

    global messageItems
    # Message Menu
    messageItems = sorted([
        [ "All", "all"],
        [ "New", "new"],
        [ "Recent", "recent"],
        [ "User by Username", "user"]
    ])
    messageItems.insert(0,[ "Back", "main"])

    global fileItems
    # File Type Menu
    fileItems = sorted([
        [ "Image", "image"],
        [ "Gallery", "gallery"],
        [ "Performer", "performer"],
        # [ "Scene", "scene"],
        [ "Video", "video"],
    ])
    if str(settings.DEBUG) == "True":
        fileItems.append([ "Scene", "scene"])
    fileItems.insert(0,[ "Back", "main"])

    global locationItems
    # File Location Menu
    locationItems = sorted([
        [ "Local", "local"],
        [ "Google Drive", "google"]
    ])
    locationItems.insert(0,[ "Back", "main"])

    global promotionItems
    if str(settings.DEBUG) == "True":
        promotionItems = sorted([
            [ "Enter Email", "email" ],
            # [ "Select User", "select" ]
        ])
    promotionItems.insert(0,[ "Back", "main"])

    # print("Initialized Menu")
    INITIALIZED = True

#####################
##### Functions #####
#####################

### Action Menu - file type
def action():
    for item in actionItems:
        print(colorize("[" + str(actionItems.index(item)) + "] ", 'teal') + list(item)[0])
    while True:
        choice = input(">> ")
        try:
            if int(choice) < 0 or int(choice) >= len(actionItems): raise ValueError
            if str(actionItems[int(choice)][1]) == "main":
                return main()
            elif str(actionItems[int(choice)][1]) == "reset":
                OnlySnarf.remove_local()
            elif str(actionItems[int(choice)][1]) == "message":
                actionChoice = list(actionItems[int(choice)])[1]
                return finalizeMessage(actionChoice)
            elif str(actionItems[int(choice)][1]) == "promotion":
                actionChoice = list(actionItems[int(choice)])[1]
                return finalizePromotion(actionChoice)
            else:
                actionChoice = list(actionItems[int(choice)])[1]
                return finalizeAction(actionChoice)
        except (ValueError, IndexError):
            print("Error: Incorrect Index")
        except Exception as e:
            settings.maybePrint(e)
            print("Error: Missing Method") 

### Action Menu - finalize
def finalizeAction(actionChoice):
    for item in fileItems:
        print(colorize("[" + str(fileItems.index(item)) + "] ", 'teal') + list(item)[0])
    while True:
        fileChoice = input(">> ")
        try:
            if int(fileChoice) < 0 or int(fileChoice) >= len(fileItems): raise ValueError
            if str(fileItems[int(fileChoice)][1]) == "main":
                return action()
            # Call the matching function
            fileChoice = list(fileItems[int(fileChoice)])[1]
            return performAction(actionChoice, fileChoice)
        except (ValueError, IndexError):
            print("Error: Incorrect Index")
        except Exception as e:
            settings.maybePrint(e)
            print("Error: Missing Method") 

### Action Menu - perform
def performAction(actionChoice, fileChoice):
    try:
        method = getattr(OnlySnarf, str(actionChoice))
        response = method(fileChoice)
        if response:
            if str(actionChoice) == "download":
                for setting in settingItems:
                    if setting[0] == "File Name":
                        setting[1] = response[0]
                    elif setting[0] == "File Path":
                        setting[1] = response[1]
    except (ValueError, IndexError):
        print("Error: Incorrect Index")
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Missing Method") 
    mainMenu()

# Message Menu - finalize
def finalizeMessage(actionChoice):
    for item in messageItems:
        print(colorize("[" + str(messageItems.index(item)) + "] ", 'teal') + list(item)[0])
    while True:
        choice = input(">> ")
        try:
            choice = int(choice)
            if int(choice) < 0 or int(choice) >= len(messageItems): raise ValueError
            if str(messageItems[int(choice)][1]) == "main":
                return action()
            return performMessage(actionChoice, messageItems[int(choice)][1])
        except (ValueError, IndexError):
            print(sys.exc_info()[0])
            print("Error: Incorrect Index")

# Message Menu - perform
def performMessage(actionChoice, messageChoice):
    username = None
    if str(messageChoice) == "user":
        users = displayUsers()
        seeking = True
        while seeking:
            choice = input(">> ")
            try:
                if int(choice) < 0 or int(choice) > len(users): raise ValueError
                if int(choice) == 0:
                    return finalizeMessage(actionChoice)
                username = users[int(choice)-1].username
                seeking = False
            except (ValueError, IndexError):
                print(sys.exc_info()[0])
                print("Error: Incorrect Index")
                return mainMenu()
    images = selectImage(messageChoice)
    # [folder , image_file]
    # print("len: " + str(len(images)))
    while True:
        choice = input(">> ")
        try:
            if int(choice) < 0 or int(choice) > len(images): raise ValueError
            if int(choice) == 0:
                return finalizeMessage(actionChoice)
            try:
                image = images[int(choice)-1]
                message(messageChoice, [image[1],image[0]], username)
                return mainMenu()
            # except (ValueError, IndexError):
                # print("Error: Incorrect Index")
            except Exception as e:
                settings.maybePrint(e)
                print("Error: Missing Method")
        except (ValueError, IndexError):
            print("Error: Incorrect Index")
    # mainMenu()    

# {
#   image: file
#   folder: folder
# }
def message(choice, image=None, username=None):
    message = input("Message: ")
    waiting = True
    while waiting:
        try:
            price = input("Price: ")
            "{:.2f}".format(float(price))
            waiting = False
        except ValueError:
            print("Enter a currency amount!")
    if not image or not image[0] or image[0] == None:
        print("Error: Missing Image")
        return
    file_path = Google.download_file(image[0])
    successful_message = OnlySnarf.message(choice=choice, message=message, image=file_path, price=price, username=username)
    if successful_message and str(choice) != "new":
        Google.move_file(image[0])
    else:
        print("Error: Failure Messaging")
        return False

# Promotion Menu - finalize
def finalizePromotion(actionChoice):
    for item in promotionItems:
        print(colorize("[" + str(promotionItems.index(item)) + "] ", 'teal') + list(item)[0])
    while True:
        choice = input(">> ")
        try:
            choice = int(choice)
            if int(choice) < 0 or int(choice) > len(promotionItems): raise ValueError
            if str(promotionItems[int(choice)][1]) == "main":
                return action()
            choice = list(promotionItems[int(choice)])[1]
            return performPromotion(actionChoice, choice)
        except (ValueError, IndexError):
            settings.maybePrint(sys.exc_info()[0])
            print("Error: Incorrect Index")

def performPromotion(actionChoice, promotionChoice):
    def promote(username):
        if username == None:
            print("Warning: No user found")
        else:
            OnlySnarf.give_trial(username)
        mainMenu()    
    try:
        username = None
        if str(promotionChoice) == "email":
            # prompt
            choice = input("Email: ")
            username = str(choice)
            return promote(username)
        elif str(promotionChoice) == "select":
            users = displayUsers()    
            while True:
                choice = input(">> ")
                try:
                    if int(choice) < 0 or int(choice) > len(users): raise ValueError
                    if int(choice) == 0:
                        return finalizePromotion(actionChoice)
                    return promote(str(users[int(choice)-1].username))

                except (ValueError, IndexError):
                    settings.maybePrint(sys.exc_info()[0])
                    print("Error: Incorrect Index")            
    except (ValueError, IndexError):
        print("Error: Incorrect Index")
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Missing Method") 
    mainMenu()

# displays and returns users
def displayUsers():
    users = OnlySnarf.get_users()
    print(colorize("[0] ", 'blue') + "Back")
    # show list
    i = 1
    for user in users:
        print(colorize("[" + str(i) + "] ", 'blue') + str(user.username))
        i = i+1
    return users

def selectImage(folderName):
    images = Google.get_images()
    print(colorize("[0] ", 'blue') + "Back")
    i = 1
    for image in images:
        print(colorize("[" + str(i) + "] ", 'blue') + str(image[0]["title"]) + " - " + str(image[1]['title']))
        i = i+1
    return images
    # performMessage -> [folder , image_file] -> performMessage


###########################

### Settings Menu
def set_settings():
    showHeader()
    print(colorize("Set:",'menu'))
    global settingItems
    for item in settingItems:
        print(colorize("[" + str(settingItems.index(item)) + "] ", 'blue') + list(item)[0])
    while True:
        choice = input(">> ")
        try:
            if int(choice) < 0 or int(choice) >= len(settingItems): raise ValueError
            settingChoice = list(settingItems[int(choice)])[0]
            settingValue = list(settingItems[int(choice)])[1]
            if str(settingChoice) == "Back":
                return main()
            elif str(settingChoice) == "File Name":
                settingValue = input("Enter the file name: ")
            elif str(settingChoice) == "File Path":
                settingValue = input("Enter the file path: ")
            elif str(settingChoice) == "Text":
                settingValue = input("Enter the upload text: ")
            elif str(settingChoice) == "Mount Path":
                settingValue = input("Enter the mount path: ")
            elif str(settingChoice) == "Google: Root Folder Path":
                settingValue = input("Enter the drive path (folderName/folderName/...): ")
            elif str(settingChoice) == "Image":
                settingValue = input("Enter the image path: ")
            elif str(settingChoice) == "Google: Root Folder Name":
                settingValue = input("Enter the Google root folder name: ")
            elif str(settingChoice) == "Google: Drive Folders":
                settingValue = input("Enter the Google drive folders (separated by ',', no spaces): ")
                settingValue = settingValue.split(",")
            elif str(settingChoice) == "Image Limit":
                settingValue = input("Enter the image upload limit: ")
            elif str(settingChoice) == "Image Max":
                settingValue = input("Enter the image upload max: ")
            else:
                list_ = list(settingItems[int(choice)][2])
                print(colorize(str(settingChoice)+" =", 'blue'))
                for item in list_:
                    print(colorize("[" + str(list_.index(item)) + "] ", 'pink') + str(item))
                while True:
                    updateChoice = input(">> ")
                    try:
                        if int(updateChoice) < 0 or int(updateChoice) >= len(list(settingItems[int(choice)][2])): raise ValueError
                        settingValue = list_[int(updateChoice)]
                        break
                    except (ValueError, IndexError):
                        print("Error: Incorrect Index")
                    except Exception as e:
                        settings.maybePrint(e)
                        break
            global UPDATED
            UPDATED = settingChoice
            global UPDATED_TO
            UPDATED_TO = settingValue
            settingItems[int(choice)][1] = settingValue
            settings.update_value(settingChoice, settingValue)
            return set_settings()
        except (ValueError, IndexError):
            print("Error: Incorrect Index")
        except Exception as e:
            settings.maybePrint(e)
            return main()

###########################

def colorize(string, color):
    if not color in colors: return string
    return colors[color] + string + '\033[0m'
  
def exit():
    print("Shnarrf?")
    sys.exit(0)

###########################
import atexit
def exit_handler():
    print('Shnnarrrff!')
    exit()
atexit.register(exit_handler)

import signal
def signal_handler(sig, frame):
    print('Shnnnarf?')
    exit()
signal.signal(signal.SIGINT, signal_handler)
###########################

def main():
    showHeader()
    mainMenu()

def mainMenu():
    ### Main Menu
    print(colorize("Select an option:", 'menu'))
    for item in menuItems:
        print(colorize("[" + str(menuItems.index(item)) + "] ", 'blue') + list(item)[0])
    while True:
        choice = input(">> ")
        try:
            if int(choice) < 0 or int(choice) >= len(menuItems): raise ValueError
            # Call the matching function
            method_name = list(menuItems[int(choice)])[1]
            possibles = globals().copy()
            possibles.update(locals())
            method = possibles.get(method_name)
            if method is not None:
                return method()
            else:
                print("Error: Missing Option")    
        except (ValueError, IndexError, KeyboardInterrupt):
            print("Error: Incorrect Index")
            pass

def showHeader():
    os.system('clear')
    # Print some badass ascii art header here !
    print(colorize(header, 'header'))
    print(colorize('version '+version+'\n', 'green'))
    showSettings()

def showSettings():
    print('Settings:')
    for setting in settingItems:
        if str(setting[0]) == "Image Limit" and setting[3]:
            print(' - '+setting[0]+' = '+str(setting[1])+"/"+str(settings.IMAGE_UPLOAD_MAX))
        elif str(setting[0]) != "Back" and str(settings.DEBUG) == "True":
            print(' - '+setting[0]+' = '+str(setting[1]))
        elif str(setting[0]) != "Back" and setting[3]:
            print(' - '+setting[0]+' = '+str(setting[1]))
        
    global UPDATED
    global UPDATED_TO
    if str(UPDATED) != "False":
        print('\nUpdated: '+str(UPDATED)+' -> '+str(UPDATED_TO))
    UPDATED = False
    print('\r')

###########################

if __name__ == "__main__":
    try:
        main_other()
    except:
        # print(sys.exc_info()[0])
        print("Shhhhhnnnnnarf!")
    finally:
        sys.exit(0)

def main_other():
    settings.initialize()
    initialize()
    main()
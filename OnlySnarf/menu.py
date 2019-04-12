#!/usr/bin/python
# 3/28/2019 Skeetzo
# onlysnarf.py menu system

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
from . import settings
from . import onlysnarf
 
###################
##### Globals #####
###################

version = "0.2.1"
header = "\n ________         .__          _________                     _____ \n \
\\_____  \\   ____ |  | ___.__./   _____/ ____ _____ ________/ ____\\\n \
 /   |   \\ /    \\|  |<   |  |\\_____  \\ /    \\\\__  \\\\_   _ \\   __\\ \n \
/    |    \\   |  \\  |_\\___  |/        \\   |  \\/ __ \\ |  |\\/| |   \n \
\\_______  /___|  /____/ ____/_______  /___|  (____  \\\\__|  |_|   \n \
        \\/     \\/     \\/            \\/     \\/     \\/              \n"

UPDATED = False
UPDATED_TO = False

colors = {
        'blue': '\033[94m',
        'header': '\033[48;1;34m',
        'teal': '\033[96m',
        'pink': '\033[95m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'menu': '\033[48;1;44m'
        }

# Main Menu
menuItems = [
    [ "Actions", "action"],
    [ "Settings", "set_settings"],
    [ "Exit", "exit"]
]

# Actions Menu
actionItems = sorted([
    [ "Test", ["test"]],
    [ "All", ["all"]],
    [ "Download", ["download"]],
    # [ "Upload", ["upload"]],
    # [ "Backup", ["backup"]],
    # [ "Download & Upload", ["download", "upload"]],
    # [ "Download, Upload, & Backup", ["download", "upload", "backup"]],
    # [ "Upload & Backup", ["upload", "backup"]],
    [ "Message", ["message"]],
    [ "Reset", ["reset"]]
])
actionItems.insert(0,[ "Back", ["main"]])

# Message Menu
messageItems = sorted([
    [ "All", ["message_all"]],
    [ "Recent", ["message_recent"]],
    [ "User by Username", ["message_by_username"]],
    [ "User by ID", ["message_by_id"]]
])
messageItems.insert(0,[ "Back", ["main"]])

# File Type Menu
fileItems = sorted([
    [ "Image", "image"],
    [ "Gallery", "gallery"],
    [ "Performer", "performer"],
    [ "Scene", "scene"],
    [ "Video", "video"],
])
fileItems.insert(0,[ "Back", "main"])

# File Location Menu
locationItems = sorted([
    [ "Local", "local"],
    [ "Google Drive", "google"]
])
locationItems.insert(0,[ "Back", "main"])

# Settings Menu
settingItems = sorted([
    [ "File Name", settings.FILE_NAME],
    [ "File Path", settings.FILE_PATH],
    [ "Location", settings.LOCATION, ["Local","Google"]],
    [ "Backup", settings.BACKING_UP, ["True","False"]],
    [ "Delete Google", settings.DELETING, ["True","False"]],
    [ "Delete Local", settings.REMOVE_LOCAL, ["True","False"]],
    [ "Hashtag", settings.HASHTAGGING, ["True","False"]],
    [ "Force Upload", settings.FORCE_UPLOAD, ["True","False"]],
    [ "Mount Path", settings.MOUNT_PATH],
    [ "Users Path", settings.USERS_PATH],
    [ "Show Window", settings.SHOW_WINDOW, ["True","False"]],
    [ "Text", settings.TEXT],
    [ "Type", settings.TYPE],
    [ "Image", settings.IMAGE],
    [ "Tweeting", settings.TWEETING, ["True","False"]],
    [ "Debug", settings.DEBUG, ["True","False"]],
    [ "Debug Skip Download", settings.SKIP_DOWNLOAD, ["True","False"]]    
])
settingItems.insert(0,[ "Back", "main"])

###########################
import atexit
def exit_handler():
    print('Shnnarrrff!')
atexit.register(exit_handler)

import signal
def signal_handler(sig, frame):
    print('Shnnnarf?')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
# print('Press Ctrl+C')
# signal.pause()
###########################

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
            if str(actionItems[int(choice)][0]) == "Back":
                return main()
            elif str(actionItems[int(choice)][0]) == "Reset":
                onlysnarf.remove_local()
            elif str(actionItems[int(choice)][0]) == "Message":
                actionChoice = list(actionItems[int(choice)])[1]
                return finalizeMessage(actionChoice)
            else:
                actionChoice = list(actionItems[int(choice)])[1]
                return finalizeAction(actionChoice)
        except (ValueError, IndexError, KeyboardInterrupt):
            print("Incorrect Index")
        except:
            print(sys.exc_info()[0])
            print("Missing Method") 

### Action Menu - finalize
def finalizeAction(actionChoice):
    for item in fileItems:
        print(colorize("[" + str(fileItems.index(item)) + "] ", 'teal') + list(item)[0])
    while True:
        fileChoice = input(">> ")
        try:
            if int(fileChoice) < 0 or int(fileChoice) >= len(fileItems): raise ValueError
            if str(fileItems[int(fileChoice)][0]) == "Back":
                return action()
            # Call the matching function
            fileChoice = list(fileItems[int(fileChoice)])[1]
            settings.TYPE = fileChoice
            return performAction(actionChoice)
        except (ValueError, IndexError, KeyboardInterrupt):
            print("Incorrect Index")
        except:
            print(sys.exc_info()[0])
            print("Missing Method") 

### Action Menu - perform
def performAction(actionChoice):
    for action in actionChoice:
        try:
            method = getattr(onlysnarf, str(action))
            response = method(settings.TYPE)
            if response:
                if str(action) == "download":
                    for setting in settingItems:
                        if setting[0] == "File Name":
                            setting[1] = response[0]
                        elif setting[0] == "File Path":
                            setting[1] = response[1]
        except (ValueError, IndexError, KeyboardInterrupt):
            print("Incorrect Index")
        except:
            print(sys.exc_info()[0])
            print("Missing Method") 
    mainMenu()

# Message Menu - finalize
def finalizeMessage(actionChoice):
    for item in messageItems:
        print(colorize("[" + str(messageItems.index(item)) + "] ", 'teal') + list(item)[0])
    while True:
        choice = input(">> ")
        try:
            if int(choice) < 0 or int(choice) >= len(messageItems): raise ValueError
            if str(messageItems[int(choice)][0]) == "Back":
                return action()
            # Call the matching function
            choice = list(messageItems[int(choice)])[1]
            return performMessage(actionChoice, choice)
        except (ValueError, IndexError, KeyboardInterrupt):
            print(sys.exc_info()[0])
            print("Incorrect Index")

# Message Menu - perform
def performMessage(actionChoice, messageChoice):
    for action in actionChoice:
        try:
            method = getattr(onlysnarf, str(action))
            response = method(messageChoice)    
        except (ValueError, IndexError, KeyboardInterrupt):
            print("Incorrect Index")
        except:
            print(sys.exc_info()[0])
            print("Missing Method") 
    mainMenu()    

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
            elif str(settingChoice) == "Image":
                settingValue = input("Enter the image path: ")
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
                    except (ValueError, IndexError, KeyboardInterrupt):
                        print("Incorrect Index")
                    except Exception as e:
                        print('What did shnnarf break?')
                        print(e)
                        break
            global UPDATED
            UPDATED = settingChoice
            global UPDATED_TO
            UPDATED_TO = settingValue
            settingItems[int(choice)][1] = settingValue
            return set_settings()
        except (ValueError, IndexError, KeyboardInterrupt):
            print("Incorrect Index")
        except:
            print(sys.exc_info()[0])
            return main()

###########################

def colorize(string, color):
    if not color in colors: return string
    return colors[color] + string + '\033[0m'
  
def exit():
    print("Shnarrf?")
    sys.exit(0)

def main():
    showHeader()
    mainMenu()

def showHeader():
    os.system('clear')
    # Print some badass ascii art header here !
    print(colorize(header, 'header'))
    print(colorize('version '+version+'\n', 'green'))
    showSettings()

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
                print("Missing Option")    
        except (ValueError, IndexError, KeyboardInterrupt):
            print("Incorrect Index")
            pass

def showSettings():
    print('Settings:')
    for setting in settingItems:
        if str(setting[0]) != "Back":
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
        main()
    except:
        # print(sys.exc_info()[0])
        print("Shhhhhnnnnnarf!")
    finally:
        sys.exit(0)
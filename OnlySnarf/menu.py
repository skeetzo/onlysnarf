#!/usr/bin/python
# 2/3/2019 - Skeetzo
# script.py menu system

# GIANT TO;DO
# uploads files via download or local to onlyfans location
# can set whether to backup or delete
# can do each thing separately
# can do groups of things
## can be installed easily via pip
## is the main run script when installed
## includes instructions in the ascii menu etc for setup
### can run locally with a filePath of a video, image, or gallery (USB, mounted, etc)
### link to author, etc

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
import OnlySnarf.onlysnarf as onlysnarf
###########################
header = "\n ________         .__          _________                     _____ \n \
\\_____  \\   ____ |  | ___.__./   _____/ ____ _____ ________/ ____\\\n \
 /   |   \\ /    \\|  |<   |  |\\_____  \\ /    \\\\__  \\\\_   _ \\   __\\ \n \
/    |    \\   |  \\  |_\\___  |/        \\   |  \\/ __ \\ |  |\\/| |   \n \
\\_______  /___|  /____/ ____/_______  /___|  (____  \\\\__|  |_|   \n \
        \\/     \\/     \\/            \\/     \\/     \\/              \n"
 
###########################
CONFIG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.json')
with open(CONFIG_FILE) as config_file:    
    config = json.load(config_file)
DEBUG = False
DEBUG_SKIP_DOWNLOAD = True
IMAGE_UPLOAD_LIMIT = 6
REMOVE_LOCAL = True
LOCATION = "google"
# backup uploaded content
BACKING_UP = True
# delete uploaded content
DELETING = False
# Twitter hashtags
HASHTAGGING = False
# -f -> force / ignore upload max wait
FORCE_UPLOAD = False
# -show -> shows window
SHOW_WINDOW = False
# -t -> text
TEXT = "Default"
# -q -> quiet / no tweet
TWEETING = True
FILE_NAME = None
FILE_PATH = None
UPDATED = False
UPDATED_TO = False
i = 0
while i < len(sys.argv):
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

###########################
colors = {
        'blue': '\033[94m',
        'header': '\033[48;1;34m',
        'teal': '\033[96m',
        'pink': '\033[95m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'menu': '\033[48;1;44m'
        }

menuItems = [
    [ "Actions", "action"],
    [ "Settings", "settings"],
    [ "Exit", "exit"]
]

actionItems = sorted([
    [ "All", ["all"]],
    [ "Download", ["download"]],
    # [ "Upload", ["upload"]],
    # [ "Backup", ["backup"]],
    # [ "Download & Upload", ["download", "upload"]],
    # [ "Download, Upload, & Backup", ["download", "upload", "backup"]],
    # [ "Upload & Backup", ["upload", "backup"]],
    [ "Reset", ["reset"]]
])
actionItems.append([ "Back", ["main"]])

fileItems = sorted([
    [ "Image", "image"],
    [ "Gallery", "gallery"],
    [ "Video", "video"],
])

locationItems = sorted([
    [ "Local", "local"],
    [ "Google Drive", "google"]
])

settingItems = sorted([
    [ "File Name", FILE_NAME],
    [ "File Path", FILE_PATH],
    [ "Location", LOCATION, ["Local","Google"]],
    [ "Backup", BACKING_UP, ["True","False"]],
    [ "Delete Google", DELETING, ["True","False"]],
    [ "Delete Local", REMOVE_LOCAL, ["True","False"]],
    [ "Hashtag", HASHTAGGING, ["True","False"]],
    [ "Force Upload", FORCE_UPLOAD, ["True","False"]],
    [ "Show Window", SHOW_WINDOW, ["True","False"]],
    [ "Text", TEXT],
    [ "Tweeting", TWEETING, ["True","False"]],
    [ "Debug", DEBUG, ["True","False"]],
    [ "Debug Skip Download", DEBUG_SKIP_DOWNLOAD, ["True","False"]]    
])
settingItems.append([ "Back", "main"])

###########################
import atexit
def exit_handler():
    print('Shnnarrrff!')
atexit.register(exit_handler)
###########################

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
            else:
                actionChoice = list(actionItems[int(choice)])[1]
                return finalizeAction(actionChoice)
        except (ValueError, IndexError, KeyboardInterrupt):
            print("Incorrect Index")
            pass

### Action Menu - finalize
def finalizeAction(actionChoice):
    for item in fileItems:
        print(colorize("[" + str(fileItems.index(item)) + "] ", 'teal') + list(item)[0])
    while True:
        fileChoice = input(">> ")
        try:
            if int(fileChoice) < 0 or int(fileChoice) >= len(fileItems): raise ValueError
            # Call the matching function
            fileChoice = list(fileItems[int(fileChoice)])[1]
            return performAction(actionChoice, fileChoice)
        except (ValueError, IndexError, KeyboardInterrupt):
            print("Incorrect Index")
            pass

### Action Menu - perform
def performAction(actionChoice, fileChoice):
    for action in actionChoice:
        try:
            method = getattr(onlysnarf, str(action))
            response = method(fileChoice, json.dumps(settingItems))
            if str(action) == "download":
                settingItems[0][1] = response[0]
                settingItems[1][1] = response[1]
        except (AttributeError, KeyboardInterrupt):
            print("Missing Method") 
    mainMenu()

###########################

### Settings Menu
def settings():
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
                    except (IndexError, ValueError, KeyboardInterrupt):
                        print("Incorrect Index")
                        pass
                    except:
                        print('What did shnnarf break?')
                        print(sys.exc_info()[0])
                        break
            global UPDATED
            UPDATED = settingChoice
            global UPDATED_TO
            UPDATED_TO = settingValue
            settingItems[int(choice)][1] = settingValue
            return settings()
        except (IndexError, ValueError, KeyboardInterrupt):
            print("Incorrect Index")
            pass
        except:
            print(sys.exc_info()[0])
            return main()
            pass

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
    print(colorize('version 0.0.6\n', 'green'))
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
    if UPDATED:
        print('\nUpdated: '+str(UPDATED)+' -> '+str(UPDATED_TO))
    else:
        print('\n'+str(UPDATED))
    UPDATED = False
    print('\r')

if __name__ == "__main__":
    try:
        main()
    except:
        # print(sys.exc_info()[0])
        print("Shhhhhnnnnnarf!")
    finally:
        sys.exit(0)
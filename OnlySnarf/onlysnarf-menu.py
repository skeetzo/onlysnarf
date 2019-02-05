#!/usr/bin/python
# 2/3/2019 - Skeetzo
# onlysnarf.py menu system

# GIANT TO;DO
# menu for updating and setting the config file
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
###########################
header = " ________         .__          _________                     _____ \n \
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
TEXT = None
# -q -> quiet / no tweet
TWEETING = True
FILE_NAME = None
FILE_PATH = None
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
        'teal': '\033[96m',
        'pink': '\033[95m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        }

menuItems = [
    [ "Actions", "action"],
    [ "Settings", "settings"],
    [ "Exit", "exit"]
]

actionItems = [
    [ "All", ["all"]],
    [ "Download", ["download"]],
    # [ "Upload", ["upload"]],
    # [ "Backup", ["backup"]],
    # [ "Download & Upload", ["download", "upload"]],
    # [ "Download, Upload, & Backup", ["download", "upload", "backup"]],
    # [ "Upload & Backup", ["upload", "backup"]],
    [ "Back", ["main"]]
]

fileItems = [
    [ "Image", "image"],
    [ "Gallery", "gallery"],
    [ "Video", "video"],
]

locationItems = [
    [ "Local", "local"],
    [ "Google Drive", "google"]
]

settingItems = [
    [ "File Name", FILE_NAME],
    [ "File Path", FILE_PATH],
    [ "Location", LOCATION],
    [ "Backup", BACKING_UP],
    [ "Delete Google", DELETING],
    [ "Delete Local", REMOVE_LOCAL],
    [ "Hashtag", HASHTAGGING],
    [ "Force Upload", FORCE_UPLOAD],
    [ "Show Window", SHOW_WINDOW],
    [ "Text", TEXT],
    [ "Tweeting", TWEETING],
    [ "Debug", DEBUG],
    [ "Debug Skip Download", DEBUG_SKIP_DOWNLOAD],
    [ "Back", "main"]
]

runtimeItems = [
    [ "Debug", DEBUG],
    [ "Delete Google", DELETING],
    [ "Delete Local", REMOVE_LOCAL],
    [ "Force Upload", FORCE_UPLOAD],
    [ "Hashtag", HASHTAGGING],
    [ "Location", LOCATION],
    [ "Show Window", SHOW_WINDOW],
    [ "Text", TEXT],
    [ "Tweeting", TWEETING]
]

###########################
# import atexit
# def exit_handler():
#     print('')
# atexit.register(exit_handler)
###########################

### Action Menu - file type
def action():
    for item in actionItems:
        print(colorize("[" + str(actionItems.index(item)) + "] ", 'teal') + list(item)[0])
    while True:
        actionChoice = input(">> ")
        try:
            if int(actionChoice) < 0 or int(actionChoice) >= len(actionItems): raise ValueError
            if actionItems[int(actionChoice)] == "Back":
                return main()
            actionChoice = list(actionItems[int(actionChoice)])[1]
            return finalizeAction(actionChoice)
        except (ValueError, IndexError, KeyboardInterrupt):
            print("Incorrect Index")
            pass

### Action Menu - finalize
def finalizeAction(choice):
    for item in fileItems:
        print(colorize("[" + str(fileItems.index(item)) + "] ", 'teal') + list(item)[0])
    while True:
        fileChoice = input(">> ")
        try:
            if int(fileChoice) < 0 or int(fileChoice) >= len(fileItems): raise ValueError
            # Call the matching function
            fileChoice = list(fileItems[int(fileChoice)])[1]
            return performAction(choice, fileChoice)
        except (ValueError, IndexError, KeyboardInterrupt):
            print("Incorrect Index")
            pass

### Action Menu - perform
def performAction(actionChoice, fileChoice):
    import onlysnarf
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
    for item in settingItems:
        print(colorize("[" + str(settingItems.index(item)) + "] ", 'blue') + list(item)[0])
    while True:
        settingChoice = input(">> ")
        try:
            if int(settingChoice) < 0 or int(settingChoice) >= len(settingItems): raise ValueError
            settingChoice = list(settingItems[int(settingChoice)])[0]
            settingValue = list(settingItems[int(settingChoice)])[1]
            if settingChoice == "Back":
                return main()
            if settingChoice == "Location":
                if settingValue == "Google":
                    settingValue = "Local"
                elif settingValue == "Local":
                    settingValue = "Google"
            elif settingValue:
                settingValue = False
            elif settingValue == False:
                settingValue = True
            list(settingItems[int(settingChoice)])[1] = settingValue
            print("Updated: "+settingChoice)
            return main()
        except (ValueError, IndexError, KeyboardInterrupt):
            print("Incorrect Index")
            pass

###########################

def colorize(string, color):
    if not color in colors: return string
    return colors[color] + string + '\033[0m'
  
def exit():
    sys.exit(0)

def main():
    os.system('clear')
    # Print some badass ascii art header here !
    print(colorize(header, 'pink'))
    print(colorize('version 0.0.6\n', 'green'))
    import onlysnarf
    showSettings()
    mainMenu()

def mainMenu():
    ### Main Menu
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
    print('OnlySnarf Settings:')
    for setting in runtimeItems:
        print(' - '+setting[0]+' = '+str(setting[1]))

if __name__ == "__main__":
    main()
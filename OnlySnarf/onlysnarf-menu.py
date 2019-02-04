import random
import os
import shutil
import datetime
import json
import sys
import pathlib

CONFIG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.json')

with open(CONFIG_FILE) as config_file:    
    config = json.load(config_file)

# GIANT TO;DO
# menu for updating and setting the config file
# downloads and uploads files from a drive location to onlyfans location
# can set whether to backup or delete
# can do each thing separately
# can do groups of things
## can be installed easily via pip
## is the main run script when installed
## includes instructions in the ascii menu etc for setup
### can run locally with a filePath of a video, image, or gallery (USB, mounted, etc)
### link to author, etc

# OnlyFans
# - Download & Upload
# -- Image
# -- Gallery
# -- Video
# - Download, Upload, & Backup
# -- Image
# -- Gallery
# -- Video

# Download
# - Image
# - Gallery
# - Video
# Upload
# - Image (file)
# - Gallery (directory)
# - Video (file)
# Config
# - Show
# - Update


header = " ________         .__          _________                     _____ \n \
\\_____  \\   ____ |  | ___.__./   _____/ ____ _____ ________/ ____\\\n \
 /   |   \\ /    \\|  |<   |  |\\_____  \\ /    \\\\__  \\\\_   _ \\   __\\ \n \
/    |    \\   |  \\  |_\\___  |/        \\   |  \\/ __ \\ |  |\\/| |   \n \
\\_______  /___|  /____/ ____/_______  /___|  (____  \\\\__|  |_|   \n \
        \\/     \\/     \\/            \\/     \\/     \\/              \n"
 
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
    [ "Download", ["download"]],
    [ "Upload", ["upload"]],
    [ "Backup", ["backup"]],
    [ "Download & Upload", ["download", "upload"]],
    [ "Download, Upload, & Backup", ["download", "upload", "backup"]],
    [ "Upload & Backup", ["upload", "backup"]]
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
    [ "Local", "local"],
]
# menuItems = list(menuItems)
 
ARGS = {
    "content_type": "video",
    "remove_local": True,
    "backup": True,
    "delete": False
}

FILE_NAME = None
FILE_PATH = None

def settings():
    for item in settingItems:
        print(colorize("[" + str(settingItems.index(item)) + "] ", 'blue') + list(item)[0])
    return

def action():
    ### File Menu
    for item in actionItems:
        print(colorize("[" + str(actionItems.index(item)) + "] ", 'teal') + list(item)[0])
    while True:
        actionChoice = input(">> ")
        try:
            if int(actionChoice) < 0 or int(actionChoice) >= len(actionItems): raise ValueError
            # Call the matching function
            actionChoice = list(actionItems[int(actionChoice)])[1]
            return finalizeAction(actionChoice)
        except (ValueError, IndexError):
            print("Incorrect Index")
            pass

def finalizeAction(choice):
    ### File Menu
    for item in fileItems:
        print(colorize("[" + str(fileItems.index(item)) + "] ", 'teal') + list(item)[0])
    while True:
        fileChoice = input(">> ")
        try:
            if int(fileChoice) < 0 or int(fileChoice) >= len(fileItems): raise ValueError
            # Call the matching function
            fileChoice = list(fileItems[int(fileChoice)])[1]
            return performAction(choice, fileChoice)
        except (ValueError, IndexError):
            print("Incorrect Index")
            pass

def performAction(actionChoice, fileChoice):
    import onlysnarf
    for action in actionChoice:
        try:
            method = getattr(onlysnarf, str(action))
            output = method(fileChoice)
        except (AttributeError):
            print("Missing Method") 

def colorize(string, color):
    if not color in colors: return string
    return colors[color] + string + '\033[0m'
  
def exit():
    sys.exit(0)

def main():
    os.system('clear')
    # Print some badass ascii art header here !
    print(colorize(header, 'pink'))
    print(colorize('version 1.0.0\n', 'green'))
    import onlysnarf
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
        except (ValueError, IndexError):
            print("Incorrect Index")
            pass

if __name__ == "__main__":
    main()
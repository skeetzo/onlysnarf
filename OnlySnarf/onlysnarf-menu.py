import random
import os
import shutil
import datetime
import json
import sys
import pathlib
import OnlySnarf 
import importlib.util
spec = importlib.util.spec_from_file_location("module.name", "/path/to/file.py")


header = "\
_________               .__    __________                   __               __\n\
\_   ___ \  ____   ____ |  |   \______   \_______  ____    |__| ____   _____/  |_\n\
/    \  \/ /  _ \ /  _ \|  |    |     ___/\_  __ \/  _ \   |  |/ __ \_/ ___\   __\\\n\
\     \___(  <_> |  <_> )  |__  |    |     |  | \(  <_> )  |  \  ___/\  \___|  |\n\
 \______  /\____/ \____/|____/  |____|     |__|   \____/\__|  |\___  >\___  >__|\n\
        \/                                             \______|    \/     \/      \n"
 
colors = {
        'blue': '\033[94m',
        'pink': '\033[95m',
        'green': '\033[92m',
        }
 
def colorize(string, color):
    if not color in colors: return string
    return colors[color] + string + '\033[0m'
 
def foo():
    print("You called foo()")
    input("Press [Enter] to continue...")
 
def bar():
    print("You called bar()")
    input("Press [Enter] to continue...")
 
def exit():
    sys.exit(0)


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

menuItems = [
    [ "Download, Upload, & Backup", "downloadUploadAndBackup"],
    [ "Exit", "exit"]
]
# menuItems = list(menuItems)
 
ARGS = {
    "content_type": "video",
    "remove_local": True,
    "backup": True,
    "delete": False
}

with open(CONFIG_FILE) as config_file:    
    config = json.load(config_file)


def main():
    # Print some badass ascii art header here !
    print(colorize(header, 'pink'))
    print(colorize('version 0.1\n', 'green'))
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
                method(ARGS)
            else:
                print("Missing Option")    
        except (ValueError, IndexError):
            print("Incorrect Index")
            pass


if __name__ == "__main__":
    main()
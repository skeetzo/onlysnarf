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
from OnlySnarf import cron as Cron

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
methodItems = []

def initialize():
    # print("Initializing Menu")
    global INITIALIZED
    if INITIALIZED:
        # print("Already Initialized, Skipping")
        return
    global settingItems
    # Settings Menu
    settingItems = [
        [ "Verbose", settings.VERBOSE, ["True","False"],True],
        [ "Debug", settings.DEBUG, ["True","False"],False],
        [ "Backup", settings.BACKUP, ["True","False"],True],
        [ "Show Window", settings.SHOW_WINDOW, ["True","False"],False],
        [ "Delete Google", settings.DELETE_GOOGLE, ["True","False"],False],
        [ "Skip Delete", settings.SKIP_DELETE, ["True","False"],False],
        [ "Tweeting", settings.TWEETING, ["True","False"],True],
        [ "Image Limit", settings.IMAGE_UPLOAD_LIMIT,None,True],
    ]
    if str(settings.VERBOSE) == "True":
        settingItems.append([ "Skip Backup", settings.SKIP_BACKUP, ["True","False"],False])
        settingItems.append([ "Mount Path", settings.MOUNT_PATH,None,False])
        settingItems.append([ "Drive Path", settings.DRIVE_PATH,None,False])
        settingItems.append([ "Users Path", settings.USERS_PATH,None,False])
        settingItems.append([ "Google Root", settings.ROOT_FOLDER,None,False])
        settingItems.append([ "Drive Folder", settings.DRIVE_FOLDERS,None,False])
        settingItems.append([ "Create Drive", settings.CREATE_DRIVE, ["True","False"],False])
    if str(settings.DEBUG) == "True":
        settingItems.append([ "Skip Upload", settings.SKIP_UPLOAD, ["True","False"],False])
        settingItems.append([ "Force Delete", settings.FORCE_DELETE, ["True","False"],False])
        settingItems.append([ "Force Backup", settings.FORCE_BACKUP, ["True","False"],False])
        settingItems.append([ "Force Upload", settings.FORCE_UPLOAD, ["True","False"],False])
        settingItems.append([ "Skip Download", settings.SKIP_DOWNLOAD, ["True","False"],False])
        settingItems.append([ "Image Max", settings.IMAGE_UPLOAD_MAX,None,False])
        settingItems.append([ "Text", settings.TEXT,None,False])
        settingItems.append([ "Local", settings.INPUT,None,False])
        settingItems.append([ "Image", settings.IMAGE,None,False])
        settingItems.append([ "Prefer Local", settings.PREFER_LOCAL,["True","False"],True])
        # settingItems.append([ "Overwrite Local", settings.OVERWRITE_LOCAL,["True","False"],True])
    settingItems = sorted(settingItems)
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
    actionItems = [
        [ "Upload", "release" ],
        [ "Download", "download" ],
        # [ "Promotion", "promotion" ],
        [ "Message", "message" ],
        [ "Discount", "discount" ],
        [ "Post", "post" ],
        [ "Reset", "reset" ]
    ]
    if str(settings.DEBUG) == "True":
        actionItems.append([ "Test", "test"])
        actionItems.append([ "Promotion", "promotion" ])
        actionItems.append([ "Cron", "cron" ])
    actionItems = sorted(actionItems)
    actionItems.insert(0,[ "Back", "main"])

    global messageItems
    # Message Menu
    messageItems = [
        [ "All", "all"],
        # [ "New", "new"],
        [ "Recent", "recent"],
        # [ "Favorite", "favorite"],
        [ "User by Username", "user"],
        [ "Select User", "select"]
    ]
    if str(settings.DEBUG) == "True":
        messageItems.append([ "New", "new"])
        messageItems.append([ "Favorite", "favorite"])
    messageItems = sorted(messageItems)
    messageItems.insert(0,[ "Back", "main"])

    global fileItems
    # File Type Menu
    fileItems = [
        [ "Image", "image"],
        [ "Gallery", "gallery"],
        [ "Performer", "performer"],
        # [ "Scene", "scene"],
        [ "Video", "video"],
    ]
    if str(settings.DEBUG) == "True":
        fileItems.append([ "Scene", "scene"])
    fileItems = sorted(fileItems)
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
            [ "Select User", "select" ]
        ])
    promotionItems.insert(0,[ "Back", "main"])

    global methodItems
    methodItems = sorted([
        [ "Choose", "choose" ],
        [ "Random", "random" ]
    ])
    methodItems.insert(0,[ "Back", "main"])

    global postItems
    postItems = sorted([
        [ "Enter", "enter" ],
        [ "Select", "select" ]
    ])
    postItems.insert(0,[ "Back", "main"])

    global cronItems
    cronItems = sorted([
        [ "Add", "add" ],
        [ "List", "list" ],
        [ "Delete", "delete" ],
        [ "Delete All", "deleteall" ]
    ])
    cronItems.insert(0,[ "Back", "main"])

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
            elif str(actionItems[int(choice)][1]) == "discount":
                actionChoice = list(actionItems[int(choice)])[1]
                return finalizeDiscount(actionChoice)
            elif str(actionItems[int(choice)][1]) == "promotion":
                actionChoice = list(actionItems[int(choice)])[1]
                return finalizePromotion(actionChoice)
            elif str(actionItems[int(choice)][1]) == "post":
                actionChoice = list(actionItems[int(choice)])[1]
                return finalizePost(actionChoice)
            elif str(actionItems[int(choice)][1]) == "cron":
                actionChoice = list(actionItems[int(choice)])[1]
                return finalizeCron(actionChoice)
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
            return selectMethod(actionChoice, fileChoice)
        except (ValueError, IndexError):
            print("Error: Incorrect Index")
        except Exception as e:
            settings.maybePrint(e)
            print("Error: Missing Method") 

def selectMethod(actionChoice, fileChoice):
    # if settings.INPUT and methodItems doesn't include Input option already
    if [ "Local", "local" ] not in methodItems and actionChoice == "release":
        methodItems.append([ "Local", "local" ])
    for item in methodItems:
        print(colorize("[" + str(methodItems.index(item)) + "] ", 'teal') + list(item)[0])
    while True:
        methodChoice = input(">> ")
        try:
            if int(methodChoice) < 0 or int(methodChoice) >= len(methodItems): raise ValueError
            methodChoice_ = list(methodItems[int(methodChoice)])[1]
            if str(methodItems[int(methodChoice)][1]) == "main":
                return action()
            elif str(methodItems[int(methodChoice)][1]) == "choose":
                if str(fileChoice) == "gallery":
                    choices = displayFolders("galleries")
                elif str(fileChoice) == "video":
                    choices = displayFolders("videos")
                elif str(fileChoice) == "image":
                    choices = displayFolders("images")
                elif str(fileChoice) == "performer":
                    choices = displayFolders("performers")
                elif str(fileChoice) == "scene":
                    choices = displayFolders("scenes")
                seeking = True
                while seeking:
                    choice = input(">> ")
                    try:
                        if int(choice) < 0 or int(choice) > len(choices): raise ValueError
                        if int(choice) == 0:
                            return selectMethod(actionChoice, fileChoice)
                        file = choices[int(choice)-1]
                        parent = file
                        seeking = False
                        if str(fileChoice) == "gallery" or str(fileChoice) == "image"  or str(fileChoice) == "video" or str(fileChoice) == "performer":
                            if str(fileChoice) == "gallery":
                                choices_ = displayFolders(file['title'], parent="galleries")
                            elif str(fileChoice) == "image":
                                choices_ = displayFiles(file['title'], parent="images")
                            elif str(fileChoice) == "video":
                                choices_ = displayFiles(file['title'], parent="videos")
                            elif str(fileChoice) == "performer":
                                choices_ = displayFolders(file['title'], parent="performers")
                            seeking_ = True
                            while seeking_:
                                choice_ = input(">> ")
                                try:
                                    if int(choice_) < 0 or int(choice_) > len(choices_): raise ValueError
                                    if int(choice_) == 0:
                                        return selectMethod(actionChoice, fileChoice)
                                    file = choices_[int(choice_)-1]
                                    seeking_ = False
                                    folderName = file['title']
                                    if str(fileChoice) == "performer":
                                        # parent = file
                                        # choices_ = displayFiles(file['title'], parent=parent)
                                        choices_ = displayBoth(file['title'], parent=parent)
                                        seeking__ = True
                                        while seeking__:
                                            choice_ = input(">> ")
                                            try:
                                                if int(choice_) < 0 or int(choice_) > len(choices_): raise ValueError
                                                if int(choice_) == 0:
                                                    return selectMethod(actionChoice, fileChoice)
                                                file = choices_[int(choice_)-1]
                                                seeking__ = False
                                                return performAction(actionChoice, fileChoice, methodChoice_, file=file, folderName=folderName, parent=parent)
                                            except (ValueError, IndexError):
                                                print(sys.exc_info()[0])
                                                print("Error: Incorrect Index")
                                                return finalizeAction(actionChoice)
                                except (ValueError, IndexError):
                                    print(sys.exc_info()[0])
                                    print("Error: Incorrect Index")
                                    return finalizeAction(actionChoice)
                        return performAction(actionChoice, fileChoice, methodChoice_, file=file, folderName=folderName, parent=parent)
                    except (ValueError, IndexError):
                        print(sys.exc_info()[0])
                        print("Error: Incorrect Index")
                        return finalizeAction(actionChoice)
            return performAction(actionChoice, fileChoice, methodChoice_)
        except (ValueError, IndexError):
            print("Error: Incorrect Index")
        except Exception as e:
            settings.maybePrint(e)
            print("Error: Missing Method") 

### Action Menu - perform
def performAction(actionChoice, fileChoice, methodChoice, file=None, folderName=None, parent=None):
    try:
        method = getattr(OnlySnarf, str(actionChoice))
        response = method(fileChoice, methodChoice=methodChoice, file=file, folderName=folderName, parent=parent)
        if response:
            if str(actionChoice) == "download":
                settings.update_value("input",response.get("path"))
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
    if str(messageChoice) == "select":
        messageChoice = "user"
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
    elif str(messageChoice) == "user":
        print("Username:")
        username = input(">> ")
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
    OnlySnarf.remove_local()
    try: 
        image = Google.download_file(image[0]).get("path")
    except Exception as e:
        OnlySnarf.remove_local()
        try:
            image = Google.download_gallery(image[0]).get("path")
        except Exception as e:
            print("Error: Missing Image(s)")
            image = None
            # pass
    OnlySnarf.message(choice, message=message, image=image, price=price, username=username)

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

def finalizeDiscount(actionChoice):
    for item in messageItems:
        print(colorize("[" + str(messageItems.index(item)) + "] ", 'teal') + list(item)[0])
    while True:
        choice = input(">> ")
        try:
            choice = int(choice)
            if int(choice) < 0 or int(choice) >= len(messageItems): raise ValueError
            if str(messageItems[int(choice)][1]) == "main":
                return action()
            return performDiscount(actionChoice, messageItems[int(choice)][1])
        except (ValueError, IndexError):
            print(sys.exc_info()[0])
            print("Error: Incorrect Index")

def performDiscount(actionChoice, discountChoice):
    username = None
    if str(discountChoice) == "user":
        user = input("Username: ")
        OnlySnarf.discount(user, depth=int(choice))
        mainMenu()
    elif str(discountChoice) == "select":
        users = displayUsers()
        seeking = True
        while seeking:
            choice = input(">> ")
            try:
                if int(choice) < 0 or int(choice) > len(users): raise ValueError
                if int(choice) == 0:
                    return finalizeDiscount(actionChoice)
                OnlySnarf.discount(users[int(choice)-1], depth=int(choice))
                mainMenu()
            except (ValueError, IndexError):
                print(sys.exc_info()[0])
                print("Error: Incorrect Index")
                return mainMenu()
    OnlySnarf.discount(discountChoice)
    mainMenu()    

def finalizePost(actionChoice):
    for item in postItems:
        print(colorize("[" + str(postItems.index(item)) + "] ", 'teal') + list(item)[0])
    while True:
        choice = input(">> ")
        try:
            choice = int(choice)
            if int(choice) < 0 or int(choice) >= len(postItems): raise ValueError
            if str(postItems[int(choice)][1]) == "main":
                return action()
            elif str(postItems[int(choice)][1]) == "enter":
                OnlySnarf.post()
            else:
                selectPost()
            return mainMenu()
        except (ValueError, IndexError):
            print(sys.exc_info()[0])
            print("Error: Incorrect Index")

def selectPost():
    postMenu = []
    for key in settings.POSTS:
        postMenu.append([ key.title().replace("_"," "), settings.POSTS[key]])
    postMenu.insert(0,[ "Back", "main"])
    for item in postMenu:
        print(colorize("[" + str(postMenu.index(item)) + "] ", 'teal') + list(item)[0] + " - {}".format(list(item)[1][:50]))
    while True:
        choice = input(">> ")
        try:
            choice = int(choice)
            if int(choice) < 0 or int(choice) >= len(postMenu): raise ValueError
            if str(postMenu[int(choice)][1]) == "main":
                return action()
            text = postMenu[int(choice)][1]
            OnlySnarf.post(text=text)
            return mainMenu()
        except (ValueError, IndexError):
            print(sys.exc_info()[0])
            print("Error: Incorrect Index")

def finalizeCron(actionChoice):
    for item in cronItems:
        print(colorize("[" + str(cronItems.index(item)) + "] ", 'teal') + list(item)[0])
    while True:
        cronChoice = input(">> ")
        try:
            if int(cronChoice) < 0 or int(cronChoice) >= len(cronItems): raise ValueError
            if str(cronItems[int(cronChoice)][1]) == "main":
                return action()
            cronChoice = list(cronItems[int(cronChoice)])[1]
            return performCron(actionChoice, cronChoice)
        except (ValueError, IndexError):
            print("Error: Incorrect Index")
        except Exception as e:
            settings.maybePrint(e)
            print("Error: Missing Method") 

def performCron(actionChoice, cronChoice):
    if str(cronChoice) == "add":
        print("Comment:")
        comment = input(">> ")
        print("Args:")
        args = input(">> ")
        args = args.split(",")
        print("Minute:")
        minute = input(">> ")
        print("Hours:")
        hour = input(">> ")
        Cron.create(comment, args=args, minute=minute, hour=hour)
    elif str(cronChoice) == "list":
        Cron.list()
    elif str(cronChoice) == "delete":
        jobs = Cron.getAll()
        print(colorize("[0] ", 'teal') + "Back")
        jobs_ = []
        for job in jobs:
            jobs_.append(str(job.comment))
            print(colorize("[" + str(jobs.index(job)+1) + "] ", 'teal') + str(job))
        while True:
            choice = input(">> ")
            try:
                choice = int(choice)
                if int(choice) < 0 or int(choice) > len(jobs): raise ValueError
                if int(choice) == 0: return finalizeCron(actionChoice)
                Cron.delete(jobs_[int(choice)-1])
                return mainMenu()
            except (ValueError, IndexError):
                print(sys.exc_info()[0])
                print("Error: Incorrect Index")
        
    elif str(cronChoice) == "deleteall":
        Cron.deleteAll()
    else:
        print("Error: Missing Cron Action")
    mainMenu()    

def displayBoth(folderName, parent=None):
    files = Google.get_files_of_folder(folderName, parent=parent)
    folders = Google.get_folders_of_folder(folderName, parent=parent)
    files_both = []
    for f in files: files_both.append(f)
    for f in folders: files_both.append(f)
    print(colorize("[0] ", 'blue') + "Back")
    i = 1
    for file in files_both:
        print(colorize("[" + str(i) + "] ", 'blue') + str(file['title']))
        i = i+1
    return files_both

def displayFiles(folderName, parent=None):
    files = Google.get_files_of_folder(folderName, parent=parent)
    print(colorize("[0] ", 'blue') + "Back")
    i = 1
    for file in files:
        print(colorize("[" + str(i) + "] ", 'blue') + str(file['title']))
        i = i+1
    return files

def displayFolders(folderName, parent=None):
    folders = Google.get_folders_of_folder(folderName, parent=parent)
    print(colorize("[0] ", 'blue') + "Back")
    i = 1
    for folder in folders:
        print(colorize("[" + str(i) + "] ", 'blue') + str(folder['title']))
        i = i+1
    return folders

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
            elif str(settingChoice) == "Local":
                settingValue = input("Enter the local path: ")
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
    showUser()
    showSettings()

def showSettings():
    print('Settings:')
    for setting in settingItems:
        if str(setting[0]) == "Image Limit" and setting[3]:
            print(" - {} = {}/{}".format(setting[0],setting[1],settings.IMAGE_UPLOAD_MAX))
        elif str(setting[0]) != "Back" and str(settings.DEBUG) == "True":
            print(" - {} = {}".format(setting[0],setting[1]))
        elif str(setting[0]) != "Back" and setting[3]:
            print(" - {} = {}".format(setting[0],setting[1]))
    global UPDATED
    global UPDATED_TO
    if str(UPDATED) != "False":
        print('\nUpdated: '+str(UPDATED)+' -> '+str(UPDATED_TO))
    UPDATED = False
    print('\r')

def showUser():
    print("User:")
    print(" - Username = {}".format(settings.USERNAME))
    if settings.PASSWORD and str(settings.PASSWORD) != "":
        pass_ = "******"
    else:
        pass_ = ""
    print(" - Password = {}".format(pass_))
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
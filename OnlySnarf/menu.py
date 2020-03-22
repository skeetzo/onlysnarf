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
# from OnlySnarf import OnlySnarf
from OnlySnarf import google as Google
from OnlySnarf import cron as Cron
from OnlySnarf.snarf import Snarf

###################
##### Globals #####
###################

snarf = Snarf()

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
        [ "Image Limit", settings.IMAGE_DOWNLOAD_LIMIT,None,True],
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
        settingItems.append([ "Image Max", settings.IMAGE_UPLOAD_LIMIT,None,False])
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
        [ "Settings", "set_settings"]
    ]
    if str(settings.DEBUG) == "True":
        menuItems.append(["Profile", "profile"])
    menuItems = sorted(menuItems)
    menuItems.append([ "Exit", "exit"])

    ###
    ### Actions
    ###

    global actionItems
    # Actions Menu
    actionItems = [
        # [ "Download", "download" ],
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
        [ "Recent", "recent"],
        # [ "Favorite", "favorite"],
        [ "Enter Username", "user"],
        [ "Select Username", "select"]
    ]
    if str(settings.DEBUG) == "True":
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
    for str(category) in settings.get_categories():
        fileItems.append([ str(category).capitalize(), str(category).lower()])
    # if str(settings.DEBUG) == "True":
    fileItems = sorted(fileItems)
    fileItems.insert(0,[ "Back", "main"])

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

    ###
    ### Cron
    ###

    global cronItems
    cronItems = sorted([
        [ "Add", "add" ],
        [ "List", "list" ],
        [ "Delete", "delete" ],
        [ "Delete All", "deleteall" ]
    ])
    cronItems.insert(0,[ "Back", "main"])

    ###
    ### Settings
    ###

    global settingsItems
    settingsItems = sorted([
        [ "Profile", "profileSettings" ],
        [ "Account", "accountSettings" ],
        [ "Notification", "notificationSettings" ],
        [ "Security", "securitySettings" ],
        [ "Other", "otherSettings" ],
        [ "Sync", "sync" ]
    ])
    settingsItems.insert(0,[ "Back", "main", "main"])

    # text, path, url, price, get, country, ip, or bool
    global profileSettingsItems
    profileSettingsItems = sorted([
        [ "Cover Image", "coverImage", "path" ],
        [ "Profile Photo", "profilePhoto", "path" ],
        [ "Display Name", "displayName", "text" ],
        [ "Subscription Price", "subscriptionPrice", "price" ],
        [ "About", "about", "text" ],
        [ "Location", "location", "text" ],
        [ "Website URL", "websiteURL", "url" ]
    ])
    profileSettingsItems.insert(0,[ "Back", "main", "main"])

    global accountSettingsItems
    accountSettingsItems = sorted([
        [ "Username", "username", "text" ],
        [ "Email", "email", "text" ],
        [ "Password", "password", "text" ]
    ])
    accountSettingsItems.insert(0,[ "Back", "main"])

    global notificationSettingsItems
    notificationSettingsItems = sorted([
        [ "Email Notifications", "emailNotifs", "bool" ],
        [ "New Referral", "emailNotifsNewReferral", "bool" ],
        [ "New Stream", "emailNotifsNewStream", "bool" ],
        [ "New Subscriber", "emailNotifsNewSubscriber", "bool" ],
        [ "New Tip", "emailNotifsNewTip", "bool" ],
        [ "Renewal", "emailNotifsRenewal", "bool" ],
        [ "New Likes Summary", "emailNotifsNewLikes", "bool" ],
        [ "New Posts Summary", "emailNotifsNewPosts", "bool" ],
        [ "New Private Message Summary", "emailNotifsNewPrivMessages", "bool" ],
        [ "Site Notifications", "siteNotifs", "bool" ],
        [ "New Comment", "siteNotifsNewComment", "bool" ],
        [ "New Favorite", "siteNotifsNewFavorite", "bool" ],
        [ "New Discounts", "siteNotifsDiscounts", "bool" ],
        [ "New Subscriber", "siteNotifsNewSubscriber", "bool" ],
        [ "New Tip", "siteNotifsNewTip", "bool" ],
        [ "Toast Notifications", "toastNotifs", "bool" ],
        [ "New Comment", "toastNotifsNewComment", "bool" ],
        [ "New Favorite", "toastNotifsNewFavorite", "bool" ],
        [ "New Subscriber", "toastNotifsNewSubscriber", "bool" ],
        [ "New Tip", "toastNotifsNewTip", "bool" ]
    ])
    notificationSettingsItems.insert(0,[ "Back", "main"])

    global securitySettingsItems
    securitySettingsItems = sorted([
        [ "Fully Private Profile", "fullyPrivate", "bool" ],
        [ "Enable Comments", "enableComments", "bool" ],
        [ "Show Fans Count on your Profile", "showFansCount", "bool" ],
        [ "Show Posts Tips Summary", "showPostsTip", "bool" ],
        [ "Public Friends List", "publicFriendsList", "bool" ],
        [ "IP and Geo Blocking - By Country", "ipCountry", "country" ],
        [ "IP and Geo Blocking - By IP", "ipIP", "ip" ],
        [ "Watermark - Enabled", "watermark", "bool" ],
        [ "Watermark - Photos", "watermarkPhoto", "bool" ],
        [ "Watermark - Videos", "watermarkVideo", "bool" ],
        [ "Watermark - Custom Text", "watermarkText", "text" ]
    ])
    securitySettingsItems.insert(0,[ "Back", "main"])

    global otherSettingsItems
    otherSettingsItems = sorted([
        [ "Live Server", "liveServer", "get" ],
        [ "Live Key", "liveServerKey", "get" ]
    ])
    otherSettingsItems.insert(0,[ "Back", "main"])

    # print("Initialized Menu")
    INITIALIZED = True

#####################
##### Functions #####
#####################



from __future__ import print_function, unicode_literals
from PyInquirer import prompt, print_json
from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, print_json
from PyInquirer import Validator, ValidationError
from examples import custom_style_2
from pprint import pprint
from __future__ import print_function, unicode_literals
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt, Separator
from examples import custom_style_2
from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, print_json
from examples import custom_style_2
from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, print_json
from examples import custom_style_2
from __future__ import print_function, unicode_literals
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt, Separator
from examples import custom_style_2
from __future__ import print_function
from pprint import pprint
from PyInquirer import prompt
from examples import custom_style_1
from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt
from examples import custom_style_2
from __future__ import print_function, unicode_literals
import regex
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
from examples import custom_style_3
from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, print_json
from PyInquirer import Validator, ValidationError
from examples import custom_style_2
from pprint import pprint
from __future__ import print_function, unicode_literals
import regex
from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt
from PyInquirer import Validator, ValidationError
from examples import custom_style_2







# get all settings from settings.get_etc and argparse
# confirm settings

# first menu prompt for actions, settings, etc
# actions prompts actions dialogue tree
# settings prompts settings dialogue tree

# so make actions dialogue tree
# - discount, message, post

# make settings dialogue tree
# - app settings

# make profile settings dialogue tree
# - profile (synced and unsynced)



# main menu
# show header
# show options
# - Action
# - Crons
# - Profile
# - Settings

# Action
# - Discount
# - Message
# - Post
# - Promotion

# Discount
# - all, recent, etc
# - by username
# - select
# 
# - user, 
# - amount (%), duration (months)

# Message
# - all, recent, etc
# - by username
# - select

# Post
# - text, files
# - keywords, tags, performers
# - schedule, poll, expiration
#
# - date: day, time
# - questions, duration (preset 1, 3, 5, ...)
# - expiration (preset 1, 3, 5, ...)

# Promotion
# - all, recent, etc
# - create new
# - delete [all]
# - user
# - from examples
#
# - user
# - amount (preset or incremental %), duration (months)

#####

# Profile
# - account, [ other page names]

#####
# Settings
# - args, [ other options]







def show_header():
    # os.system('clear')
    print(colorize(header, 'header'))
    print(colorize('version '+version+'\n', 'green'))
    showUser()
    showSettings()


def ask_direction():
    directions_prompt = {
        'type': 'list',
        'name': 'direction',
        'message': 'Which direction would you like to go?',
        'choices': ['Forward', 'Right', 'Left', 'Back']
    }
    answers = prompt(directions_prompt)
    return answers['direction']

# TODO better to use while loop than recursion!


def main():
    print('You find yourself in a small room, there is a door in front of you.')
    exit_house()

def main():
    show_header()
    main_menu()


def ask_menu():
    menu_prompt = {
        'type': 'list',
        'name': 'menu',
        'message': 'Please select an option:',
        'choices': ['Action', 'Profile', 'Settings', 'Exit']
    }
    answers = prompt(menu_prompt)
    return answers['menu']

def main_menu():
    direction = ask_menu()
    if (direction == 'Action'): action_menu()
    elif (direction == 'Profile'): profile_menu()
    elif (direction == 'Settings'): settings_menu()
    else: exit()

def ask_action():
    menu_prompt = {
        'type': 'list',
        'name': 'action',
        'message': 'Please select an action:',
        'choices': ['Back', 'Discount', 'Message', 'Post', 
            # 'Promotion'
        ]
    }
    if str(settings.DEBUG) == "True":
        menu_prompt["choices"].append("Promotion")
    answers = prompt(menu_prompt)
    return answers['action']

def action_menu():
    action = ask_action()
    if (action == 'Back'):main()
    elif (action == 'Discount'): discount_menu()
    elif (action == 'Message'): message_menu()
    elif (action == 'Post'): post_menu()
    elif (action == 'Promotion'): promotion_menu()
    else: main()

def myround(x, base=5):
    return base * round(x/base)

def discount_menu():
    user = user_menu()
    # 5-55% / 5
    discount_prompt = {
        'type': 'input',
        'name': 'amount',
        'message': 'Amount (increments of 5) in %?',
        'validate': NumberValidator,
        'filter': lambda val: int(myround(val))
    },
    # 1-12 months
    {
        'type': 'input',
        'name': 'duration',
        'message': 'Months?',
        'validate': NumberValidator,
        'filter': lambda val: int(val)

    }
    answers = prompt(discount_prompt)
    Snarf.discount(choice=user, discount={"amount":answers["amount"], "duration":answers["duration"]})
    main()

# returns the list of usernames to select
def user_menu():
    pass

def message_menu():
    message = Message()
    Snarf.message(message=message.prompt())
    main()

def post_menu():
    pass

def promotion_menu():
    pass



def encounter2b():
    prompt({
        'type': 'list',
        'name': 'weapon',
        'message': 'Pick one',
        'choices': [
            'Use the stick',
            'Grab a large rock',
            'Try and make a run for it',
            'Attack the wolf unarmed'
        ]
    }, style=custom_style_2)
    print('The wolf mauls you. You die. The end.')



class PhoneNumberValidator(Validator):
    def validate(self, document):
        ok = regex.match('^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid phone number',
                cursor_position=len(document.text))  # Move cursor to end


class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end


print('Hi, welcome to Python Pizza')

questions = [
    {
        'type': 'confirm',
        'name': 'toBeDelivered',
        'message': 'Is this for delivery?',
        'default': False
    },
    {
        'type': 'input',
        'name': 'phone',
        'message': 'What\'s your phone number?',
        'validate': PhoneNumberValidator
    },
    {
        'type': 'list',
        'name': 'size',
        'message': 'What size do you need?',
        'choices': ['Large', 'Medium', 'Small'],
        'filter': lambda val: val.lower()
    },
    {
        'type': 'input',
        'name': 'quantity',
        'message': 'How many do you need?',
        'validate': NumberValidator,
        'filter': lambda val: int(val)
    },
    {
        'type': 'expand',
        'name': 'toppings',
        'message': 'What about the toppings?',
        'choices': [
            {
                'key': 'p',
                'name': 'Pepperoni and cheese',
                'value': 'PepperoniCheese'
            },
            {
                'key': 'a',
                'name': 'All dressed',
                'value': 'alldressed'
            },
            {
                'key': 'w',
                'name': 'Hawaiian',
                'value': 'hawaiian'
            }
        ]
    },
    {
        'type': 'rawlist',
        'name': 'beverage',
        'message': 'You also get a free 2L beverage',
        'choices': ['Pepsi', '7up', 'Coke']
    },
    {
        'type': 'input',
        'name': 'comments',
        'message': 'Any comments on your purchase experience?',
        'default': 'Nope, all good!'
    },
    {
        'type': 'list',
        'name': 'prize',
        'message': 'For leaving a comment, you get a freebie',
        'choices': ['cake', 'fries'],
        'when': lambda answers: answers['comments'] != 'Nope, all good!'
    }
]

answers = prompt(questions, style=custom_style_3)
print('Order receipt:')
pprint(answers)






questions = [
    {
        'type': 'rawlist',
        'name': 'theme',
        'message': 'What do you want to do?',
        'choices': [
            'Order a pizza',
            'Make a reservation',
            Separator(),
            'Ask opening hours',
            'Talk to the receptionist'
        ]
    },
    {
        'type': 'rawlist',
        'name': 'size',
        'message': 'What size do you need',
        'choices': ['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
        'filter': lambda val: val.lower()
    }
]

answers = prompt(questions, style=custom_style_2)
print_json(answers)




questions = [
    {
        'type': 'input',
        'name': 'first_name',
        'message': 'What\'s your first name',
    }
]

answers = prompt(questions)
print_json(answers)  # use the answers as input for your app


def get_delivery_options(answers):
    options = ['bike', 'car', 'truck']
    if answers['size'] == 'jumbo':
        options.append('helicopter')
    return options


questions = [
    {
        'type': 'list',
        'name': 'theme',
        'message': 'What do you want to do?',
        'choices': [
            'Order a pizza',
            'Make a reservation',
            Separator(),
            'Ask for opening hours',
            {
                'name': 'Contact support',
                'disabled': 'Unavailable at this time'
            },
            'Talk to the receptionist'
        ]
    },
    {
        'type': 'list',
        'name': 'size',
        'message': 'What size do you need?',
        'choices': ['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
        'filter': lambda val: val.lower()
    },
    {
        'type': 'list',
        'name': 'delivery',
        'message': 'Which vehicle you want to use for delivery?',
        'choices': get_delivery_options,
    },
]

answers = prompt(questions, style=custom_style_2)
pprint(answers)



def get_password_options(answers):
    return {
        'type': 'password',
        'message': 'Enter your Twitter password',
        'name': 'password'
    }



questions = [
    {
        'type': 'checkbox',
        'qmark': '😃',
        'message': 'Select toppings',
        'name': 'toppings',
        'choices': [ 
            Separator('= The Meats ='),
            {
                'name': 'Ham'
            },
            {
                'name': 'Ground Meat'
            },
            {
                'name': 'Bacon'
            },
            Separator('= The Cheeses ='),
            {
                'name': 'Mozzarella',
                'checked': True
            },
            {
                'name': 'Cheddar'
            },
            {
                'name': 'Parmesan'
            }
        ],
        'validate': lambda answer: 'You must choose at least one topping.' \
            if len(answer) == 0 else True
    }
]
questions = [
    {
        'type': 'confirm',
        'message': 'Do you want to continue?',
        'name': 'continue',
        'default': True,
    },
    {
        'type': 'confirm',
        'message': 'Do you want to exit?',
        'name': 'exit',
        'default': False,
    },
]


























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
                File.remove_local()
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
        # method = getattr(snarf, str(actionChoice))
        response = snarf.upload_prep(fileChoice, methodChoice=methodChoice, file=file, folderName=folderName, parent=parent)
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
    settings.remove_local()
    try:
        image = Google.download_file(image[0]).get("path")
    except Exception as e:
        settings.remove_local()
        try:
            image = Google.download_gallery(image[0]).get("path")
        except Exception as e:
            print("Error: Missing Image(s)")
            image = None
            # pass
    snarf.message(choice, message=message, image=image, price=price, username=username)

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
            snarf.give_trial(username)
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
        snarf.discount(user, depth=int(choice))
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
                snarf.discount(users[int(choice)-1], depth=int(choice))
                mainMenu()
            except (ValueError, IndexError):
                print(sys.exc_info()[0])
                print("Error: Incorrect Index")
                return mainMenu()
    snarf.discount(discountChoice)
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
                snarf.post()
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
            snarf.post(text=text)
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
    # def get_files_by_folder_id(folderID):
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
    # def get_files_by_folder_id(folderID):
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
    users = snarf.get_users()
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


#################################################################################################
#################################################################################################
#################################################################################################

































# this pattern needs to be turned into a function
# it needs to take one of the arrays of settings options and update the ones passed in

### Profile Settings
# profile settings need to know what is currently configured in your OnlyFans
# the driver needs to be updated with functionality that scans your settings
# 
### Profile Menu
def set_profile():
    showHeader()
    print(colorize("Set:",'menu'))
    def selectProfileSettings():
        global settingItems
        for item in settingsItems:
            print(colorize("[" + str(settingsItems.index(item)) + "] ", 'teal') + list(item)[0])
        while True:
            choice = input(">> ")
            try:
                if int(choice) < 0 or int(choice) >= len(settingsItems): raise ValueError
                if str(choice) == 0: return main()
                # selection points to the array of the next selection
                if str(settingsItems[int(choice)][1]) == "sync": return sync_profile()
                array = globals()[str(settingsItems[int(choice)][1])]
                print("array: "+str(array))
                response = selectProfileSetting(settingsItems[int(choice)][0],array)
                return main()
            except (ValueError, IndexError):
                print("Error: Incorrect Index")
            except Exception as e:
                settings.maybePrint(e)
                return main()
    def selectProfileSetting(label, setting):
        for item in setting:
            print(colorize("[" + str(setting.index(item)) + "] ", 'teal') + list(item)[0])
            while True:
                choice = input(">> ")
                try:
                    if int(choice) < 0 or int(choice) >= len(setting): raise ValueError
                    if str(choice) == 0: return set_profile()
                    # text, path, url, price, get, country, ip, or bool
                    settingChoice = list(setting[int(choice)])[0] # text
                    settingValue = list(setting[int(choice)])[1] # var name
                    settingType = list(setting[int(choice)])[2] # var type
                    if str(settingChoice) == "Sync":
                        return sync_to_profile_tab(label)
                    elif str(settingType) == "text":
                        print("> {}".format(settingValue))
                        settingValue = input("Enter text: ")
                    elif str(settingChoice) == "path":
                        settingValue = input("Enter the file path: ")
                    elif str(settingChoice) == "url":
                        settingValue = input("Enter the url: ")
                    elif str(settingChoice) == "price":
                        settingValue = input("Enter the new price ($): ")
                        ###
                        # price checking here
                        ###
                    elif str(settingChoice) == "country":
                        # enter list of countries as text
                        # verify against country list
                        pass
                    elif str(settingChoice) == "ip":
                        # enter ip range as text
                        # verify ip range text
                        pass
                    elif str(settingChoice) == "bool":
                        settingValueText = "Enabled"
                        if str(settingValue) == "False":
                            settingValueText = "Disabled"
                        print("> {}".format(settingValueText))
                        settingValue = input("Enabled|Disabled: ")
                    elif str(settingChoice) == "get":
                        print("> {}".format(settingValue))
                        return selectProfileSettings()
                    global UPDATED
                    UPDATED = settingChoice
                    global UPDATED_TO
                    UPDATED_TO = settingValue
                    setting[int(choice)][1] = settingValue
                    settings.update_profile_value(settingChoice, settingValue)
                    return set_profile()
                except (ValueError, IndexError):
                    print("Error: Incorrect Index")
                except Exception as e:
                    settings.maybePrint(e)
                    return set_profile()
    #
    selectProfileSettings()
    #

def sync_from_profile():
    # syncs profile settings w/ onlyfans
    pass

def sync_to_profile():
    # syncs profile settings to onlyfans
    pass

def sync_to_profile_tab(label):
    # syncs profile settings for the specificed tab to onlyfans
    pass
    





































### OnlySnarf Settings Menu
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
            elif str(settingChoice) == "Local":
                settingValue = input("Enter the file path: ")
            elif str(settingChoice) == "Text":
                settingValue = input("Enter the upload text: ")
            elif str(settingChoice) == "Mount Path":
                settingValue = input("Enter the mount path: ")
            elif str(settingChoice) == "Drive Path":
                settingValue = input("Enter the drive path (folderName/folderName/...): ")
            elif str(settingChoice) == "Image":
                settingValue = input("Enter the image path: ")
            elif str(settingChoice) == "Google Root":
                settingValue = input("Enter the Google root folder name: ")
            # elif str(settingChoice) == "Google: Drive Folders":
            #     settingValue = input("Enter the Google drive folders (separated by ',', no spaces): ")
            #     settingValue = settingValue.split(",")
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

######################################################

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
  
def exit():
    print("Shnarrf?")
    sys.exit(0)

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
            print(" - {} = {}/{}".format(setting[0],setting[1],settings.IMAGE_UPLOAD_LIMIT))
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

















######################################################

if __name__ == "__main__":
    try:
        main_other()
    except:
        # print(sys.exc_info()[0])
        print("Shhhhhnnnnnarf!")
    finally:
        exit()

def main_other():
    settings.initialize()
    if str(settings.VERSION) == "True": return settings.version_check()
    initialize()
    main()
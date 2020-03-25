#!/usr/bin/python3
# App Settings
import re
import sys
import os
import json
import pkg_resources
import shutil
import time
from OnlySnarf import colorize
from OnlySnarf.args import CONFIG as config

DEBUGGING = [
    ""
]

class Settings:
    def __init__(self):
        DISCOUNT = None
        MESSAGE = None
        POLL = None
        QUESTIONS = None
        last_updated = False

    # def __getitem__(self, key):
    #     return getattr(self, key)

    # def __setitem__(self, key, val):
    #     return setattr(self, key, val)

    ###################################################

    #####################
    ##### Functions #####
    #####################

    def debug_delay_check(self):
        if str(config.DEBUG) == "True" and str(config.DEBUG_DELAY) == "True":
            time.sleep(int(10))

    def print(self):
        if int(config.VERBOSE) == 1:
            print(colorize(text, "teal"))

    def maybe_print(self):
        if int(config.VERBOSE) == 2:
            print(colorize(text, "teal"))

    # update for verbosity
    def dev_print(self, text):
        if int(config.VERBOSE) == 3:
            if "successful" in str(text).lower():
                print(colorize(text, "green"))
            elif "failure" in str(text).lower():
                print(colorize(text, "red")) 
            else:
                print(colorize(text, "blue"))

    def header(self):
        if str(self.last_updated) != "False":
            print('\nUpdated: '+str(self.last_updated)+' -> '+str(self.last_updated))
        self.last_updated = False
        print('\r')


    def confirm(text):
        import PyInquirer
        questions = [
            {
                'type': 'confirm',
                'message': 'Is this correct? -> {}'.format(text),
                'name': 'covfefe',
                'default': True,
            }
        ]
        return PyInquirer.prompt(questions)["covfefe"]

    def prompt(text):
        import PyInquirer
        confirm = [
            {
                'type': 'confirm',
                'message': '{}?'.format(str(text).capitalize()),
                'name': 'confirm',
                'default': True,
            }
        ]
        return PyInquirer.prompt(confirm)["confirm"]

    def get_action(self):
        return getattr(config, "action")

    def get_discount(self):
        if self.DISCOUNT: return self.DISCOUNT
        amount = config.AMOUNT or config.DISCOuNT_MIN_AMOUNT
        months = config.MONTHS or config.DISCOUNT_MIN_MONTHS
        discount = {"amount":amount,"months":months}
        self.DISCOUNT = discount
        return discount

    def get_categories(self):
        return list(config.CATEGORIES_DEFAULT).extend(list(config.CATEGORIES))

    def get_keywords(self):
        keywords = config.KEYWORDS.split(",")
        keywords = [n.strip() for n in keywords]
        return keywords

    def get_message(self):
        if config.MESSAGE: return config.MESSAGE
        message = Message()
        message.get_post()
        config.MESSAGE = message
        return message

    def get_performers(self):
        performers = config.PERFORMERS.split(",")
        performers = [n.strip() for n in performers]
        return performers

    def get_poll(self):
        poll = None
        duration = config.DURATION or None
        questions = config.QUESTIONS or None
        poll = {"duration":duration,"questions":questions}
        if not duration or not questions: return None
        return poll

    def get_schedule(self):
        if str(config.SCHEDULE) != "None": return config.SCHEDULE
        if  str(config.DATE) != "None":
            if str(config.TIME) != "None":
                config.SCHEDULE = "{}:{}".format(config.DATE,config.TIME)
            else:
                config.SCHEDULE = "{}:{}".format(config.DATE,"00:00")
        return None

    def get_tags(self):
        tags = config.TAGS.split(",")
        tags = [n.strip() for n in tags]
        return tags

    def get_text(self):
        return config.text

    # comma separated string of usernames
    def get_users(self):
        users = config.USERS.split(",")
        users = [n.strip() for n in users]
        return users

    def get_user(self):
        user = User()
        setattr(user, "username", config.USER)
        return user

    def menu(self):
        print('Settings:')
        for key, value in var(self):
            if str(key).lower() in DEBUGGING and str(config.DEBUG) != "True": continue
            # limited ints
            # if certain int
            # if str(key) == "Image Limit":
            # print(" - {} = {}/{}".format(setting[0],setting[1],config.IMAGE_UPLOAD_LIMIT))



            print(" - {} = {}".format(key, value))

###########################################################################

SETTINGS = Settings()









































































































































    def update_value(self, variable, newValue):
        variable = str(variable).upper().replace(" ","_")
        try:
            # print("Updating: {} = {}".format(variable, newValue))
            setattr(self, variable, newValue)
            # print("Updated: {} = {}".format(variable, getattr(self, variable)))
        except Exception as e:
            maybePrint(e)

# move this behavior to user
    def update_profile_value(self, variable, newValue):
        variable = str(variable).upper().replace(" ","_")
        try:
            # print("Updating: {} = {}".format(variable, newValue))
            self.PROFILE.setattr(self, variable, newValue)
            # print("Updated: {} = {}".format(variable, getattr(self, variable)))
        except Exception as e:
            maybePrint(e)






UPDATED = False
UPDATED_TO = False
INITIALIZED = False
menuItems = []
actionItems = []
messageItems = []
fileItems = []
promotionItems = []
settingItems = []
methodItems = []





# Settings Menu
settingItems = [
    [ "Verbose", config.VERBOSE, ["True","False"],True],
    [ "Debug", config.DEBUG, ["True","False"],False],
    [ "Backup", config.BACKUP, ["True","False"],True],
    [ "Show Window", config.SHOW_WINDOW, ["True","False"],False],
    [ "Delete Google", config.DELETE_GOOGLE, ["True","False"],False],
    [ "Skip Delete", config.SKIP_DELETE, ["True","False"],False],
    [ "Tweeting", config.TWEETING, ["True","False"],True],
    [ "Image Limit", config.IMAGE_DOWNLOAD_LIMIT,None,True],
]
if str(config.VERBOSE) == "True":
    settingItems.append([ "Skip Backup", config.SKIP_BACKUP, ["True","False"],False])
    settingItems.append([ "Mount Path", config.MOUNT_PATH,None,False])
    settingItems.append([ "Drive Path", config.DRIVE_PATH,None,False])
    settingItems.append([ "Users Path", config.USERS_PATH,None,False])
    settingItems.append([ "Google Root", config.ROOT_FOLDER,None,False])
    settingItems.append([ "Drive Folder", config.DRIVE_FOLDERS,None,False])
    settingItems.append([ "Create Drive", config.CREATE_DRIVE, ["True","False"],False])
if str(config.DEBUG) == "True":
    settingItems.append([ "Skip Upload", config.SKIP_UPLOAD, ["True","False"],False])
    settingItems.append([ "Force Delete", config.FORCE_DELETE, ["True","False"],False])
    settingItems.append([ "Force Backup", config.FORCE_BACKUP, ["True","False"],False])
    settingItems.append([ "Force Upload", config.FORCE_UPLOAD, ["True","False"],False])
    settingItems.append([ "Skip Download", config.SKIP_DOWNLOAD, ["True","False"],False])
    settingItems.append([ "Image Max", config.IMAGE_UPLOAD_LIMIT,None,False])
    settingItems.append([ "Text", config.TEXT,None,False])
    settingItems.append([ "Local", config.INPUT,None,False])
    settingItems.append([ "Image", config.IMAGE,None,False])
    settingItems.append([ "Prefer Local", config.PREFER_LOCAL,["True","False"],True])
    # settingItems.append([ "Overwrite Local", config.OVERWRITE_LOCAL,["True","False"],True])
settingItems = sorted(settingItems)
settingItems.insert(0,[ "Back", "main"])

# Main Menu
menuItems = [
    [ "Actions", "action"],
    [ "Settings", "set_settings"]
]
if str(config.DEBUG) == "True":
    menuItems.append(["Profile", "profile"])
menuItems = sorted(menuItems)
menuItems.append([ "Exit", "exit"])

###
### Cron
###

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

accountSettingsItems = sorted([
    [ "Username", "username", "text" ],
    [ "Email", "email", "text" ],
    [ "Password", "password", "text" ]
])
accountSettingsItems.insert(0,[ "Back", "main"])

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

otherSettingsItems = sorted([
    [ "Live Server", "liveServer", "get" ],
    [ "Live Key", "liveServerKey", "get" ]
])
otherSettingsItems.insert(0,[ "Back", "main"])






### OnlySnarf Settings Menu
def set_settings():
    showHeader()
    print(colorize("Set:",'menu'))


    for item in settingItems:
        print(colorize("[" + str(settingItems.index(item)) + "] ", 'blue') + list(item)[0])


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
                




















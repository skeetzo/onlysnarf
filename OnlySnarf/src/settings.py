#!/usr/bin/python3
# App Settings
import re
import sys
import os
import json
import pkg_resources
import shutil
import time
from .colorize import colorize
from .args import CONFIG as config
import PyInquirer

DEBUGGING = [
    ""
]

CATEGORIES_DEFAULT = [
  "images",
  "galleries",
  "videos"
]
DEFAULT_MESSAGE = ":)"
DEFAULT_REFRESHER = "hi!"
DEFAULT_GREETING = "hi! thanks for subscribing :3 do you have any preferences?"
DISCOUNT_MAX_AMOUNT = 55
DISCOUNT_MIN_AMOUNT = 10
DISCOUNT_MAX_MONTHS = 7
DISCOUNT_MIN_MONTHS = 1
DURATION_ALLOWED = ["1","3","7","30","99","no limit"]
EXPIRATION_ALLOWED = ["1","3","7","30","99","no limit"]
IMAGE_DOWNLOAD_LIMIT = 6
IMAGE_UPLOAD_LIMIT = 20
IMAGE_UPLOAD_LIMIT_MESSAGES = 5
MESSAGE_CHOICES = ["all", "recent", "favorite"]
PRICE_MINIMUM = 3
UPLOAD_MAX_DURATION = 12 # 2 hours

class Settings:
    last_updated = False
    MESSAGE = None

    def __init__():
        pass

    #####################
    ##### Functions #####
    #####################

    def confirm(text):
        if list(text) == []: return False
        if str(text) == "": return False
        if not Settings.is_confirm(): return True
        questions = [
            {
                'type': 'confirm',
                'message': 'Is this correct? -> {}'.format(text),
                'name': 'covfefe',
                'default': True,
            }
        ]
        return PyInquirer.prompt(questions)["covfefe"]

    def debug_delay_check():
        if Settings.is_debug() and Settings.is_debug_delay():
            time.sleep(int(10))

    def print(text):
        if int(config.get("VERBOSE")) == 1:
            print(colorize(text, "teal"))

    def maybe_print(text):
        if int(config.get("VERBOSE")) == 2:
            print(colorize(text, "teal"))

    # update for verbosity
    def dev_print(text):
        if int(config.get("VERBOSE")) == 3:
            if "successful" in str(text).lower():
                print(colorize(text, "green"))
            elif "failure" in str(text).lower():
                print(colorize(text, "red")) 
            else:
                print(colorize(text, "blue"))

    def header():
        if str(Settings.last_updated) != "False":
            print('\nUpdated: '+str(Settings.last_updated)+' -> '+str(Settings.last_updated))
        Settings.last_updated = False
        print('\r')

    # Gets

    def get_action():
        return config.get("ACTION")

    def get_discount():
        amount = config.get("AMOUNT") or config.get("DISCOUNT_MIN_AMOUNT")
        months = config.get("MONTHS") or config.get("DISCOUNT_MIN_MONTHS")
        discount = {"amount":amount,"months":months}
        return discount

    def get_category():
        return config.get("CATEGORY") or ""

    def get_categories():
        return list(CATEGORIES_DEFAULT).extend(list(config.get("CATEGORIES")))

    def get_price_minimum():
        return PRICE_MINIMUM or 0

    def get_date():
        return config.get("DATE") or ""

    def get_default_greeting():
        return DEFAULT_GREETING or ""

    def get_default_refresher():
        return DEFAULT_REFRESHER or ""
        
    def get_discount_max_amount():
        return DISCOUNT_MAX_AMOUNT or 0
        
    def get_discount_min_amount():
        return DISCOUNT_MIN_AMOUNT or 0
        
    def get_discount_max_months():
        return DISCOUNT_MAX_MONTHS or 0
        
    def get_discount_min_months():
        return DISCOUNT_MIN_MONTHS or 0

    def get_download_max():
        return config.get("DOWNLOAD_MAX") or IMAGE_DOWNLOAD_LIMIT
        
    def get_drive_ignore():
        return config.get("NOTKEYWORDS") or ""
        
    def get_drive_keyword():
        return config.get("BYKEYWORDS") or ""
        
    def get_duration():
        return config.get("DURATION") or 0
        
    def get_duration_allowed():
        return DURATION_ALLOWED or []
        
    def get_expires():
        return config.get("EXPIRATION") or 0
        
    def get_expiration_allowed():
        return EXPIRATION_ALLOWED or []

    def get_input():
        return config.get("INPUT") or ""

    def get_keywords():
        keywords = config.get("KEYWORDS") or []
        keywords = [n.strip() for n in keywords]
        return keywords
        
    def get_message():
        if Settings.MESSAGE: return Settings.MESSAGE
        from .message import Message
        message = Message()
        message.get_post()
        Settings.MESSAGE = message
        return message

    def get_message_choices():
        return MESSAGE_CHOICES

    def get_mount_path():
        return config["MOUNT_PATH"] or ""

    def get_performers():
        performers = config.get("PERFORMERS") or []
        performers = [n.strip() for n in performers]
        return performers

    def get_poll():
        duration = Settings.get_duration()
        questions = Settings.get_questions()
        if duration == "" or len(questions) == 0: return None
        return {"duration":duration,"questions":questions}

    def get_promotion():
        return None
        # if Settings.PROMOTION: return Settings.PROMOTION
        # from .promotion import Promotion
        # promotion = Promotion()
        # promotion.get()
        # Settings.PROMOTION = promotion
        # return promotion

    def get_recent_user_count():
        return config.get("RECENT_USERS_COUNT") or 0

    def get_password():
        return config.get("PASSWORD") or ""

    def get_download_path():
        return config.get("DOWNLOAD_PATH") or ""

    def get_drive_path():
        return config.get("DRIVE_PATH") or ""

    def get_users_path():
        return config.get("USERS_PATH") or ""

    def get_google_path():
        print(config.get("GOOGLE_PATH"))
        return config.get("GOOGLE_PATH") or ""

    def get_secret_path():
        return config.get("CLIENT_SECRET") or ""

    def get_schedule():
        if str(config.get("SCHEDULE")) != "None": return config.get("SCHEDULE")
        if  Settings.get_date() != "":
            if str(Settings.get_time()) != "":
                config.set("SCHEDULE", "{}:{}".format(Settings.get_date(), Settings.get_time()))
            else:
                config.set("SCHEDULE", "{}:{}".format(Settings.get_date(), "00:00"))
        return config.get("SCHEDULE")

    def get_tags():
        tags = config.get("TAGS") or []
        tags = [n.strip() for n in tags]
        return tags

    def get_text():
        return config.get("text")

    def get_time():
        return config.get("TIME") or ""

    def get_title():
        return config.get("TITLE") or ""
        
    def get_skipped_users():
        return config.get("SKIPPED_USERS") or []
        
    def get_questions():
        return config.get("QUESTIONS") or []
        
    def get_upload_max():
        return config.get("UPLOAD_MAX") or IMAGE_UPLOAD_LIMIT
        
    def get_upload_max_messages():
        return config.get("UPLOAD_LIMIT_MESSAGES") or 0
        
    def get_upload_max_duration():
        return config.get("UPLOAD_MAX_DURATION") or 12 # 2 hours

    # comma separated string of usernames
    def get_users():
        users = config.get("USERS") or []
        users = [n.strip() for n in users]
        return users

    def get_user():
        from .user import User
        user = User({})
        setattr(user, "username", config.get("USER"))
        return user

    def get_username():
        return config.get("USERNAME") or ""

    def get_users_favorite():
        return config.get("USERS_FAVORITE") or []
        
    def get_verbosity():
        return config.get("VERBOSE") or 0

    # Bools

    def is_confirm():
        return config.get("CONFIRM") or True

    def is_debug():
        return config.get("DEBUG") or False

    def is_debug_delay():
        return config.get("DEBUG_DELAY") or False

    def is_prefer_local():
        return config.get("PREFER_LOCAL") or False
        
    def is_save_users():
        return config.get("SAVE_USERS") or False
        
    def is_reduce():
        return config.get("ENABLE_REDUCE") or False
    
    def is_show_window():
        return config.get("SHOW") or False

    def is_split():
        return config.get("ENABLE_SPLIT") or False
        
    def is_trim():
        return config.get("ENABLE_TRIM") or False
        
    def is_tweeting():
        return config.get("TWEETING") or False
        
    def is_backup():
        return config.get("BACKUP") or False
        
    def is_skip_download():
        return config.get("SKIP_DOWNLOAD") or False
        
    def is_skip_upload():
        return config.get("SKIP_UPLOAD") or False

        ### OnlySnarf Settings Menu
    def menu():
        print('Settings')
        question = {
            'type': 'list',
            'name': 'choice',
            'message': 'Set:',
            'choices': [key.replace("_"," ").title() for key in config.keys()],
            'filter': lambda val: val.lower()
        }
        answer = prompt(question)["choice"]
        if not Settings.confirm(answer): return
        Settings.set_setting(answer)

    def prompt(text):
        question = {
            'type': 'confirm',
            'message': '{}?'.format(str(text).capitalize()),
            'name': 'confirm',
            'default': True,
        }
        return PyInquirer.prompt(question)["confirm"]

    def prompt_username():
        question = {
            'type': 'input',
            'message': 'Twitter username:',
            'name': 'username'
        }
        username = PyInquirer.prompt(question)["username"]
        Settings.set_username(username)
        return username

    def prompt_password():
        question = {
            'type': 'password',
            'message': 'Twitter password:',
            'name': 'password'
        }
        pw = PyInquirer.prompt(question)["password"]
        Settings.set_password(pw)
        return pw

    def set_confirm(value):
        config["CONFIRM"] = bool(value)

    def set_username(username):
        config["USERNAME"] = str(username)

    def set_password(password):
        config["PASSWORD"] = str(password)

    def set_setting(key):
        key = key.replace("_"," ").title()
        question = {
            'type': 'input',
            'name': 'key',
            'message': key,
            'default': value
        }
        if isinstance(value, bool):
            question = {
                'type': 'confirm',
                'name': 'key',
                'message': key,
                'default': value
            }
        answer = prompt(question)
        setattr(config, key, answer["key"])


###########################################################################



#     def update_value(self, variable, newValue):
#         variable = str(variable).upper().replace(" ","_")
#         try:
#             # print("Updating: {} = {}".format(variable, newValue))
#             setattr(self, variable, newValue)
#             # print("Updated: {} = {}".format(variable, getattr(self, variable)))
#         except Exception as e:
#             maybePrint(e)

# # move this behavior to user
#     def update_profile_value(self, variable, newValue):
#         variable = str(variable).upper().replace(" ","_")
#         try:
#             # print("Updating: {} = {}".format(variable, newValue))
#             Settings.PROFILE.setattr(self, variable, newValue)
#             # print("Updated: {} = {}".format(variable, getattr(self, variable)))
#         except Exception as e:
#             maybePrint(e)





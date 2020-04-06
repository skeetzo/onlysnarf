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
DURATION_ALLOWED = [1,3,7,30,99]
EXPIRATION_ALLOWED = [1,3,7,30,99]
IMAGE_DOWNLOAD_LIMIT = 6
IMAGE_UPLOAD_LIMIT = 20
IMAGE_UPLOAD_LIMIT_MESSAGES = 5
MESSAGE_CHOICES = ["all", "recent", "favorite"]
PRICE_MINIMUM = 3
UPLOAD_MAX_DURATION = 12 # 2 hours

class Settings:
    last_updated = False
    CONFIRM = True
    DISCOUNT = None
    FILES = None
    PROMPT = True
    MESSAGE = None
    POLL = None
    PROFILE = None
    PROMOTION = None
    SCHEDULE = None

    def __init__():
        pass

    #####################
    ##### Functions #####
    #####################

    def confirm(text):
        try:
            if text == None: return False
            if list(text) == []: return False
            if str(text) == "": return False
            if not Settings.CONFIRM: return True
        except: pass
        questions = [
            {
                'type': 'confirm',
                'message': 'Is this correct? -> {}'.format(text),
                'name': 'confirm',
                'default': True,
            }
        ]
        return PyInquirer.prompt(questions)["confirm"]

    def debug_delay_check():
        if Settings.is_debug() and Settings.is_debug_delay():
            time.sleep(int(10))

    def print(text):
        if int(config["VERBOSE"]) >= 1:
            print(colorize(text, "teal"))

    def maybe_print(text):
        if int(config["VERBOSE"]) >= 2:
            print(colorize(text, "teal"))

    # update for verbosity
    def dev_print(text):
        if int(config["VERBOSE"]) >= 3:
            if "successful" in str(text).lower():
                print(colorize(text, "green"))
            elif "failure" in str(text).lower():
                print(colorize(text, "red")) 
            else:
                print(colorize(text, "blue"))

    def header():
        if Settings.last_updated:
            print("Updated: {} = {}".format(Settings.last_updated, config[Settings.last_updated.replace(" ","_").upper()]))
            print('\r')
        Settings.last_updated = None

    # Gets

    def get_action():
        return config["ACTION"]

    def get_amount():
        return config["AMOUNT"]

    def get_months():
        return config["MONTHS"]

    def get_discount():
        if Settings.DISCOUNT: return Settings.DISCOUNT
        from .classes import Discount
        discount = Discount()
        discount.get()
        Settings.DISCOUNT = discount
        return discount

    def get_category():
        cat = config["CATEGORY"]
        if str(cat) == "image": cat = "images"
        if str(cat) == "gallery": cat = "galleries"
        if str(cat) == "video": cat = "videos"
        if str(cat) == "performer": cat = "performers"
        return cat or None

    def get_categories():
        cats = []
        cats.extend(list(CATEGORIES_DEFAULT))
        cats.extend(list(config["CATEGORIES"]))
        return list(set(cats)).sort()

    def get_price():
        return config["PRICE"] or ""

    def get_price_minimum():
        return PRICE_MINIMUM or 0

    def get_date():
        return config["DATE"] or None

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
        return config["DOWNLOAD_MAX"] or IMAGE_DOWNLOAD_LIMIT
        
    def get_drive_ignore():
        return config["NOTKEYWORD"] or None
        
    def get_drive_keyword():
        return config["BYKEYWORD"] or None
        
    def get_duration():
        return config["DURATION"] or 0
        
    def get_duration_allowed():
        return DURATION_ALLOWED or []
        
    def get_expiration():
        return config["EXPIRATION"] or 0
        
    def get_expiration_allowed():
        return EXPIRATION_ALLOWED or []

    def get_input():
        return config["INPUT"] or []

    def get_input_as_files():
        if Settings.FILES: return Settings.FILES
        from .file import File
        files = []
        for file_path in config["INPUT"]:
            file = File()
            files.append(file)
        Settings.FILES = files
        return files

    def get_keywords():
        keywords = config["KEYWORDS"] or []
        keywords = [n.strip() for n in keywords]
        return keywords

    def get_limit():
        return config["LIMIT"] or 1
        
    def get_message():
        if Settings.MESSAGE: return Settings.MESSAGE
        from .message import Message
        message = Message()
        # message.get_post()
        Settings.MESSAGE = message
        return message

    def get_message_choices():
        return MESSAGE_CHOICES

    def get_mount_path():
        return config["MOUNT_PATH"] or "/opt/onlysnarf"

    def get_performers():
        performers = config["PERFORMERS"] or []
        performers = [n.strip() for n in performers]
        return performers

    def get_profile():
        if Settings.PROFILE: return Settings.PROFILE
        from .profile import Profile
        profile = Profile()
        profile.get()
        Settings.PROFILE = profile
        return profile

    def get_poll():
        if Settings.POLL: return Settings.POLL
        from .classes import Poll
        poll = Poll()
        poll.get()
        if not poll.check(): return None
        Settings.POLL = poll
        return poll

    def get_promotion():
        if Settings.PROMOTION: return Settings.PROMOTION
        from .classes import Promotion
        promotion = Promotion()
        promotion.get()
        Settings.PROMOTION = promotion
        return promotion

    def get_recent_user_count():
        return config["RECENT_USERS_COUNT"] or 0

    def get_password():
        return config["PASSWORD"] or ""

    def get_download_path():
        return config["DOWNLOAD_PATH"] or ""

    def get_drive_path():
        return config["DRIVE_PATH"] or "root"

    def get_drive_root():
        return config["DRIVE_ROOT"] or "OnlySnarf"

    def get_users_path():
        return config["USERS_PATH"] or ""

    def get_google_path():
        return config["GOOGLE_PATH"] or ""

    def get_secret_path():
        return config["CLIENT_SECRET"] or ""

    def get_Schedule():
        if Settings.SCHEDULE: return Settings.SCHEDULE
        from .classes import Schedule
        schedule = Schedule()
        schedule.get()
        if not schedule.check(): return None
        Settings.SCHEDULE = schedule
        return schedule

    def get_schedule():
        if str(config["SCHEDULE"]) != "None": return config["SCHEDULE"]
        if Settings.get_date():
            if Settings.get_time():
                config["SCHEDULE"] = "{} {}".format(Settings.get_date(), Settings.get_time())
            else:
                config["SCHEDULE"] = "{}".format(Settings.get_date())
        return config["SCHEDULE"]

    def get_tags():
        tags = config["TAGS"] or []
        tags = [n.strip() for n in tags]
        return tags

    def get_text():
        return config["TEXT"] or None

    def get_time():
        return config["TIME"] or None

    def get_title():
        return config["TITLE"] or None
        
    def get_skipped_users():
        return config["SKIPPED_USERS"] or []
        
    def get_questions():
        return config["QUESTIONS"] or []
        
    def get_upload_max():
        return config["UPLOAD_MAX"] or IMAGE_UPLOAD_LIMIT
        
    def get_upload_max_messages():
        return config["UPLOAD_MAX_MESSAGES"] or 0
        
    def get_upload_max_duration():
        return config["UPLOAD_MAX_DURATION"] or 12 # 2 hours

    # comma separated string of usernames
    def get_users():
        users = config["USERS"] or []
        users = [n.strip() for n in users]
        from .user import User
        users_ = []
        for user in users:
            # user = User({})
            user = User({"username":config["USER"]})
            # setattr(user, "username", config["USER"])
            users_.append(user)
        return users_

    def get_user():
        if not config["USER"]: return None
        from .user import User
        user = User({"username":config["USER"]})
        # setattr(user, "username", config["USER"])
        return user

    def get_username():
        return config["USERNAME"] or ""

    def get_users_favorite():
        return config["USERS_FAVORITE"] or []
        
    def get_verbosity():
        return config["VERBOSE"] or 0

    # Bools

    def is_confirm():
        return Settings.CONFIRM or False

    def is_prompt():
        return Settings.PROMPT or False

    def is_create_drive():
        return config["CREATE_DRIVE"] or False

    def is_debug():
        return config["DEBUG"] or False

    def is_debug_delay():
        return config["DEBUG_DELAY"] or False

    def is_delete():
        return config["DELETE_GOOGLE"] or False

    def is_prefer_local():
        return config["PREFER_LOCAL"] or False
        
    def is_save_users():
        return config["SAVE_USERS"] or False
        
    def is_reduce():
        return config["ENABLE_REDUCE"] or False
    
    def is_show_window():
        return config["SHOW"] or False

    def is_split():
        return config["ENABLE_SPLIT"] or False
        
    def is_trim():
        return config["ENABLE_TRIM"] or False
        
    def is_tweeting():
        return config["TWEETING"] or False
        
    def is_backup():
        return config["BACKUP"] or False
        
    def is_skip_download():
        return config["SKIP_DOWNLOAD"] or False
        
    def is_skip_upload():
        return config["SKIP_UPLOAD"] or False

        ### OnlySnarf Settings Menu
    def menu():
        skipList = ["action", "amount", "category", "categories", "cron", "input", "messages", "posts", "date", "duration", "expiration", "keywords", "limit", "months", "bykeyword", "notkeyword", "price", "config_path", "google_path", "client_secret", "questions", "schedule", "skipped_users", "tags", "text", "time", "title", "user", "users", "username", "password", "users_favorite"]
        print('Settings')
        keys = [key.replace("_"," ").title() for key in config.keys() if key.lower() not in skipList and "categories" not in str(key).lower() and "messages" not in str(key).lower()]
        keys.insert(0, "Back")
        question = {
            'type': 'list',
            'name': 'choice',
            'message': 'Set:',
            'choices': keys,
            'filter': lambda val: val.lower()
        }
        answer = PyInquirer.prompt(question)["choice"]
        if str(answer).lower() == "back": return
        answer = answer.replace(" ", "_").upper()
        Settings.set_setting(answer)

    def prompt(text):
        if list(text) == []: return False
        if str(text) == "": return False
        if not Settings.PROMPT: return False
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

    def select_category():
        question = {
            'type': 'list',
            'message': 'Category?',
            'name': 'category',
            'choices': Settings.get_categories(),
        }
        cat = PyInquirer.prompt(question)["category"]
        if not Settings.confirm(cat): return Settings.select_category()
        return cat

    def set_confirm(value):
        Settings.CONFIRM = bool(value)

    def set_username(username):
        config["USERNAME"] = str(username)

    def set_password(password):
        config["PASSWORD"] = str(password)

    def set_prefer_local(buul):
        config["PREFER_LOCAL"] = bool(buul)

    def set_prompt(value):
        Settings.PROMPT = bool(value)

    def set_setting(key):
        value = config[key]
        key = key.replace("_"," ").title()
        print("Current: {}".format(value))
        if str(value) == "True" or str(value) == "False":
            question = {
                'type': 'confirm',
                'name': 'setting',
                'message': "Toggle value?",
                # 'default': int(value)
            }
            answer = PyInquirer.prompt(question)["setting"]
            if not answer: return Settings.menu()
            if value: config[key.upper()] = False
            else: config[key.upper()] = True
        else:
            question = {
                'type': 'input',
                'name': 'setting',
                'message': "New value:",
                # 'default': int(value)
            }
            answer = PyInquirer.prompt(question)["setting"]
            if not Settings.confirm(answer): return Settings.menu()
            config[key.upper()] = answer
        Settings.last_updated = key
        # return Settings.menu()

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





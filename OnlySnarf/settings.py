#!/usr/bin/python3
# App Settings
import re
import sys
import os
import json
import pkg_resources
import shutil
import time

class Settings:
    def __init__(self):
        pass

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, val):
        return setattr(self, key, val)

    def initialize(self):
        print("Initializing Settings")
        try:
            if self.INITIALIZED:
                print("Already Initialized, Skipping")
                return
        except:
            self.INITIALIZED = False
        ##
        # -action
        # the action to be performed
        self.ACTION = "upload"
        ##
        # -amount
        # action: discount
        # the amount to discount a user by
        self.AMOUNT = 0
        ##
        # -backup
        # backup uploaded content to "posted" folder
        self.BACKUP = False
        ##
        # -bykeyword
        # the keyword to find in folder selection
        self.BYKEYWORD = None
        ##
        # -create-drive 
        # creates missing OnlySnarf folders in Google Drive
        self.CREATE_DRIVE = False
        ##
        # -cron
        # determines whether script running is a cronjob
        self.CRON = False
        ##
        # -cron-user
        # the user to run OnlySnarf as
        self.CRON_USER = "root"
        ##
        # -date
        # date in MM-DD-YYYY:HH:MM 
        self.DATE = None
        ##
        # -debug
        # debugging - skips uploading and deleting unless otherwise forced
        self.DEBUG = False
        ##
        # -debug-force
        # forces expiration and poll modals to save instead of cancel when debugging
        self.DEBUG_FORCE = False
        ##
        # -debug-delay
        # user message delay
        self.DEBUG_DELAY = False
        # -debug-delay-amount
        # duration in seconds
        self.DEBUG_DELAY_AMOUNT = 10
        ##
        # -delete-google
        # delete uploaded content
        self.DELETE_GOOGLE = False
        ##
        # default message for debugging
        self.DEFAULT_MESSAGE = ":)"
        ##
        # default price for user messages
        self.DEFAULT_PRICE = "10.00"
        ##
        # default user greeting
        self.DEFAULT_GREETING = "hi! thanks for subscribing :3 do you have any preferences?"
        ##
        ##
        #
        self.DISCOuNT_MAX_AMOUNT = 55
        self.DISCOuNT_MIN_AMOUNT = 10
        self.DISCOUNT_MAX_MONTHS = 7
        self.DISCOUNT_MIN_MONTHS = 1
        self.DISCOUNT = None
        ##
        # download path
        self.DOWNLOAD_PATH = "/opt/apps/onlysnarf/downloads"
        ##
        # configurable w/ profile.conf
        # OnlySnarf Drive folder list
        self.DRIVE_FOLDERS = [
            "images",
            "galleries",
            "performers",
            "scenes",
            "videos"
        ]
        ##
        # -duration
        # poll or post duration
        self.DURATION = None
        self.DURATION_ALLOWED = ["1","3","7","30","99","no limit"]
        self.EXPIRATION_ALLOWED = ["1","3","7","30","99","no limit"]
        ##
        # -exit
        # exit upon each action
        self.EXIT = True
        ##
        # -expires
        # date of post or poll expiration
        self.EXPIRES = None
        ##
        # -force-backup
        # force Google backup
        self.FORCE_BACKUP = False
        ##
        # -force-delete
        # force Google file deletion upon upload
        self.FORCE_DELETE = False
        ##
        # -force-reduce
        # force mp4 reduction
        self.FORCE_REDUCTION = False
        ##
        # -force-upload
        # ignore upload max wait
        self.FORCE_UPLOAD = False
        ##
        # -input
        # path to local file(s) to upload
        self.INPUT = None
        ##
        # -image
        # path to local image to use for message or upload
        self.IMAGE = None
        ##
        # -image-download-limit
        # maximum number of images to download
        self.IMAGE_DOWNLOAD_LIMIT = 6
        ##
        # -image-upload-limit
        # maximum number of images that can be uploaded
        self.IMAGE_UPLOAD_LIMIT = 20
        ##
        # - image-upload-limit-messages
        # maximum number of images that can be uploaded in a message
        self.IMAGE_UPLOAD_LIMIT_MESSAGES = 5
        ##
        # -keywords
        # keywords to # in post
        self.KEYWORDS = []
        ##
        # -manual
        # posting requires clicking open window
        # self.MANUAL = False # removed
        ##
        # available mass messaging choices
        self.MESSAGE_CHOICES = ["all", "recent", "favorite"]
        ##
        # -months
        # action: discount
        # the number of months to discount for
        self.MONTHS = 0
        ##
        # -method
        # random | input
        self.METHOD = "random"
        ##
        # -mount-path
        # the mounth path for a local directory of OnlyFans config files
        self.MOUNT_PATH = None
        ##
        # -notkeyword
        # the keyword to skip in folder selection
        self.NOTKEYWORD = None
        ##
        # -overwrite-local
        # self.OVERWRITE_LOCAL = False
        ##
        # -password
        # the password for the OnlyFans / Twitter
        self.PASSWORD = None
        ##
        # -performers
        # list of performers to tag in post
        self.PERFORMERS = []
        # -prefer-local
        # prefers local cache over refreshing first call
        self.PREFER_LOCAL = False
        ##
        # -price
        # action: message
        # the price to be set in a message
        self.PRICE = 0
        self.PRICE_MINIMUM = 3
        ##
        # profile settings for the account
        self.PROFILE = None

        ###
        ### PATHS ###
        # -drive-path
        # the folder path within Google Drive for OnlySnarf's root folder
        self.DRIVE_PATH = None
        # -config-path
        # the path to the config.conf file
        self.CONFIG_PATH = "/etc/onlysnarf/config.conf"
        # -google-path
        # the path to the google_creds.txt
        self.GOOGLE_PATH = "google_creds.txt"
        # the path to the client_secret.json
        self.SECRET_PATH = "client_secret.json"
        # -user-path
        # the path to the users.json file
        self.USERS_PATH = "users.json"
        ###
        ##
        # -questions
        # poll questions
        self.QUESTIONS = []
        ###
        # the maximum number of recent users
        self.RECENT_USER_COUNT = 3
        ##
        # enables file reduction
        self.REDUCE = False
        ##
        # enables file repair (buggy)
        self.REPAIR = False
        ##
        # can be set in profile.conf
        # root Google drive folder
        self.ROOT_FOLDER = "OnlySnarf"
        ##
        # -save-users
        # saves OnlyFans users upon exit
        self.SAVE_USERS = False
        ##
        # -schedule
        # 
        self.SCHEDULE = None
        ##
        # -skip-backup
        # skips file backup if enabled by .conf
        self.SKIP_BACKUP = False
        ##
        # -skip-delete
        # skip local file deletion before and after upload
        self.SKIP_DELETE = False
        ##
        # -skip-delete-google
        # skips Google file deltion if enabled by .conf
        self.SKIP_DELETE_GOOGLE = False
        ##
        # -skip-download
        self.SKIP_DOWNLOAD = False
        ##
        # -skip-reduce
        # skip mp4 reducing
        self.SKIP_REDUCE = False
        ##
        # -skip-repair
        # skip mp4 repairs
        self.SKIP_REPAIR = False
        ##
        # -skip-upload
        # skips file upload
        self.SKIP_UPLOAD = False
        ##
        # list of users to skip
        self.SKIP_USERS = []
        ##
        # -show 
        # shows window
        self.SHOW_WINDOW = False
        ##
        # -tags
        # @[tag]
        self.TAGS = []
        ##
        # -text
        # text for message or upload
        self.TEXT = None
        ##
        # -time
        # time in HH:MM
        self.TIME = None
        ##
        # fixes thumbnail preview
        self.THUMBNAILING_PREVIEW = False
        ##
        # -type
        # the type of upload
        self.TYPE = None
        ##
        # -tweet
        # enabled tweeting
        self.TWEETING = False
        ##
        # -upload-max
        # the max number of 10 minute intervals to upload for
        self.UPLOAD_MAX_DURATION = 12 # 2 hours
        ##
        # -user
        # the user to target
        self.USER = None
        ##
        # -users
        # the users to target
        self.USERS = []
        ##
        # user id found in OnlyFans
        self.USER_ID = None
        ##
        # -users-favorite
        # list of favorited users
        self.USERS_FAVORITE = []
        ##
        # -username
        # the OnlyFans / Twitter username to use
        self.USERNAME = None
        ##
        # -verbose
        # more output
        self.VERBOSE = False
        # shows devPrint success|failure
        self.VERBOSER = False
        # shows devPrint all
        self.VERBOSEST = False
        ##
        # -version
        # prints version
        self.VERSION = False
        ##
        # not currently implemented
        # custom repair option for shitty gopro videos
        self.WORKING_VIDEO = "video.mp4"
        # config file
        if os.path.exists(self.CONFIG_PATH):
            readConf(self, self.CONFIG_PATH)
        elif os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.conf")):
            readConf(self, os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.conf"))
        i = 0
        while i < len(sys.argv):
            sys.argv[i] = sys.argv[i][1:] # remove - in front
            # truths set the variable True when provided
            truths_ = ["VERBOSEST","VERSION","VERBOSER","DEBUG_FORCE","REPAIR","REDUCE","SKIP_DELETE_GOOGLE","SKIP_BACKUP","BACKUP","CREATE_DRIVE","DEBUG","DEBUG_DELAY","DELETE_GOOGLE","FORCE_DELETE","FORCE_UPLOAD","FORCE_REDUCTION","PREFER_LOCAL","SAVE_USERS","SHOW_WINDOW","SKIP_DELETE","SKIP_DOWNLOAD","SKIP_REDUCE","SKIP_REPAIR","SKIP_UPLOAD","TWEETING","VERBOSE","THUMBNAILING_PREVIEW"]
            # falses set the variable False when provided
            falses_ = ["EXIT"]
            # nexts set the variable to the next provided argument input
            nexts_ = ["TAGS","USERS","DOWNLOAD_PATH","IMAGE_UPLOAD_LIMIT_MESSAGES","UPLOAD_MAX_DURATION","NOTKEYWORD","BYKEYWORD","PERFORMERS","KEYWORDS","DURATION","QUESTIONS","DATE","TIME","SCHEDULE","EXPIRES","USERS_FAVORITE","CRON","METHOD","PRICE","AMOUNT","MONTHS","ACTION","CRON_USER","INPUT","IMAGE","IMAGE_DOWNLOAD_LIMIT","IMAGE_UPLOAD_LIMIT","TYPE","TEXT","USER","DRIVE_PATH","GOOGLE_PATH","MOUNT_PATH","USERS_PATH","USERNAME","PASSWORD","USER_ID"]
            j = 0
            while j < len(truths_):
                if str(truths_[j]).upper() == str(sys.argv[i]).upper().replace("-","_"):
                    # self.set(truths_[j], True)
                    self[truths_[j]] = True
                j = j + 1
            j = 0
            while j < len(falses_):
                if str(falses_[j]).upper() == str(sys.argv[i]).upper().replace("-","_"):
                    # self.set(falses_[j], False)
                    self[falses_[j]] = False
                j = j + 1
            j = 0
            while j < len(nexts_):
                if str(nexts_[j]).upper() == str(sys.argv[i]).upper().replace("-","_"):
                    # self.set(nexts_[j], sys.argv[i+1])  
                    try:
                        self[nexts_[j]] = sys.argv[i+1]
                    except Exception as e:
                        # print(e)
                        pass
                j += 1
            i += 1
        if self.MOUNT_PATH is not None:
            self.CONFIG_PATH = os.path.join(self.MOUNT_PATH, self.CONFIG_PATH)
            self.SECRET_PATH = os.path.join(self.MOUNT_PATH, self.SECRET_PATH)
            self.GOOGLE_PATH = os.path.join(self.MOUNT_PATH, self.GOOGLE_PATH)
            self.USERS_PATH = os.path.join(self.MOUNT_PATH, self.USERS_PATH)
            self.WORKING_VIDEO = os.path.join(self.MOUNT_PATH, self.WORKING_VIDEO)
        else:
            self.CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.CONFIG_PATH)
            self.SECRET_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.SECRET_PATH)
            self.GOOGLE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.GOOGLE_PATH)
            self.USERS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.USERS_PATH)
            self.WORKING_VIDEO = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.WORKING_VIDEO)
        self.INITIALIZED = True
        # print("Settings Initialized")
    ###################################################

    #####################
    ##### Functions #####
    #####################

    def debug_delay_check(self):
        if str(self.DEBUG) == "True" and str(self.DEBUG_DELAY) == "True":
            time.sleep(int(self.DEBUG_DELAY_AMOUNT))

    def devPrint(self, text):
        if str(self.VERBOSER) == "True":
            if "Successful" in str(text):
                print(colorize(text, "green"))
            elif "Failure" in str(text):
                print(colorize(text, "red")) 
            elif str(self.VERBOSEST) == "True":
                print(colorize(text, "blue"))

    def get_action(self):
        action = None
        if str(settings.ACTION) != "discount":
            action = None
        elif str(settings.ACTION) != "post":
            action = []
        elif str(settings.ACTION) != "message":
            action = []
        else:

    def get_discount(self):
        if settings.DISCOUNT: return settings.DISCOUNT
        amount = settings.AMOUNT or settings.DISCOuNT_MIN_AMOUNT
        months = settings.MONTHS or settings.DISCOUNT_MIN_MONTHS
        discount = {"amount":amount,"months":months}
        settings.DISCOUNT = discount
        return discount

    def get_message(self):
        if settings.MESSAGE: return settings.MESSAGE
        message = Message()
        message.get_post()
        settings.MESSAGE = message
        return message

    def get_keywords(self):
        keywords = []
        if str(settings.KEYWORDS) == "None":
            keywords = []
        elif str(settings.KEYWORDS) == "[]":
            keywords = []
        elif str(settings.KEYWORDS) == " ":
            keywords = []
        else:
            keywords = settings.KEYWORDS.split(",")
            keywords = [n.strip() for n in keywords]
        return keywords

    def get_performers(self):
        performers = []
        if str(settings.PERFORMERS) == "None":
            performers = []
        elif str(settings.PERFORMERS) == "[]":
            performers = []
        elif str(settings.PERFORMERS) == " ":
            performers = []
        else:
            performers = settings.PERFORMERS.split(",")
            performers = [n.strip() for n in performers]
        return performers

    def get_tags(self):
        tags = []
        if str(settings.TAGS) == "None":
            tags = []
        elif str(settings.TAGS) == "[]":
            tags = []
        elif str(settings.TAGS) == " ":
            tags = []
        else:
            tags = settings.TAGS.split(",")
            tags = [n.strip() for n in tags]
        return tags

    def get_poll(self):
        if isinstance(self.QUESTIONS, str): self.QUESTIONS = self.QUESTIONS.split(",")
        poll = None
        duration = self.DURATION or None
        questions = self.QUESTIONS or None
        poll = {"duration":duration,"questions":questions}
        if not duration or not questions: return None
        return poll

    def get_schedule(self):
        if str(self.SCHEDULE) != "None": return self.SCHEDULE
        if  str(self.DATE) != "None":
            if str(self.TIME) != "None":
                self.SCHEDULE = "{}:{}".format(self.DATE,self.TIME)
            else:
                self.SCHEDULE = "{}:{}".format(self.DATE,"00:00")
        return None

    # comma separated string of usernames
    def get_users(self):
        users = []
        if str(settings.USERS) == "None":
            users = []
        elif str(settings.USERS) == "[]":
            users = []
        elif str(settings.USERS) == " ":
            users = []
        else:
            users = settings.USERS.split(",")
            users = [n.strip() for n in users]
        return users

    def loginPrompt(self):
        username = input("Twitter Username ({}): ".format(self.USERNAME))
        password = input("Twitter Password: ")
        if str(username) != "" and str(username) != " ":
            self.USERNAME = username
        if str(password) != "" and str(password) != " ":
            self.PASSWORD = password

    def maybePrint(self, text):
        if str(self.VERBOSE) == "True":
            print(colorize(text, "teal"))

    def save_password(self, newPassword):
        settings.PASSWORD = str(newPassword)
        # from passlib.context import CryptContext
        # pwd_context = CryptContext(
        #         schemes=["pbkdf2_sha256"],
        #         default="pbkdf2_sha256",
        #         pbkdf2_sha256__default_rounds=30000
        # )
        # def encrypt_password(password):
        #     return pwd_context.encrypt(password)
        # def check_encrypted_password(password, hashed):
        #     return pwd_context.verify(password, hashed)
        # settings.PASSWORD = encrypt_password(newPassword)

    def version_check(self):
        print("OnlySnarf version: {}".format(colorize(pkg_resources.get_distribution("onlysnarf").version,"yellow")))

    def update_value(self, variable, newValue):
        variable = str(variable).upper().replace(" ","_")
        try:
            # print("Updating: {} = {}".format(variable, newValue))
            setattr(self, variable, newValue)
            # print("Updated: {} = {}".format(variable, getattr(self, variable)))
        except Exception as e:
            maybePrint(e)

    def update_profile_value(self, variable, newValue):
        variable = str(variable).upper().replace(" ","_")
        try:
            # print("Updating: {} = {}".format(variable, newValue))
            self.PROFILE.setattr(self, variable, newValue)
            # print("Updated: {} = {}".format(variable, getattr(self, variable)))
        except Exception as e:
            maybePrint(e)

SETTINGS = Settings()

def colorize(string, color):
    if not color in colors: return string
    return colors[color] + string + '\033[0m'
 
colors = {
        'blue': '\033[94m',
        'header': '\033[48;1;34m',
        'teal': '\033[96m',
        'pink': '\033[95m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'menu': '\033[48;1;44m'
        }

def readConf(self, conf):
    posts = False
    self.POSTS = AttrDict()
    with open(conf) as f:
        for line in f:
            if str(line[0]) == "#": continue
            try:
                if "\"" in str(line):
                    spl = re.split("\"*\"", line)
                    key = spl[0] or None
                    val = spl[1] or None
                else:
                    (key, val) = line.split()
                key = key.strip()
                if str(val)[0] == "\"": val = str(val[1:])
                if str(val)[len(val)-1] == "\"": val = str(val[:len(val)-1])
                # print("{} : {} ".format(key.upper(),val))
                if "_post" in key: setattr(self.POSTS, key.upper().replace("_post",""), val)
                else: setattr(self, key.upper(), val)
            except Exception as e:
                pass
                # self.maybePrint(e)
                # print("Warning: Error Parsing Config")

# def send_email(email, text):
#     print("Sending Email: "+str(email))
#     pass

class AttrDict(dict):
    def __init__(self):
        dict.__init__(self)

    # Override getattr and setattr so that they return the values of getitem / setitem
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        return self[name]

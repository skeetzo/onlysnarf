#!/usr/bin/python3
# Global Settings
import re
import sys
import os
import json

class Profile:

    # profile settings are either:
    #   enabled or disabled
    #   display text, variable type, variable name in settings
    def __init__(self):
        # url path or file upload
        self.coverImage = None
        # url path or file upload
        self.profilePhoto = None
        # text
        self.displayName = ""
        # text in $
        # minimum $4.99 or free
        self.subscriptionPrice = "4.99"
        # text
        self.about = ""
        # text
        self.location = ""
        # text as url
        self.websiteURL = None
        # text
        self.username = ""
        # text, can't be changed
        self.email = ""
        # text
        self.password = ""
        # enabled or disabled
        self.emailNotifs = False
        # enabled or disabled
        self.emailNotifsNewReferral = False
        # enabled or disabled
        self.emailNotifsNewStream = False
        # enabled or disabled
        self.emailNotifsNewSubscriber = False
        # enabled or disabled
        self.emailNotifsNewTip = False
        # enabled or disabled
        self.emailNotifsRenewal = False
        # enabled or disabled
        self.emailNotifsNewLikes = False
        # enabled or disabled
        self.emailNotifsNewPosts = False
        # enabled or disabled
        self.emailNotifsNewPrivMessages = False
        # enabled or disabled
        self.siteNotifs = False
        # enabled or disabled
        self.siteNotifsNewComment = False
        # enabled or disabled
        self.siteNotifsNewFavorite = False
        # enabled or disabled
        self.siteNotifsDiscounts = False
        # enabled or disabled
        self.siteNotifsNewSubscriber = False
        # enabled or disabled
        self.siteNotifsNewTip = False
        # enabled or disabled
        self.toastNotifs = False
        # enabled or disabled
        self.toastNotifsNewComment = False
        # enabled or disabled
        self.toastNotifsNewFavorite = False
        # enabled or disabled
        self.toastNotifsNewSubscriber = False
        # enabled or disabled
        self.toastNotifsNewTip = False
        # enabled or disabled
        self.fullyPrivate = False
        # enabled or disabled
        self.enableComments = False
        # enabled or disabled
        self.showFansCount = False
        # enabled or disabled
        self.showPostsTip = False
        # enabled or disabled
        self.publicFriendsList = False
        # selection of countries
        self.ipCountry = getCountryList()
        # text of ip ranges
        self.ipIP = ""
        # enabled or disabled
        self.watermark = True
        # enabled or disabled
        self.watermarkPhoto = False
        # enabled or disabled
        self.watermarkVideo = False
        # the custom watermark text
        self.watermarkText = ""
        if self.username and str(self.username) != "":
            self.watermarkText = "OnlyFans.com/{}".format(self.username)
        # the obs live server
        self.liveServer = ""
        # the obs live server key
        self.liveServerKey = ""

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, val):
        return setattr(self, key, val)

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
        # -image-limit
        # maximum number of images to upload
        self.IMAGE_UPLOAD_LIMIT = 6
        ##
        # -image-max
        # maximum number of images that can be uploaded
        self.IMAGE_UPLOAD_MAX = 20
        ##
        # maximum number of images that can be uploaded in a message
        self.IMAGE_UPLOAD_MAX_MESSAGES = 5
        ##
        # -keywords
        # keywords to # in post
        self.KEYWORDS = []
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

        ##
        # profile settings for the account
        self.PROFILE = Profile()

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
            truths_ = ["SKIP_DELETE_GOOGLE","SKIP_BACKUP","BACKUP","CREATE_DRIVE","DEBUG","DEBUG_DELAY","DELETE_GOOGLE","FORCE_DELETE","FORCE_UPLOAD","FORCE_REDUCTION","PREFER_LOCAL","SAVE_USERS","SHOW_WINDOW","SKIP_DELETE","SKIP_DOWNLOAD","SKIP_REDUCE","SKIP_REPAIR","SKIP_UPLOAD","TWEETING","VERBOSE","THUMBNAILING_PREVIEW"]
            falses_ = []
            nexts_ = ["UPLOAD_MAX_DURATION","NOTKEYWORD","BYKEYWORD","PERFORMERS","KEYWORDS","DURATION","QUESTIONS","DATE","TIME","SCHEDULE","EXPIRES","USERS_FAVORITE","CRON","METHOD","PRICE","AMOUNT","MONTHS","ACTION","CRON_USER","INPUT","IMAGE","IMAGE_UPLOAD_LIMIT","IMAGE_UPLOAD_MAX","TYPE","TEXT","USER","DRIVE_PATH","GOOGLE_PATH","MOUNT_PATH","USERS_PATH","USERNAME","PASSWORD","USER_ID"]
            j = 0
            while j < len(truths_):
                if str(truths_[j]).upper() in str(sys.argv[i]).upper().replace("-","_"):
                    # self.set(truths_[j], True)
                    self[truths_[j]] = True
                j = j + 1
            j = 0
            while j < len(falses_):
                if str(falses_[j]).upper() in str(sys.argv[i]).upper().replace("-","_"):
                    # self.set(falses_[j], False)
                    self[falses_[j]] = False
                j = j + 1
            j = 0
            while j < len(nexts_):
                if str(nexts_[j]).upper() in str(sys.argv[i]).upper().replace("-","_"):
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
        if self.KEYWORDS != "":
            if str(self.KEYWORDS) == "None":
                self.KEYWORDS = []
            elif str(self.KEYWORDS) == "[]":
                self.KEYWORDS = []
            elif str(self.KEYWORDS) == " ":
                self.KEYWORDS = []
            else:
                self.KEYWORDS = self.KEYWORDS.split(",")
                self.KEYWORDS = [n.strip() for n in self.KEYWORDS]
        if self.PERFORMERS != "":
            if str(self.PERFORMERS) == "None":
                self.PERFORMERS = []
            elif str(self.PERFORMERS) == "[]":
                self.PERFORMERS = []
            elif str(self.PERFORMERS) == " ":
                self.PERFORMERS = []
            else:
                self.PERFORMERS = self.PERFORMERS.split(",")
                self.PERFORMERS = [n.strip() for n in self.PERFORMERS]

        self.INITIALIZED = True
        # print("Settings Initialized")
    ###################################################

    #####################
    ##### Functions #####
    #####################

    def getInput(self):
        if str(self.INPUT) == "None":
            self.maybePrint("Error: Missing Local Input")
            return False
        if os.path.isdir(str(self.INPUT)):  
            print("Found: Directory")  
        elif os.path.isfile(str(self.INPUT)):  
            print("Found: File")  
        else:  
            self.maybePrint("Warning: Missing Local Path")
        return self.INPUT

    def getPoll(self):
        if isinstance(self.QUESTIONS, str): self.QUESTIONS = self.QUESTIONS.split(",")
        poll = None
        duration = self.DURATION or None
        questions = self.QUESTIONS or None
        poll = {"period":duration,"questions":questions}
        if not duration or not questions: return None
        return poll

    def getSchedule(self):
        if str(self.SCHEDULE) != "None": return self.SCHEDULE
        if  str(self.DATE) != "None":
            if str(self.TIME) != "None":
                self.SCHEDULE = "{}:{}".format(self.DATE,self.TIME)
            else:
                self.SCHEDULE = "{}:{}".format(self.DATE,"00:00")
        return None

    def getTmp(self):
        # mkdir /tmp
        tmp = os.getcwd()
        if self.MOUNT_PATH != None:
            tmp = os.path.join(self.MOUNT_PATH, "tmp")
        else:
            tmp = os.path.join(tmp, "tmp")
        if not os.path.exists(str(tmp)):
            os.mkdir(str(tmp))
        return tmp

    def loginPrompt(self):
        username = input("Twitter Username ({}): ".format(self.USERNAME))
        password = input("Twitter Password: ")
        if str(username) != "" and str(username) != " ":
            self.USERNAME = username
        if str(password) != "" and str(password) != " ":
            self.PASSWORD = password

    def maybePrint(self, text):
        if str(self.VERBOSE) == "True":
            print(text)

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

def getCountryList():
    return ["USA","Canada"]

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

class AttrDict(dict):
    def __init__(self):
        dict.__init__(self)

    # Override getattr and setattr so that they return the values of getitem / setitem
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        return self[name]
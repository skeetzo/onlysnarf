#!/usr/bin/python3
# Global Settings
import sys
import os
import json

class Settings:
    def __init__(self):
        pass

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, val):
        return setattr(self, key, val)

    def initialize(self):
        # print("Initializing self...")
        try:
            if self.INITIALIZED:
                # print("Already Initialized, Skipping")
                return
        except:
            self.INITIALIZED = False
        # -backup
        # backup uploaded content to "posted" folder
        self.BACKUP = False
        # -cron-user
        # the user to run OnlySnarf as
        self.CRON_USER = "root"
        # -force-backup
        # force Google backup
        self.FORCE_BACKUP = False
        # -debug
        # debugging - skips uploading and deleting unless otherwise forced
        self.DEBUG = False
        # default message for debugging
        self.DEFAULT_MESSAGE = ":)"
        # default price for user messages
        self.DEFAULT_PRICE = "10.00"
        # default user greeting
        self.DEFAULT_GREETING = "hi! thanks for subscribing :3 do you have any preferences?"
        # -debug-delay
        # user message delay
        self.DEBUG_DELAY = False
        self.DEBUG_DELAY_AMOUNT = 10
        # -delete-google
        # delete uploaded content
        self.DELETE_GOOGLE = False
        # -create-drive 
        # creates missing OnlySnarf folders in Google Drive
        self.CREATE_DRIVE = False
        # configurable w/ profile.conf
        # OnlySnarf Drive folder list
        self.DRIVE_FOLDERS = [
            "images",
            "galleries",
            "performers",
            "scenes",
            "videos"
        ]
        # -force-delete
        # force Google file deletion upon upload
        self.FORCE_DELETE = False
        # -force-reduce
        # force mp4 reduction
        self.FORCE_REDUCTION = False
        # -force-upload
        # ignore upload max wait
        self.FORCE_UPLOAD = False
        # -image-path
        # path to local file to use
        self.PATH_LOCAL = None
        # -input
        # path to local file(s) to upload
        self.INPUT = None
        # -image
        # path to local image to use for message or upload
        self.IMAGE = None
        # -image-limit
        # maximum number of images to upload
        self.IMAGE_UPLOAD_LIMIT = 6
        # -image-max
        # maximum number of images that can be uploaded
        self.IMAGE_UPLOAD_MAX = 20
        # -overwrite-local
        # self.OVERWRITE_LOCAL = False
        # -mount-path
        # the mounth path for a local directory of OnlyFans config files
        self.MOUNT_PATH = None
        # -password
        # the password for the OnlyFans / Twitter
        self.PASSWORD = None
        # -drive-path
        # the folder path within Google Drive for OnlySnarf's root folder
        self.DRIVE_PATH = None
        # -user-path
        # the path to the users.json file
        self.USERS_PATH = "users.json"
        # -config-path
        # the path to the config.json file
        self.PATH_CONFIG = "config.json"
        # -google-path
        # the path to the google_creds.txt
        self.GOOGLE_PATH = "google_creds.txt"
        # the path to the client_secret.json
        self.PATH_SECRET = "client_secret.json"
        # -prefer-local
        # prefers local cache over refreshing first call
        self.PREFER_LOCAL = False
        # the maximum number of recent users
        self.RECENT_USER_COUNT = 3
        # can be set in profile.conf
        # root Google drive folder
        self.ROOT_FOLDER = "OnlySnarf"
        # -save-users
        # saves OnlyFans users upon exit
        self.SAVE_USERS = False
        # -skip-delete
        # skip local file deletion before and after upload
        self.SKIP_DELETE = False
        # -skip-download
        self.SKIP_DOWNLOAD = False
        # -skip-reduce
        # skip mp4 reducing
        self.SKIP_REDUCE = False
        # -skip-repair
        # skip mp4 repairs
        self.SKIP_REPAIR = False
        # -skip-thumb
        # skip video thumbnailing when repairing
        self.SKIP_THUMBNAIL = False
        # can be set in profile.conf
        # -skip-upload
        # skips file upload
        self.SKIP_UPLOAD = False
        # list of users to skip
        self.SKIP_USERS = []
        # -show 
        # shows window
        self.SHOW_WINDOW = False
        # -text
        # text for message or upload
        self.TEXT = None
        # fixes thumbnail preview
        self.THUMBNAILING_PREVIEW = True
        # -type
        # the type of upload
        self.TYPE = None
        # -tweet
        # enabled tweeting
        self.TWEETING = False
        # -user
        # the user to target
        self.USER = None
        # user id found in OnlyFans
        self.USER_ID = None
        # -username
        # the OnlyFans / Twitter username to use
        self.USERNAME = None
        # -verbose
        # more output
        self.VERBOSE = False
        # custom repair option for shitty gopro videos
        self.WORKING_VIDEO = "video.mp4"
        # updates w/ values from /etc/onlysnarf/profile.conf
        profile = None
        if os.path.exists("/etc/onlysnarf/profile.conf"):
            readConf(self, "/etc/onlysnarf/profile.conf")
        elif os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "profile.conf")):
            readConf(self, os.path.join(os.path.dirname(os.path.realpath(__file__)), "profile.conf"))
        self.POSTS = {}
        # if os.path.exists("/etc/onlysnarf/posts.conf"):
        #     readPosts(self, "/etc/onlysnarf/posts.conf")
        # elif os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "posts.conf")):
        #     readPosts(self, os.path.join(os.path.dirname(os.path.realpath(__file__)), "posts.conf"))
        i = 0
        while i < len(sys.argv):
            sys.argv[i] = sys.argv[i][1:] # remove - in front
            truths_ = ["BACKUP","CREATE_DRIVE","DEBUG","DEBUG_DELAY","DELETE_GOOGLE","FORCE_DELETE","FORCE_UPLOAD","FORCE_REDUCTION","PREFER_LOCAL","SAVE_USERS","SHOW_WINDOW","SKIP_DELETE","SKIP_DOWNLOAD","SKIP_REDUCE","SKIP_REPAIR","SKIP_UPLOAD","SKIP_THUMBNAIL","TWEETING","VERBOSE"]
            falses_ = []
            nexts_ = ["CRON_USER","INPUT","IMAGE","IMAGE_UPLOAD_LIMIT","IMAGE_UPLOAD_MAX","TYPE","TEXT","USER","DRIVE_PATH","GOOGLE_PATH","MOUNT_PATH","USERS_PATH","USERNAME","PASSWORD","USER_ID"]
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
                    self[nexts_[j]] = sys.argv[i+1]
                j = j + 1
            i += 1
        if self.MOUNT_PATH is not None:
            self.PATH_CONFIG = os.path.join(self.MOUNT_PATH, self.PATH_CONFIG)
            self.PATH_SECRET = os.path.join(self.MOUNT_PATH, self.PATH_SECRET)
            self.GOOGLE_PATH = os.path.join(self.MOUNT_PATH, self.GOOGLE_PATH)
            self.USERS_PATH = os.path.join(self.MOUNT_PATH, self.USERS_PATH)
            self.WORKING_VIDEO = os.path.join(self.MOUNT_PATH, self.WORKING_VIDEO)
        else:
            self.PATH_CONFIG = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.PATH_CONFIG)
            self.PATH_SECRET = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.PATH_SECRET)
            self.GOOGLE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.GOOGLE_PATH)
            self.USERS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.USERS_PATH)
            self.WORKING_VIDEO = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.WORKING_VIDEO)
        # config file
        try:
            with open(self.PATH_CONFIG) as config_file:    
                config = json.load(config_file)
            self.USERNAME = config.get("username")
            self.PASSWORD = config.get("password")
        except Exception as e:
            print(e)
        
        self.INITIALIZED = True
        # print("Settings Initialized")
    ###################################################

    #####################
    ##### Functions #####
    #####################

    def getInput(self):
        if str(self.INPUT) == "None":
            self.maybePrint("Error: Missing Input Path")
            return False
        if os.path.isdir(str(self.INPUT)):  
            print("Found: Directory")  
        elif os.path.isfile(str(self.INPUT)):  
            print("Found: File")  
        else:  
            self.maybePrint("Error: Missing Input Path")
            return False
        return self.INPUT

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
        if username != "" and username != " ":
            self.USERNAME = username
        if password != "" and password != " ":
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

SETTINGS = Settings()

def readConf(self, conf):
    with open(conf) as f:
        for line in f:
            (key, val) = line.split()
            if str(key[0]) == "#": continue
            setattr(self, key, val)

def readPosts(self, conf):
    with open(conf) as f:
        for line in f:
            (key, val) = line.split()
            print("key: {} :- {}: val".format(key, val))
            if str(key[0]) == "#": continue
            setattr(self.POSTS, key, val)
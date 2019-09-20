#!/usr/bin/python3
# Global Settings
import sys
import os

class Settings:
    def __init__(self):
        pass

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
        self.DRIVE_CREATE_MISSING = False
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
        self.FORCE_DELETE_GOOGLE = False
        # -force-reduce
        # force mp4 reduction
        self.FORCE_REDUCTION = False
        # -force-upload
        # ignore upload max wait
        self.FORCE_UPLOAD = False
        # -image-path
        # path to local file to use
        self.PATH_LOCAL = None
        # -image
        # path to local image to use for message or upload
        self.IMAGE = None
        # -image-limit
        # maximum number of images to upload
        self.IMAGE_UPLOAD_LIMIT = 6
        # -image-max
        # maximum number of images that can be uploaded
        self.IMAGE_UPLOAD_MAX = 15
        # -mount-path
        # the mounth path for a local directory of OnlyFans config files
        self.PATH_MOUNT = None
        # -drive-path
        # the folder path within Google Drive for OnlySnarf's root folder
        self.PATH_DRIVE = None
        # -user-path
        # the path to the users.json file
        self.PATH_USERS = "users.json"
        # -config-path
        # the path to the config.json file
        self.PATH_CONFIG = "config.json"
        # -google-path
        # the path to the google_creds.txt
        self.PATH_GOOGLE_CREDS = "google_creds.txt"
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
        # totally not implemented
        # todo: this
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
        # the user to run OnlySnarf as
        self.USER = "root"
        # -verbose
        # more output
        self.VERBOSE = False
        # custom repair option for shitty gopro videos
        self.WORKING_VIDEO = "video.mp4"
        # updates w/ values from /etc/onlysnarf/profile.conf
        profile = None
        if os.path.exists("/etc/onlysnarf/profile.conf"):
            readProfile(self, "/etc/onlysnarf/profile.conf")
        elif os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), "profile.conf")):
            readProfile(self, os.path.join(os.path.dirname(os.path.realpath(__file__)), "profile.conf"))
        i = 0
        while i < len(sys.argv):
            if '-backup' in str(sys.argv[i]):
                self.BACKUP = True
            elif '-create-drive' in str(sys.argv[i]):
                self.DRIVE_CREATE_MISSING = True
            elif '-debug' in str(sys.argv[i]):
                self.DEBUG = True
            elif '-debug-delay' in str(sys.argv[i]):
                self.DEBUG_DELAY = True
            elif '-delete-google' in str(sys.argv[i]):
                self.DELETE_GOOGLE = False
            elif '-force-backup' in str(sys.argv[i]):
                self.FORCE_BACKUP = True 
            elif '-force-delete' in str(sys.argv[i]):
                self.FORCE_DELETE_GOOGLE = True
            elif '-force-upload' in str(sys.argv[i]):
                self.FORCE_UPLOAD = True
            elif '-force-reduc' in str(sys.argv[i]):
                self.FORCE_REDUCTION = True
            elif '-image' in str(sys.argv[i]):
                self.IMAGE = str(sys.argv[i+1])
            elif '-image-limit' in str(sys.argv[i]):
                self.IMAGE_UPLOAD_LIMIT = str(sys.argv[i+1])
            elif '-image-max' in str(sys.argv[i]):
                self.IMAGE_UPLOAD_MAX = str(sys.argv[i+1])
            elif '-prefer-local' in str(sys.argv[i]):
                self.PREFER_LOCAL = True
            elif '-save-users' in str(sys.argv[i]):
                self.SAVE_USERS = True
            elif '-show' in str(sys.argv[i]):
                self.SHOW_WINDOW = True
            elif '-skip-delete' in str(sys.argv[i]):
                self.SKIP_DELETE = True
            elif '-skip-reduce' in str(sys.argv[i]):
                self.SKIP_REDUCE = True
            elif '-skip-repair' in str(sys.argv[i]):
                self.SKIP_REPAIR = True
            elif '-skip-thumb' in str(sys.argv[i]):
                self.SKIP_THUMBNAIL = True
            elif '-type' in str(sys.argv[i]):
                self.TYPE = str(sys.argv[i+1])
            elif '-text' in str(sys.argv[i]):
                self.TEXT = str(sys.argv[i+1])
            elif '-tweet' in str(sys.argv[i]):
                self.TWEETING = True
            elif '-user' in str(sys.argv[i]):
                self.USER = str(sys.argv[i+1])
            elif '-verbose' in str(sys.argv[i]):
                self.VERBOSE = True
            elif '-drive-path' in str(sys.argv[i]):
                self.PATH_DRIVE = str(sys.argv[i+1])
            elif '-google-path' in str(sys.argv[i]):
                self.PATH_GOOGLE_CREDS = str(sys.argv[i+1])
            elif '-mount-path' in str(sys.argv[i]):
                self.PATH_MOUNT = str(sys.argv[i+1])
            elif '-user-path' in str(sys.argv[i]):
                self.PATH_USERS = str(sys.argv[i+1])
            i += 1
        if self.PATH_MOUNT is not None:
            self.PATH_CONFIG = os.path.join(self.PATH_MOUNT, self.PATH_CONFIG)
            self.PATH_SECRET = os.path.join(self.PATH_MOUNT, self.PATH_SECRET)
            self.PATH_GOOGLE_CREDS = os.path.join(self.PATH_MOUNT, self.PATH_GOOGLE_CREDS)
            self.PATH_USERS = os.path.join(self.PATH_MOUNT, self.PATH_USERS)
            self.WORKING_VIDEO = os.path.join(self.PATH_MOUNT, self.WORKING_VIDEO)
        else:
            self.PATH_CONFIG = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.PATH_CONFIG)
            self.PATH_SECRET = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.PATH_SECRET)
            self.PATH_GOOGLE_CREDS = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.PATH_GOOGLE_CREDS)
            self.PATH_USERS = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.PATH_USERS)
            self.WORKING_VIDEO = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.WORKING_VIDEO)
        self.INITIALIZED = True
        # print("Settings Initialized")
    ###################################################

    #####################
    ##### Functions #####
    #####################

    def getTmp(self):
        # mkdir /tmp
        tmp = os.getcwd()
        if self.PATH_MOUNT != None:
            tmp = os.path.join(self.PATH_MOUNT, "tmp")
        else:
            tmp = os.path.join(tmp, "tmp")
        if not os.path.exists(str(tmp)):
            os.mkdir(str(tmp))
        return tmp

    def maybePrint(self, text):
        if str(self.VERBOSE) == "True":
            print(text);

    def update_value(self, variable, newValue):
        variable = str(variable).upper().replace(" ","_")
        try:
            # print("Updating: {} = {}".format(variable, newValue))
            setattr(self, variable, newValue)
            # print("Updated: {} = {}".format(variable, getattr(self, variable)))
        except Exception as e:
            settings.maybePrint(e)

SETTINGS = Settings()

def readProfile(self, profile):
    with open(profile) as f:
        for line in f:
            (key, val) = line.split()
            if str(key[0]) == "#": continue
            setattr(self, key, val)
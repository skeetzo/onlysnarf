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

        self.DEFAULT_MESSAGE = ":)"

        self.DEBUG = False

        self.SKIP_DOWNLOAD = False

        self.IMAGE_UPLOAD_LIMIT = 6

        self.IMAGE_UPLOAD_MAX = 15

        self.REMOVE_LOCAL = True

        # backup uploaded content
        self.BACKING_UP = False

        self.BACKING_UP_FORCE = False

        # delete uploaded content
        self.DELETING = False
        self.DELETING_FORCED = False
        
        # -video
        # -gallery
        # -image
        # -scene
        self.TYPE = None

        # Twitter hashtags
        self.HASHTAGGING = False

        # -force / ignore upload max wait
        self.FORCE_UPLOAD = False

        # -show -> shows window
        self.SHOW_WINDOW = False

        self.SPECIAL_CRONS = [
            "queuedMessages",
            "greetNew"
        ]

        # -text
        self.TEXT = None

        # -quiet
        self.TWEETING = True

        self.LOCATION = "google"

        # def init(sys.argv):
        self.MOUNT_PATH = None
        self.MOUNT_DRIVE = None
        self.USERS_PATH = "users.json"
        self.CONFIG_PATH = "config.json"
        self.GOOGLE_CREDS_PATH = "google_creds.txt"
        self.SECRET_PATH = "client_secret.json"
        self.WORKING_VIDEO = "video.mp4"

        self.FILE_NAME = None
        self.FILE_PATH = None

        self.THUMBNAILING_PREVIEW = True

        self.IMAGE = None

        self.RECENT_USER_COUNT = 3

        self.DEFAULT_PRICE = "10.00"

        self.FORCE_REDUCTION = False

        self.CREATE_MISSING_FOLDERS = False

        self.VERBAL = False

        self.ROOT_FOLDER = "OnlySnarf"

        self.SKIP_REPAIR = False
        self.SKIP_REDUCE = False
        self.SKIP_THUMBNAIL = False

        self.SKIP_USERS = [
            "6710870",
            
            "5451153",
            "1771880",
            "5057708",
            "7825384",
            "4883991",

            "1633091",
            "3055233"
        ]

        self.DRIVE_FOLDERS = [
            "images",
            "galleries",
            "performers",
            "scenes",
            "videos"
        ]

        self.user_DEFAULT_GREETING = "hi! thanks for subscribing :3 do you have any preferences?"


        # user message delay
        self.DELAY = False

        i = 0
        while i < len(sys.argv):
            if '-image' in str(sys.argv[i]):
                self.TYPE = "image"
            if '-gallery' in str(sys.argv[i]):
                self.TYPE = "gallery"
            if '-video' in str(sys.argv[i]):
                self.TYPE = "video"
            if '-scene' in str(sys.argv[i]):
                self.TYPE = "scene"
            if '-text' in str(sys.argv[i]):
                self.TEXT = str(sys.argv[i+1])
            if '-debug' in str(sys.argv[i]):
                self.DEBUG = True
            if '-verbal' in str(sys.argv[i]):
                self.VERBAL = True
            if '-backup' in str(sys.argv[i]):
                self.BACKING_UP = True
            if '-force-delete' in str(sys.argv[i]):
                self.DELETING_FORCED = True
            if '-show' in str(sys.argv[i]):
                self.SHOW_WINDOW = True
            if '-quiet' in str(sys.argv[i]):
                self.TWEETING = False
            if '-delete' in str(sys.argv[i]):
                self.DELETING = False
            if '-mount-path' in str(sys.argv[i]):
                self.MOUNT_PATH = str(sys.argv[i+1])
            if '-mount-drive' in str(sys.argv[i]):
                self.MOUNT_DRIVE = str(sys.argv[i+1])
            if '-users' in str(sys.argv[i]):
                self.USERS_PATH = str(sys.argv[i+1])
            if '-image' in str(sys.argv[i]):
                self.IMAGE = str(sys.argv[i+1])
            if '-force-upload' in str(sys.argv[i]):
                self.FORCE_UPLOAD = True
            if '-force-reduc' in str(sys.argv[i]):
                self.FORCE_REDUCTION = True
            if '-force-backup' in str(sys.argv[i]):
                self.BACKING_UP_FORCE = True
            if '-delay' in str(sys.argv[i]):
                self.DELAY = True
            if '-image-limit' in str(sys.argv[i]):
                self.IMAGE_UPLOAD_LIMIT = str(sys.argv[i+1])
            if '-image-max' in str(sys.argv[i]):
                self.IMAGE_UPLOAD_MAX = str(sys.argv[i+1])
            if '-create-folders' in str(sys.argv[i]):
                self.CREATE_MISSING_FOLDERS = True
            if '-skip-reduce' in str(sys.argv[i]):
                self.SKIP_REDUCE = True
            if '-skip-repair' in str(sys.argv[i]):
                self.SKIP_REPAIR = True
            if '-skip-thumb' in str(sys.argv[i]):
                self.SKIP_THUMBNAIL = True
            # skeetzo profile
            if '-skeetzo' in str(sys.argv[i]):
                self.VERBAL = True
                self.BACKING_UP = True
                self.TWEETING = False
                self.MOUNT_PATH = "/mnt/apps/onlysnarf"
                self.MOUNT_DRIVE = "Pron/dbot"
            if '-schizo' in str(sys.argv[i]):
                self.SKIP_THUMBNAIL = True
                # self.SKIP_REPAIR = True
                # self.SKIP_REDUCE = True
                self.VERBAL = True
                self.BACKING_UP = True
                self.TWEETING = False
                self.MOUNT_PATH = "/opt/apps/onlysnarf"
                self.MOUNT_DRIVE = "Pron/dbot"
            if '-dbot' in str(sys.argv[i]):
                self.SKIP_THUMBNAIL = True
                # self.SKIP_REPAIR = True
                # self.SKIP_REDUCE = True
                self.VERBAL = True
                self.BACKING_UP = True
                self.TWEETING = False
                self.MOUNT_PATH = "/mnt/dbot/dev/onlysnarf"
                self.MOUNT_DRIVE = "Pron/dbot"
            i += 1
        
        if self.MOUNT_PATH is not None:
            self.CONFIG_PATH = os.path.join(self.MOUNT_PATH, self.CONFIG_PATH)
            self.SECRET_PATH = os.path.join(self.MOUNT_PATH, self.SECRET_PATH)
            self.GOOGLE_CREDS_PATH = os.path.join(self.MOUNT_PATH, self.GOOGLE_CREDS_PATH)
            self.USERS_PATH = os.path.join(self.MOUNT_PATH, self.USERS_PATH)
            self.WORKING_VIDEO = os.path.join(self.MOUNT_PATH, self.WORKING_VIDEO)
        else:
            self.CONFIG_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.CONFIG_PATH)
            self.SECRET_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.SECRET_PATH)
            self.GOOGLE_CREDS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.GOOGLE_CREDS_PATH)
            self.USERS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.USERS_PATH)
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
        if self.MOUNT_PATH != None:
            tmp = os.path.join(self.MOUNT_PATH, "tmp")
        else:
            tmp = os.path.join(tmp, "tmp")
        if not os.path.exists(str(tmp)):
            os.mkdir(str(tmp))
        return tmp

    def maybePrint(self, text):
        if str(self.VERBAL) == "True":
            print(text);

    def update_value(self, variable, newValue):
        variable = str(variable).upper().replace(" ","_")
        try:
            # print("Updating: {} = {}".format(variable, newValue))
            setattr(self, variable, newValue)
            # print("Updated: {} = {}".format(variable, getattr(self, variable)))
        except Exception as e:
            print(e)

SETTINGS = Settings()

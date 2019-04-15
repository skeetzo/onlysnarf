# Global Settings
import sys
import os

class Settings:
    def __init__(self):
        pass

    def initialize(self):
        # print("Initializing Settings...")
        try:
            if self.INITIALIZED:
                # print("Already Initialized, Skipping")
                return
        except:
            self.INITIALIZED = False

        self.DEFAULT_MESSAGE = ":)"

        self.DEBUG = False

        self.SKIP_DOWNLOAD = True

        self.IMAGE_UPLOAD_LIMIT = 6

        self.IMAGE_UPLOAD_MAX = 15

        self.REMOVE_LOCAL = True

        # backup uploaded content
        self.BACKING_UP = True

        self.BACKING_UP_FORCE = True

        # delete uploaded content
        self.DELETING = False

        # -video
        # -gallery
        # -image
        self.TYPE = None

        # Twitter hashtags
        self.HASHTAGGING = False

        # -force / ignore upload max wait
        self.FORCE_UPLOAD = False

        # -show -> shows window
        self.SHOW_WINDOW = False

        # -text
        self.TEXT = None

        # -quiet
        self.TWEETING = True

        self.LOCATION = "google"

        # def init(sys.argv):
        self.MOUNT_PATH = None
        self.USERS_PATH = None

        self.FILE_NAME = None
        self.FILE_PATH = None

        self.IMAGE = None

        self.RECENT_USER_COUNT = 3

        self.DEFAULT_PRICE = "10.00"


        self.FORCE_REDUCTION = False

        self.SKIP_USERS = [
            "6710870",
            "7248614",
            "5451153",
            "1771880",
            "5057708",
            "7825384",
            "4883991"
        ]

        self.user_DEFAULT_GREETING = "hi! thanks for subscribing :3 do you have any preferences?"

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
            if '-hash' in str(sys.argv[i]):
                self.HASHTAGGING = True
            if '-force' in str(sys.argv[i]):
                self.FORCE_UPLOAD = True
            if '-show' in str(sys.argv[i]):
                self.SHOW_WINDOW = True
            if '-quiet' in str(sys.argv[i]):
                self.TWEETING = False
            if '-delete' in str(sys.argv[i]):
                self.DELETING = False
            if '-mount' in str(sys.argv[i]):
                self.MOUNT_PATH = str(sys.argv[i+1])
            if '-users' in str(sys.argv[i]):
                self.USERS_PATH = str(sys.argv[i+1])
            if '-image' in str(sys.argv[i]):
                self.IMAGE = str(sys.argv[i+1])
            if '-force-upload' in str(sys.argv[i]):
                self.FORCE_UPLOAD = True
            if '-force-reduc' in str(sys.argv[i]):
                self.FORCE_REDUCTION = True
            if '-delay' in str(sys.argv[i]):
                self.DELAY = True
            i += 1

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
        if str(self.DEBUG) == "True":
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

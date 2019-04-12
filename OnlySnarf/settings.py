# Global Settings
import sys
import os

global DEFAULT_MESSAGE
DEFAULT_MESSAGE = ":)"

global DEBUG
DEBUG = False

global SKIP_DOWNLOAD
SKIP_DOWNLOAD = True

global IMAGE_UPLOAD_LIMIT
IMAGE_UPLOAD_LIMIT = 6

global IMAGE_UPLOAD_MAX
IMAGE_UPLOAD_MAX = 15

global REMOVE_LOCAL
REMOVE_LOCAL = True

# backup uploaded content
global BACKING_UP
BACKING_UP = True

global BACKING_UP_FORCE
BACKING_UP_FORCE = True

# delete uploaded content
global DELETING
DELETING = False

# -video
# -gallery
# -image
global TYPE
TYPE = None

# Twitter hashtags
global HASHTAGGING
HASHTAGGING = False

# -force / ignore upload max wait
global FORCE_UPLOAD
FORCE_UPLOAD = False

# -show -> shows window
global SHOW_WINDOW
SHOW_WINDOW = False

# -text
global TEXT
TEXT = None

# -quiet
global TWEETING
TWEETING = True

global LOCATION
LOCATION = "google"

# def init(sys.argv):
global MOUNT_PATH
MOUNT_PATH = None
global USERS_PATH
USERS_PATH = None

global FILE_NAME
FILE_NAME = None
global FILE_PATH
FILE_PATH = None

global IMAGE
# IMAGE = "/home/skeetzo/Projects/onlysnarf/OnlySnarf/images/snarf.jpg"
IMAGE = None

global RECENT_USER_COUNT
RECENT_USER_COUNT = 3

global DEFAULT_PRICE
DEFAULT_PRICE = "10.00"


global FORCE_REDUCTION
FORCE_REDUCTION = False

global SKIP_USERS
SKIP_USERS = [
    "6710870"
]

global user_DEFAULT_GREETING
user_DEFAULT_GREETING = "hi! thanks for subscribing :3 do you have any preferences?"

global user_DEFAULT_REFRESHER
user_DEFAULT_GREETING = "hi! thanks for subscribing :3 do you have any preferences?"


i = 0
while i < len(sys.argv):
    if '-image' in str(sys.argv[i]):
        TYPE = "image"
    if '-gallery' in str(sys.argv[i]):
        TYPE = "gallery"
    if '-video' in str(sys.argv[i]):
        TYPE = "video"
    if '-scene' in str(sys.argv[i]):
        TYPE = "scene"
    if '-text' in str(sys.argv[i]):
        TEXT = str(sys.argv[i+1])
    if '-debug' in str(sys.argv[i]):
        DEBUG = True
    if '-hash' in str(sys.argv[i]):
        HASHTAGGING = True
    if '-force' in str(sys.argv[i]):
        FORCE_UPLOAD = True
    if '-show' in str(sys.argv[i]):
        SHOW_WINDOW = True
    if '-quiet' in str(sys.argv[i]):
        TWEETING = False
    if '-delete' in str(sys.argv[i]):
        DELETING = False
    if '-mount' in str(sys.argv[i]):
        MOUNT_PATH = str(sys.argv[i+1])
    if '-users' in str(sys.argv[i]):
        USERS_PATH = str(sys.argv[i+1])
    if '-image' in str(sys.argv[i]):
        IMAGE = str(sys.argv[i+1])
    if '-force-upload' in str(sys.argv[i]):
        FORCE_UPLOAD = True
    if '-force-reduc' in str(sys.argv[i]):
        FORCE_REDUCTION = True
    i += 1

#####################
##### Functions #####
#####################

def getTmp():
    # mkdir /tmp
    tmp = os.getcwd()
    global MOUNT_PATH
    if MOUNT_PATH:
        tmp = os.path.join(MOUNT_PATH, "tmp")
    else:
        tmp = os.path.join(tmp, "tmp")
    if not os.path.exists(str(tmp)):
        os.mkdir(str(tmp))
    return tmp

def maybePrint(text):
    global DEBUG
    if DEBUG:
        print(text);

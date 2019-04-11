# Global Settings
import sys
import os

# def init(sys.argv):
global MOUNT_PATH
MOUNT_PATH = None
global USERS_PATH
USERS_PATH = None
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
global BACKING_UP
# backup uploaded content
BACKING_UP = True
global BACKING_UP_FORCE
BACKING_UP_FORCE = True
global DELETING
# delete uploaded content
DELETING = False

global TYPE
# -v -> video
# -g -> gallery
# -i -> image
TYPE = None

global HASHTAGGING
# Twitter hashtags
HASHTAGGING = False
global FORCE_UPLOAD
# -f -> force / ignore upload max wait
FORCE_UPLOAD = False
global SHOW_WINDOW
# -show -> shows window
SHOW_WINDOW = False
global TEXT
# -t -> text
TEXT = None
global TWEETING
# -q -> quiet / no tweet
TWEETING = True
global LOCATION
LOCATION = "google"
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
global DEFAULT_MESSAGE
DEFAULT_MESSAGE = ":)"

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
    if '-t' in str(sys.argv[i]):
        TEXT = str(sys.argv[i+1])
    if '-d' in str(sys.argv[i]):
        DEBUG = True
    if '-h' in str(sys.argv[i]):
        HASHTAGGING = True
    if '-f' in str(sys.argv[i]):
        FORCE_UPLOAD = True
    if '-show' in str(sys.argv[i]):
        SHOW_WINDOW = True
    if '-q' in str(sys.argv[i]):
        TWEETING = False
    if '-delete' in str(sys.argv[i]):
        DELETING = False
    if '-mount' in str(sys.argv[i]):
        MOUNT_PATH = str(sys.argv[i+1])
    if '-users' in str(sys.argv[i]):
        USERS_PATH = str(sys.argv[i+1])
    if '-i' in str(sys.argv[i]):
        IMAGE = str(sys.argv[i+1])
    if '-force-upload' in str(sys.argv[i]):
        FORCE_UPLOAD = True
    if '-force-reduc' in str(sys.argv[i]):
        FORCE_REDUCTION = True
    i += 1

# global initialized
# initialized = True

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

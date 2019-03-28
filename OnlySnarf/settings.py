# Global Settings
import sys

# def init(sys.argv):
global MOUNT_PATH
MOUNT_PATH = None
global DEBUG
DEBUG = False
global SKIP_DOWNLOAD
SKIP_DOWNLOAD = True
global IMAGE_UPLOAD_LIMIT
IMAGE_UPLOAD_LIMIT = 6
global REMOVE_LOCAL
REMOVE_LOCAL = True
global BACKING_UP
# backup uploaded content
BACKING_UP = True
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
    i += 1

# global initialized
# initialized = True
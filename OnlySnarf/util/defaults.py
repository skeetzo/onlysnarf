import os
from pathlib import Path

##
# Defaults 
##

SOURCES = [ "local","remote" ]

CATEGORIES = [ "images", "galleries", "videos", "performers" ]

# selenium browser
REMOTE_BROWSER = "127.0.0.1"
BROWSER_PORT = 4444
# sftp
REMOTE_HOST = "127.0.0.1"
REMOTE_PORT = 22

DEFAULT_MESSAGE = ":)"
DEFAULT_REFRESHER = "hi!"
DEFAULT_GREETING = "hi! thanks for subscribing :3 do you have any preferences?"

DISCOUNT_MAX_AMOUNT = 55
DISCOUNT_MIN_AMOUNT = 10
DISCOUNT_MAX_MONTHS = 7
DISCOUNT_MIN_MONTHS = 1
EXPIRATION_ALLOWED = [1,3,7,30,99]
IMAGE_LIMIT = 15
MESSAGE_CHOICES = ["all", "recent", "favorite", "renew on"]
PRICE_MINIMUM = 3
UPLOAD_MAX_DURATION = 6*6 # increments of 10 minutes; 6 = 1 hr
USER_LIMIT = 10

# days
DURATION_ALLOWED = [1,3,7,30,99]
# %
LIMIT_ALLOWED = [0,1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100]
# %
PROMOTION_EXPIRATION_ALLOWED = [int(i) for i in range(30)]
PROMOTION_EXPIRATION_ALLOWED.insert(0,0)
# number
PROMOTION_OFFER_LIMIT = [0,1,2,3,4,5,6,7,8,9,10]
# various datetime
PROMOTION_DURATION_ALLOWED = ["1 day","3 days","7 days","14 days","1 month","3 months","6 months","12 months"]

# Paths
USER = os.getenv('USER')
if str(os.getenv('SUDO_USER')) != "root" and str(os.getenv('SUDO_USER')) != "None":
    USER = os.getenv('SUDO_USER')
USER_HOME = "/home/{}".format(USER)

ROOT_PATH = "{}/OnlySnarf".format(USER_HOME)
DOWNLOAD_PATH = os.path.join(ROOT_PATH, "downloads")
UPLOAD_PATH = os.path.join(ROOT_PATH, "uploads")
LOG_PATH = os.path.join(ROOT_PATH, "snarf.log")
REMOTE_PATH = ROOT_PATH

CONFIGS_PATH = "{}/.onlysnarf".format(USER_HOME)
USERS_PATH = os.path.join(CONFIGS_PATH, "users.json")
PROFILE_PATH = os.path.join(CONFIGS_PATH, "profile.json")
CONFIG_PATH = os.path.join(CONFIGS_PATH, "config.conf")
PROFILES_PATH = os.path.join(CONFIGS_PATH, "users")

# print(ROOT_PATH)
# print(DOWNLOAD_PATH)
# print(UPLOAD_PATH)
# print(CONFIGS_PATH)

Path(ROOT_PATH).mkdir(parents=True, exist_ok=True)
Path(DOWNLOAD_PATH).mkdir(parents=True, exist_ok=True)
Path(UPLOAD_PATH).mkdir(parents=True, exist_ok=True)
Path(CONFIGS_PATH).mkdir(parents=True, exist_ok=True)

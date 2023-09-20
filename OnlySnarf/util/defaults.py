import os
from datetime import datetime
from pathlib import Path

##
# Defaults 
##

ACTIONS = [ "Discount", "Message", "Post", "Profile", "Promotion" ]

AMOUNT_NONE = 0

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
SCHEDULE_FORMAT = "{} {}".format(DATE_FORMAT, TIME_FORMAT)

date_ = datetime.strptime(str(datetime.now().strftime(SCHEDULE_FORMAT)), SCHEDULE_FORMAT)

DATE = date_.date().strftime(DATE_FORMAT)[:10]
TIME = date_.time().strftime(TIME_FORMAT)[:9]
SCHEDULE = date_.strftime(SCHEDULE_FORMAT)

TIME_NONE = "00:00:00"

DEFAULT_MESSAGE = ":)"
DEFAULT_REFRESHER = "hi!"
DEFAULT_GREETING = "hi! thanks for subscribing :3 do you have any preferences?"

DISCOUNT_MAX_AMOUNT = 55
DISCOUNT_MIN_AMOUNT = 5
DISCOUNT_MAX_MONTHS = 12
DISCOUNT_MIN_MONTHS = 1

## note: '99' aka 'No Limit' no longer allowed?
# DURATION_ALLOWED = [1,3,7,30, 99] # in days
DURATION_ALLOWED = [1,3,7,30] # in days
DURATION_NONE = 0

EXPIRATION_MIN = 1
EXPIRATION_MAX = 30
EXPIRATION_NONE = 0

IMAGE_LIMIT = 15

LIMIT_ALLOWED = [0,1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100] # in %

MAX_TABS = 20

MESSAGE_CHOICES = ["all", "recent", "favorite", "renew on"]

PROMOTION_EXPIRATION_ALLOWED = [int(i) for i in range(30)] # in %
PROMOTION_EXPIRATION_ALLOWED.insert(0,0)
# number
PROMOTION_OFFER_LIMIT = [0,1,2,3,4,5,6,7,8,9,10]
# various datetime
PROMOTION_DURATION_ALLOWED = ["1 day","3 days","7 days","14 days","1 month","3 months","6 months","12 months"]

PRICE_MINIMUM = 3
PRICE_MAXIMUM = 200

# sftp
# selenium browser
REMOTE_BROWSER = "127.0.0.1"
BROWSER_PORT = 4444

REMOTE_HOST = "127.0.0.1"
REMOTE_PORT = 22

#3600 # 1hr in seconds
UPLOAD_MAX_DURATION = 60 # 1 minute

USERNAME = "$USERNAME"
PASSWORD = "$PASSWORD"
GOOGLE_USERNAME = "$UGOOGLE"
GOOGLE_PASSWORD = "$PGOOGLE"
TWITTER_USERNAME = "$UTWITTER"
TWITTER_PASSWORD = "$PTWITTER"

USER_LIMIT = 10

#########
# Paths #
#########

import getpass
USER = getpass.getuser()
if str(os.getenv('SUDO_USER')) != "root" and str(os.getenv('SUDO_USER')) != "None":
    USER = os.getenv('SUDO_USER')

# linux default
HOME_DIR = "/home"
# check for Windows
if os.name == 'nt':
    HOME_DIR = "C:\\Users"
ROOT_PATH = os.path.join(HOME_DIR, USER, ".onlysnarf")

LOG_PATH = os.path.join(ROOT_PATH, "log")
    
DOWNLOAD_PATH = os.path.join(ROOT_PATH, "downloads")
UPLOAD_PATH = os.path.join(ROOT_PATH, "uploads")

CONFIGS_PATH = os.path.join(ROOT_PATH, "conf")
CONFIG_PATH = os.path.join(CONFIGS_PATH, "config.conf")
PROFILE_PATH = os.path.join(CONFIGS_PATH, "profile.json")
USERS_PATH = os.path.join(CONFIGS_PATH, "users")

if str(os.environ.get('ENV')).lower() == "test":
    CONFIG_PATH = os.path.join(os.getcwd(), "OnlySnarf", "conf", "test-config.conf")
    # LOG_PATH = os.path.join(os.getcwd(), "log")

LOG_PATH_SNARF = os.path.join(LOG_PATH, "snarf.log")
LOG_PATH_CHROMEDRIVER = os.path.join(LOG_PATH, "chromedriver.log")
LOG_PATH_CHROMEDRIVER_BRAVE = os.path.join(LOG_PATH, "chromedriver-brave.log")
LOG_PATH_CHROMEDRIVER_CHROMIUM = os.path.join(LOG_PATH, "chromedriver-chromium.log")
LOG_PATH_CHROMEDRIVER_EDGE = os.path.join(LOG_PATH, "chromedriver-edge.log")
LOG_PATH_CHROMEDRIVER_IE = os.path.join(LOG_PATH, "chromedriver-ie.log")
LOG_PATH_CHROMEDRIVER_OPERA = os.path.join(LOG_PATH, "chromedriver-opera.log")
LOG_PATH_GECKODRIVER = os.path.join(LOG_PATH, "geckodriver.log")

Path(ROOT_PATH).mkdir(parents=True, exist_ok=True)
Path(DOWNLOAD_PATH).mkdir(parents=True, exist_ok=True)
Path(UPLOAD_PATH).mkdir(parents=True, exist_ok=True)
Path(CONFIGS_PATH).mkdir(parents=True, exist_ok=True)
Path(USERS_PATH).mkdir(parents=True, exist_ok=True)

USERS_PATH = os.path.join(CONFIGS_PATH, "users.json")

if os.environ.get('ENV') == "test":
    print("###########")
    print("## PATHS ##")
    print("###########")
    print("root: "+ROOT_PATH)
    print("configs: "+CONFIGS_PATH)
    print("config: "+CONFIG_PATH)
    print("users: "+USERS_PATH)
    print("profiles: "+USERS_PATH)
    print("profile: "+PROFILE_PATH)
    print("download: "+DOWNLOAD_PATH)
    print("upload: "+UPLOAD_PATH)
    print("log: "+LOG_PATH)

    # TODO: maybe print out more default settings?
##
# Defaults 
##

ACTIONS = [
	"discount", "message", "post", "profile", "promotion", 
	"bot",
	"test"
]

SOURCES = [ "local",
	"dropbox",
	"google",
	"remote"
]

CATEGORIES = [ "images", "galleries", "videos", "performers" ]

BROWSER_PORT = 4444
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
# 12 = 2 hrs
# 24 = 4 hrs
# 36 = 6 hrs
DURATION_ALLOWED = [1,3,7,30,99]
LIMIT_ALLOWED = [0,1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100]
PROMOTION_EXPIRATION_ALLOWED = [int(i) for i in range(30)]
PROMOTION_EXPIRATION_ALLOWED.insert(0,0)
PROMOTION_OFFER_LIMIT = [0,1,2,3,4,5,6,7,8,9,10]
PROMOTION_DURATION_ALLOWED = ["1 day","3 days","7 days","14 days","1 month","3 months","6 months","12 months"]

# Paths
MOUNT_PATH = "/opt/onlysnarf"
DOWNLOAD_PATH = os.path.join(MOUNT_PATH, "downloads")
CONFIG_PATH = os.path.join(MOUNT_PATH, "config.conf")
GOOGLE_PATH = os.path.join(MOUNT_PATH, "google_creds.txt")
SECRET_PATH = os.path.join(MOUNT_PATH, "client_secrets.json")
USERS_PATH = os.path.join(MOUNT_PATH, "users.json")
PROFILE_PATH = os.path.join(MOUNT_PATH, "profile.json")
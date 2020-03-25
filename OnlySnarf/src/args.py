import argparse, os

CATEGORIES_DEFAULT = [
  "images",
  "galleries",
  "videos"
]
DEFAULT_MESSAGE = ":)"
DEFAULT_GREETING = "hi! thanks for subscribing :3 do you have any preferences?"
DISCOuNT_MAX_AMOUNT = 55
DISCOuNT_MIN_AMOUNT = 10
DISCOUNT_MAX_MONTHS = 7
DISCOUNT_MIN_MONTHS = 1
DURATION_ALLOWED = ["1","3","7","30","99","no limit"]
EXPIRATION_ALLOWED = ["1","3","7","30","99","no limit"]
IMAGE_DOWNLOAD_LIMIT = 6
IMAGE_UPLOAD_LIMIT = 20
IMAGE_UPLOAD_LIMIT_MESSAGES = 5
MESSAGE_CHOICES = ["all", "recent", "favorite"]
PRICE_MINIMUM = 3
UPLOAD_MAX_DURATION = 12 # 2 hours

# Paths
MOUNT_PATH = "/opt/onlysnarf"
DOWNLOAD_PATH = os.path.join(MOUNT_PATH, "downloads")
CONFIG_PATH = os.path.join(MOUNT_PATH, "config.conf")
GOOGLE_PATH = os.path.join(MOUNT_PATH, "google_creds.txt")
SECRET_PATH = os.path.join(MOUNT_PATH, "client_secret.json")
USERS_PATH = os.path.join(MOUNT_PATH, "users.json")

class AttrDict(dict):
  def __init__(self):
    dict.__init__(self)
  # Override getattr and setattr so that they return the values of getitem / setitem
  def __setattr__(self, name, value):
    self[name] = value
  def __getattr__(self, name):
    return self[name]

# overwrites args with config parameters
def read_config(args):
  conf = False 
  if os.path.exists(CONFIG_PATH):
    conf = CONFIG_PATH
  if os.path.exists(getattr(args, "CONFIG_PATH")):
    conf = CONFIG_PATH
  if not conf: return args
  POSTS = AttrDict()
  with open(conf) as f:
    for line in f:
      if str(line[0]) == "#": continue
      try:
        if "\"" in str(line):
          spl = re.split("\"*\"", line)
          key = spl[0] or None
          val = spl[1] or None
        else:
          (key, val) = line.split()
        key = key.strip()
        if str(val)[0] == "\"": val = str(val[1:])
        if str(val)[len(val)-1] == "\"": val = str(val[:len(val)-1])
        # print("{} : {} ".format(key.upper(),val))
        if "_post" in key: setattr(POSTS, key.upper().replace("_post",""), val)
        else: setattr(args, key.upper(), val)
      except Exception as e:
        print("Warning: Error Parsing Config")
        # pass
  setattr(args, "POSTS", POSTS)
  return args

# Validators

def valid_date(s):
  try:
    return datetime.strptime(s, "%Y-%m-%d")
  except ValueError:
    msg = "Not a valid date: '{0}'.".format(s)
    raise argparse.ArgumentTypeError(msg)

def valid_time(s):
  try:
    return datetime.strptime(s, "%H:%M")
  except ValueError:
    msg = "Not a valid time: '{0}'.".format(s)
    raise argparse.ArgumentTypeError(msg)

def valid_price(s):
  try:
    "{:.2f}".format(float(s))
  except ValueError:
    msg = "Not a valid price: '{0}'.".format(s)
    raise argparse.ArgumentTypeError(msg)

def valid_duration(s):
  if str(s) not in DURATION_ALLOWED:
    msg = "Not a valid duration: '{0}'.".format(s)
    raise argparse.ArgumentTypeError(msg)

def valid_expiration(s):
  if str(s) not in EXPIRATION_ALLOWED:
    msg = "Not a valid expiration: '{0}'.".format(s)
    raise argparse.ArgumentTypeError(msg)

def valid_schedule(s):
  try:
    return datetime.strptime(s, "%Y-%m-%d:%H:%M")
  except ValueError:
    msg = "Not a valid schedule: '{0}'.".format(s)
    raise argparse.ArgumentTypeError(msg)

def valid_month(s):
  if int(s) < 1 or int(s) > 12:
    msg = "Not a valid month number: '{0}'.".format(s)
    raise argparse.ArgumentTypeError(msg)

# def valid_discount(s):
  # pass

# def valid_category(s):
#   if str(s) not in CATEGORIES_DEFAULT:
#     msg = "Not a valid category: '{0}'.".format(s)
#     raise argparse.ArgumentTypeError(msg)

# Argument Parser

parser = argparse.ArgumentParser(prog='onlysnarf', allow_abbrev=False, epilog="Shnarrf!", 
  description='Post or send messages to OnlyFans.')
# mutually exclusive
# duration & expiration
durationAndExpiration = parser.add_mutually_exclusive_group()
# schedule and date&time
# scheduleAndDate = parser.add_mutually_exclusive_group()
# scheduleAndTime = parser.add_mutually_exclusive_group()
# discount and amount&duration
#
# -action
# the action to be performed
parser.add_argument('-action', '--action', metavar='action', type=str, 
  help='the action to take', choices=['discount','post','message'], default='post')
##
# -amount
# action: discount
# the amount to discount a user by
parser.add_argument('-amount', '--amount', metavar='amount', type=int, 
  help='the amount (%) to discount by', default=0)
##
# -disable-backup
# backup uploaded content to "posted" folder
parser.add_argument('-disable-backup', '--disable-backup', action='store_true', 
  metavar='disable backup', help='disables backup processes')
##
# -category
# the category of folder to upload from
parser.add_argument('-cat', '-category', '--category', metavar='category', type=str, default='video'
  help='the category of content to post or message')
##
# configurable w/ profile.conf
# OnlySnarf Drive folder list
parser.add_argument('-categories', '--categories', metavar='categories', dest='categories', 
  action='append', help='the categories to list in menu (images, gallery, video)', 
  default=['images','gallery','video'])
##
# -create-drive 
# creates missing OnlySnarf folders in Google Drive
parser.add_argument('-create-drive', '--create-drive', action='store_true', 
  help='creates missing OnlySnarf folders in Google Drive')
##
# -cron
# determines whether script running is a cronjob
parser.add_argument('-cron', '--cron', action='store_true', help='toggle cron behavior')
##
# -cron-user
# the user to run OnlySnarf as
parser.add_argument('-cron-user', '--cron-user', metavar='cron user', type=str, 
  help='the user to run OnlySnarf as', default='root')
##
# -date
# date in MM-DD-YYYY
parser.add_argument('-date', '--date', metavar='date', type=valid_date, default=None,
  help='schedule date (MM-DD-YYYY)')
##
# -debug
# debugging - skips uploading and deleting unless otherwise forced
parser.add_argument('-d', '-debug', '--debug', metavar='debug', action='store_true', 
  help='enable debugging')
##
# -debug-force-save
# forces expiration and poll modals to save instead of cancel when debugging
parser.add_argument('-debug-force-save', '--debug-force-save', action='store_true',
  help='force expiration and poll to save when debugging')
##
# -debug-delay
# user message delay
parser.add_argument('-debug-delay', '--debug-delay', metavar='debug delay', action='store_true', 
  help='enable a wait between crucial steps for debugging')
##
# -delete-google
# delete uploaded content instaed of backing it up
parser.add_argument('-delete-google', '--delete-google', action='store_true', 
  help='delete file instead of backing up')
##
# -discount
# create a format validator for discount where its "[amount]:[duration]"
# parser.add_argument('-discount', '--discount', metavar='discount', type=valid_discount, default=None,
  # help='discount to apply in format [amount]:[duration]')
##
# download path
parser.add_argument('-download-path', '--download-path', metavar='download path', type=str, 
  help='the path to download files to locally', default=DOWNLOAD_PATH)
##
# -duration
# poll or post duration
durationAndExpiration.add_argument('-duration', '--duration', metavar='duration',
  help='the duration', choices=DURATION_ALLOWED, default='{0}')
##
# -expiration
# date of post or poll expiration
durationAndExpiration.add_argument('-expiration', '--expiration', metavar='expiration',
  help='the expiration', choices=EXPIRATION_ALLOWED, default='{0}')
##
# -force-upload
# ignore upload max wait
parser.add_argument('-force-upload', '--force-upload', metavar='force upload', action='store_true', 
  help='ignore upload max wait attempts')
##
# -image-download-limit
# maximum number of images to download
parser.add_argument('-image-download-max', '--image-download-max', type=int, default=IMAGE_DOWNLOAD_LIMIT,
  help='the max number of images to download')
##
# -image-upload-limit
# maximum number of images that can be uploaded
parser.add_argument('-image-upload-max', '--image-upload-max', type=int, default=IMAGE_UPLOAD_LIMIT,
  help='the max number of images to upload')
##
# - image-upload-limit-messages
# maximum number of images that can be uploaded in a message
parser.add_argument('-image-message-max', '--image-message-max', type=int, default=IMAGE_UPLOAD_LIMIT_MESSAGES,
  help='the max number of images to message')
##
# -keywords
# keywords to # in post
parser.add_argument('-keywords', '--keywords', dest='keywords', action='append', 
  help="the keywords (#[keyword]")
##
# -months
# action: discount
# the number of months to discount for
parser.add_argument('-months', '--months', metavar='months', type=valid_month, default=1,
  help='the number of months to discount or apply promotion')
##
# -mount-path
# the mounth path for a local directory of OnlyFans config files
parser.add_argument('-mount-path', '--mount-path', metavar='mount path', type=str, 
  help='the local path to OnlySnarf processes')
##
# -notkeyword
# the keyword to skip in folder selection
parser.add_argument('-notkeywords', '--not-keywords', dest='notkeywords', action='append', 
  help="search for folder not by keywords")
##
# -password
# the password for the OnlyFans / Twitter
parser.add_argument('-password', '--password', metavar='password', type=str, 
  help='the Twitter password for login')
##
# -performers
# list of performers to tag in post
parser.add_argument('-performers', '--performers', dest='performers', action='append', 
  metavar='performers', help='the performers to list (w/ @[performer]')
# -prefer-local
# prefers local user cache over refreshing first call
parser.add_argument('-prefer-local', '--prefer-local', action='store_true', metavar='prefer local', 
  help='prefer recently cached data')
##
# -price
# the price to be set in a message
parser.add_argument('-price', '--price', metavar='price', type=valid_price, help='the price', default=0)
###
### PATHS ###
# -drive-path
# the folder path within Google Drive for OnlySnarf's root folder
parser.add_argument('-drive-path', '--drive-path', metavar='Drive path', type=str, 
  help='the folder path within Drive to root OnlySnarf (/OnlySnarf)')
# -config-path
# the path to the config.conf file
parser.add_argument('-config-path', '--config-path', metavar='config path', type=str, 
  help='the path to list', default=CONFIG_PATH)
# -google-path
# the path to the google_creds.txt
parser.add_argument('-google-creds', '--google-creds', metavar='google creds', type=str, 
  help='the path to Google credentials', default=GOOGLE_PATH)
# the path to the client_secret.json
parser.add_argument('-client-secret', '--client-secret', metavar='client secret', type=str, 
  help='the path to Google secret credentials', default=SECRET_PATH)
# -user-path
# the path to the users.json file
parser.add_argument('-users-path', '--users-path', metavar='users path', type=str, 
  help='the path to cache users locally', default=USERS_PATH)
###
##
# -questions
# poll questions
parser.add_argument('-questions', '--questions', metavar='questions', dest='questions', action='append',
  help='the questions to ask')
###
# the maximum number of recent users
parser.add_argument('-recent-user-count', '--recent-user-count', metavar='recent user count', default=3,
  type=int, help='the number of users to consider recent')
##
# enables file reduction
parser.add_argument('-enable-reduce', '--enable-reduce', metavar='reduce', action='store_true', 
  help='enable reducing files under 50 MB')
##
# enables file repair (buggy)
parser.add_argument('-enable-repair', '--enable-repair', metavar='repair', action='store_true', 
  help='enable repairing videos as appropriate')
##
# can be set in profile.conf
# root Google drive folder
parser.add_argument('-drive-root', '--drive-root', metavar='Drive root', type=str, default='OnlySnarf',
  help='the Google Drive root folder name')
##
# -save-users
# saves OnlyFans users upon exit
parser.add_argument('-save-users', '--save-users', metavar='save users', action='store_true', 
  help='enable saving users locally on exit')
##
# -schedule
# 
parser.add_argument('-schedule', '--schedule', metavar='schedule', type=valid_schedule, default=None,
  help='the schedule (MM-DD-YYYY:HH:MM)')
##
# list of users to skip
parser.add_argument('-skip-users', '--skip-users', metavar='skip users', dest='skip_users', 
  action='append', help='the users to skip or ignore ')
##
# -show-window
# shows window
parser.add_argument('-show','-show-window', '--show-window', metavar='show', action='store_true', 
  help='enable displaying the browser window')
##
# -tags
# @[tag]
parser.add_argument('-tags', '--tags', metavar='tags', dest='tags', action='append',
  help='the tags (@[tag])')
##
# -text
# text for message or upload
parser.add_argument('-text', '--text', metavar='text', type=str, default='',
  help='the text to type')
##
# -time
# time in HH:MM
parser.add_argument('-time', '--time', metavar='time', type=valid_time, default=None,
  help='the time (HH:MM)')
##
# -tweet
# enabled tweeting
parser.add_argument('-tweeting', '--tweeting', metavar='tweeting', action='store_true', 
  help='enable tweeting when posting')
##
# -upload-max
# the max number of 10 minute intervals to upload for
parser.add_argument('-upload-max-duration', '--upload-max-duration', metavar='upload max duration', 
  type=int, help='the number of 10 minute intervals to wait while uploading a file')
##
# -user
# the user to target
parser.add_argument('-user', '--user', metavar='user', type=str,  default=None,
  help='the user to message')
##
# -users
# the users to target
parser.add_argument('-users', '--users', metavar='users', dest='users', action='append',
  help='the users to message')
##
# -users-favorite
# list of favorited users
parser.add_argument('-users-favorite', '--users-favorite', metavar='favorite users', 
  dest='users_favorite', action='append', help='supplied list of favorite users')
##
# -username
# the OnlyFans / Twitter username to use
parser.add_argument('-username', '--username', metavar='username', type=str, default=None,
  help='the Twitter username for login')
##
# -verbose
# v, vv, vvv
parser.add_argument('-v', '-verbose', '--verbose', action='count', default=0, 
  help="verbosity level (max 3)")
##
# -version
# prints version
import pkg_resources
parser.version = str(pkg_resources.get_distribution("onlysnarf").version)
parser.add_argument('-version', '--version', metavar='version', action='version')
############################################################################################
args = vars(parser.parse_args())
CONFIG = {}
for key in args:
  setattr(CONFIG, key.upper(), getattr(args, key))
CONFIG = read_config(CONFIG)
###################################################################
##                          DEPRECATED                           ##
###################################################################
# these have all been moved from optionalargs to config file only #
###################################################################

##
# removed ?/?/2021
##

##
# configurable w/ profile.conf
# OnlySnarf Drive folder list, appends to defaults
parser.add_argument('-categories', dest='categories',
  action='append', help='the categories to list in menu (appends to \'{}\''.format("\'".join(CATEGORIES_DEFAULT)), 
  default=[])
##
# -create-missing 
# creates missing OnlySnarf folders
parser.add_argument('-create-missing', action='store_true', dest='create_missing',
  help='creates missing OnlySnarf folders at target source')

##
# -cron
# determines whether script running is a cronjob
parser.add_argument('-cron', action='store_true', help='toggle cron behavior', dest='cron')
##
# -cron-user
# the user to run OnlySnarf as
parser.add_argument('-cron-user', type=str, dest='cron_user',
  help='the user to run OnlySnarf as', default='root')

##
# -debug-delay
# user message delay
parser.add_argument('-debug-delay', action='store_true', dest='debug_delay',
  help='enable a wait between crucial steps for debugging')

##
# -delete-empty
# delete empty content folders
parser.add_argument('-delete-empty', action='store_true', dest='delete_empty',
  help='delete empty content folders')

##
# download path
parser.add_argument('-download-path', type=str, dest='download_path',
  help='the path to download files to locally', default=DOWNLOAD_PATH)

# Combined / Deleted into new args

##
# -delete-google
# delete uploaded content instaed of backing it up
parser.add_argument('-delete-google', action='store_true', dest='delete_google',
  help='delete file instead of backing up')
##
# -delete
# delete content instaed of backing it up
parser.add_argument('-delete', action='store_true', dest='delete',
  help='delete file instead of backing up')
##
# -download-max
# maximum number of images to download
parser.add_argument('-download-max', type=int, default=IMAGE_DOWNLOAD_LIMIT, dest="download_limit",
  help='the max number of images to download')
##
# -upload-max
# maximum number of images that can be uploaded
parser.add_argument('-upload-max', type=int, default=IMAGE_UPLOAD_LIMIT, dest='upload_max',
  help='the max number of images to upload')

##
# removed 9/9/2022
##

##
# -cookies
# load & save from/to local cookies path
parser.add_argument('-cookies', action='store_true', dest='cookies',
  help='enable loading & saving from/to the local cookies path')

##
# -debug-firefox
# enables trace logging for firefox
parser.add_argument('-debug-firefox', action='store_true', dest='debug_firefox',
  help='enable debugging of firefox')

##
# -debug-google
# enables trace logging for google chrome
parser.add_argument('-debug-chrome', action='store_true', dest='debug_chrome',
  help='enable debugging of google chrome')

##
# -debug-selenium
# enables selenium logging
parser.add_argument('-debug-selenium', action='store_true', dest='debug_selenium',
  help='enable debugging of selenium')

##
# -download-path
# the path to the downloaded files
parser.add_argument('-download-path', type=str, dest='path_download',
  help='the path to download files to', default=DEFAULT.DOWNLOAD_PATH)

##
# -duration-promo
# promotion duration
parser.add_argument('-duration-promo', type=valid_promo_duration, dest='duration_promo',
  help='the duration in days (99 for \'No Limit\') for a promotion', choices=DEFAULT.PROMOTION_DURATION_ALLOWED, default=None)

##
# -email
# the OnlyFans email to use for login
parser.add_argument('-email', type=str, default="", dest='email',
  help='the email for an OnlyFans profile')

##
# -image-download-max
# maximum number of images that can be downloaded / uploaded
parser.add_argument('-image-download-max', type=int, default=DEFAULT.IMAGE_LIMIT, dest='image_download_limit',
  help='the max number of images to download')
##
# -image-upload-max
# maximum number of images that can be downloaded / uploaded
parser.add_argument('-image-upload-max', type=int, default=DEFAULT.IMAGE_LIMIT, dest='image_upload_limit',
  help='the max number of images to upload')

##
# -keywords
# keywords to # in post
parser.add_argument('-keywords', dest='keywords', action='append', default=[], 
  help="the keywords (#[keyword])")

##
# -bykeyword
# the keyword to search for in folder selection
parser.add_argument('-bykeyword', dest='bykeyword', default=None, 
  help="search for folder by keyword")
##
# -notkeyword
# the keyword to skip in folder selection
parser.add_argument('-notkeyword', dest='notkeyword', default=None,
  help="search for folder not by keyword")

##
# -password
# the password for OnlyFans
parser.add_argument('-password', type=str, dest='password',
  help='the OnlyFans user password for login (used with username)')

##
# -password
# the password for Google
parser.add_argument('-password-google', type=str, dest='google_password',
  help='the Google password for login')

##
# -password
# the password for Twitter
parser.add_argument('-password-twitter', type=str, dest='twitter_password',
  help='the Twitter password for login')

##
# -username-google
# the Google username to use
parser.add_argument('-username-google', type=str, default="", dest='google_username',
  help='the Google username for login')

##
# -prefer-local
# prefers local user cache over refreshing first call
parser.add_argument('-prefer-local', default=True, action='store_false', dest='prefer_local',
  help='prefer recently cached data')

##
# -repair
# enables file repair (buggy)
parser.add_argument('-repair', action='store_true', dest='repair',
  help='enable repairing videos as appropriate (buggy)')

##
# -recent-users-count
# the maximum number of recent users
parser.add_argument('-recent-users-count', default=3, dest='recent_users_count',
  type=int, help='the number of users to consider recent')

##
# -reduce
# enables file reduction
parser.add_argument('-reduce', action='store_true', dest='reduce',
  help='enable reducing files over 50 MB')

##
# -skip-download
parser.add_argument('-skip-download', action='store_true', dest='skip_download',
  help='skip file downloads')
##
# -skip-upload
# skips file upload
parser.add_argument('-skip-upload', action='store_true', dest='skip_upload',
  help='skip file uploads')

##
# -title
# the title of a file to search for
parser.add_argument('-title', default=None, dest='title',
  help='the title of the file to search for')

##
# -remote-path
# root remote folder. can be set in profile.conf
parser.add_argument('-remote-path', type=str, default=DEFAULT.REMOTE_PATH, dest='remote_path',
  help='the root remote file sharing folder name')

##
# -remote-host
# the remote host to connect to
parser.add_argument('-remote-host', type=str, dest='remote_host',
  help='the remote host to connect to for file sharing', default="127.0.0.1")

##
# -remote-host
# the remote host to connect to
parser.add_argument('-remote-browser-host', type=str, dest='remote_browser_host',
  help='the remote host to connect to for remote browser', default="127.0.0.1")

##
# -remote-port
# the remote port to connect to
parser.add_argument('-remote-port', type=int, dest='remote_port',
  help='the remote port to connect to for file sharing', default=22)

##
# -remote-browser-port
# the remote port to connect to
parser.add_argument('-remote-browser-port', type=int, dest='remote_browser_port',
  help='the remote port to connect to for remote browser', default=4444)

##
# -remote-username
# the remote username to use
parser.add_argument('-remote-username', type=str, dest='remote_username',
  help='the remote username to use', default=None)

##
# -remote-password
# the remote password to use
parser.add_argument('-remote-password', type=int, dest='remote_password',
  help='the remote password to use', default=None)

##
# -session-id
parser.add_argument('-session-id', default=None, dest='session_id',
  help='the session id to use')

# -session-url
parser.add_argument('-session-url', default=None, dest='session_url',
  help='the session url to use')

##
# list of users to skip
parser.add_argument('-skip-users', dest='skipped_users', 
  action='append', help='the users to skip or ignore ')

##
# -thumbnail
# attempt to fix thumbnail
parser.add_argument('-thumbnail', action='store_true', dest='thumbnail',
  help='fix thumbnails when necessary')

##
# -users-read
# the number of users read when checking messages
parser.add_argument('-users-read', type=int, dest='users_read',
  help='the number of users to read when checking messages', default=10)

## 
# -profile-method
parser.add_argument('-profile-method', dest="profile_method", default="syncfrom", choices=["syncto","syncfrom"],
  help='the profile method to use')

##
# -promotion
# the promotion method to use
parser.add_argument('-promotion-method', dest='promotion_method', default="campaign", choices=["campaign","trial","grandfather","user"],
  help='the promotion method to use')

##
# -promotion-user
parser.add_argument('-promotion-user', dest="promotion_user", action='store_true', 
  help="uses user method when combined with action=promotion")

##
# -user-path
# the path to the users.json file
parser.add_argument('-users-path', type=str, dest='path_users',
  help='the path to cache users locally', default=DEFAULT.USERS_PATH)

##
# -profile-path
# the path to the profile.json file
parser.add_argument('-profile-path', type=str, dest='profile_path',
  help='the path to cache profile locally', default=DEFAULT.PROFILE_PATH)

##
# -root-path
# the root path for a local directory of OnlyFans config files
parser.add_argument('-root-path', dest='root_path',
  help='the local path to OnlySnarf processes')
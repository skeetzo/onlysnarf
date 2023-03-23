###################################################################
##                          DEPRECATED                           ##
###################################################################
# these have all been moved from optionalargs to config file only #
###################################################################

##
# removed 10/4/2021
# mostly temporary
##

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
# -profile-path
# the path to the profile.json file
parser.add_argument('-profile-path', type=str, dest='path_profile',
  help='the path to cache profile locally', default=DEFAULT.PROFILE_PATH)

##
# -promotion-expiration
# expiration for a promotion
parser.add_argument('-promotion-expiration', type=valid_promo_expiration, dest='promotion_expiration',
  help='the promotions expiration in days)', choices=DEFAULT.PROMOTION_EXPIRATION_ALLOWED, default=None)
##
# -promotion-limit
# maximum number of subscribers for a promotion
parser.add_argument('-promotion-limit', type=valid_limit, default=None, dest='promotion_limit', choices=DEFAULT.LIMIT_ALLOWED,
  help='the max number of subscribers allowed for a promotion')

##
# -username-google
# the Google username to use
parser.add_argument('-username-google', type=str, default="", dest='google_username',
  help='the Google username for login')
##
# -username-twitter
# the Twitter username to use
parser.add_argument('-username-twitter', type=str, default="", dest='twitter_username',
  help='the Twitter username for login')

############
## Remote ##
############

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
# removed 9/9/2022
##



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
# -title
# the title of a file to search for
parser.add_argument('-title', default=None, dest='title',
  help='the title of the file to search for')

##
# -session-id
parser.add_argument('-session-id', default=None, dest='session_id',
  help='the session id to use')

# -session-url
parser.add_argument('-session-url', default=None, dest='session_url',
  help='the session url to use')

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
# -root-path
# the root path for a local directory of OnlyFans config files
parser.add_argument('-root-path', dest='root_path',
  help='the local path to OnlySnarf processes')
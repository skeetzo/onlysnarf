
from .validators import valid_amount, valid_price
from .validators import valid_date, valid_month, valid_schedule, valid_time
from .validators import valid_duration, valid_expiration, valid_limit
from .validators import valid_promo_duration, valid_promo_expiration
from . import defaults as DEFAULT

def apply_args(parser):

  # mutually exclusive
  # duration & expiration
  durationAndExpiration = parser.add_mutually_exclusive_group()

  ##########
  ## ARGS ##
  ##########

  ##
  # -amount
  # action: discount
  # the amount to discount a user by
  parser.add_argument('-amount', type=valid_amount, dest='amount',
    help='the amount (%%) to discount by', default=None)
  ##
  # -backup
  # backup uploaded content to designated folder at "destination"
  parser.add_argument('-backup', action='store_true', dest='backup',
    help='enables backup processes')
  ##
  # -browser
  parser.add_argument('-browser', type=str, default="auto", choices=["auto","google","firefox","auto-remote","remote","remote-chrome","remote-firefox","reconnect"], dest='browser',
    help='the web browser to use')
  ##
  # -category
  # the category of folder to upload from
  parser.add_argument('-category', default=None, dest='category',
    help='the category of content to post or message')
  ##
  # -config-path
  # the path to the config.conf file
  parser.add_argument('-config-path', dest="path_config", type=str, 
    help='the path to the config.conf', default=DEFAULT.CONFIG_PATH)
  ##
  # -date
  # date in MM-DD-YYYY
  parser.add_argument('-date', type=valid_date, default=None, dest='date',
    help='schedule date (MM-DD-YYYY)')
  ##
  # -delete
  # delete content after upload
  parser.add_argument('-delete', action='store_true', dest='delete',
    help='delete file instead of backing up')
  ##
  # -destination
  # the destination to use when backing up content
  parser.add_argument('-destination', dest='destination', default=None, choices=["remote","local"],
    help='file backup location. uses same as -source if none specified')
  ##
  # -duration
  # poll duration
  parser.add_argument('-duration', type=valid_duration, dest='duration',
    help='the duration in days (99 for \'No Limit\') for a poll', choices=DEFAULT.DURATION_ALLOWED, default=None)
  ##
  # -expiration
  # date of post or poll expiration
  parser.add_argument('-expiration', type=valid_expiration, dest='expiration',
    help='the expiration in days (99 for \'No Limit\')', choices=DEFAULT.EXPIRATION_ALLOWED, default=None)
  ##
  # -keep
  # keep the browser window open
  parser.add_argument('-keep', action='store_true', dest='keep',
    help='keep the browser window open after scripting ends')
  ##
  # -login
  # the method to prefer when logging in
  parser.add_argument('-login', dest='login', default="auto", choices=["auto","onlyfans","twitter"],
    help='the method of user login to prefer')
  ##
  # -months
  # action: discount
  # the number of months to discount for
  parser.add_argument('-months', type=valid_month, default=None, dest='months',
    help='the number of months to discount or apply promotion')
  ##
  # -performers
  # list of performers to upload matching content of
  parser.add_argument('-performers', dest='performers', action='append',  default=[],
    help='the performers to upload. adds \"w/ @[...performers]\"')
  ##
  # -price
  # the price to be set in a message
  parser.add_argument('-price', type=valid_price, help='the price to charge', default=0, dest='price')
  
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
  ###
  ##
  # -question
  # poll questions
  parser.add_argument('-question', dest='questions', action='append', default=[],
    help='the questions to ask')
  ##
  # -save-users
  # saves OnlyFans users upon exit
  parser.add_argument('-save-users', action='store_true', dest='save_users',
    help='enable saving users locally on exit')
  ##
  # -schedule
  # the schedule to upload a post for
  parser.add_argument('-schedule', type=valid_schedule, default=None, dest='schedule',
    help='the schedule (MM-DD-YYYY:HH:MM)')
  ##
  # -sort
  # the sort method to use when selecting content unprompted
  parser.add_argument('-sort', dest='sort', default="random", choices=["ordered","random","least","greatest"],
    help='the sort method to use when selecting content unprompted')
  ##
  # -source
  # the source to use when searching for content
  parser.add_argument('-source', dest='source', default="local", choices=["remote","local"],
    help='file host location')
  ##
  # -tags
  # @[tag]
  parser.add_argument('-tags', dest='tags', action='append', default=[],
    help='the tags (@[tag])')
  ##
  # -text
  # text for message or upload
  parser.add_argument('-text', default=None, dest='text',
    help='the text to type')
  ##
  # -time
  # time in HH:MM
  parser.add_argument('-time', type=valid_time, default=None, dest='time',
    help='the time (HH:MM)')
  ##
  # -tweet
  # enabled tweeting
  parser.add_argument('-tweet', action='store_true', dest='tweeting',
    help='enable tweeting when posting')
  ##
  # -upload-max
  # the max number of 10 minute intervals to upload for
  parser.add_argument('-upload-max-duration', dest='upload_max_duration', default=DEFAULT.UPLOAD_MAX_DURATION,
    type=int, help='the number of 10 minute intervals to wait while uploading a file')
  ##
  # -user
  # the user to target
  parser.add_argument('-user', type=str,  default=None, dest='user',
    help='the user to target with an action')
  ##
  # -users
  # the users to target
  parser.add_argument('-users', dest='users', action='append', default=[],
    help='the users to target with actions')
  ##
  # -username
  # the OnlyFans username to use
  parser.add_argument('-username', type=str, default="", dest='username',
    help='the OnlyFans username')
  ##
  # -username-twitter
  # the Twitter username to use
  parser.add_argument('-username-twitter', type=str, default="", dest='twitter_username',
    help='the Twitter username for login')

  ###############
  ## DEBUGGING ##
  ###############

  # -debug
  # debugging - skips uploading and deleting unless otherwise forced
  parser.add_argument('-debug', action='store_true', dest='debug',
    help='enable debugging')
  # -force-backup 
  # force backup during debugging
  parser.add_argument('-force-backup', action='store_true', dest='force_backup',
    help='force backup when debugging')
  ##
  # -force-upload
  # ignore upload max wait
  parser.add_argument('-force-upload', action='store_true', dest='force_upload',
    help='ignore upload max wait attempts')
  ##
  # -show
  # shows window
  parser.add_argument('-show','-show-window', dest='show', action='store_true', 
    help='enable displaying the browser window')
  ##
  # -verbose
  # v, vv, vvv
  parser.add_argument('-v', '-verbose', dest="verbose", action='count', default=0, 
    help="verbosity level (max 3)")

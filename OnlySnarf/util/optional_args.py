import argparse
from .validators import valid_amount, valid_price
from .validators import valid_date, valid_month, valid_schedule, valid_time
from .validators import valid_duration, valid_expiration, valid_limit
from .validators import valid_promo_duration, valid_promo_expiration
from . import defaults as DEFAULT

def apply_args(parser):

  subparsers = parser.add_subparsers(help='Include a sub-command to run a corresponding action:')

  ##############
  ## Discount ##
  ##############

  parser_discount = subparsers.add_parser('dicount', help='> discount one or more users')
  ##
  # -amount
  # action: discount
  # the amount to discount a user by
  parser_discount.add_argument('-amount', '-A', type=valid_amount, dest='amount',
    help='the amount (%%) to discount by', default=DEFAULT.AMOUNT_NONE)
  ##
  # -months
  # action: discount
  # the number of months to discount for
  parser_discount.add_argument('-months', '-M', type=valid_month, default=None, dest='months',
    help='the number of months to discount')
  ##
  # -user
  # the user to discount
  parser_discount.add_argument('-user', '-U', type=str,  default=None, dest='user',
    help='the user to discount')
  ##
  # -users
  # the users to discount
  parser_discount.add_argument('-users', '-Us', dest='users', action='append', default=[],
    help='the users to discount')

  #############
  ## Message ##
  #############

  parser_message = subparsers.add_parser('message', help='> send a message to one or more users')
  dateAndSchedule = parser_message.add_mutually_exclusive_group()

  ##
  # -date
  # date in MM-DD-YYYY
  dateAndSchedule.add_argument('-date', type=valid_date, default=DEFAULT.DATE, dest='date',
    help='schedule date (MM-DD-YYYY)')
  ##
  # -price
  # the price to be set in a message
  parser_message.add_argument('-price', '-P', type=valid_price, help='the price to charge', default=0, dest='price')
  ##
  # -schedule
  # the schedule to upload a post for
  dateAndSchedule.add_argument('-schedule', type=valid_schedule, default=DEFAULT.SCHEDULE, dest='schedule',
    help='the schedule (MM-DD-YYYY:HH:MM:SS)')
  ##
  # -time
  # time in HH:MM
  parser_message.add_argument('-time', type=valid_time, default=DEFAULT.TIME, dest='time',
    help='the time (HH:MM)')
  ##
  # -tags
  # @[tag]
  # parser_message.add_argument('-tags', dest='tags', action='append', default=[], help='the tags (@[tag])')
  ##
  # -text
  # text for message or upload
  parser_message.add_argument('-text', '-T', default=None, dest='text', help='the text to send')
  ##
  # -user
  # the user to message
  parser_message.add_argument('-user', '-U', type=str,  default=None, dest='user',
    help='the user to message')
  ##
  # -users
  # the users to message
  parser_message.add_argument('-users', '-Us', dest='users', action='append', default=[],
    help='the users to message')

  ##########
  ## Post ##
  ##########

  parser_post = subparsers.add_parser('post', help='> upload a post')
  dateAndSchedule = parser_post.add_mutually_exclusive_group()
  durationAndExpiration = parser_post.add_mutually_exclusive_group()

  ##
  # -date
  # date in MM-DD-YYYY
  dateAndSchedule.add_argument('-date', type=valid_date, default=DEFAULT.DATE, dest='date', help='schedule date (MM-DD-YYYY)')
  ##
  # -duration
  # poll duration
  durationAndExpiration.add_argument('-duration', type=valid_duration, dest='duration',
    help='the duration in days (99 for \'No Limit\') for a poll', choices=DEFAULT.DURATION_ALLOWED, default=DEFAULT.DURATION_NONE)
  ##
  # -expiration
  # date of post or poll expiration
  durationAndExpiration.add_argument('-expiration', type=valid_expiration, dest='expiration', help='the expiration in days (999 for \'No Limit\')', default=DEFAULT.EXPIRATION_NONE)
  ##
  # -price
  # the price to be set in a message
  parser_post.add_argument('-price', '-P', type=valid_price, help='the price to charge', default=0, dest='price')
  ##
  # -schedule
  # the schedule to upload a post for
  dateAndSchedule.add_argument('-schedule', type=valid_schedule, default=DEFAULT.SCHEDULE, dest='schedule', help='the schedule (MM-DD-YYYY:HH:MM:SS)')
  ##
  # -time
  # time in HH:MM
  parser_post.add_argument('-time', type=valid_time, default=DEFAULT.TIME, dest='time', help='the time (HH:MM)')
  ##
  # -tags
  # @[tag]
  parser_post.add_argument('-tags', dest='tags', action='append', default=[], help='the tags (@[tag])')
  ##
  # -text
  # text for message or upload
  parser_post.add_argument('-text', '-T', default=None, dest='text', help='the text to send')
  ##
  # -question
  # poll questions
  parser_post.add_argument('-poll', dest='questions', action='append', default=[], help='the questions to ask for a poll')

  #############
  ## General ##
  #############

  ##
  # -backup
  # backup uploaded content to designated folder at "destination"
  parser.add_argument('-backup', '-Bu', action='store_true', dest='backup', help='enables backup processes')
  ##
  # -browser
  parser.add_argument('-browser', '-B', type=str, default="auto", choices=["auto","chrome","firefox","remote", "remote-chrome","remote-firefox","reconnect","reconnect-chrome","reconnect-firefox"], dest='browser',
    help='the web browser to use')
  ##
  # -category
  # the category of folder to upload from
  # parser.add_argument('-category', default=DEFAULT.CATEGORY_NONE, dest='category',
    # help='the category of content to post or message')
  ##
  # -delete
  # delete content after upload
  parser.add_argument('-delete', action='store_true', dest='delete', help='delete file instead of backing up')
  ##
  # -destination
  # the destination to use when backing up content
  # parser.add_argument('-destination', dest='destination', default=None, choices=["remote","local"], help='file backup location. uses same as -source if none specified')
  ##
  # -login
  # the method to prefer when logging in
  parser.add_argument('-login', '-L', dest='login', default="auto", choices=["auto","onlyfans","twitter"], help='the method of user login to prefer')
  ##
  # -performers
  # list of performers to upload matching content of
  # parser.add_argument('-performers', dest='performers', action='append',  default=[],
  #   help='the performers to upload. adds \"w/ @[...performers]\"')
  ##
  # -save-users
  # saves OnlyFans users upon exit
  parser.add_argument('-save-users', '-Su', action='store_true', dest='save_users', help='enable saving users locally on exit')
  ##
  # -sort
  # the sort method to use when selecting content unprompted
  # parser.add_argument('-sort', dest='sort', default="random", choices=["ordered","random","least","greatest"],
    # help='the sort method to use when selecting content unprompted')
  ##
  # -source
  # the source to use when searching for content
  # parser.add_argument('-source', dest='source', default="local", choices=["remote","local"], help='file host location')
  ##
  # -tweet
  # enabled tweeting
  parser.add_argument('-tweet', action='store_true', dest='tweeting', help='enable tweeting when posting')
  ##
  # -username
  # the OnlyFans username to use
  parser.add_argument('-username', '-OF', type=str, default="", dest='username', help='the OnlyFans username to use')

  ###############
  ## DEBUGGING ##
  ###############

  ##
  # -config
  # the path to the config.conf file
  parser.add_argument('-config', '-C', dest="path_config", type=str, help='the path to the config.conf', default=DEFAULT.CONFIG_PATH)
  ##
  # -cookies
  # load & save from/to local cookies path
  parser.add_argument('-cookies', action='store_true', dest='cookies', help=argparse.SUPPRESS)
  # -debug
  # debugging - skips uploading and deleting unless otherwise forced
  parser.add_argument('-debug', '-D', action='store_true', dest='debug', help='enable debugging')
  ##
  # -debug-delay
  # user message delay
  parser.add_argument('-debug-delay', '-DD', action='store_true', dest='debug_delay', help=argparse.SUPPRESS)
  ##
  # -debug-firefox
  # enables trace logging for firefox
  parser.add_argument('-debug-firefox', action='store_true', dest='debug_firefox', help=argparse.SUPPRESS)
  ##
  # -debug-google
  # enables trace logging for google chrome
  parser.add_argument('-debug-chrome', action='store_true', dest='debug_chrome', help=argparse.SUPPRESS)
  ##
  # -debug-selenium
  # enables selenium logging
  parser.add_argument('-debug-selenium', action='store_true', dest='debug_selenium', help=argparse.SUPPRESS)
  ##
  # -download-max
  # maximum number of images to download
  parser.add_argument('-download-max', type=int, default=DEFAULT.IMAGE_LIMIT, dest="download_limit", help=argparse.SUPPRESS)
  ##
  # -download-path
  # the path to the downloaded files
  parser.add_argument('-download-path', type=str, dest='path_download', default=DEFAULT.DOWNLOAD_PATH, help=argparse.SUPPRESS)
  # -force-backup 
  # force backup during debugging
  parser.add_argument('-force-backup', action='store_true', dest='force_backup', help=argparse.SUPPRESS)
  ##
  # -force-upload
  # ignore upload max wait
  parser.add_argument('-force-upload', action='store_true', dest='force_upload', help=argparse.SUPPRESS)
  ##
  # -keep
  # keep the browser window open
  parser.add_argument('-keep', '-K', action='store_true', dest='keep', help='keep the browser window open after scripting ends')
  ##
  # -show
  # shows window
  parser.add_argument('-show', '-show-window', '-SW', dest='show', action='store_true',  help='enable displaying the browser window')
  ##
  # -skip-download
  parser.add_argument('-skip-download', action='store_true', dest='skip_download', help=argparse.SUPPRESS)
  ##
  # -skip-upload
  # skips file upload
  parser.add_argument('-skip-upload', action='store_true', dest='skip_upload', help=argparse.SUPPRESS)
  ##
  # -skip-users
  # list of users to skip
  parser.add_argument('-skip-users', dest='skipped_users', action='append', help=argparse.SUPPRESS)
  ##
  # -upload-max
  # maximum number of images that can be uploaded
  parser.add_argument('-upload-max', type=int, default=DEFAULT.IMAGE_LIMIT, dest='upload_max', help=argparse.SUPPRESS)
  ##
  # -upload-max-duration
  # the max number of 10 minute intervals to upload for
  parser.add_argument('-upload-max-duration', dest='upload_max_duration', default=DEFAULT.UPLOAD_MAX_DURATION, type=int, help=argparse.SUPPRESS)
  ##
  # -user-path
  # the path to the users.json file
  parser.add_argument('-users-path', type=str, dest='path_users', default=DEFAULT.USERS_PATH, help=argparse.SUPPRESS)
  ##
  # -verbose
  # v, vv, vvv
  parser.add_argument('-v', '-verbose', dest="verbose", action='count', default=0, help="verbosity level (max 3)")


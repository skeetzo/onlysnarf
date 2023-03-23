import argparse
from .validators import valid_amount, valid_price, valid_path
from .validators import valid_date, valid_month, valid_schedule, valid_time
from .validators import valid_duration, valid_expiration, valid_limit
from .validators import valid_promo_duration, valid_promo_expiration
from . import defaults as DEFAULT

def apply_args(parser):

  #############
  ## General ##
  #############

  ##
  # -browser
  parser.add_argument('-browser', '-B', type=str, default="auto", choices=["auto","brave","chrome","chromium","firefox","remote"], dest='browser', help='web browser to use')
  # parser.add_argument('-browser', '-B', type=str, default="auto", choices=["auto","brave","chrome","chromium","firefox","ie","edge","opera","remote"], dest='browser', help='web browser to use')
  ##
  # -login
  # method to prefer when logging in
  parser.add_argument('-login', '-L', dest='login', default="auto", choices=["auto","onlyfans","twitter"], help='method of user login to prefer')
  ##
  # -reduce
  # enables file reduction
  parser.add_argument('-reduce', action='store_true', dest='reduce', help='enable reducing files over 50 MB')
  ##
  # --save
  # saves OnlyFans users upon exit
  parser.add_argument('-save', '-S', action='store_true', dest='save_users', help='enable saving users locally on exit')
  ##
  # -tweet
  # enabled tweeting
  parser.add_argument('-tweet', action='store_true', dest='tweeting', help='enable tweeting when posting')
  ##
  # -username
  # OnlyFans username to use
  parser.add_argument('--username', '--u', type=str, default="", dest='username', help='OnlyFans username to use')

  ###############
  ## DEBUGGING ##
  ###############

  ##
  # -config
  # path to config.conf file
  parser.add_argument('-config', '-C', dest="path_config", type=str, help='path to config.conf', default=DEFAULT.CONFIG_PATH)
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
  parser.add_argument('-debug-delay', action='store_true', dest='debug_delay', help=argparse.SUPPRESS)
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
  ##
  # -force-upload
  # ignore upload max wait
  parser.add_argument('-force-upload', action='store_true', dest='force_upload', help=argparse.SUPPRESS)
  ##
  # -keep
  # keep the browser window open
  parser.add_argument('-keep', '-K', action='store_true', dest='keep', help='keep browser window open after scripting ends')
  ##
  # -prefer-local
  # prefers local user cache over refreshing first call
  parser.add_argument('-prefer-local', default=True, action='store_false', dest='prefer_local', help='prefer recently cached data')
  ##
  # -show
  # shows window
  parser.add_argument('-show', '-SW', dest='show', action='store_true',  help='enable displaying browser window')
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


def apply_subcommand_args(parser):

  subparsers = parser.add_subparsers(help='Include a sub-command to run a corresponding action:', dest="action", required=True)

  ##############
  ## Discount ##
  ##############

  parser_discount = subparsers.add_parser('discount', help='> discount one or more users')
  userAndUsers = parser_discount.add_mutually_exclusive_group()
  ##
  # -amount
  # action: discount
  # the amount to discount a user by
  parser_discount.add_argument('-amount', type=valid_amount, dest='amount', help='amount (%%) to discount by', default=DEFAULT.AMOUNT_NONE)
  ##
  # -months
  # action: discount
  # the number of months to discount for
  parser_discount.add_argument('-months', type=valid_month, default=None, dest='months', help='number of months to discount')
  ##
  # -user
  # the user to discount
  userAndUsers.add_argument('-user', type=str,  default=None, dest='user', help='user to discount')
  ##
  # -users
  # the users to discount
  userAndUsers.add_argument('-users', dest='users', action='append', default=[], help='users to discount')

  #############
  ## Message ##
  #############

  parser_message = subparsers.add_parser('message', help='> send a message to one or more users')
  dateAndSchedule = parser_message.add_mutually_exclusive_group()
  userAndUsers = parser_message.add_mutually_exclusive_group()
  ##
  # -date
  # date in MM-DD-YYYY
  dateAndSchedule.add_argument('-date', type=valid_date, default=DEFAULT.DATE, dest='date', help='schedule date (MM-DD-YYYY)')
  ##
  # -performers
  # list of performers to tag
  parser_message.add_argument('-performers', dest='performers', action='append',  default=[], help='performers to reference. adds \"@[...performers]\"')
  ##
  # -price
  # the price to be set in a message
  parser_message.add_argument('-price', type=valid_price, help='price to charge ($)', default=0, dest='price')
  ##
  # -schedule
  # the schedule to upload a post for
  dateAndSchedule.add_argument('-schedule', type=valid_schedule, default=DEFAULT.SCHEDULE, dest='schedule', help='schedule (MM-DD-YYYY:HH:MM:SS)')
  ##
  # -time
  # time in HH:MM
  parser_message.add_argument('-time', type=valid_time, default=DEFAULT.TIME, dest='time', help='time (HH:MM)')
  ##
  # -tags
  # @[tag]
  parser_message.add_argument('-tags', dest='tags', action='append', default=[], help='the tags (@[tag])')
  ##
  # -text
  # text for message or upload
  parser_message.add_argument('-text', default=None, dest='text', help='text to send')
  ##
  # -user
  # the user to message
  userAndUsers.add_argument('-user', type=str,  default=None, dest='user', help='user to message')
  ##
  # -users
  # the users to message
  userAndUsers.add_argument('-users', dest='users', action='append', default=[], help='users to message')
  ##
  # input
  parser_message.add_argument('input', default=[], nargs=argparse.REMAINDER, type=valid_path, help='one or more paths to files (or folder) to include in the message')

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
    help='duration in days (99 for \'No Limit\') for a poll', choices=DEFAULT.DURATION_ALLOWED, default=DEFAULT.DURATION_NONE)
  ##
  # -expiration
  # date of post or poll expiration
  durationAndExpiration.add_argument('-expiration', type=valid_expiration, dest='expiration', help='expiration in days (999 for \'No Limit\')', default=DEFAULT.EXPIRATION_NONE)
  ##
  # -performers
  # list of performers to tag
  parser_post.add_argument('-performers', dest='performers', action='append',  default=[], help='performers to reference. adds \"@[...performers]\"')
  ##
  # -price
  # price to be set in a message
  parser_post.add_argument('-price', type=valid_price, help='price to charge ($)', default=0, dest='price')
  ##
  # -schedule
  # schedule to upload a post for
  dateAndSchedule.add_argument('-schedule', type=valid_schedule, default=DEFAULT.SCHEDULE, dest='schedule', help='schedule (MM-DD-YYYY:HH:MM:SS)')
  ##
  # -time
  # time in HH:MM
  parser_post.add_argument('-time', type=valid_time, default=DEFAULT.TIME, dest='time', help='time (HH:MM)')
  ##
  # -tags
  # @[tag]
  parser_post.add_argument('-tags', dest='tags', action='append', default=[], help='tags (@[tag])')
  ##
  # -text
  # text for message or upload
  parser_post.add_argument('-text', default=None, dest='text', help='text to send')
  ##
  # -question
  # poll questions
  parser_post.add_argument('-question', '-Q', dest='questions', action='append', default=[], help='questions to ask')
  ##
  # input
  parser_post.add_argument('input', default=[], nargs=argparse.REMAINDER, type=valid_path, help='one or more paths to files (or folders) to include in the post')

  ##########
  ## User ##
  ##########

  parser_user = subparsers.add_parser('users', help='> scan & save users')

def apply_shim_args(parser):
  parser.add_argument('-amount', type=valid_amount, dest='amount', help='amount (%%) to discount by', default=DEFAULT.AMOUNT_NONE)
  parser.add_argument('-months', type=valid_month, default=None, dest='months', help='number of months to discount')
  parser.add_argument('-user', type=str,  default=None, dest='user', help='user to discount')
  parser.add_argument('-users', dest='users', action='append', default=[], help='users to discount')
  parser.add_argument('-date', type=valid_date, default=DEFAULT.DATE, dest='date', help='schedule date (MM-DD-YYYY)')
  parser.add_argument('-price', type=valid_price, help='price to charge ($)', default=0, dest='price')
  parser.add_argument('-schedule', type=valid_schedule, default=DEFAULT.SCHEDULE, dest='schedule', help='schedule (MM-DD-YYYY:HH:MM:SS)')
  parser.add_argument('-time', type=valid_time, default=DEFAULT.TIME, dest='time', help='time (HH:MM)')
  parser.add_argument('-tags', dest='tags', action='append', default=[], help='the tags (@[tag])')
  parser.add_argument('-text', default=None, dest='text', help='text to send')
  parser.add_argument('-duration', type=valid_duration, dest='duration', help='duration in days (99 for \'No Limit\') for a poll', choices=DEFAULT.DURATION_ALLOWED, default=DEFAULT.DURATION_NONE)
  parser.add_argument('-expiration', type=valid_expiration, dest='expiration', help='expiration in days (999 for \'No Limit\')', default=DEFAULT.EXPIRATION_NONE)
  parser.add_argument('-question', '-Q', dest='questions', action='append', default=[], help='questions to ask')
  parser.add_argument('input', default=[], nargs=argparse.REMAINDER, type=valid_path, help='one or more paths to files (or folder) to include in the message')

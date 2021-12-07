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


## Combined / Deleted into new args

# ##
# # -delete-google
# # delete uploaded content instaed of backing it up
# parser.add_argument('-delete-google', action='store_true', dest='delete_google',
#   help='delete file instead of backing up')

# ##
# # -delete
# # delete content instaed of backing it up
# parser.add_argument('-delete', action='store_true', dest='delete',
#   help='delete file instead of backing up')




# ##
# # -download-max
# # maximum number of images to download
# parser.add_argument('-download-max', type=int, default=IMAGE_DOWNLOAD_LIMIT, dest="download_limit",
#   help='the max number of images to download')
# ##
# # -upload-max
# # maximum number of images that can be uploaded
# parser.add_argument('-upload-max', type=int, default=IMAGE_UPLOAD_LIMIT, dest='upload_max',
#   help='the max number of images to upload')


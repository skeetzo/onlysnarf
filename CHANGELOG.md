# OnlySnarf  

## Changelog  
**0.0.1 : 9/25/2018**
  - code organized
  **0.0.2 : 10/20/2018**
  - python package organized
  **0.0.3 : 1/14/2019**
  - sync with DBot updates; while loop upload
  **0.0.4 : 1/21/2019**
  - upload fix & hashtagging
  **0.0.5 : 1/29/2019**
  - demo
  **0.1.0 : 2/3/2019**
  - menu
  - package & setup.py
  **0.1.1 : 2/4/2019**
  - menu fixes
  **0.1.2 : 2/7/2019**
  - config.py
  - script names updated
  - readme updated
  **2/9/2019**
  - fuck you PyDrive
  **0.1.3 : 2/24/2019**
  - jpeg
  **0.1.4 : 3/4/2019**
  - mount path
  **0.1.5 : 3/7/2019**
  - updated send_post_button refs
  **0.1.6 : 3/19/2019**
  - module separation
  **0.1.7 : 3/28/2019**
  - settings.py
  - user.py
  **0.1.8 : 3/31/2019**
  - debugging
  - Drive API for mp4 downloads
  **0.2.0 : 4/10/2019**
  - User: read_chat
  **0.2.1 : 4/12/2019**
  - upload performer
  - upload scene
  **0.2.2 : 4/15/2019**
  - settings now actually updates
  - settings globals -> class
  **4/16/2019**
  - fucking default variables
**1.0.0 : Release : 4/22/2019**
  - save image_name instead of path
  - uploaded to pip
  **1.0.1**
  - removed video.mp4
  **1.0.2**
  - minor adjustments
  **1.0.3 : 5/3/2019**
  - minor bug fixes
  **1.0.4 : 5/8/2019**
  - more minor bug fixes
  **1.1.0 : 5/12/2019**
  - added: (settings).MOUNT_DRIVE, ROOT_FOLDER, DRIVE_FOLDERS, CREATE_MISSING_FOLDERS
  - create Google folder structure programmatically
  - predefine Google root
  **5/14/2019**
  - removed: settings.TYPE
  - added: settings profile -> skeetzo
  - updated: scenes to include trailer addition
  **1.1.1 : 5/23/2019**
  - fixed tweeting bug
  - todo priority queue
  **1.1.2 : 5/25/2019**
  - added: cron.py
  - |_ needs a menu system to be added
  **1.1.3 : 6/26/2019**
  - fixed file & directory uploads
  - removed config initialization from google.py
  - updated ReadMe
  **1.1.4**
  - fixed MANIFEST and credentials
  **1.1.5**
  - removed credentials
  **1.1.6**
  - relative imports -> absolute
  - fixed messaging: input price
  **1.1.7 : 7/3/2019**
  - collapsed upload_file & upload_directory into upload_to
  **1.1.8 : 7/19/2019**
  - fixed user scrape css
  **1.1.9 : 8/14/2019**
  - fixed user scrape css again
  **1.1.10 : 8/21/2019**
  - really really fixed user scrape css
  - removed apiclient from setup.py
  **1.2.0 : 9/2/2019**
  - fixed user scrape & cache
  - added promotions (unfinished)
  **1.2.1 : 9/4/2019**
  - removed innate debug profiles and added profile.conf
  - added google creds to onlysnarf-config
  - updated readme to reflect creds process
  **1.2.2 : 9/5/2019**
  - fixed user scrape & messaging
  - fixed messaging by username
  **1.3.0 : 9/8/2019**
  - finished testing promotions- unworkable w/o email or clipboard utility
  - finished testing messages & user selection
  - hidden unworking functions in menu w/o debug
  **1.3.1 : 9/9/2019**
  - error messages cleanup in user messaging
  **1.3.2 : 9/10/2019**
  - submit button works again
  - added: way to select google drive file to message
  **1.3.3 : 9/15/2019**
  - package install fix & dynamic version in menu
  **1.3.4 : 9/15/2019**
  - menu cleanup
  **1.4.0 : 9/15/2019**
  - chromedriver binary version set = 77.0.3865.40
  - added catch for image upload error
  **1.4.1 : 9/16/2019**
  - cleaned print & maybePrint outputs
  - cleaned up settings.py
  - cron cleanup
  **1.4.2 : 9/17/2019**
  - text fix
  - fixed verbose output
  **1.4.3 : 9/21/2019**
  - dbot issue
**2.0.0 : 9/25/2019**
  - added functionality to choose instead of random
  **2.0.1**
  - oops
  **2.1.0 9/29/2019**
  - discount: all or select users x% for n months
  - fixed local user load
  - updated User(mess=mess) -> User(data)
  **2.1.1**
  - shameless 2.1.0 fix
  **2.2.0**
  - cleaned up & mostly fixed release via selection
  - cleaned up release via random
  - nonrandom uploads now confirm entered information
  - cleaned out user methods from driver -> static
  - updated download_performers and seperated randomizing selection
  **2.2.1**
  - release: keywords and performers can be deleted
  **2.2.2**
  - standalone script bug
  **2.2.3**
  - removed pointless User cache -> fixed User count bug
  - removed overwrite-local
  - added BROWSER.url checks
  **2.2.4**
  - user selections -> debug
  **2.3.0**
  - added: post
  **2.4.0**
  - settings cleanup
  - release -> upload
  - onlyfans var cleanup
  - added local input
  - added posts beginning -> needs configparser
  **2.5.0 : 10/5/2019**
  - configparser -> profile.conf updated
  - posts & text prompt
  - functionality to create a post w/ text
  |_ create multiple basic posts such as "greetings" or "going on holiday" or a trip, or question of what to post more of?
  |_ a menu of standardized posts like above
  |_ a menu of questions|greetings to message to users
  - added: easier way to select local file to upload
  **2.5.1**
  - more verbose cleanup
  **2.6.0**
  - config cleanup
  |_ profile.conf & posts.conf & config.json -> config.conf
  - added: cron feature for adding, deleting, listing crons
  - added: Twitter login prompt
  - added: `local` setting
  - added check for failed login
  - added post: "OnlySnarf Bot commands: !pic | !pic dick | !pic ass"
  **2.6.1**
  - creds cleanup
  **2.7.0**
  - menu sort
  - onlysnarfpy
  **2.7.1**
  - driver auth fix
  - cron fix
  **2.8.0 : 10/8/2019**
  - added Expiration
  - added Schedule
  - added: Poll
  - upload a gallery to a message
  **2.9.0**
  - a post that advertises custom requests
  - a post that advertises tipping price for messaging
  - a post that advertises prices for paid messages for individual photo requests
  - a post for requesting people to comment or dm me individuals they'd like to see me with
  - a post thanking followers for being followers
  **2.9.1**
  - args fix: keywords, performers, input
  **2.9.2**
  - text fix
  **2.9.3**
  - add video reduce to somewhere it can impact INPUT files
  **2.9.4**
  - input bug?
  **2.10.0**
  - discount css update
  - message image upload fix
  - added gifs
  **2.11.0**
  - OFKEYWORD - specifies random folder
  **2.11.1**
  - oops
  **2.11.2**
  - oops
  **2.11.3**
  - oopsies
  **2.11.4**
  - more oopsies
  **2.12.0**
  - added setting: skip-backup
  **2.12.1**
  - fixed BYKEYWORD bug preventing random upload
  - fixed messaging folder of images
  **2.13.0**
  - fixed: skip-backup
  - added: skip-delete-google

----------------------------------------

## ToDo

### Low Priority
  - add: read messages html for emojis
  - update: backup function to include original folder name -> posted/galleries/$file
  - [MESSAGES] layout in config for preset message formats
  - bot functionality to check posts for quiz answers

### Medium Priority

  -> Promotions
  - add email|Twitter functionality for sending trial link; add clipboard function to copy link

  -> Scenes - FIX
  - update: data.txt for scenes with trailer
  - update: scene to include trailer
  - update: upload trailer same time as previews instead of content
  - add: feature for if missing scene previews to capture thumbnail from content/trailer
  - rewrite scene release to NOT upload until releaseDate days after
  -- requires daily check or cron job
  - add: scene feature to check data.txts for content to release n days after trailer/preview
  - prepare: a scene for release
  |_ requires: scene cron feature

### High Priority  

  -> Cron
  - bot functionality that checks user messages for bot commands
  - ability to download images to upload / send later

  -> Twitter
  - tweet reminders
  - can enter text that is tweeted
  - any links to include (counts against text limit) of content or images
  - must not spam, must follow a schedule. monthly, weekly on a day, daily at an hour
  -- maybe delete previous tweets?
  - maybe tweet once and pin it?

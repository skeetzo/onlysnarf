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
  
----------------------------------------

## ToDo

### Low Priority
  - add: read messages html for emojis
  - finalize / fix: script exit
  - add: Twitter (social media reminders)
  - update: backup function to include original folder name -> posted/galleries/$file
  - add: feature for if missing scene previews to capture thumbnail from content/trailer
  - add: easier way to select local file to upload

### Medium Priority
  - add: login prompt for saving Twitter password -> base64 hash instead of in config.json
  |_ add: `Auth` option to settings?
  - add: `local` setting

  - update: data.txt for scenes with trailer
  - update: scene to include trailer
  - update: upload trailer same time as previews instead of content

  - add email functionality for sending trial link; add clipboard function to copy link

### High Priority
  - prepare: a scene for release
  |_ requires: scene cron feature

  - rewrite scene release to NOT upload until releaseDate days after
  -- requires daily check or cron job

  - test: performers upload w/ change to images/videos preferences

  - add: same change to other folder download preferences
  |_ ? which change
  - add: scene feature to check data.txts for content to release n days after trailer/preview
  |_ requires: cron feature
  - add: cron feature for installing crons
  |_ all it has to do is write to the crontab file

Performers mostly advertise on Twitter
- so add a feature that routinely tweets defined reminders
- text that is tweeted
- any links to include (counts against text limit)
- must support emojis
- must not spam, must follow a schedule. monthly, weekly on a day, daily at an hour
- maybe delete previous tweets?
- maybe tweet once and pin it?

General Solutions:
- needs to solve fanbase interaction for someone like me who really doesn't get it get it
  - it should ask fans what more of they want to see
    - add: ability to post polls
  - it should message fans individually more of what they want to see
    - add: ask all new users their preferences; run once for existing users
- it should backup sent message/images differently than the current posted folder -> why?
- it should ask users what they like and then build its own profile and then message that user approrpiately -> "do you like dick pics or ass pics?" -> n days later -> here's a dick pic just for you ;)"

-> Cron that checks user messages for bot commands
 - post: "OnlySnarf Bot commands: !pic | !pic dick | !pic ass"
-- sends [pic] to [user]
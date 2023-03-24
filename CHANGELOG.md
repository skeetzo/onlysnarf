# Changelog  

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
  **1.0.0 : Production : 4/22/2019**
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
  - replaced: settings.TYPE - settings.ACTION
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
  **2.13.1**
  - fixed fixed: skip-backup
  - fixed: enter upload
  **2.13.2**
  - updated: google mimetypes
  **2.14.0**
  - added: NOTKEYWORD for excluding folders by keyword
  **2.14.1**
  - updated: upload_to_OnlyFans w/ more error checks in attempt to fix below bug
  - BUG: does not find "send_post_button" from chromebook ubuntu laptop using ChromeDriver 74.0.3729.6 | Google Chrome 74.0.3729.131
  - cleaned up settings.py comments
  - added: remember me upon login is checked, does nothing
  **2.14.2**
  - added: error_checker for not found elements
  **2.14.3**
  - fixed: user scrapes
  - updated: config.py, unable to test
  **2.14.4**
  - class reorg
  - added 'dynamic' element searching
  - fixed css elements for major functions
  - added element.py
  **2.15.0**
  - major functionality restored
  **2.15.1**
  - fixed menu
  - added -version flag
  **2.15.2**
  - settings options debugging
  - added: tabbing to inputs
  - undid tabbing to inputs -> unpredictable odd behavior
  - minor random debugging (??wtf?)
  - xmas scripts
  **2.15.3**
  - better sorted test scripts
  - changed error_window:filename fix to just closing window
  - fixed mimetype upload (sorta)
  **2.15.4**
  - updated test scripts output
  - added setting: verbosest
  - cleaned up driver&profile elements
  **2.15.5**
  - more settings prep
  - minor fixes to login
  **2.16.0**
  - fixed: post
  - updated menu.md
  **2.16.1**
  - fixed: browser closes now
  **2.16.2**
  - more Settings integration
  - updated method of messaging all, recent, favorite
  **2.16.3**
  - OnlySnarf classname -> Snarf
  - updated profile init
  **2.16.4**
  - minor bugs
  **2.16.5**
  - updated BYKEYWORD and NOTKEYWORD -> str != str
  **2.16.6**
  - fixed: message all price submit
  - fixed: random files now properly downloaded, again
  **2.16.7**
  - fixed: messageAll
  - fixed: go_to_page
  **2.16.8**
  - update: go_to_* auths first
  - added: following_get
  **2.16.9**
  - update: users_get, following_get -> speed +, reliability +
  - mostly functional
  **2.16.10** debugging pre 2.17.0
  - upload -> post
  - Message, File, Google_File, Google_Folder, Video, Image classes
  - ffmpeg.py
  - login function cleaned up / spawn_browser
  - settings -> argsparse
  - menu cleaned up
  - file system selection cleaned up
  - category
  **2.17.0**
  - massive spaghetti -> api overhaul
  - new menu
  **2.17.1**
  - fixed packaging
  **2.17.2**
  - fixed post/message w/o prompt
  **2.17.3**
  - fucking a
  **2.17.4**
  - fixed google uploads w/o prompt
  **2.17.5**
  - fixed video extensions
  **2.17.6**
  - increased UPLOAD_MAX_DURATION to 6 hrs
  - minor fixes to menu input
  **2.17.7**
  - fixed backup pathing
  - fixed file upload max
  **2.17.8**
  - added remote webdriver operations
  - added firefox
  - add performers; debugging
  **2.17.9**
  - debugged 2.17.8
  **2.17.10**
  - removed moviepy
  - exit(1) when missing driver
  **2.17.11**
  - fixed messaging a user
  - fixed performer operations
  **2.17.12**
  - minor fixes to launching firefox
  **2.17.13**
  - fixed post uploads with random content
  - updated onlysnarf-config
  **2.17.14**
  - herpderp
  **2.17.15**
  - herpaderpaderp
  - fixedfixed uploading
  **2.17.16**
  - herpaderpaderpa
  - fixed more uploading prompts
  **2.17.17**
  - debugged firefox
  - debugged Profile (a bit)
  - debugged backup content
  - args: added username_account to differentiate from twitter username for login
  - args: added source & destination
  - added remote ssh dir
  - added: login source [onlyfans|twitter]
  **2.17.18**
  - oops; fixed firefox "binary"
  **2.17.19**
  - User: following_get, following_write (still needs debugging)
  - remote: updated connection priorities; auto -> form -> twitter -> google
  - login: google; needs debugging
  **2.17.20**
  - oops, disabled auto_reconnect until debugging
  **2.17.21**
  - minor fixes to menu
  **2.18.0**
  - menu updates
  - profile / settings updates
  - cleaned up menu.md
  - updated profile: sync from, sync to, backup
  - updated login methods
  - added: delete-empty folders; properly remove empty folders that all images have been removed from when backing up / moving files
  - debugged: google login
  - debugged: following_write
  -> remote webserver behavior
  - added: session_id, session_url
  - added: remote-chrome, remote-firefox, auto-remote
  - added: reconnect
  - added: session_id & session_url -> session.json for reconnecting to existing browser sessions
  **2.18.1**
  - debugged: redundant category asking
  - debugging: local
  - updated: tests
  **2.18.2**
  - debugged: local
  - create-drive -> create-missing
  - debugging: remote
  **2.18.3**
  - failed expires/poll/schedule ends post
  - fixed date validator
  - debugged: schedule, date, time
  - debugged: post schedule
  - debugging promotion: updated promotion args
  - debugged: discount
  - debugging: promotion (mostly)
  **2.18.4**
  - debugged: promotion- free trial (ish)
  - debugging: promotion- campaign
  **2.18.5**
  - debugged: promotion- campaign
  - debugging: settings
  **2.19.0**
  - added: tabs behavior
  - added: cookies - wow i'm a fucking idiot for not adding this sooner
  - debugging: bot
  - properly tested: settings get
  - properly testedish: settings set
  **2.20.0**
  - added: bot functionality - menu prompt, tip parsing
  **2.20.1**
  - updated: saving session_id and session_url
  - more bot debugging
  - fixed bin/install-firefox.sh: update for processor
  **2.20.2**
  - more debugging
  - fixed: file input
  - debugging: grandfathered
  **3.0.0 : Bot Experiments : 9/21/2020**
  - major updates to browsers debugged
  - added: grandfather promotion
  - added: user lists (finally) - favorites, bookmarks, friends, etc
  - fixed: performer uploads
  - added: specify inner category for performers via 'category-performer'
  - added: fetch file by 'sort' - random|ordered
  -> Bot
  - bot functionality to check posts for tips
  - automatically heart / send dick pics to tips in messages
  **3.0.1**
  - added argument error catch
  **3.0.2**
  - documentation started
  **3.0.3**
  - selenium version 3.141.1 -> 3.141.59
  - bin/install-firefox version 26 -> 29
  **3.0.4**
  - jk no selenium bump...
  **4.0.0 : Flask & React : 3/24/2021**
  - flask-react integration and folder restructure
  **4.0.1 : 3/25/2021**
  - combined args: download_max & upload_max -> image-limit
  - added arg: delete (from delete_google)
  - removed: all cron references
  - changed: output print to log and uppercase to lowercase, except for menu cli
  **4.0.2 : 4/14/2021**
  - added test skeletons
  **4.0.3 : 12/6/2021**
  - removed react shit...
  - cleaned up dir structure; needs updates to package links
  **4.0.4 : 12/8/2021**
  - cleaned up snarf.py staticness
  - updated test_snarf
  **4.1.0 : Beginning Phase Out : 2/19/2022**
  - removed all the flask stuff that was being added
  - updated readme
  - dropped prices to free account
  - grandfathered everyone currently to a free amount a while ago
  - removed paid account $ structure
  - add flask gui for onlysnarf, etc -> submodules -> idea moved to next encompassing project -> ?
  - review setup / config
  - removed all email notifications implementations
  - added easier on off toggle states
  - checked DD writeup / ended project, elaborated on crypto payments and current market forewarning w/ fans
  - completely removed cron features
  - checked / cleaned content folders -> organize for free model funnel
  - cleaned up social links + snapchat
  - updated from.package imports to be shorter -> properly add to __init__.py files
  **4.1.1 : 3/10/2022**
  - take a look at AVN stars, maybe (re) set up profile, bio, socials etc and integrate ---> nah, too lazy
  **4.1.2 : 7/15/2022**
  - added docstring comments for menu.py
  - moved config baseDir -> "/HOME/$USER/.onlysnarf"
  - removed google & dropbox (finally)
  - fixed action: Settings -> now sets values again
  **4.1.3 : 8/23/2022**
  - begin testing finally yay
  - moved saving configs & user configs & session id & cookies to .onlysnarf
  - added method for reading profiles from conf/users / .onlysnarf/users
  **4.1.4 : 8/29/2022**
  - finished first login test
  - removed 'email' from config for fetching username for login
  **4.1.5 : 8/31/2022**
  - added 'debug-firefox' to args for enabling trace logging
  - added 'debug-selenium' to control logging
  - finished test_users
  - added temporary fix for boolean bug: using "True" and "False" strings instead of booleans
  **4.1.6 : 9/1/2022**
  - finished debugging test_discount
  **4.1.7 : 9/5/2022**
  - updates code and docstrings in messages.py; left off in file.py 
  - added classes for enums
  - added beginnings of IPFS 
  **4.1.8 : 9/7/2022**
  - more code cleanup; debugging process for messages & posts uploading files
  - switched git branch to development to break things less
  **4.1.9 : 9/8/2022 : God save the Queen**
  - added xmas test; need to add xmas shnarfs for testing
  - cleaned up more test code, still not much headway on uplading a file
  - began updates for rest of old sh test scripts into python test scripts
  **4.1.10 : 9/9/2022**
  - updated menu.md, updated removed_args.py
  - cleaned up args & commands & docs of such
  - add / ensure all default values to config.conf
  - cleand up config files and example
  - cleaned up dir structure references across project
  **4.2.0 : 9/12/2022**
    - finished debugging test_message & test_post; uploading files works again
    - tested changes made from removing / cleaning up args and commands
    - cleaned up tests (broke again)
  **4.2.1 : 9/13/2022**
    - mostly finished debugging (again): test_message
    - more finishing touches to uploading post & message (and rebroken fixed things)
    - major updates / fixes to browser creation flow / attempts to fix reconnect bug
    - fixed issue in lib/driver with media upload popup from multiple of the same file --> updated error window close
  **4.2.2 : 9/14/2022**
    - finished testing test_message and test_post (again)
    - added tests for selenium browser configurations
    - mostly finished updating expiration, poll, schedule new .get() return dict({})
    - mostly finished testing: test_discount (again), test_poll, test_schedule
    - major updates to classes/schedule & util/settings for proper datetime manipulation
    - added new tests for schedule variables
  **4.2.3 : 9/15/2022, 9/18/2022**
    - more updates to debugging schedule & poll
    - continued finalizing sufficient OK testing responses
  **4.2.4 : 9/19/2022**
    - more debugging schedule & poll, reconnect
    - added tests for trying different browsers, reconnecting, keeping open, remote sessions
    - schedule tests pass they just don't set the right hour
    - major snarf tests all OK (minus poll)
  **4.3.0 : 9/20/2022, 9/21/2022**
  - updated selenium, google chrome, & firefox geckodriver versions
  - driver updates to accomodate selenium version changes
  - changed Driver back to a basic class instead of all static, needs more debugging (again)
  - more individual tests for messages
  - mostly OK on basic tests
  - reconnect works again for chrome
  **4.3.1 : 9/22/2022**
  - more test debugging and finalizing basic OKs
  - browser reconnect reconnects to browser / retains session
  - debugging cookies somewhat saving login session
  - finished test for cookies; finished debugging cookies
  - finished debugging browser reconnect completely (maybe)
  **4.3.2 : 9/22/2022**
  - mostly finished debugging schedule
  - preparing for pypi upload version bump
  - almost done completely debugging basic snarf functionality
  **4.3.3 : 9/24/2022**
  - updated readme
  - update & test pypi upload process
  - updated / checked pypi config
  - mostly finished / updated tests: all OKs
  - reorganized tests for grouping
  **4.3.4 : 9/26/2022**
  - fixed driver: schedule hours not being set now work again
  - reorganized schedule in prep for individual component testing
  - finished debugging schedule (date & time)
  - fixed driver: poll button not being clicked and rest of poll functionality
  - finished debugging poll
  - updated cookie process to check if logged in from session data before overwriting existing cookies and re logging in
  - fixed message price not entering 
  **4.3.5 : 9/27/2022**
  - added text clear from post to message
  - added snarf pic to readme
  - completely finished debugging basic snarf functionality
  - ran full tests suite before final upload to pypi
  **4.3.6 : 10/2/2022**
  - update / check '-help' output; add to readme
  - ensure docs/menu.md is properly updated
  **4.3.7 : 10/4/2022**
  - added subcommands to -help
  - changed 'questions' to 'poll'
  - reorganize tests as necessary (none)
  **4.3.8 : 10/5/2022**
  - finished cleaning up class/user
  - cleaned up user class & simplified current methods for selecting user(s) aka removed prompts for now
  - restructured class/discount and how users are passed via args
  - updated message for new way of handling users passed via args
  **4.3.9: 10/6/2022**
  - added 'min' and 'max' to arg inputs: price, expiration, duration, amount, months, limit
  - changed 'poll' args back to 'question'
  - prepared commands for generating previews to record functionality with ala: "onlysnarf discount -user random"
  **4.3.10: 10/7/2022**
  - finished adding docstrings to classes/user.py
  - added subcommand for fetching users
  - reupdated menu.md w/ pruned config & args
  - updated help.md
  - more debugging for new subcommand structure
  **4.3.11: 10/8/2022**
  - updated method of importing config/args to allow for full subcommand testing via pytest by adding shim for args
  **4.3.12: 10/10/2022**
  - fixed tab handling in driver
  - debugged & tested newly added subcommand structure: discount, message, post --> snarf.py
  - beginning recordings for behavior previews
  **4.4.0: 10/11/2022**
  - fixed args & config overwrite direction
  - recorded new videos for demos
  - updated preview gifs of behavior for readme w/ OBS: discount, message, poll, post, schedule, users
  - cleaned up config files w/ final changes
  - added previews to readme
  - updated user config explainer to readme
  - cleaned up packages
  - cleaned up classes/files to keep up with gutting google, etc; removed Remote & Bot and saved in notes/old
  - doublechecked code for missing docstrings... aka finished cleaning up code (wow go me)
  - double checked / re-enabled performers & tags functionality
  - updated help.md and menu.md with new text changes
  - fixed driver & message actually sending... haha and discount applying.... woops
  - synced with main/master branch
  - uploaded working changes to pypi
  **4.4.1: 10/12/2022**
  - minor text changes
  - fixed file upload when posting (of course this would still be semi broken after publishing changes)
  **10/13/2022**
  - more minor text changes
  - changed text: bin/google* --> bin/chrome*
  **4.4.2: 10/14/2022**
  - fixed args validator for duration's "min" "max"
  - debugging project deployment & installer scripts for web browsers
  **4.4.3: 10/15/2022**
  - add a way for installation to work for webdrivers for pypi
  - added: webdriver_manager; cleaned up driver spawn code and packages : https://pypi.org/project/webdriver-manager/
  - debugging webdriver install processes on rpi4
  - added browser options to help with debugging on rpi: brave, chromium, ie, edge, and opera
  - added tests for new browser options
  **4.4.4: 10/20/2022**
  - continued debugging attempts for browsers on rpi4
  - added notes for debugging browsers
  **4.4.5: 10/20/2022**
  - added travis.cli config
  - connected travis to github
  - more driver debugging for added webmanager autoinstalls
  **4.4.6: 10/27/2022**
  - added travisci for testing python versions & os installs
  - more rpi debugging attempts; added attempt scripts
  **4.4.7: 3/17/2023**
  - upgraded selenium to 4.0
  - prep for project cleanup and python update
  - pruned prompts
  - fixed webdriver manager configurations for most browsers: brave, chrome, chromium, and firefox
  **3/18/2023**
  - fixed cookies for chrome but not firefox
  - rpi4 testing and prep for selenium cleanup
  - added a way for installation to work for webdrivers for pypi
  **4.4.8: 3/20/2023**
  - added check for rpi processor for chrome only
  - finished testing new browser changes
  - finished debugging web browser on rpi4
  - checked current instructions for installing from github
  - updated to python10
  - updated install scripts and organize by usability by platform; distinguish arm scripts for rpis
  - finished debugging new webdriver manager system
  **4.4.9: 3/21/2023**
  - fixed unknown bug when fetching random user
  - fixed applying discounts and updated min/max tests for discounts 
  - fixed messaging and posting 
  **3/22/2023**
  - fixed poll and schedule
  - pytest bug w/ final arg
  - updated any webscraping as necessary
  - added tests for alternate logins (that probably won't work anyways *cough* google)
  - begin prepping for merging new changes to main and publishing to pypi
**4.4.10: 3/23/2023**
  - completely finished fixing schedule
  - super duper verified test results
  - full test coverage
  - merged w/ main
  - published changes to pypi
**4.4.11**
  - fixed 'onlysnarf' cmd references
  - removed nonworking browser references in optional args
  - fixed discount bug

------------------------------------------------------------------------------------

## TODO

- add bypass for 2fa
https://www.geeksforgeeks.org/two-factor-authentication-using-google-authenticator-in-python/
https://stackoverflow.com/questions/55870489/how-to-handle-google-authenticator-with-selenium
https://stackoverflow.com/questions/8529265/google-authenticator-implementation-in-python

(review usability and code first)
-> OnlyFans: Promos
- clean up / fix & test
- add min/max to args & validators
- re-enable / add promo subcommands and config variables

-> OnlyFans: Profile
- new - setup - Twitter -> profile, banner; Price and Settings
- new - advertise
- new - posts - tweet to advertise new account, tweet to ask about what you should post, etc; recommend what to post
- need to add 'create' to Profile for asking for profile settings when syncing to
- add config for profile templates when testing profile features again
- add tests for profile integration / behavior
- re-enable / add profile subcommands and config variables

-> OnlyFans
- add quiz & target interactions (onlyfans buttons)
- add functionality that follows profiles that are free for a month
- update schedule, date, and time args to accept strings aka "1 day" or "1 day 2 hours"
- update time to accept strings that modify to add to current time aka "+2" or "2 hours" adds 2 hours to the current time

(once everything else in app works again)
- run new auth tests w/ appropriately connected accounts
-> Twitter
- actually test if tweeting behavior works in driver
- needs a dummy account to test actual tweeting w/
- tweet reminders from inlaid config behavior
- can enter and edit the final text that is tweeted
- can include media attachments
-- add checks for previously existing tweets
-- keep track of tweets (somehow)

-> Tests
- separate driver functions into individual components ala schedule --> individual steps; for easier testing (and to clean up the giant ass driver file)
- add tests for newly separated driver files / functions
- add tests for additional config variables such as browser and image/video options, limits
- finish adding tests for individual messaging circumstances: all, recent, favorite, renew on
- finish adding tests for individual message entry parts, individual post entry parts
- add and finish tests for remote browser testing; requires remote server setup for testing? or test on same device or the rpi

(webdriver)
- (if necessary) finish integrating edge, ie, and opera
- figure out how to request specific webdriver versions installs to test v102 for edge

-> CLI Menu
(probably never)
- re-add menu system
- fix any new cli menu errors made while updating major processes
- re-enable prompting for discount amount&months in Settings or somewhere else (at some point)
- re-add removed user select code in notes/selectstuff.py (for menu prompts)
- re-enable menu command

## Fix / Debug

(unlikely to be fixed soon, if ever)
- google login: unsafe browser warning --> possibly end of usability --> should I just remove this? form login works, twitter login works (i think)
-- maybe just cut out / leave as is until can debug "unsafe browser" issue?

- debug: discover the cause of the super slow web scraping
-- probably not: debug_delay
---- possibly improved via recent updated coding? (4.3.10)

- figure out how to suppress the chrome stacktrace debugging messages
- fix driver.firefox: DeprecationWarning: service_log_path has been deprecated, please pass in a Service object

### Browser Changes

working: brave, chrome, chromium, firefox 
not working: edge, ie, opera

existing browsers: chrome, firefox
added new browsers: brave, chromium, ie, edge, and opera
other potential browsers: phantomjs (requires node), safari (requires python2.7)

https://pypi.org/project/webdriver-manager/
https://stackoverflow.com/questions/58686471/how-to-use-edge-chromium-webdriver-unknown-error-cannot-find-msedge-binary

notes:

#### edge:
requires: msedge-selenium-tools
- might only work for selenium v102
- might only work on Windows
"There are various issues for chromium drivers for browser v103 used by Edge and Google Chrome. These are being addressed in v104, but they are still in beta. Advise that you downgrade for now to v102."
https://stackoverflow.com/questions/72773330/when-running-selenium-edge-in-pyton-getting-sedgedriver-exe-unexpectedly-exite


#### ie:
- might only work on Windows
https://stackoverflow.com/questions/49787327/selenium-on-mac-message-chromedriver-executable-may-have-wrong-permissions

#### opera:
- might have a version limit requirement

updating permissions didn't work:
chown -R ubuntu /home/ubuntu/.wdm/drivers

what helps in general:
>> using correct webdriver options generator
>> specifying binary paths
>> correct permissions on binary paths

# Bugs

**4.1.4**
  - boolean checks from "Settings.is_" functions are failing: replaced with redundant string checks for if == "True"
**4.3.12**
  - message: drag&drop has decided to occasionally stop working; maybe a selenium version issue?
**4.4.0**
  - discount: amount&months still require 2 passes on average to update values correctly
**4.4.6**
  - followed instructions here for enabled firefox on ubuntu 22.04: https://www.reddit.com/r/learnpython/comments/umft75/selenium_your_firefox_profile_cannot_be_loaded_it/ -> https://support.mozilla.org/en-US/kb/install-firefox-linux#w_install-firefox-from-mozilla-builds-for-advanced-users
**4.4.9:**
  - when running pytest, the final arg is mistakenly picked up as an input (and passes validation, because it's a file) and tests therefore have multiple repeat file uploads    

# Web Browser Versions
(no longer as relevant as of 4.4.7ish updates)

Version Check:
stable => Google Chrome 106.0.5249.40 beta
beta => Google Chrome 106.0.5249.40 beta
binary => Version: 106.0.5249.21.0
geckodriver => geckodriver 0.31.0 (b617178ef491 2022-04-06 11:57 +0000)

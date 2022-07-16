# Menu

`onlysnarf *args`

## Action

### Discount
user: all | recent | new | select | username   
amount (%): 0-55  
months: 1-12  

### Message
user: all | recent | new | select | username  
text: ""  
image: "/path/to/file"  
price ($): "0.00"  

Message [all, recent, new, username] users $message with $image for $price.

### Post
category: **image** | **gallery** | **video** | **performer**  
text: ""  
schedule: "mm/dd/YYYY:HH:MM"  
date: "mm/dd/YYYY"  
time: "HH:MM"  
questions: "your mom", "is very hot", "today"  
duration (poll): 1, 3, 7, 99 or "No limit"  
expires: 1, 3, 7, 99 or "No limit"  
keywords: key, words -> #key #words  
performers: performerName1, performerName2 -> w/ @performerName1 @performerName2  

Upload $category of content from $source as a post with $text, $keywords, and tagged $performers.
  
### User
**All**: all users  
**Recent**: users subscribed within last 5 days  
**New**: users subscribed within last month who haven't been messaged  
**Select**: selects User from list  
**Username**: enter User by username  


## Profile

### Backup
**Content**: Downloads all posted content
**Messages**: Downloads (roughly) all messaged content
**Content & Messages**: both of above

### Sync From
Gets / reads settings from OnlyFans profile and saves locally.
### Sync To
Updates / writes settings to OnlyFans profile from local save.

## args
OnlySnarf can be run as a promptless script via:
`onlysnarfpy *args`

-action [discount|message|post|promotion]
The action to take.
-amount %
The amount in percent to discount.
-backup
Backup uploaded content after upload
-browser [auto|firefox|google|reconnect|remote]
Browser to connect to. Remote requires $remote-host &| $remote-port or a local session.json file 
-category image  
Uploads a random image labeled: 'fileName'  
-category gallery  
Uploads a random gallery labeled: 'folderName'  
-category video  
Uploads a random video labeled: 'fileName'  
-categories
The categories / folders to include in searches.
-create-drive
Enables creating missing folders in Google Drive.
-cron
Flags the script as a cron operation.
-cron-user
The user to run cron script as.
-date
The date required for a scheduled post.
-delete-empty
Delete empty folders when searching for content.
-delete-google
Enable deleting Google files after upload (after backup if enabled).
-destination
Destination for backed up content
-download-path
The download path for files.
-drive-path
The Google Drive path to the main OnlySnarf content folder.
-duration [0,3,7,99]
The duration for a post.
-email
The email to send a promotion to.
-expiration [0,3,7,99]
The expiration to use for a post.
-force-backup
Enable forcing backup.
-force-upload
Enable forcing upload despite long upload time.
-download-max #
The maximum number of files to download.
-upload-max #
The maximum number of files to upload.
-keep
Keep the browser open when finished (allows for reconnect).
-keywords
The folder by keyword to download & upload.
-promotion-limit
The max number of subscribers for a promotion.
-login [OnlyFans|Twitter|Google]
The method to use to log in.
-months
The number of months to specify for a schedule.
-mount-path
The location of local data.
-bykeyword
The keyword to search for content by location.
-notbykeyword
The keyword to ignore when searching for content by location.
-password
The password to log in for OnlyFans.
-password_google
The password to log in for Google.
-password_twitter
The password to log in for Twitter.
-performers
The performers to specificy for upload.
-perfer-local
Whether or not to use local file for referencing users.
-price
The price to specify for file uploads / messages.
-profile-backup
Enabled profile backup w/ 'profile' action.
-profile-syncto
Enabled profile sync to w/ 'profile' action.
-profile-syncfrom
Enabled profile sync from w/ 'profile' action.
-promotion-user
Enables user method..
-promotion-trial
-config-path
The path to the config file.
-google-creds
The path to the google_credentials.txt file.
-client-secret
The path to the client_secrets.json file.
-users-path
The path to the users file.
-profile-path
The path to the profile file.
-remote-host
The remote host to connect to for a reconnect.
-remote-port
The remote port to use for connecting to a reconnect.
-remote-username
The remote host username for accessing remote content.
-remote-password
The remote host password for accessing remote content.
-remote-host
The remote host for accessing remote content.
-remote-port
The remote port for accessing remote content.
-question
A question to include when posting a questions response. Can be provided in multiple up to 5.
-recent-users-count
-reduce
Reduce the file size before uploading.
-drive-root
The Google Drive root folder path.
-save-users
Enable saving users before exiting browser.
-schedule
Schedule post for upload via $date and $time
-session-id
The session id to use for reconnecting.
-session-url
The session url to use for reconnecting.
-skip-download
Skip file downloads.
-skip-upload
Skip file uploads.
-show
Show web browser.
-source [local, remote, google, dropbox]
Source to search for content.
-tags
Tags to @ when creating text.
-text
Text to be entered upon upload / message.
-time
Time for scheduled posts.
-title
Specific title of file to search for remotely. 
-thumbnail
Fix thumbnail before uploading.
-tweeting
Enable Tweeting (if Twitter connected).
-upload-max-duration
The number of 10 minute intervals to wait while uploading a file.
-user
The user by username to specify for operations.
-users
The users by username to specify for operations.
-users-favorite
The favorite users by username to specify for favorite operations.
-username
The OnlyFans username to log in as.
-password
OnlyFans password for login
-username-google
Google username for login
-password-google
OnlyFans password for login
-username_twitter
Twitter username for login
-password_twitter
Twitter password for login
-reduce
Reduce mp4s before uploading
-source [local, google]
Uses the provided source to search for files.
/path/to/fileOrDirectory
Uploads a file or directory of files at path.  

Example:
  `onlysnarfpy -category video -date "12/25/2019" -expires 7`  
Uploads a random video, schedules it to release at midnight on Christmas, and sets the post to expire after 7 days.  

## Debugging

-debug  
Tests configuration. Does not upload or remove from Google Drive.

-debug-delay
Delays certain portions for visual monitoring.

-verbose
Shows additional log output (up to 3)

-version
Prints the version

Complete Debugging:
  `onlysnarfpy -debug -verbose -verbose -verbose -show -debug-delay`

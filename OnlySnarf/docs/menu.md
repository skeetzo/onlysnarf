# Menu

`onlysnarf *args`

Please refer to the example config file provided for a complete listing of available options.

## Action

An action is performed by including the required combinations of arguments & input.

### Discount
user: "all" | "recent" | "new" | "select" | "username" | "random"
amount (%): 0-55  
months: 1-12  

### Message
user: "all" | "recent" | "new" | "select" | "username" | "random"
text: ""  

(optional)
category: "image" | "gallery" | "video"
input: "/path/to/folderOrFile"
source: "[local, remote, ipfs]"
destination: "[local, remote, ipfs]"

(optional, requires image)
price ($): "0.00"  

Message $user users $text possibly with $image for $price.

### Post
text: ""  

(optional, "date" & "time" or only "schedule")
schedule: "mm/dd/YYYY:HH:MM"  
date: "mm/dd/YYYY"  
time: "HH:MM"

(optional)
category: "image" | "gallery" | "video"
input: "/path/to/folderOrFile"
source: "[local, remote, ipfs]"
destination: "[local, remote, ipfs]"
tags: key, words -> #key #words  
performers: performerName1, performerName2 -> w/ @performerName1 @performerName2  

poll:
questions: "your mom", "is very hot", "today"  
duration (poll): 1, 3, 7, 99 or "No limit"  
expires: 1, 3, 7, 99 or "No limit"  

Upload $category of content from $source as a post with $text, $tags, and detected (or provided) $performers.
  If provided: enters questions as provided in order, enter's poll duration, expiration, and/or scheduling.

### User
**All**: all users  
**Recent**: users subscribed within last 5 days  
**New**: users subscribed within last month who haven't been messaged  
**Select**: selects User from list  
**Username**: enter User by username  
**Random**: select user at random

### Profile (probably not working)

Backup:
**Content**: Downloads all posted content
**Messages**: Downloads (roughly) all messaged content
**Content & Messages**: both of above

## args
OnlySnarf actions can be fulfilled as a promptless script via:
`onlysnarf /path/to/fileOrDirectory` aka `onlysnarf -help`

/path/to/fileOrDirectory
The file or folder of content to use.

### General

-config-path /path/to/file
The path to the config file.

-login [onlyfans|twitter]
The method to use to log in.

-username
The OnlyFans username to login as.

### Content

-backup
Backup uploaded content after upload.

-category [image | gallery | video]
The category of content to use.

-delete
Delete content after uploading (instead of backing up).

-destination [local, remote, ipfs]
Destination for backed up content.

-performers [performerNames or Ids ...]
The performers to tag with "@" symbols.

-sort [ordered, random, least, greatest]
The sort method to use when fetching content files.

-source [local, remote, ipfs]
Source to search for content files.

### OnlySnarf

-amount %
The amount in percent to discount.

-date "01/01/2000"
The date required for a scheduled post.

-duration [0,3,7,99]
The duration for a post.

-expiration [0,3,7,99]
The expiration to use for a post.

-months
The number of months to specify for a schedule.

-price
The price to specify for file uploads / messages.

-promotion-expiration
The expiration to use for a promotion.

-promotion-limit
The max number of subscribers for a promotion.

-question "text"
A question to include when posting a questions response. Can be provided in multiple up to 5.

-schedule
Schedule post for upload via $date and $time

-tags
Tags to become #tags when creating text.

-text
Text to be entered upon upload / message.

-time
Time for scheduled posts.

-tweet
Enable Tweeting (if Twitter connected).

-user
The user by username to specify for operations.

-users
The users by username to specify for operations.

Example:
  `onlysnarf -category video -date "12/25/2019" -expires 7`  
Uploads a random video, schedules it to release at midnight on Christmas, and sets the post to expire after 7 days.  

## more args

### Selenium

-browser [auto|firefox|google|reconnect|remote]
Browser to connect to. Remote requires $remote-host &| $remote-port or a local session.json file.

-keep
Keep the browser open when finished (allows for reconnect).

-save-users
Enable saving users before exiting browser.

-upload-max-duration
The number of 10 minute intervals to wait while uploading a file.

### Debugging

-debug  
Tests configuration. Does not upload or remove from Google Drive.

-force-backup
Enable forcing backup.

-force-upload
Enable forcing upload despite long upload time.

-show
Show web browser.

-verbose
Shows additional log output (up to 3)

-version
Prints the version

Complete Debugging:
  `onlysnarf -debug -verbose -verbose -verbose -show -debug-delay`

## Config File Only

### Debugging

-debug-delay
Delays certain portions for visual monitoring.

-debug-firefox
Enable debugging of Firefox.

-debug-google
Enable debugging of google chrome.

-download-path
The download path for files.

-prefer-local: default True
Whether or not to use local file for referencing users.

-repair
Try to repair video files.

-skip-download
Skip file downloads.

-skip-upload
Skip file uploads.

-skip-users
Skip specific users by username or id.

-users-read
The number of users to count when reading messages.

### General

-image-download-max #
The maximum number of files to download.

-image-upload-max #
The maximum number of files to upload.

-recent-users-count #
The number of users to count as "recent".

-reduce
Reduce the file size before uploading.

## In Development Hell

Sync From: Gets / reads relevant settings from OnlyFans profile and saves locally.
Sync To: Updates / writes relevant settings to OnlyFans profile from local save.

### Not In Use
(possibly ever)

-email
The email to send a promotion to.

-thumbnail
Fix thumbnail before uploading.

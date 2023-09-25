# Menu

`snarf *args`

Please refer to the example config file provided for a complete listing of available options.

## Actions

An action is performed by including the required combination of subcommands, arguments, and input. OnlySnarf actions can be fulfilled as a promptless script via:
`snarf post /path/to/fileOrDirectory`

For more help with an action: `snarf post -h`

Users are easily referenced using keywords:  
**All**: all users  
**Recent**: users subscribed within last 5 days  
**New**: users subscribed within last month who haven't been messaged  
**Select**: selects User from list (currently unavailable)  
**Username**: enter User by username  
**Random**: select user at random  

### Discount
user: "all" | "recent" | "new" | "select" | "username" | "random"  
amount (%): 0-55 | "min" | "max"  
months: 1-12 | "min" | "max"  

### Message
user: "all" | "recent" | "new" | "select" | "username" | "random"
text: ""  

(optional)  
input: "/path/to/fileoOrFolder"  

(when input is specified)  
price ($): "0.00" | "min" | "max"  
keywords: key, words -> #key #words  
performers: performerName1, performerName2 -> @performerName1 @performerName2  

Schedule: ("date" & "time" or only "schedule")  
schedule: "mm/dd/YYYY:HH:MM"  
date: "mm/dd/YYYY"  
time: "HH:MM"  

includes: "all" | "favorites" | "recent" | ...  
excludes: "all" | "favorites" | "recent" | ...  

Message $USER the provided $TEXT with $TAGS and uploaded $IMAGE available for $PRICE.  

If schedule: schedules the message for the provided date and time.  

### Post
text: ""  

(optional)  
input: "/path/to/fileoOrFolder"  
keywords: key, words -> #key #words  
performers: performerName1, performerName2 -> @performerName1 @performerName2  

**Schedule**: (when specificying "date" & "time" or only "schedule")  
schedule: "mm/dd/YYYY:HH:MM"  
date: "mm/dd/YYYY"  
time: "HH:MM"  

**Poll**:  
questions: "your mom", "is very hot", "today"  
duration: 1, 3, 7, 99 or "No limit" | "min" | "max"  
expires: 1, 3, 7, 99 or "No limit" | "min" | "max"  

Upload provided $INPUT with $TEXT, $TAGS, and provided list of $PERFORMERS.  

If schedule: schedules the post for the provided date and time.  
If poll: enters questions as provided in order, the duration, and expiration.  

### Profile (currently not working)

Backup:  
**Content**: Downloads all posted content  
**Messages**: Downloads (roughly) all messaged content  
**Content & Messages**: both of above  

### Users
(none)

## Args

General, debugging, and selenium related args apply to any action. Each action's available args are further described below.  

### General

-config, -C /path/to/file  
The path to the config file.  

-login, -L [onlyfans|twitter]  
The method to use to log in.  

--username, --u ""  
The OnlyFans username to login as.  

-phone ##########
The OnlyFans phone number associated with the account for verifying Twitter login.

### Discount
-amount #  
The amount in percent to discount.  

-months #  
The number of months to specify for a schedule.  

-user ""  
The user by username to specify for discounting.  

-users "user1,user2"  
The users by username to specify for discounting.  

### Message
-date "01/01/2000"  
The date required for a scheduled message.  

-performers "name1" -performers "name2" ...  
Performer usernames to reference. Adds to text with "@" symbols.  

-price 0  
The price to specify for file uploads.  

-schedule "mm/dd/YYYY:HH:MM"  
Schedule message for upload via $date and $time.  

-keywords "key1" -keywords "key2" ...  
Keywords to become # tagged when creating text.  

-text ""  
Text to be entered.  

-time "HH:MM"  
Time for scheduled message.  

-user ""  
The user by username to specify for messages.  

-users "user1,user2"  
The users by username to specify for messages.  

-includes "list1" -includes "list2"  
The lists to include when sending a mass message. Examples: all, favorites, recent  

-excludes "list1" -excludes "list2"  
The lists to exclude when sending a mass message. Examples: all, favorites, recent  

### Post
-date "01/01/2000"  
The date required for a scheduled post.  

-duration [0,3,7,99,min,max]  
The duration for a post.  

-expiration [0,3,7,99,min,max]  
The expiration to use for a post.  

-performers "name1" -performers "name2" ...  
Performer usernames to reference. Adds to text with "@" symbols.  

-schedule "mm/dd/YYYY:HH:MM"  
Schedule post for upload via $date and $time.  

-keywords "key1" -keywords "key2" ...  
Keywords to become # tagged when creating text.  

-text ""  
Text to be entered.  

-time "HH:MM"  
Time for scheduled posts.  

-tweet  
Enable Tweeting (if Twitter connected).  

-question, -Q "text"  
A question to include when posting a questions response. Can be provided in multiple up to 5. For example: `-question "first" -question "second" -question "third"`  

### Users

(none)  

## more args

Some args are hidden from the help command. All args are available via the config file and are (sometimes) further notated there as well.  

### Selenium

-browser, -B [auto|firefox|google|reconnect|remote]  
Browser to connect with.  

-keep, -K  
Keep the browser open when finished (allows for reconnect).  

-upload-max-duration #  
The number of 10 minute intervals to wait while uploading a file.  

### Debugging

-debug, -D  
Tests configuration. Does not upload or remove from Google Drive.  

-show, -SW  
Show web browser.  

-verbose  
Shows additional log output (up to 3).  

-version  
Prints the version  

Basic debugging preface:  
`snarf -debug -verbose -verbose -verbose -show -debug-delay`  

## Config File Only

### Debugging

-debug-delay  
Delays certain portions for visual monitoring.  

-download-path ""  
The download path for files.  

-image-download-max #  
The maximum number of files to download.  

-image-upload-max #  
The maximum number of files to upload.  

-recent-users-count #  
The number of users to count as "recent".  

-skip-upload  
Skip file uploads.  

-users-read #  
The number of users to count when reading messages.  

## In Development Hell

Sync From: Gets / reads relevant settings from OnlyFans profile and saves locally.  
Sync To: Updates / writes relevant settings to OnlyFans profile from local save.  

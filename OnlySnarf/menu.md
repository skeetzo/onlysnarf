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
  `onlysnarfpy -action message -text 'hello fans' '/path/to/fileOrDirector'`  
The action to take.

-backup
Backup content to Google Drive via upload or moving original file

-category image  
  `onlysnarfpy -category image`  
Uploads a random image labeled: 'fileName'  

-category gallery  
  `onlysnarfpy -category gallery`  
Uploads a random gallery labeled: 'folderName'  

-category video  
  `onlysnarfpy -category video`  
Uploads a random video labeled: 'fileName'  

-text  
  `onlysnarfpy -category video -text "your mom"`  
Uploads a random video labeled: 'your mom'  

-tweeting
  `onlysnarfpy -tweeting -action post -text 'hi mom'`  
Enables tweeting upon posting

-username
  `onlysnarfpy -username 'beepbeep'`  
OnlyFans username for login

-password
  `onlysnarfpy -username 'usetheconfigfile' -password 'beepitybeep'`  
OnlyFans password for login

-username_twitter
  `onlysnarfpy -username_twitter 'beepbeep'`  
Twitter username for login

-password_twitter
  `onlysnarfpy -username_twitter 'usetheconfigfile' -password_twitter 'beepitybeep'`  
Twitter password for login

-reduce
  `onlysnarfpy -reduce /path/to/mp4file`  
Reduce mp4s before uploading

-source [local, google]
  `onlysnarfpy -source google -category image`
Uses the provided source to search for files.

/path/to/fileOrDirectory
  `onlysnarfpy /path/to/fileOrDirectory`  
Uploads a file or directory of files at path.  

Example:
  `onlysnarfpy -category video -date "12/25/2019" -expires 7`  
Uploads a random video, schedules it to release at midnight on Christmas, and sets the post to expire after 7 days.  

## Debugging

-debug  
  `onlysnarfpy -debug`  
Tests configuration. Does not upload or remove from Google Drive.

-debug-delay
  `onlysnarfpy -debug -debug-delay`
Delays certain portions for visual monitoring.

-show
  `onlysnarfpy -show`
Shows the Chromium browser

-verbose
  `onlysnarfpy -verbose -verbose -verbose`
Shows additional log output (up to 3)

-version
  `onlysnarfpy -version`
Prints the version

Complete Debugging:
  `onlysnarfpy -debug -verbose -verbose -verbose -show -debug-delay`

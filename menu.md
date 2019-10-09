# Menu

## Actions

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
text: ""  
schedule: "mm/dd/YYYY:HH:MM"  
date: "mm/dd/YYYY"  
time: "HH:MM"  
questions: "your mom", "is very hot", "today"  
duration (poll): 1, 3, 7, 99 or "No limit"  
expires: 1, 3, 7, 99 or "No limit"  
  
### User
**All**: all users  
**Recent**: users subscribed within last 5 days  
**New**: users subscribed within last month who haven't been messaged  
**Select**: selects User from list  
**Username**: enter User by username  

### Upload
type: **image** | **gallery** | **video** | **performer**  
text: ""  
method: "random" | "input" | "choose"  
keywords: key, words -> #key #words  
performers: performerName1, performerName2 -> @performerName1 @performerName2  

Upload $type of content by $method as post with $text and tag $performer. Adds hashtagged $keywords.

## args

-debug  
  `onlysnarfpy -debug`  
Tests configuration. Does not upload or remove from Google Drive.

-type image  
  `onlysnarfpy -type image`  
Uploads a random image labeled: 'imageName - %d%m%y'  

-type gallery  
  `onlysnarfpy -type gallery`  
Uploads a random gallery labeled: 'folderName - %d%m%y'  

-type video  
  `onlysnarfpy -type video`  
Uploads a random video labeled: 'folderName - %d%m%y'  

-text  
  `onlysnarfpy -type video -text "your mom"`  
Uploads a random video labeled: 'your mom - %d%m%y'  

-input /path/to/fileOrDirectory
  `onlysnarfpy -input /path/to/fileOrDirectory`  
Uploads a file or directory of files at path.  

-input /path/to/fileOrDirectory
  `onlysnarfpy -type video -date "12/25/2019" -expires 7`  
Uploads a random video, schedules it to release at midnight on Christmas, and sets the post to expire after 7 days.  

-show-window
  `python3 onlysnarf.py -show-window`
Shows the Chromium browser
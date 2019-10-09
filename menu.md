# Menu

## Actions

### Discount
user:  
**All**  : all users  
**Recent** : users subscribed within last 5 days  
**New** : users subscribed within last month who haven't been messaged  
**User** : selects User from list  
**Username** : enter User by username  
amount  
months  

### Message
user:  
**All**  : all users  
**Recent** : users subscribed within last 5 days  
**New** : users subscribed within last month who haven't been messaged  
**User** : selects User from list  
**Username** : enter User by username  
text  
image  
price  

Message [all, recent, new] users $message with $image for $price.

### Post
text  
schedule | -date && -time  
questions & - duration  
expires & - duration  

### Upload
type : **Image** | **Gallery** | **Video** | **Performer**  
text  
method : random | input | choose  
keywords -> hashtagged  
performers -> @  

Upload $type of content by $method as post with $text and tag $performer. Adds hashtagged $keywords.

## args

-debug  
  `python3 onlysnarf.py -debug`  
Tests configuration. Does not upload or remove from Google Drive.

-type image  
  `python3 onlysnarf.py -type image`  
Uploads an image labeled: 'imageName - %d%m%y'  

-type gallery  
  `python3 onlysnarf.py -type gallery`  
Uploads a gallery labeled: 'folderName - %d%m%y'  

-type video  
  `python3 onlysnarf.py -type video`  
Uploads a video labeled: 'folderName - %d%m%y'  

-text  
  `python3 onlysnarf.py -type video -text "your mom"`  
Uploads a video labeled: 'your mom - %d%m%y'  

-show-window
  `python3 onlysnarf.py -show-window`
Shows the Chromium browser
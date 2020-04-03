
###
### Settings
###

settingsItems = sorted([
    [ "Profile", "profileSettings" ],
    [ "Account", "accountSettings" ],
    [ "Notification", "notificationSettings" ],
    [ "Security", "securitySettings" ],
    [ "Other", "otherSettings" ],
    [ "Sync", "sync" ]
])
settingsItems.insert(0,[ "Back", "main", "main"])

# text, path, url, price, get, country, ip, or bool
profileSettingsItems = sorted([
    [ "Cover Image", "coverImage", "path" ],
    [ "Profile Photo", "profilePhoto", "path" ],
    [ "Display Name", "displayName", "text" ],
    [ "Subscription Price", "subscriptionPrice", "price" ],
    [ "About", "about", "text" ],
    [ "Location", "location", "text" ],
    [ "Website URL", "websiteURL", "url" ]
])
profileSettingsItems.insert(0,[ "Back", "main", "main"])

accountSettingsItems = sorted([
    [ "Username", "username", "text" ],
    [ "Email", "email", "text" ],
    [ "Password", "password", "text" ]
])
accountSettingsItems.insert(0,[ "Back", "main"])

notificationSettingsItems = sorted([
    [ "Email Notifications", "emailNotifs", "bool" ],
    [ "New Referral", "emailNotifsNewReferral", "bool" ],
    [ "New Stream", "emailNotifsNewStream", "bool" ],
    [ "New Subscriber", "emailNotifsNewSubscriber", "bool" ],
    [ "New Tip", "emailNotifsNewTip", "bool" ],
    [ "Renewal", "emailNotifsRenewal", "bool" ],
    [ "New Likes Summary", "emailNotifsNewLikes", "bool" ],
    [ "New Posts Summary", "emailNotifsNewPosts", "bool" ],
    [ "New Private Message Summary", "emailNotifsNewPrivMessages", "bool" ],
    [ "Site Notifications", "siteNotifs", "bool" ],
    [ "New Comment", "siteNotifsNewComment", "bool" ],
    [ "New Favorite", "siteNotifsNewFavorite", "bool" ],
    [ "New Discounts", "siteNotifsDiscounts", "bool" ],
    [ "New Subscriber", "siteNotifsNewSubscriber", "bool" ],
    [ "New Tip", "siteNotifsNewTip", "bool" ],
    [ "Toast Notifications", "toastNotifs", "bool" ],
    [ "New Comment", "toastNotifsNewComment", "bool" ],
    [ "New Favorite", "toastNotifsNewFavorite", "bool" ],
    [ "New Subscriber", "toastNotifsNewSubscriber", "bool" ],
    [ "New Tip", "toastNotifsNewTip", "bool" ]
])
notificationSettingsItems.insert(0,[ "Back", "main"])


securitySettingsItems = sorted([
    [ "Fully Private Profile", "fullyPrivate", "bool" ],
    [ "Enable Comments", "enableComments", "bool" ],
    [ "Show Fans Count on your Profile", "showFansCount", "bool" ],
    [ "Show Posts Tips Summary", "showPostsTip", "bool" ],
    [ "Public Friends List", "publicFriendsList", "bool" ],
    [ "IP and Geo Blocking - By Country", "ipCountry", "country" ],
    [ "IP and Geo Blocking - By IP", "ipIP", "ip" ],
    [ "Watermark - Enabled", "watermark", "bool" ],
    [ "Watermark - Photos", "watermarkPhoto", "bool" ],
    [ "Watermark - Videos", "watermarkVideo", "bool" ],
    [ "Watermark - Custom Text", "watermarkText", "text" ]
])
securitySettingsItems.insert(0,[ "Back", "main"])

otherSettingsItems = sorted([
    [ "Live Server", "liveServer", "get" ],
    [ "Live Key", "liveServerKey", "get" ]
])
otherSettingsItems.insert(0,[ "Back", "main"])

















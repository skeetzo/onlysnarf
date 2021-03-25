# profile settings elements

ELEMENTS = [
    ## Settings ##

    ## Account
    # cover image enter
    {
        "name": "coverImage",
        "classes": ["g-btn.m-rounded.m-sm.m-border"],
        "text": ["Upload cover image"],
        "id": []
    },
    # cover image cancel button
    {
        "name": "coverImageCancel",
        "classes": ["b-user-panel__del-btn.m-cover"],
        "text": [],
        "id": []
    },
    # profile photo
    {
        "name": "profilePhoto",
        "classes": ["g-btn.m-rounded.m-sm.m-border"],
        "text": ["Upload profile photo"],
        "id": []
    },
    # profile photo cancel button
    {
        "name": "profilePhotoCancel",
        "classes": ["b-user-panel__del-btn.m-avatar"],
        "text": [],
        "id": []
    },
    # username
    {
        "name": "username",
        "classes": [],
        "text": [],
        "id": ["input-login"]
    },
    # display name
    {
        "name": "displayName",
        "classes": [],
        "text": [],
        "id": ["input-name"]
    },
    # subscription price
    {
        "name": "subscriptionPrice",
        "classes": ["form-control.g-input"],
        "text": ["Free"],
        "id": []
    },
    # subscription bundle
    # TODO
    {
        "name": "subscriptionBundle",
        "classes": [None],
        "text": [],
        "id": []
    },
    # referral award enabled / disabled
    # TODO
    {
        "name": "referralReward",
        "classes": [None],
        "text": [],
        "id": []
    },

    # ADD reward for subscriber referrals
    # about
    {
        "name": "about",
        "classes": [],
        "text": [],
        "id": ["input-about"]
    },
    # location
    {
        "name": "location",
        "classes": [],
        "text": [],
        "id": ["input-location"]
    },
    # website url
    {
        "name": "websiteURL",
        "classes": [],
        "text": [],
        "id": ["input-website"]
    },

    ## Advanced
    # username
    # BLANK
    # username
    # {
    #     "name": "username",
    #     "classes": ["form-control.g-input"],
    #     "text": [],
    #     "id": []
    # },
    # email
    {
        "name": "email",
        "classes": ["form-control.g-input"],
        "text": [],
        "id": []
    },
    # connect other onlyfans accounts username enter area
    # BLANK
    # password
    {
        "name": "password",
        "classes": ["form-control.g-input"],
        "text": [],
        "id": []
    },
    # password 2x
    {
        "name": "newPassword",
        "classes": ["form-control.g-input"],
        "text": [],
        "id": []
    },
    # confirm new password
    {
        "name": "confirmPassword",
        "classes": ["form-control.g-input"],
        "text": [],
        "id": []
    },

    ## Messaging
    # all TODO

    {
        "name": "welcomeMessageToggle",
        "classes": [None],
        "text": [],
        "id": []
    },

    {
        "name": "welcomeMessageText",
        "classes": [None],
        "text": [],
        "id": []
    },

    {
        "name": "welcomeMessageUpload",
        "classes": [None],
        "text": [],
        "id": []
    },

    {
        "name": "welcomeMessageVoice",
        "classes": [None],
        "text": [],
        "id": []
    },

    {
        "name": "welcomeMessageVideo",
        "classes": [None],
        "text": [],
        "id": []
    },

    {
        "name": "welcomeMessagePrice",
        "classes": [None],
        "text": [],
        "id": []
    },

    {
        "name": "welcomeMessageSave",
        "classes": [None],
        "text": [],
        "id": []
    },

    {
        "name": "welcomeMessageHideToggle",
        "classes": [None],
        "text": [],
        "id": []
    },

    {
        "name": "showFullTextInEmailToggle",
        "classes": [None],
        "text": [],
        "id": []
    },

    ## Notifications
    # push notifications
    {
        "name": "pushNotifs",
        "classes": ["g-input__wrapper.m-checkbox__toggle"],
        "text": [],
        "id": ["push-notifications"]
    },
    # email notifications
    {
        "name": "emailNotifs",
        "classes": ["g-input__wrapper.m-checkbox__toggle"],
        "text": [],
        "id": ["email-notifications"]
    },
    # new referral email
    {
        "name": "emailNotifsReferral",
        "classes": ["b-input-radio"],
        "text": ["New Referral"],
        "id": []
    },
    # new stream email
    {
        "name": "emailNotifsStream",
        "classes": ["b-input-radio"],
        "text": ["New Stream"],
        "id": []
    },
    # new subscriber email
    {
        "name": "emailNotifsSubscriber",
        "classes": ["b-input-radio"],
        "text": ["New Subscriber"],
        "id": []
    },
    # new tip email
    {
        "name": "emailNotifsSubscriber",
        "classes": ["b-input-radio"],
        "text": ["New Tip"],
        "id": []
    },
    # new renewal email
    {
        "name": "emailNotifsSubscriber",
        "classes": ["b-input-radio"],
        "text": ["Renewal"],
        "id": []
    },

    {
        "name": "emailNotifsTip",
        "classes": ["b-input-radio"],
        "text": [],
        "id": []
    },
    #
    {
        "name": "emailNotifsRenewal",
        "classes": ["b-input-radio"],
        "text": [],
        "id": []
    },
    # new likes summary
    {
        "name": "emailNotifsLikes",
        "classes": [None],
        "text": [],
        "id": []
    },
    # new posts summary
    {
        "name": "emailNotifsPosts",
        "classes": [None],
        "text": [],
        "id": []
    },
    # new private message summary
    {
        "name": "emailNotifsPrivMessages",
        "classes": [None],
        "text": [],
        "id": []
    },
    # telegram bot button
    # BLANK
    # site notifications
    {
        "name": "siteNotifs",
        "classes": [None],
        "text": [],
        "id": []
    },
    # new comment notification
    {
        "name": "siteNotifsComment",
        "classes": [],
        "text": ["New comment"],
        "id": []
    },
    # new favorite notification
    {
        "name": "siteNotifsFavorite",
        "classes": [],
        "text": ["New favorite (like)"],
        "id": []
    },
    # discounts from users i've used to follow notification
    {
        "name": "siteNotifsDiscounts",
        "classes": [],
        "text": ["Discounts from users I used to follow"],
        "id": []
    },
    # new subscriber notification
    {
        "name": "siteNotifsSubscriber",
        "classes": [],
        "text": ["New Subscriber"],
        "id": []
    },
    # new tip notification
    {
        "name": "siteNotifsTip",
        "classes": [],
        "text": ["New Tip"],
        "id": []
    },
    # toast notification new comment
    {
        "name": "toastNotifsComment",
        "classes": [],
        "text": ["New comment"],
        "id": []
    },
    # toast notification new favorite
    {
        "name": "toastNotifsFavorite",
        "classes": [],
        "text": ["New favorite (like)"],
        "id": []
    },
    # toast notification new subscriber
    {
        "name": "toastNotifsSubscriber",
        "classes": [],
        "text": ["New Subscriber"],
        "id": []
    },
    # toast notification new tip
    {
        "name": "toastNotifsTip",
        "classes": [],
        "text": ["New Tip"],
        "id": []
    },

    ## Security

    # two step toggle
    # BLANK
    # fully private profile
    {
        "name": "fullyPrivate",
        "classes": [],
        "text": [],
        "id": ["is_private"]
    },
    # enable comments
    {
        "name": "enableComments",
        "classes": [],
        "text": [],
        "id": ["is_want_comments"]
    },
    # show fans count on profile
    {
        "name": "showFansCount",
        "classes": [],
        "text": [],
        "id": ["show_subscribers_count"]
    },
    # show posts tips summary
    {
        "name": "showPostsTip",
        "classes": [],
        "text": [],
        "id": ["show_posts_tips"]
    },
    # public friends list
    {
        "name": "publicFriendsList",
        "classes": [],
        "text": [],
        "id": ["show_friends_list"]
    },
    # geo blocking
    {
        "name": "ipCountry",
        "classes": ["multiselect__input"],
        "text": [],
        "id": []
    },
    # ip blocking
    {
        "name": "ipIP",
        "classes": [],
        "text": [],
        "id": ["input-blocked-ips"]
    },
    # watermarks photos
    {
        "name": "watermarkPhoto",
        "classes": [],
        "text": [],
        "id": ["hasWatermarkPhoto"]
    },
    # watermarks video
    {
        "name": "watermarkVideo",
        "classes": [],
        "text": [],
        "id": ["hasWatermarkVideo"]
    },
    # watermarks text
    {
        "name": "watermarkText",
        "classes": ["form-control.g-input"],
        "text": [],
        "id": []
    },
    ####### save changes may be the same for each
    ## Story
    # allow message replies - nobody
    {
        "name": "storyAllowRepliesNobody",
        "classes": [],
        "text": [],
        "id": ["allowNobody"]
    },
    # allow message replies - subscribers
    {
        "name": "storyAllowRepliesSubscribers",
        "classes": [],
        "text": [],
        "id": ["allowSubscribers"]
    },
    ## Other
    # obs server
    {
        "name": "liveServer",
        "classes": [],
        "text": [],
        "id": ["obsstreamingserver"]
    },
    # obs key
    {
        "name": "liveServerKey",
        "classes": [],
        "text": [],
        "id": ["streamingobskey"]
    },
    # welcome chat message toggle
    {
        "name": "welcomeMessageToggle",
        "classes": [],
        "text": [],
        "id": ["autoMessage"]
    },
    # then same pattern for message enter text or add stuff and price
    {
        "name": "welcomeMessageText",
        "classes": ["form-control.b-chat__message-input"],
        "text": [],
        "id": []
    },
    # save button for welcome chat message
    {
        "name": "welcomeMessageSave",
        "classes": ["g-btn.m-rounded.b-chat__btn-submit"],
        "text": [],
        "id": []
    },
    {
        "name": "profileSave",
        "classes": ["g-btn.m-rounded"],
        "text": ["Save changes"],
        "id": [],
    }

]


# # working
########################
# username
# displayName
# about
# location
# websiteURL

## security
# fullyPrivate
# enableComments
# showFansCount
# showPostsTip
# publicFriendsList
# ipCountry
# ipIP
# watermarkPhoto
# watermarkVideo
# watermarkText
# welcomeMessageToggle
## other
# liveServer
# liveServerKey

# # sorta working
########################
# coverImage
# profilePhoto
# password
# newPassword
# confirmPassword

# # all the notifs are probably false positives
# # are all b.input radio should maybe nth one found
# emailNotifsReferral
# emailNotifsStream
# emailNotifsSubscriber
# emailNotifsTip
# emailNotifsRenewal

# # not working
# ########################
# email
# emailNotifs
# emailNotifsPosts
# emailNotifsPrivMessages
# siteNotifs
# siteNotifsComment
# siteNotifsFavorite
# siteNotifsDiscounts
# siteNotifsSubscriber
# siteNotifsTip
# toastNotifsComment
# toastNotifsSubscriber
# toastNotifsTip
# welcomeMessageText

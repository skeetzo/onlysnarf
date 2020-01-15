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
    # BLANK
    # email notifications
    {
        "name": "emailNotifs",
        "classes": [None],
        "text": [],
        "id": []
    },
    # new referral email
    {
        "name": "emailNotifsReferral",
        "classes": [None],
        "text": [],
        "id": []
    },
    # new stream email
    {
        "name": "emailNotifsStream",
        "classes": ["b-input-radio"],
        "text": [],
        "id": []
    },
    # new subscriber email
    {
        "name": "emailNotifsSubscriber",
        "classes": ["b-input-radio"],
        "text": [],
        "id": []
    },
    # new tip email
    {
        "name": "emailNotifsSubscriber",
        "classes": ["b-input-radio"],
        "text": [],
        "id": []
    },
    # new renewal email
    {
        "name": "emailNotifsSubscriber",
        "classes": ["b-input-radio"],
        "text": [],
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
        "classes": [None],
        "text": [],
        "id": []
    },
    # new favorite notification
    {
        "name": "siteNotifsFavorite",
        "classes": [None],
        "text": [],
        "id": []
    },
    # discounts from users i've used to follow notification
    {
        "name": "siteNotifsDiscounts",
        "classes": [None],
        "text": [],
        "id": []
    },
    # new subscriber notification
    {
        "name": "siteNotifsSubscriber",
        "classes": [None],
        "text": [],
        "id": []
    },
    # new tip notification
    {
        "name": "siteNotifsTip",
        "classes": [None],
        "text": [],
        "id": []
    },
    # toast notification new comment
    {
        "name": "toastNotifsComment",
        "classes": [None],
        "text": [],
        "id": []
    },
    # toast notification new favorite
    {
        "name": "toastNotifsFavorite",
        "classes": [None],
        "text": [],
        "id": []
    },
    # toast notification new subscriber
    {
        "name": "toastNotifsSubscriber",
        "classes": [None],
        "text": [],
        "id": []
    },
    # toast notification new tip
    {
        "name": "toastNotifsTip",
        "classes": [None],
        "text": [],
        "id": []
    },

    ## Security

    # two step toggle
    # BLANK
    # fully private profile
    {
        "name": "fullyPrivate",
        "classes": [None],
        "text": [],
        "id": []
    },
    # enable comments
    {
        "name": "enableComments",
        "classes": [None],
        "text": [],
        "id": []
    },
    # show fans count on profile
    {
        "name": "showFansCount",
        "classes": [None],
        "text": [],
        "id": []
    },
    # show posts tips summary
    {
        "name": "showPostsTip",
        "classes": [None],
        "text": [],
        "id": []
    },
    # public friends list
    {
        "name": "publicFriendsList",
        "classes": [None],
        "text": [],
        "id": []
    },
    # geo blocking
    {
        "name": "ipCountry",
        "classes": [None],
        "text": [],
        "id": []
    },
    # ip blocking
    {
        "name": "ipIP",
        "classes": [None],
        "text": [],
        "id": []
    },
    # watermarks photos
    {
        "name": "watermarkPhoto",
        "classes": [None],
        "text": [],
        "id": []
    },
    # watermarks video
    {
        "name": "watermarkVideo",
        "classes": [None],
        "text": [],
        "id": []
    },
    # watermarks text
    {
        "name": "watermarkText",
        "classes": [None],
        "text": [],
        "id": []
    },
    ####### save changes may be the same for each
    ## Story
    # allow message replies - nobody
    {
        "name": "storyAllowRepliesNobody",
        "classes": [None],
        "text": [],
        "id": []
    },
    # allow message replies - subscribers
    {
        "name": "storyAllowRepliesSubscribers",
        "classes": [None],
        "text": [],
        "id": []
    },
    ## Other
    # obs server
    {
        "name": "liveServer",
        "classes": [None],
        "text": [],
        "id": []
    },
    # obs key
    {
        "name": "liveServerKey",
        "classes": [None],
        "text": [],
        "id": []
    },
    # welcome chat message toggle
    {
        "name": "welcomeMessageToggle",
        "classes": [None],
        "text": [],
        "id": []
    },
    # then same pattern for message enter text or add stuff and price
    {
        "name": "welcomeMessageText",
        "classes": [None],
        "text": [],
        "id": []
    },
    # save button for welcome chat message
    {
        "name": "welcomeMessageSave",
        "classes": [None],
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
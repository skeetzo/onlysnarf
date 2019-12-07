#!/usr/bin/python3
# Profile Settings

class Profile:

    # profile settings are either:
    #   enabled or disabled
    #   display text, variable type, variable name in settings
    def __init__(self):
        # url path or file upload
        self.coverImage = None
        # url path or file upload
        self.profilePhoto = None
        # text
        self.displayName = ""
        # text in $
        # minimum $4.99 or free
        self.subscriptionPrice = "4.99"
        # text
        self.about = ""
        # text
        self.location = ""
        # text as url
        self.websiteURL = None
        # text
        self.username = ""
        # text, can't be changed
        self.email = ""
        # text
        self.password = ""
        # enabled or disabled
        self.emailNotifs = False
        # enabled or disabled
        self.emailNotifsNewReferral = False
        # enabled or disabled
        self.emailNotifsNewStream = False
        # enabled or disabled
        self.emailNotifsNewSubscriber = False
        # enabled or disabled
        self.emailNotifsNewTip = False
        # enabled or disabled
        self.emailNotifsRenewal = False
        # enabled or disabled
        self.emailNotifsNewLikes = False
        # enabled or disabled
        self.emailNotifsNewPosts = False
        # enabled or disabled
        self.emailNotifsNewPrivMessages = False
        # enabled or disabled
        self.siteNotifs = False
        # enabled or disabled
        self.siteNotifsNewComment = False
        # enabled or disabled
        self.siteNotifsNewFavorite = False
        # enabled or disabled
        self.siteNotifsDiscounts = False
        # enabled or disabled
        self.siteNotifsNewSubscriber = False
        # enabled or disabled
        self.siteNotifsNewTip = False
        # enabled or disabled
        self.toastNotifs = False
        # enabled or disabled
        self.toastNotifsNewComment = False
        # enabled or disabled
        self.toastNotifsNewFavorite = False
        # enabled or disabled
        self.toastNotifsNewSubscriber = False
        # enabled or disabled
        self.toastNotifsNewTip = False
        # enabled or disabled
        self.fullyPrivate = False
        # enabled or disabled
        self.enableComments = False
        # enabled or disabled
        self.showFansCount = False
        # enabled or disabled
        self.showPostsTip = False
        # enabled or disabled
        self.publicFriendsList = False
        # selection of countries
        self.ipCountry = getCountryList()
        # text of ip ranges
        self.ipIP = ""
        # enabled or disabled
        self.watermark = True
        # enabled or disabled
        self.watermarkPhoto = False
        # enabled or disabled
        self.watermarkVideo = False
        # the custom watermark text
        self.watermarkText = ""
        if self.username and str(self.username) != "":
            self.watermarkText = "OnlyFans.com/{}".format(self.username)
        # the obs live server
        self.liveServer = ""
        # the obs live server key
        self.liveServerKey = ""

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, val):
        return setattr(self, key, val)




def getCountryList():
    return ["USA","Canada"]

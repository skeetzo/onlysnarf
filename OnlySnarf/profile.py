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
        self.ipCountry = get_country_list()
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



    @staticmethod
    def get_country_list():
        return ["USA","Canada"]


    # place the classes in their respective elements in elements.py
    # add welcome chat message to new subscribers toggle and upload options


    # has save:
    # profile
    # account
    # security

    # doesn't have save:
    # story
    # notifications
    # other

    # update inputTypes with either text or toggle

    # returns list of settings and their classes
    @staticmethod
    def get_settings_variables():
        # ["settingVariableName","pageProfile","inputType-text"]
        return [
             ### Profile ###
            ["coverImage","profile","file"],
            ["profilePhoto","profile","file"],
            # display name needs to match: placeholder="Display name"
            ["displayName","profile","text"],
            # subscription price needs to match: name="subscribePrice" 
            ["subscriptionPrice","text"],
            # about placeholder is: placeholder="About"
            # id="input-about"
            ["about","profile","text"],
            # id="input-location"
            ["location","profile","text"],
            # id="input-website"
            ["websiteURL","profile","text"],
            #### Account ###
            # id="input-login"
            ["username","account","text"],
            # id="input-email"
            ["email","account","text"],
            # id="old_password_input"
            ["password","account","text"],
            # id="new_password_input"
            ["newPassword","account","text"],
            # id="new_password2_input"
            ["confirmPassword","account","checkbox"],
            ### Notifications ###
            # id="push-notifications"
            ["emailNotifs","notifications","toggle"],
            # id="email-notifications"
            ["emailNotifsNewReferral","notifications","checkbox"],

            ["emailNotifsNewStream","notifications","toggle"],

            ["emailNotifsNewSubscriber","notifications","toggle"],

            ["emailNotifsNewTip","notifications","toggle"],

            ["emailNotifsRenewal","notifications","toggle"],

            # this is a dropdown
            ["emailNotifsNewLikes","notifications","dropdown"],

            ["emailNotifsNewPosts","notifications","toggle"],

            ["emailNotifsNewPrivMessages","notifications","toggle"],

            ["siteNotifs","notifications","toggle"],

            ["siteNotifsNewComment","notifications","toggle"],

            ["siteNotifsNewFavorite","notifications","toggle"],

            ["siteNotifsDiscounts","notifications","toggle"],

            ["siteNotifsNewSubscriber","notifications","toggle"],

            ["siteNotifsNewTip","notifications","toggle"],

            ["toastNotifsNewComment","notifications","toggle"],

            ["toastNotifsNewFavorite","notifications","toggle"],

            ["toastNotifsNewSubscriber","notifications","toggle"],

            ["toastNotifsNewTip","notifications","toggle"],

            ### Security ###

            ["fullyPrivate","security","checkbox","toggle"],

            ["enableComments","security","toggle"],

            ["showFansCount","security","toggle"],

            ["showPostsTip","security","toggle"],

            ["publicFriendsList","security","toggle"],

            ["ipCountry","security","list"],
            # id="input-blocked-ips"
            ["ipIP","security","list"],
            # id="hasWatermarkPhoto"
            ["watermarkPhoto","security","toggle"],
            # id="hasWatermarkVideo"
            ["watermarkVideo","security","toggle"],
            # placeholder="Watermark custom text"
            ["watermarkText","security","text"],

            ### Other ###
            ["liveServer","other","text"],

            ["liveServerKey","other","text"]

        ]


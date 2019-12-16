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




def get_country_list():
    return ["USA","Canada"]


# replace the classes with their name references
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
def get_settings_variables():
    # ["settingVariableName","pageProfile",".setting.html.class","inputType-text"]
    return [
         ### Profile ###
        ["coverImage","profile","b-user-panel__cover__img","inputType"],
        ["profilePhoto","profile","g-btn.m-rounded.m-sm.m-border","inputType"],
        # display name needs to match: placeholder="Display name"
        ["displayName","profile","form-control.g-input","inputType"],
        # subscription price needs to match: name="subscribePrice" 
        ["subscriptionPrice","form-control.g-input","classname","inputType"],
        # about placeholder is: placeholder="About"
        # id="input-about"
        ["about","profile","form-control.g-input.unlimsize","inputType"],
        # id="input-location"
        ["location","profile","form-control.g-input","inputType"],
        # id="input-website"
        ["websiteURL","profile","form-control.g-input","inputType"],
        #### Account ###
        # id="input-login"
        ["username","account","form-control.g-input","inputType"],
        # id="input-email"
        ["email","account","form-control.g-input","inputType"],
        # id="old_password_input"
        ["password","account","form-control.g-input","inputType"],
        # id="new_password_input"
        ["newPassword","account","form-control.g-input","inputType"],
        # id="new_password2_input"
        ["confirmPassword","account","form-control.g-input","inputType"],
        ### Notifications ###
        # id="push-notifications"
        ["emailNotifs","notifications","checkbox","inputType"],
        # id="email-notifications"
        ["emailNotifsNewReferral","notifications","checkbox","inputType"],

        ["emailNotifsNewStream","notifications","b-input-radio","inputType"],

        ["emailNotifsNewSubscriber","notifications","b-input-radio","inputType"],

        ["emailNotifsNewTip","notifications","b-input-radio","inputType"],

        ["emailNotifsRenewal","notifications","b-input-radio","inputType"],



    # this is a dropdown
        ["emailNotifsNewLikes","notifications","checkbox","inputType"],


        # get inner text of all these

        ["emailNotifsNewPosts","notifications","checkbox","inputType"],

        ["emailNotifsNewPrivMessages","notifications","checkbox","inputType"],

        ["siteNotifs","notifications","checkbox","inputType"],

        ["siteNotifsNewComment","notifications","b-input-radio","inputType"],

        ["siteNotifsNewFavorite","notifications","b-input-radio","inputType"],

        ["siteNotifsDiscounts","notifications","b-input-radio","inputType"],

        ["siteNotifsNewSubscriber","notifications","b-input-radio","inputType"],

        ["siteNotifsNewTip","notifications","b-input-radio","inputType"],

        ["toastNotifsNewComment","notifications","b-input-radio","inputType"],

        ["toastNotifsNewFavorite","notifications","b-input-radio","inputType"],

        ["toastNotifsNewSubscriber","notifications","b-input-radio","inputType"],

        ["toastNotifsNewTip","notifications","b-input-radio","inputType"],

        ### Security ###

        ["fullyPrivate","security","checkbox","inputType"],

        ["enableComments","security","classname","inputType"],

        ["showFansCount","security","classname","inputType"],

        ["showPostsTip","security","classname","inputType"],

        ["publicFriendsList","security","classname","inputType"],

        ["ipCountry","security","multiselect__input","inputType"],
        # id="input-blocked-ips"
        ["ipIP","security","form-control.g-input.unlimsize","inputType"],
        # id="hasWatermarkPhoto"
        ["watermarkPhoto","security","classname","inputType"],
        # id="hasWatermarkVideo"
        ["watermarkVideo","security","classname","inputType"],
        # placeholder="Watermark custom text"
        ["watermarkText","security","form-control.g-input","inputType"],

        ### Other ###
        ["liveServer","other","form-control.g-input","inputType"],

        ["liveServerKey","other","form-control.g-input","inputType"]

    ]


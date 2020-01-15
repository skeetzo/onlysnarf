#!/usr/bin/python3
# Profile Settings

# from OnlySnarf.driver import Driver

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
        self.ipCountry = Profile.get_country_list()
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

    def syncFrom(self):
        # opens every settings page in the browser from pages or all
        # gets necessary variables from browser
        variables = Profile.get_setting_variables()
        pages = []
        for var in variables:
            if var[1] not in pages:
                pages.append(var[1])
        for page in pages:
            pass
            # Driver.go_to_settings_page(page)
        pass            

    def syncTo(self):
        # opens every settings page in the browser from pages or all
        # updates necessary variables in browser
        pass

    @staticmethod
    def get_country_list():
        return ["USA","Canada"]

    @staticmethod
    def get_pages():
        return ["profile", "advanced", "messaging", "notifications", "security", "story", "other"]

    @staticmethod
    def get_variables_for_page(page):
        variables = get_settings_variables()
        vars_ = []
        for var in variables:
            if str(var[1]) == str(page):
                vars_.append(var)
        return vars_

    @staticmethod
    def get_setting_variable(key):
        variables = get_setting_variables()
        for var in variables:
            if str(var[0]) == str(key):
                return var
        return None

    def update_value(self, key, value):
        try:
            if key == None or str(key) == "" or str(key) == "None": return
            self[key] = value
        except Exception as e:
            print(e)

    # returns list of settings and their classes
    # ["settingVariableName","pageProfile","inputType-text"]
    
def get_settings_variables():
    return [

        ### Profile ###

        ["coverImage","profile","file"],
        ["profilePhoto","profile","file"],
        ["username","profile","text"],
        ["displayName","profile","text"],
        ["subscriptionPrice","text"],
        ["referralReward","dropdown"],
        ["about","profile","text"],
        ["location","profile","text"],
        ["websiteURL","profile","text"],

        #### Account / Advanced ###

        # id="input-email"
        ["email","advanced","text"],
        # id="old_password_input"
        ["password","advanced","text"],
        # id="new_password_input"
        ["newPassword","advanced","text"],
        # id="new_password2_input"
        ["confirmPassword","advanced","checkbox"],

        ### Chats / Messages ###
        # welcome message toggle
        # welcome message text
        # welcome message file
        # welcome message record voice, video
        # welcome message price
        # welcome message submit

        # hide outgoing message toggle
        # show full text of message in the notification email

        ### Notifications ###

        # id="push-notifications"
        ["emailNotifs","notifications","toggle"],
        # id="email-notifications"
        ["emailNotifsReferral","notifications","checkbox"],
        ["emailNotifsStream","notifications","toggle"],
        ["emailNotifsSubscriber","notifications","toggle"],
        ["emailNotifsTip","notifications","toggle"],
        ["emailNotifsRenewal","notifications","toggle"],
        # this is a dropdown
        ["emailNotifsLikes","notifications","dropdown"],
        ["emailNotifsPosts","notifications","toggle"],
        ["emailNotifsPrivMessages","notifications","toggle"],
        ["siteNotifs","notifications","toggle"],
        ["siteNotifsComment","notifications","toggle"],
        ["siteNotifsFavorite","notifications","toggle"],
        ["siteNotifsDiscounts","notifications","toggle"],
        ["siteNotifsSubscriber","notifications","toggle"],
        ["siteNotifsTip","notifications","toggle"],
        ["toastNotifsComment","notifications","toggle"],
        ["toastNotifsFavorite","notifications","toggle"],
        ["toastNotifsSubscriber","notifications","toggle"],
        ["toastNotifsTip","notifications","toggle"],

        ### Security ###

        ["fullyPrivate","security","checkbox"],
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

        ### Story ###
        # allow message replies - nobody
        # allow message replies - subscribers

        ### Other ###

        ["liveServer","other","text"],
        ["liveServerKey","other","text"],
        ["welcomeMessageToggle","other","toggle"],
        ["welcomeMessageText","other","text"],

    ]


#!/usr/bin/python3
# Profile Settings
import json
##
from ..lib.driver import Driver
from ..util.settings import Settings
from .user import User

class Profile:
    TABS = ["profile", "advanced", "messaging", "notifications", "security", "story", "other"]

    # profile settings are either:
    #   enabled or disabled
    #   display text, variable type, variable name in settings
    def __init__(self):
        profile = Profile.fill_data()
        for key, value in profile.items():
            setattr(self, str(key), value)

    # Backup

    @staticmethod
    def backup_content():
        print("Backing Up: Content")
        Driver.download_content()
        ## TODO
        # files = Driver.download_content()
        # Files.backup(files)
        print("Backed Up: Content")
        return True

    @staticmethod
    def backup_messages():
        print("Backing Up: Messages")
        # select user
        user = "all"
        # user = User.select_user()
        Driver.download_messages(user)
        print("Backed Up: Messages")

    # new - advertise - tweet to advertise new account, tweet to ask about what you should post
    def advertise():
        pass

    def advertise_menu():
        pass

    # check settings for 'profile completion'
    # |- subscription price |- calculate recommended price from percentile count, posts numbers etc 
    # |-  Reward for subscriber referrals
    # |- about, location, website url, wishlist
    # |- if connected twitter/google
    # |- welcome message enabled
    # |- two step authentication
    # |- watermark enabled & custom text
    def check():
        if not Settings.is_debug():
            print("### Not Available ###")
            return
        print("Checking Profile Settings")
        profile = Profile.read_local() or Profile.create()
        desiredProfile = {
            "subprice":"avalue", # do manually to check price number as int
            "about":"avalue",
            "location":"avalue",
            "websiteURL":"avalue",
            "wishlist":"avalue",
            "twitter":"avalue",
            "google":"avalue",
            "welcomeMessage":"avalue",
            "twoStepAuth":True,
            "watermark":True,
            "watermarkPhoto":True,
            "watermarkVideo":True
        }
        # get profile settings
        # check against preferred settings
        # output message
        failed = False
        for key, value in profile.items():
            for key_, value_ in desiredProfile.items():
                Settings.dev_print("{}: {} = {}".format(key, value, value_))
                if value and str(value_) != "avalue":
                    if value != value_:
                        print("Warning: Unrecommended setting - {}".format(key))
                        failed = True
                elif not value or str(value) != str(value_):
                    print("Warning: Unrecommended setting - {}".format(key))
                    failed = True
        if failed:
            print("Error: Profile check failed!")
            return False
        print("Success! Profile check completed.")
        return True

    # update basic new profile settings w/ profile settings or prompt 
    # get Twitter profile & banner and use to update profile & banner
    # About, Price, Wishlist
    # watermark enabled & custom text == username
    def setup():
        if not Settings.is_debug():
            print("### Not Available ###")
            return
        print("Setting up basic profile settings")
        profile = Profile.read_local() or Profile.create()
        desiredProfile = {
            "subprice":"avalue", # do manually to check price number as int
            "about":"avalue",

            "welcomeMessage":"avalue",
            "watermark":True,
            "watermarkText":True
        }
        
        # compare to existing values to ignore already correctly set values
        for key, value in profile.items():
            for key_, value_ in desiredProfile.items():
                if str(key) == "subprice":
                    # do stuff
                    continue

                Settings.dev_print("{}: {} = {}".format(key, value, value_))
                setattr(profile, str(key), value_)

        # search for twitter banner
        twitterBanner = None
        # search for twitter profile photo
        twitterProfile = None
        # update both
        setattr(profile, "coverImage", twitterBanner)
        setattr(profile, "profilePhoto", twitterProfile)
        Profile.sync_to_profile(profile=profile)

    def posts_menu():
        if not Settings.is_debug():
            print("### Not Available ###")
            return
        action = Profile.ask_new()
        if (action == 'back'): return Profile.menu()
        elif (action == 'advertise'):
            Profile.advertise()
        # elif (action == 'new')
        # elif (action == 'new')

        Profile.menu()

    @staticmethod
    def menu():
        action = Profile.ask_action()
        if (action == 'Back'): 
            from OnlySnarf.bin.menu import Menu
            return Menu.main_menu()
        elif (action == 'backup'): Profile.backup_menu()
        elif (action == 'check'): Profile.check()
        elif (action == 'posts'): Profile.posts_menu()
        elif (action == 'setup'): Profile.setup()
        elif (action == 'sync'): Profile.sync_from_profile()
        # elif (action == 'sync to'): Profile.sync_to_profile()
        
    @staticmethod
    def get_profile():
        print("Getting Profile")
        profile = Profile()
        for tab in Profile.TABS:
            profile.sync_from_tab(tab)
        return profile

    @staticmethod
    def sync_from_profile():
        # opens every settings tab in the browser from pages or all
        # gets necessary variables from browser
        # variables = get_settings_variables()
        print("Syncing from Profile")
        profile = Profile()
        for tab in Profile.TABS:
            profile.sync_from_tab(tab)
        print("Synced from Profile")
        Profile.write_local(profile)
        return True

    @staticmethod
    def sync_to_profile(profile=None):
        # syncs profile settings to onlyfans
        print("Syncing to Profile")
        if not profile:
            profile = Profile.read_local() or Profile.create()
        for tab in Profile.TABS:
            profile.sync_to_tab(tab)
        print("Synced to Profile")
        return True

    def sync_from_tab(self, tab):
        # syncs profile settings from the specificed tab
        Driver.sync_from_settings_page(profile=self, page=tab)

    def sync_to_tab(self, tab):
        # syncs profile settings to the specificed tab
        Driver.sync_to_settings_page(profile=self, page=tab)

    @staticmethod
    def get_country_list():
        return ["USA","Canada"]

    @staticmethod
    def get_variables_for_page(page):
        variables = get_settings_variables()
        vars_ = []
        for var in variables:
            if str(var[1]) == str(page):
                vars_.append(var)
        return vars_

    @staticmethod
    def fill_data():
        prof = {
            "coverImage": None,
            "profilePhoto": None,
            "displayName": "",
            "subscriptionPrice": "4.99",
            "about": "",
            "location": "",
            "websiteURL": None,
            "wishlist":None,
            "twitter":None,
            "google":None,
            "welcomeMessage":None,
            "twoStepAuth":False,
            "username": "",
            "email": "",
            "password": "",
            "emailNotifs": False,
            "emailNotifsNewReferral": False,
            "emailNotifsNewStream": False,
            "emailNotifsNewSubscriber": False,
            "emailNotifsNewTip": False,
            "emailNotifsRenewal": False,
            "emailNotifsNewLikes": False,
            "emailNotifsNewPosts": False,
            "emailNotifsNewPrivMessages": False,
            "siteNotifs": False,
            "siteNotifsNewComment": False,
            "siteNotifsNewFavorite": False,
            "siteNotifsDiscounts": False,
            "siteNotifsNewSubscriber": False,
            "siteNotifsNewTip": False,
            "toastNotifs": False,
            "toastNotifsNewComment": False,
            "toastNotifsNewFavorite": False,
            "toastNotifsNewSubscriber": False,
            "toastNotifsNewTip": False,
            "fullyPrivate": False,
            "enableComments": False,
            "showFansCount": False,
            "showPostsTip": False,
            "publicFriendsList": False,
            "ipCountry": Profile.get_country_list(),
            "ipIP": "",
            "watermark": True,
            "watermarkPhoto": False,
            "watermarkVideo": False,
            "watermarkText": "",
            "liveServer": "",
            "liveServerKey": ""
        }
        if prof.get("username") and str(prof.get("username")) != "" and prof.get("watermarkText") == "":
            prof.set("watermarkText", "OnlyFans.com/{}".format(prof.get("username")))
        return prof

    @staticmethod
    def read_local():
        Settings.maybe_print("Getting Local Profile")
        profile = None
        try:
            profile_ = {}
            with open(str(Settings.get_profile_path())) as json_file:  
                profile_ = json.load(json_file)['profile']
            Settings.maybe_print("Loaded Local Profile")
            profile = Profile()
            for key, value in profile_:
                setattr(profile, str(key), value)
        except Exception as e:
            Settings.dev_print(e)
        return profile

    @staticmethod
    def write_local(profile=None):
        if profile is None:
            profile = Profile.get_profile()
        print("Saving Profile Locally")
        Settings.maybe_print("local profile path: "+str(Settings.get_profile_path()))
        try:
            with open(str(Settings.get_profile_path()), 'w') as outfile:  
                json.dump({"profile":profile.__dict__}, outfile, indent=4, sort_keys=True)
        except FileNotFoundError:
            print("Error: Missing Profile File")
        except OSError:
            print("Error: Missing Profile Path")

    # returns list of settings and their classes
    # ["settingVariableName","pageProfile","inputType-text"]
    
def get_settings_variables():
    return [

        ### Profile ###

        ["coverImage","profile","file"],
        ["profilePhoto","profile","file"],
        ["username","profile","text"],
        ["displayName","profile","text"],
        ["subscriptionPrice","profile","text"],
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


#!/usr/bin/python3
# Profile Settings
from PyInquirer import prompt
from .driver import Driver
from .settings import Settings

class Profile:
    TABS = ["profile", "advanced", "messaging", "notifications", "security", "story", "other"]

    # profile settings are either:
    #   enabled or disabled
    #   display text, variable type, variable name in settings
    def __init__(self):
        profile = Profile.fill_data()
        for key, value in profile.items():
            setattr(self, str(key), value)

    # def __getitem__(self, key):
    #     return getattr(self, str(key))

    # def __setitem__(self, key, val):
    #     return setattr(self, str(key), val)

    # Backup

    def ask_backup():
        options = ["back"]
        menu_prompt = {
            'type': 'list',
            'name': 'action',
            'message': 'Please select a backup action:',
            'choices': ['All', 'Content', 'Messages', 'Content & Messages', 'Profile'],
            'filter': lambda val: str(val).lower()
        }
        answers = prompt(menu_prompt)
        return answers['action']

    def backup_menu():
        if not Settings.is_debug():
            print("### Not Available ###")
            return
        backup = Profile.ask_backup()
        if (backup == 'back'): pass
        elif (backup == 'content'):
            Profile.backup_content()
        elif (backup == 'messages'):
            Profile.backup_messages()
        elif (backup == 'profile'):
            Profile.backup_profile()
        elif (backup == 'content & messages'):
            Profile.backup_content()
            Profile.backup_messages()
        elif (backup == 'all'):
            Profile.backup_content()
            Profile.backup_messages()
            Profile.backup_profile()

    @staticmethod
    def backup_content():
        print("Backing Up: Content")
        print("Backed Up: Content")

    @staticmethod
    def backup_messages():
        print("Backing Up: Messages")
        print("Backed Up: Messages")

    @staticmethod
    def backup_profile():
        print("Backing Up: Profile")
        print("Backed Up: Profile")

    @staticmethod
    def menu():
        if not Settings.is_debug():
            print("### Not Available ###")
            return
        action = Profile.ask_action()
        if (action == 'Back'): pass
        elif (action == 'backup'): Profile.backup_menu()
        elif (action == 'sync from'): Profile.sync_from_profile()
        elif (action == 'sync to'): Profile.sync_to_profile()

    def ask_action():
        menu_prompt = {
            'type': 'list',
            'name': 'action',
            'message': 'Please select a profile action:',
            'choices': ['Back', 'Backup','Sync From', 'Sync To'],
            'filter': lambda val: str(val).lower()
        }
        answers = prompt(menu_prompt)
        return answers['action']

    @staticmethod
    def create():
        # checks settings / config for profile settings config file
        # asks for missing options

        # returns a local copy / expectation of the Profile settings
        pass

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
        return profile

    @staticmethod
    def sync_to_profile(profile=None):
        # syncs profile settings to onlyfans
        print("Syncing to Profile")
        if not profile:
            profile = Profile.create()
        for tab in Profile.TABS:
            profile.sync_to_tab(tab)
        print("Synced to Profile")

    def sync_from_tab(self, tab):
        # syncs profile settings from the specificed tab
        data = Driver.sync_from_settings_page(tab)
        for key, value in data:
            print("{} - {}".format(key, value))
            setattr(self, str(key), value)

    def sync_to_tab(self, tab):
        # syncs profile settings to the specificed tab
        Driver.sync_to_settings_page(self, tab)

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
        profile_ = {}
        try:
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
            profile = Profile.sync_from_profile()
        print("Saving Profile Locally")
        Settings.maybe_print("local profile path: "+str(Settings.get_profile_path()))
        try:
            with open(str(Settings.get_profile_path()), 'w') as outfile:  
                json.dump({"profile":profile}, outfile, indent=4, sort_keys=True)
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


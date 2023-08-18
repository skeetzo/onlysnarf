#!/usr/bin/python3

from .lib.driver import Driver
from .lib.config import Config
from .lib.menu import Menu
from .util.settings import Settings
from .classes.discount import Discount
from .classes.message import Message, Post
from .classes.profile import Profile
from .classes.promotion import Promotion
from .classes.user import User
from .server import api as API

#################
##### Snarf #####
#################

class Snarf:

    """
    OnlySnarf main class and runtime parser.

    All methods are static and handle the basic runtime operations, 
     importing variables from settings & args.

    """

    def __init__(self, config):
        """Snarf object"""

        self.config = config

    @staticmethod
    def close():
        Driver.exit_all()
        Settings.print("*snarf waves goodbye*")

    @staticmethod
    def api():
        API.main()

    @staticmethod
    def config():
        Config.main()

    @staticmethod
    def menu():
        Menu.main()

    @staticmethod
    def discount():

        """
        Applies a discount to users as provided from args / prompts.


        """

        try:
            successful = []
            for user in Settings.get_users():
                Settings.print("> Discounting fan: {}".format(user.username))
                discount = Discount(user.username)
                successful.append(discount.apply())
            return all(successful)
        except Exception as e: Settings.dev_print(e)
        return False

    @staticmethod
    def message():

        """
        Sends the configured message from args / prompts.

        
        """

        try:
            successful = []
            for user in Settings.get_users():
                Settings.print("> Messaging fan: {}".format(user.username))
                message = Message(user.username)
                successful.append(message.send(user.username, user_id=user.id))
            return all(successful)
        except Exception as e: Settings.dev_print(e)
        return False
                
    @staticmethod
    def post():

        """
        Posts the configured text from args / prompts.

        
        """

        post = Post()
        try: return post.send()
        except Exception as e: Settings.dev_print(e)
        return False

    @staticmethod
    def profile():

        """
        Runs the profile method specified at runtime.

        backup - downloads all content and saves settings

        syncFrom - reads all profile settings and saves locally

        syncTo - updates profile settings with provided profile

        Extended description of function.

        """

        profile = Profile()
        try: 
            # get profile method
            method = Settings.get_profile_method()
            if method == "backup": return Profile.backup_content()
            elif method == "syncfrom": return Profile.sync_from_profile()
            elif method == "syncto": return Profile.sync_to_profile()
            else: Settings.err_print("Missing Profile Method")
        except Exception as e: Settings.dev_print(e)
        return False
        
    @staticmethod
    def promotion():

        """
        Runs the promotion method specified at runtime.

        campain - creates discount campaign

        trial - creates free trial

        user - applies directly to user

        grandfather - applies discounted price to existing users and adds them all to list

        """

        try: 
            # get promotion method
            method = Settings.get_promotion_method()
            if method == "campaign": return Promotion.create_campaign()
            elif method == "trial": return Promotion.create_trial_link()
            elif method == "user": return Promotion.apply_to_user()
            elif method == "grandfather": return Promotion.grandfathered()
            else: Settings.err_print("Missing Promotion Method")
        except Exception as e: Settings.dev_print(e)
        return False

    @staticmethod
    def users():

        """
        Scan users.

        
        """

        try:
            Settings.set_prefer_local(False)
            User.get_all_users()
            return True
        except Exception as e: Settings.dev_print(e)
        return False

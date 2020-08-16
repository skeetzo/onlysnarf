#!/usr/bin/python3
# main OnlySnarf class

import random
import os
import shutil
import datetime
import json
import sys
import pathlib
import time
##
from .settings import Settings

#####################
##### OnlySnarf #####
#####################

class Snarf:

    def __init__(self):
        pass

    ###############
    ##### Bot #####
    ###############

    @staticmethod
    def bot(bot=None):
        try:
            from .bot import Bot
            if not bot: bot = Bot()
            bot.run()
        except Exception as e: Settings.dev_print(e)

    ####################
    ##### Discount #####
    ####################

    @staticmethod
    def discount(discount=None):
        from .classes import Discount
        if not discount: discount = Discount()
        try: discount.apply()
        except Exception as e: Settings.dev_print(e)

    ###################
    ##### Message #####
    ###################

    @staticmethod
    def message(message=None):
        from .classes import Message
        from .user import User
        if not message: message = Message()
        try:
            message.get_message()
            if Settings.is_prompt():
                if not Settings.prompt("Send"): return
            if message.get_files() != "unset" and len(message.get_files()) == 0 and not message.get_text():
                print("Error: Missing Files and Text")
                return
            successful = False
            try: 
                # for user in self.get_recipients():
                for user in message.users:
                    # if isinstance(user, str) and str(user) == "post": successful_ = Driver.post(self)
                    # print("Messaging: {}".format(user.username))
                    if isinstance(user, User): successful = User.message_user(username=user.username, message=message)
                    else: successful = User.message_user(username=user, message=message)
            except Exception as e:
                Settings.dev_print(e)
                successful = False
            if successful: message.cleanup_files()
        except Exception as e: Settings.dev_print(e)
                
    ################
    ##### Post #####
    ################

    @staticmethod
    def post(message=None):
        from .classes import Message
        if not message: message = Message()
        try:
            message.get_post()
            if Settings.is_prompt():
                if not Settings.prompt("Post"): return
            if message.get_files() != "unset" and len(message.get_files()) == 0 and not message.get_text():
                print("Error: Missing Files and Text")
                return
            successful = False
            try:
                from .driver import Driver 
                successful = Driver.post(message=message)
            except Exception as e:
                Settings.dev_print(e)
                successful = False
            if successful: message.cleanup_files()
        except Exception as e: Settings.dev_print(e)

    ###################
    ##### Profile #####
    ###################

    @staticmethod
    def profile(profile=None):
        from .profile import Profile
        if not profile: profile = Profile()
        try: 
            # get profile method
            method = Settings.get_profile_method()
            if method == "backup":
                profile.backup_content()
            elif method == "syncfrom":
                Profile.sync_from_profile()
            elif method == "syncto":
                Profile.sync_to_profile()
            else: Settings.err_print("Missing Profile Method")
        except Exception as e: Settings.dev_print(e)
        
    #####################
    ##### Promotion #####
    #####################

    @staticmethod
    def promotion(promotion=None):
        from .classes import Promotion
        if not promotion: promotion = Promotion()
        try: 
            # get promotion method
            method = Settings.get_promotion_method()
            if method == "campaign":
                promotion.create_campaign()
            elif method == "trial":
                promotion.create_trial_link()
            elif method == "user":
                promotion.apply_to_user()
            else: Settings.err_print("Missing Promotion Method")
        except Exception as e: Settings.dev_print(e)

    #################
    ##### Users #####
    #################

    @staticmethod
    def get_following():
        from .user import User
        users = []
        try: users = User.get_following()
        except Exception as e: Settings.dev_print(e)
        return users

    @staticmethod
    def get_users():
        from .user import User
        users = []
        try: users = User.get_all_users()
        except Exception as e: Settings.dev_print(e)
        return users

    ###############
    ##### Dev #####
    ###############

    @staticmethod
    def test():
        from .user import User
        # from . import cron as Cron
        # print('0/3 : Deleting Locals')
        print('1/3 : Testing')
        # print('TESTING: Users')
        # response = Driver.users_get()
        # return True
        # print('TESTING: Following')
        # response = User.get_following()
        # from .classes import Promotion
        # promotion = Promotion()
        
        # promotion.create_campaign()
        # return True
        print('TESTING: Settings - Get')
        profile = Profile.sync_from_profile()
        print('TESTING: Settings - Set')
        Profile.sync_to_profile(profile=profile)

        return True
        # print('TESTING: Cron')
        # response = Cron.test()
        # if not response or response == None:
        #     print("Error: Failed to test crons")
        # reset_ = reset()
        # if not reset_:
        #     return print("Error: Failed to Reset")
        return True

################################################################################################################################################

import atexit
def exit_handler():
    from .driver import Driver
    Driver.exit_all()
    print("Shnarrf?")
    exit()
atexit.register(exit_handler)

# import signal
# def signal_handler(sig, frame):
#     print('Shnnnarf?')
#     exit()
# signal.signal(signal.SIGINT, signal_handler)
  
def exit():
    sys.exit(0)

def main():
    try:
        from .file import File
        # File.remove_local()
        Settings.set_prompt(False)
        Settings.set_confirm(False)
        action = Settings.get_action()
        print("Running - {}".format(action))
        ## Actions
        success = False
        if str(action) == "test":
            success = Snarf.test()
        elif str(action) == "bot":
            success = Snarf.bot()
        elif str(action) == "post":
            success = Snarf.post()
        elif str(action) == "message":
            success = Snarf.message()
        elif str(action) == "discount":
            success = Snarf.discount()
        elif str(action) == "promotion":
            success = Snarf.promotion()
        elif str(action) == "profile":
            success = Snarf.profile()
        else:
            print("Warning: Missing Method")
    except Exception as e:
        Settings.dev_print(e)
        print("Shnarf!")
    finally:
        exit()

################################################################################################################################################

if __name__ == "__main__":
    main()
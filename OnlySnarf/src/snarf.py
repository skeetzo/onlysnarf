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

    ####################
    ##### Discount #####
    ####################

    @staticmethod
    def discount(discount=None):
        from .classes import Discount
        if not discount: discount = Discount()
        try: discount.apply()
        except Exception as e: Settings.dev_print(e)
        Snarf.exit()

    ################
    ##### Exit #####
    ################

    @staticmethod
    def exit():
        from .driver import Driver
        Driver.exit()

    #################
    ##### Login #####
    #################

    @staticmethod
    def login():
        from .driver import Driver
        loggedIn = False
        try: loggedIn = Driver.auth()
        except Exception as e: Settings.dev_print(e)
        return loggedIn

    ###################
    ##### Message #####
    ###################

    @staticmethod
    def message(message=None):
        from .message import Message
        if not message: message = Message()
        try: message.send()
        except Exception as e: Settings.dev_print(e)
        Snarf.exit()
                
    ################
    ##### Post #####
    ################

    @staticmethod
    def post(message=None):
        from .message import Message
        if not message: message = Message()
        try: message.post()
        except Exception as e: Settings.dev_print(e)
        Snarf.exit()

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
            else: print("{}: Missing Profile Method".format(colorize("Error","red")))
        except Exception as e: Settings.dev_print(e)
        Snarf.exit()
        
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
            if method == "user":
                promotion.apply_to_user()
            elif method == "trial":
                promotion.create_trial_link()
            else: print("{}: Missing Promotion Method".format(colorize("Error","red")))
        except Exception as e: Settings.dev_print(e)
        Snarf.exit()

    #################
    ##### Reset #####
    #################

    @staticmethod
    def reset():
        from .driver import Driver
        Driver.reset()

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
        from .driver import Driver
        from . import cron as Cron
        print('0/3 : Deleting Locals')
        print('1/3 : Testing')
        print('TESTING: Users')
        response = Driver.users_get()
        # return True
        print('TESTING: Following')
        response = Driver.following_get()
        # return True
        print('TESTING: Settings - Get')
        response = Driver.settings_get_all()
        return True
        print('TESTING: Cron')
        response = Cron.test()
        if not response or response == None:
            print("Error: Failed to test crons")
        reset_ = reset()
        if not reset_:
            return print("Error: Failed to Reset")
        return True

################################################################################################################################################

def main():
    try:
        from .file import File
        File.remove_local()
        Settings.set_prompt(False)
        Settings.set_confirm(False)
        action = Settings.get_action()
        print("Running - {}".format(action))
        ## Actions
        success = False
        if str(action) == "test":
            success = Snarf.test()
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
        Snarf.exit()
    except Exception as e:
        Settings.dev_print(e)
        print("Shnarf!")
    finally:
        sys.exit(0)

################################################################################################################################################

if __name__ == "__main__":
    main()
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
from . import cron as Cron
from .classes import Discount, Promotion
from .driver import Driver
from .settings import Settings
from .user import User
from .profile import Profile

#####################
##### OnlySnarf #####
#####################

class Snarf:

    def __init__(self):
        pass
        # self.profile = Profile({})

    ####################
    ##### Discount #####
    ####################

    @staticmethod
    def discount(discount=None):
        if not discount: discount = Settings.get_discount()
        try: discount.apply()
        except Exception as e: Settings.dev_print(e)
        Snarf.exit()

    ################
    ##### Exit #####
    ################

    @staticmethod
    def exit():
        if Settings.is_show_window():
            Settings.maybe_print("Skipping: Window Close")
            return
        Driver.exit()

    ###################
    ##### Message #####
    ###################

    @staticmethod
    def message(message=None):
        if not message: message = Settings.get_message()
        try: message.send()
        except Exception as e: Settings.dev_print(e)
        Snarf.exit()
                
    ################
    ##### Post #####
    ################

    @staticmethod
    def post(message=None):
        if not message: message = Settings.get_message()
        try: message.post()
        except Exception as e: Settings.dev_print(e)
        Snarf.exit()

    ###################
    ##### Profile #####
    ###################

    @staticmethod
    def profile(profile=None):
        if not profile: profile = Settings.get_profile()
        try: profile.update()
        except Exception as e: Settings.dev_print(e)
        Snarf.exit()
        
    #####################
    ##### Promotion #####
    #####################

    # def give_trial(user):
    #     print("Applying Promotion: "+user)
    #     link = Driver.get_new_trial_link()
    #     text = "Here's your free trial link!\n"+link
    #     Settings.dev_print("Link: "+str(text))
    #     # Settings.send_email(email, text)

    @staticmethod
    def promotion(promotion=None):
        if not promotion: promotion = Settings.get_promotion()
        try: promotion.apply_to_user()
        except Exception as e: Settings.dev_print(e)
        Snarf.exit()

    #################
    ##### Reset #####
    #################

    @staticmethod
    def reset():
        Driver.reset()

    #################
    ##### Users #####
    #################

    @staticmethod
    def get_following():
        users = []
        try: users = User.get_following()
        except Exception as e: Settings.dev_print(e)
        return users

    @staticmethod
    def get_users():
        users = []
        try: users = User.get_all_users()
        except Exception as e: Settings.dev_print(e)
        return users

    ###############
    ##### Dev #####
    ###############

    @staticmethod
    def test():
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
    # try:
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
    # except Exception as e:
    #     Settings.dev_print(e)
    #     print("Shnarf!")
    # finally:
    #     sys.exit(0)

################################################################################################################################################

if __name__ == "__main__":
    main()
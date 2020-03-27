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
from .driver import Driver
# from OnlySnarf.profile import Profile
from .settings import Settings
from .file import File
from .user import User

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
    def discount(user=None, discount=None):
        if not user: user = Settings.get_user()
        if not discount: discount = Settings.get_discount()
        users = []
        if str(user.username) == "all":
            users = User.get_all_users()
        elif str(user.username) == "new":
            users = User.get_new_users()
        elif str(user.username) == "favorite":
            users = User.get_favorite_users()
        elif str(user.username) == "recent":
            users = User.get_recent_users()
        else:
            users.append(user)
        for user_ in users:
            try: user_.discount(discount)
            except Exception as e: Settings.dev_print(e)
        Snarf.exit()

    ################
    ##### Exit #####
    ################

    @staticmethod
    def exit():
        Driver.exit()

    ###################
    ##### Message #####
    ###################

    @staticmethod
    def message(message=None):
        if not message: message = Settings.get_message()
        message.send()
        Snarf.exit()
                
    ################
    ##### Post #####
    ################

    @staticmethod
    def post(message=None):
        if not message: message = Settings.get_message()
        # if not message: message = Message()
        try: message.post()
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

    def promotion(promotion=None):
        if not promotion: promotion = Settings.get_promotion()
        try: promotion.post()
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
        File.remove_local()
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
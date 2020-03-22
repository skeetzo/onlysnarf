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
from OnlySnarf import google as Google
from OnlySnarf import cron as Cron
from OnlySnarf.driver import Driver
from OnlySnarf.profile import Profile
from OnlySnarf.settings import SETTINGS as settings
from OnlySnarf.user import User

#####################
##### OnlySnarf #####
#####################

class Snarf:

    def __init__(self):
        # self.profile = Profile({})

    ####################
    ##### Discount #####
    ####################

    @staticmethod
    def discount(choice=settings.get_user(), discount=settings.get_discount()):
        users = []
        if str(choice) == "all":
            users = User.get_all_users()
        elif str(choice) == "new":
            users = User.get_new_users()
        elif str(choice) == "favorite":
            users = User.get_favorite_users()
        elif str(choice) == "recent":
            users = User.get_recent_users()
        else:
            if isinstance(choice, str):
                user = User.get_user_by_username(choice)
                users.append(user)
        for user in users:
            try: user.discount(discount)
            except Exception as e: settings.devPrint(e)
        Snarf.exit()

    ################
    ##### Exit #####
    ################

    @staticmethod
    def exit():
        if str(settings.EXIT) == "True":
            Driver.exit()

    ###################
    ##### Message #####
    ###################

    @staticmethod
    def message(message=settings.get_message()):
        message.send()
        Snarf.exit()
                
    ################
    ##### Post #####
    ################

    @staticmethod
    def post(message=settings.get_message()):
        # if not message: message = Message()
        try: message.post()
        except Exception as e: settings.devPrint(e)
        Snarf.exit()
        
    #####################
    ##### Promotion #####
    #####################

    # def give_trial(user):
    #     print("Applying Promotion: "+user)
    #     link = Driver.get_new_trial_link()
    #     text = "Here's your free trial link!\n"+link
    #     settings.devPrint("Link: "+str(text))
    #     # settings.send_email(email, text)

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
        except Exception as e: settings.devPrint(e)
        return users

    ###############
    ##### Dev #####
    ###############

    @staticmethod
    def test():
        print('0/3 : Deleting Locals')
        settings.remove_local()
        print('1/3 : Testing')
        print('TESTING: Users')
        response = Driver.users_get()
        return True
        print('TESTING: Following')
        response = Driver.following_get()
        return True
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
        if str(settings.VERSION) == "True": return settings.version_check()
        action = settings.ACTION
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
    except Exception as e:
        settings.devPrint(e)
        print("Shnarf!")
    finally:
        sys.exit(0)

################################################################################################################################################

if __name__ == "__main__":
    settings.initialize()
    main()
else:
    try:
        settings.initialize()
    except Exception as e:
        print(e)
        print("Shnnarf?")
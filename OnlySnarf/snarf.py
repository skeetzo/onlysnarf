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
        self.driver = Driver()
        self.profile = Profile({})

    ####################
    ##### Discount #####
    ####################

    def discount(self, choice, discount=None):
        users = []
        if str(choice) == "all":
            users = User.get_all_users(self.driver)
        elif str(choice) == "new":
            users = User.get_new_users(self.driver)
        elif str(choice) == "favorite":
            users = User.get_favorite_users(self.driver)
        elif str(choice) == "recent":
            users = User.get_recent_users(self.driver)
        else:
            if isinstance(choice, str):
                user = User.get_user_by_username(self.driver, choice)
                users.append(user)
        for user in users:
            try: user.discount(discount)
            except Exception as e: settings.devPrint(e)
        self.exit()

    ################
    ##### Exit #####
    ################

    def exit(self):
        if str(settings.EXIT) == "True":
            self.driver.exit()

    ###################
    ##### Message #####
    ###################

    def message(self, messages=[]):
        for message in messages:
            message.send()
        self.exit()
                
    ################
    ##### Post #####
    ################

    def post(self, messages=[]):
        # if not message: message = Message()
        for message in messages:
            try: message.post()
            except Exception as e: settings.devPrint(e)
        self.exit()
        
    #####################
    ##### Promotion #####
    #####################

    # def give_trial(self, user):
    #     print("Applying Promotion: "+user)
    #     link = self.driver.get_new_trial_link()
    #     text = "Here's your free trial link!\n"+link
    #     settings.devPrint("Link: "+str(text))
    #     # settings.send_email(email, text)

    #################
    ##### Reset #####
    #################

    def reset(self):
        self.driver.reset()

    #################
    ##### Users #####
    #################

    def get_users(self):
        users = []
        try: users = User.get_all_users()
        except Exception as e: settings.devPrint(e)
        return users

    ###############
    ##### Dev #####
    ###############

    def test(self):
        print('0/3 : Deleting Locals')
        settings.remove_local()
        print('1/3 : Testing')
        print('TESTING: Users')
        response = self.driver.users_get()
        return True
        print('TESTING: Following')
        response = self.driver.following_get()
        return True
        print('TESTING: Settings - Get')
        response = self.driver.settings_get_all()
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
        if str(settings.METHOD) != "input":
            print("0/3 : Deleting Locals")
            settings.remove_local()
        sys.stdout.flush()
        ##
        snarf = Snarf()
        ##
        print("1/3 : Running - {}".format(settings.ACTION))
        ## Actions
        success = False
        if str(settings.ACTION) == "test":
            success = snarf.test()
        elif str(settings.ACTION) == "upload":
            success = snarf.upload_prep(settings.TYPE, methodChoice=settings.METHOD)
        elif str(settings.ACTION) == "post":
            success = snarf.post(text=settings.TEXT, override=True)
        elif str(settings.ACTION) == "message":
            METHOD_ = settings.METHOD
            settings.update_value("METHOD","random")
            # settings.METHOD = "random"
            success = snarf.message(METHOD_, message=settings.TEXT, image=settings.IMAGE, price=settings.PRICE, username=settings.USER)
        elif str(settings.ACTION) == "discount":
            if str(settings.USER) == "" or str(settings.USER) == "None": settings.USER = "all"
            success = snarf.discount(settings.USER, amount=settings.AMOUNT, months=settings.MONTHS)
        else:
            print("Warning: Missing Method")
        if success and str(settings.CRON) != "False":
            Cron.delete(settings.CRON)
        ##
        sys.stdout.flush()
        print('2/3 : Cleaning Up Files')
        settings.remove_local()
        print('3/3 : OnlySnarf Exiting')
        snarf.exit()
        sys.stdout.flush()
    except Exception as e:
        print(e)
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









Message


File
Files
Folder
Google_File

Image
Video













#################
##### Scene #####
#################
# leftover idea needs to be touched up and properly readded

# upload a file or gallery
# send a message to [recent, all, user] w/ a preview image
# def release_scene(methodChoice="random", file=None, folderName=None, parent=None):
#     try:
#         print("Releasing Scene")
#         response = download("scene", methodChoice=methodChoice, file=file)
#         if response == None:
#             print("Error: Failure Releasing Scene")
#             return False
#         # settings.devPrint("Scene: {}".format(response))
#         content = response[0]
#         preview = response[1]
#         data = response[2]
#         google_folder = response[3]
#         # print("Data:\n{}".format(json.dumps(data, sort_keys=True, indent=4)))
#         data = json.loads(json.dumps(data))
#         settings.devPrint("Data: {}".format(data))
#         title = None
#         message = None
#         price = None
#         text = None
#         performers = None
#         keywords = None
#         users = None
#         title = data["title"]
#         message = data["message"]
#         price = data["price"]
#         text = data["text"]
#         performers = data["performers"]
#         keywords = data["keywords"]
#         if str(keywords) == " " or str(keywords[0]) == " ":
#             keywords = []
#         users = data["users"]
#         if title == None:
#             print("Error: Missing Scene Title")
#             return False
#         if message == None:
#             print("Error: Missing Scene Message")
#             return False
#         if price == None:
#             print("Error: Missing Scene Price")
#             return False
#         if text == None:
#             print("Error: Missing Scene Text")
#             return False
#         print("Scene:")
#         print("- Title: {}".format(title)) # name of scene
#         print("- Text: {}".format(text)) # text entered into file upload
#         print("- Price: {}".format(price)) # price of messages sent
#         print("- Message: {}".format(message)) # text sent in messages
#         print("- Keywords: {}".format(keywords)) # text sent in messages
#         print("- Performers: {}".format(performers)) # text sent in messages
#         print("- Preview: {}".format(preview)) # image sent in messages
#         print("- Content: {}".format(content)) # the file(s) to upload
#         print("- Users: {}".format(users)) # the file(s) to upload 
#         files = os.listdir(content)
#         file = files[0]
#         ext = str(os.path.splitext(file)[1].lower())
#         settings.devPrint('ext: '+str(ext))
#         successful_upload = upload(path, text, keywords, performers)
#         if successful_upload:
#             if str(users[0]) == "all" or str(users[0]) == str("recent") or str(users[0]) == str("favorites"):
#                 users = users[0]
#             if not users or str(users).lower() == "none":
#                 print("Warning: Missing User Choice")
#             elif str(users) == "all" or str(users) == "recent" or str(users) == "favorites":
#                 successful_message = OnlySnarf.message(choice=str(users), message=message, image=preview, price=price)
#             else:
#                 for user in users:
#                     successful_message = OnlySnarf.message(choice="user", message=message, image=preview, price=price, username=user)
#             if successful_message:
#                 Google.move_file(google_folder)
#             else:
#                 print("Error: Failure Messaging")
#                 return False
#         else:
#             print("Error: Failure Uploading")
#             return False
#         return True
#     except Exception as e:
#         settings.devPrint(e)
#         return False
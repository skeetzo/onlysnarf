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

#################################################################
#################################################################
#################################################################

FIFTY_MEGABYTES = 50000000

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

    def discount(self, choice, depth=1, amount=None, months=None):
        if not amount: amount = input("Discount: ")
        if not months: months = input("Months: ")
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
            # try:
            success = self.driver.discount_user(user.id, depth=depth, discount=amount, months=months)
            if not success: print("Error: There was an error discounting - {}/{}".format(user.id, user.username))
            # except Exception as e:
                # settings.maybePrint(e)
            depth = int(depth) + 1
        self.exit()
        return True

    ################
    ##### Exit #####
    ################

    def exit(self):
        if str(settings.EXIT) == "True":
            self.driver.exit()

    ###################
    ##### Message #####
    ###################

    def message(self, choice, message=None, image=None, price=None, username=None):
        if image == None and str(settings.METHOD) == "random":
            images = []
            if str(settings.TYPE) == "image":
                images = Google.get_images()
            elif str(settings.TYPE) == "gallery":
                images = Google.get_galleries()
            elif str(settings.TYPE) == "video":
                images = Google.get_videos()
            else: 
                print("Error: Missing Type")
                return False
            # if str(settings.TYPE) == "image" or str(settings.TYPE) == "None": 
            image = random.choice(images)
            if str(settings.TYPE) == "gallery":
                folders = []
                for image in images:
                    if image[1]['mimeType'] == "application/vnd.google-apps.folder":
                        folders.append(image)
                image = random.choice(folders)
            # download_file doesn't work with a folder[]
            if image[1]['mimeType'] == "application/vnd.google-apps.folder":
                image = Google.download_gallery(image[1]).get("path")
            else:
                image = Google.download_file(image[1]).get("path")
        successful = False
        if str(choice) == "all":
            print("Messaging: All")
            successful = User.message(self.driver, "all", message, image, price)
        elif str(choice) == "recent":
            print("Messaging: Recent")
            successful = User.message(self.driver, "recent", message, image, price)
        elif str(choice) == "favorites":
            print("Messaging: Recent")
            successful = User.message(self.driver, "favorite", message, image, price)
        elif str(choice) == "user":
            print("Messaging: User - {}".format(username))
            if username is None:
                print("Error: Missing Username")
                return
            user = User.get_user_by_username(self.driver, str(username))
            if user is None: return False
            settings.maybePrint("User Found: {}".format(username))
            successful = User.message(self.driver, user, message, image, price)
        else:
            print("Error: Missing Message Option")
            return
        if successful: Google.upload_input(image)
        self.exit()
        return successful
                
    ################
    ##### Post #####
    ################

    def post(self, text=None, override=False):
        expires = settings.EXPIRES or ""
        schedule = settings.getSchedule()
        poll = {"period":None,"questions":None}
        duration = settings.DURATION or ""
        questions = settings.QUESTIONS or []
        if not text: text = input("Text: ".format(text))
        else: print("Text: "+text)
        if not override:
            print("[Enter] or Text or Cancel")
            confirm = input()
            if confirm != "":
                if str(confirm) == "None" or str(confirm) == "Cancel" or str(confirm) == "C" or str(confirm) == "c":
                    print("Canceling Post")
                    return False
                else:
                    text = confirm
            print("Expiration [1, 3, 7, 99 or 'No limit']:")
            expires_ = input("({})>> ".format(expires))
            if str(expires_) != "":
                expires = expires_
            schedule_ = input("Schedule (y/n): ")
            if str(schedule_) != "" and str(schedule_).lower() != "n":
                schedule_ = input( "({})>> ".format(schedule))
                date_ = settings.DATE or ""
                print("Date [mm/dd/YY]: ")
                date = input("({})>>".format(date_))
                time_ = settings.TIME or ""
                print("Time [HH:MM]: ")
                time = input("({})>>".format(time_))
                schedule = "{}:{}".format(date, time)
            questions_ = input("Poll (y/n): ")
            if str(questions_) != "" and str(questions_).lower() != "n":
                print("Duration [1, 3, 7, 99 or 'No limit']:")
                duration_ = input("({})>> ".format(duration))
                if str(duration_) != "":
                    duration = duration_
                print("Questions:\n> {}".format("\n> ".join(questions)))
                questions_ = input(">> ")
                if str(questions_) != "":
                    questions = questions_
            poll = {"period":duration,"questions":questions}
        try:
            successful = self.driver.post(text, expires=expires, schedule=schedule, poll=poll)
            self.exit()
            return successful
        except Exception as e:
            settings.maybePrint(e)
        
    #####################
    ##### Promotion #####
    #####################

    def give_trial(self, user):
        print("Applying Promotion: "+user)
        link = self.driver.get_new_trial_link()
        text = "Here's your free trial link!\n"+link
        settings.maybePrint("Link: "+str(text))
        # settings.send_email(email, text)

    #################
    ##### Reset #####
    #################

    def reset(self):
        self.driver.reset()

    ##################
    ##### Upload #####
    ##################

    def upload(self, path, text="", keywords=[], performers=[], expires=None, schedule=None, poll=None):
        # settings.maybePrint("Uploading: {}".format(path))
        try:
            if not schedule: schedule = settings.getSchedule()
            if not poll: poll = settings.getPoll()
            successful = self.driver.upload(path=path, text=text, keywords=keywords, performers=performers, expires=expires, schedule=schedule, poll=poll)
            return successful
        except Exception as e:
            settings.maybePrint(e)
            print("Error: Unable to Upload")
            return False

    def upload_prep(self, opt, methodChoice="random", file=None, folderName=None, parent=None):
        try:
            if not opt:
                print("Error: Missing Option")
                return False
            print("Uploading: {}".format(opt))
            data = None
            if str(methodChoice) == "input":
                input_ = settings.getInput()
                if not input_: return False
                global FIFTY_MEGABYTES
                if int(os.stat(str(input_)).st_size) >= FIFTY_MEGABYTES or settings.FORCE_REDUCTION: # greater than 1GB
                    input_ = Google.reduce(input_)
                data = {"path":str(input_),"text":str(settings.TEXT)}
            else:
                data = Google.download(opt, methodChoice=methodChoice, file=file)
            if data == None:
                print("Error: Missing Data")
                return False
            text = None
            path = None
            keywords = []
            performers = []
            files = None
            expires = settings.EXPIRES or None
            schedule = settings.getSchedule()
            poll = None
            duration = settings.DURATION or ""
            questions = settings.QUESTIONS or []
            if parent: parent = parent.get("title")
            try:
                if file == None: file = data.get("file") or {}
                text = file.get("title") or data.get("text")
                path = data.get("path")
                files = data.get("files")
                keywords = data.get("keywords") or parent or settings.KEYWORDS
                performers = data.get("performers") or settings.PERFORMERS
                # if parent: keywords = parent.split(" ")
                if isinstance(keywords, str): keywords = keywords.split(" ")
                if str(opt) == "performer":
                    keywords = folderName or keywords
                    if parent: performers = parent.split(" ")
                if isinstance(keywords, list): keywords = [n.strip() for n in keywords]
                if str(methodChoice) == "choose":
                    print("Text: ")
                    text_ = input("({})>> ".format(text))
                    if text_ != "":
                        text = text_
                    print("Keywords: ")
                    keywords_ = input("({})>> ".format(keywords))
                    if keywords_ != "":
                        if str(keywords_) == "None":
                            keywords = []
                        elif str(keywords_) == "[]":
                            keywords = []
                        elif str(keywords_) == " ":
                            keywords = []
                        else:
                            keywords = keywords_.split(",")
                            keywords = [n.strip() for n in keywords]
                    print("Performers: ")
                    performers_ = input("({})>> ".format(performers))
                    if performers_ != "":
                        if str(performers_) == "None":
                            performers = []
                        elif str(performers_) == "[]":
                            performers = []
                        elif str(performers_) == " ":
                            performers = []
                        else:
                            performers = performers_.split(",")
                            performers = [n.strip() for n in performers]
                    print("Expiration [1, 3, 7, 99 or 'No limit']: ")
                    expires_ = input("({})>> ".format(expires))
                    if str(expires_) != "":
                        expires = expires_
                    schedule_ = input("Schedule (y/n): ".format(schedule))
                    if str(schedule_) != "" and str(schedule_) != "n":
                        date_ = settings.DATE or ""
                        print("Date [mm/dd/YY]: ")
                        date = input("({})>>".format(date_))
                        time_ = settings.TIME or ""
                        print("Time [HH:MM]: ")
                        time = input("({})>>".format(time_))
                        schedule = "{}:{}".format(date, time)
                    questions_ = input("Poll (y/n): ")
                    if str(questions_) != "" and str(questions_).lower() != "n":
                        print("Duration [1, 3, 7, 99 or 'No limit']:")
                        duration_ = input("({})>> ".format(duration))
                        if str(duration_) != "":
                            duration = duration_
                        print("Questions:\n> {}".format("\n> ".join(questions)))
                        questions_ = input(">> ")
                        if str(questions_) != "":
                            questions = questions_
                    if len(questions) > 0:
                        poll = {"period":duration,"questions":questions}
                    else: poll = None
            except Exception as e:
                settings.maybePrint(e)
            if path == None: print("Warning: Missing Content")
            if str(settings.DEBUG) == "True" and str(settings.VERBOSE) == "True":
                print("Data:")
                print("- Text: {}".format(text)) # name of scene
                print("- Keywords: {}".format(keywords)) # text sent in messages
                print("- Content: {}".format(path)) # the file(s) to upload
                print("- Performer(s): {}".format(performers)) # name of performers
                print("- Expiration: {}".format(expires))
                print("- Schedule: {}".format(schedule))
                print("- Poll: {}".format(poll))
            successful_upload = self.upload(path, text=text, keywords=keywords, performers=performers, expires=expires, schedule=schedule, poll=poll)
            if not successful_upload:
                pass
            elif files:
                Google.move_files(text, files)
            elif str(methodChoice) != "input":
                Google.move_file(file)
            elif str(methodChoice) == "input":
                Google.upload_input()
            return successful_upload
        except Exception as e:
            settings.maybePrint(e)
            return False

    #################
    ##### Users #####
    #################

    def get_users(self):
        settings.maybePrint("Getting Users")
        try:
            return User.get_all_users()
        except Exception as e:
            settings.maybePrint(e)
            print("Error: Unable to get users");
            return []

    ###############
    ##### Dev #####
    ###############

    def test(self):
        print('0/3 : Deleting Locals')
        settings.remove_local()
        print('1/3 : Testing')

        print('TESTING: Settings - Get')
        response = self.driver.settings_get_all()
        return True


        print('TESTING: Users')
        response = get_users()
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
#         # settings.maybePrint("Scene: {}".format(response))
#         content = response[0]
#         preview = response[1]
#         data = response[2]
#         google_folder = response[3]
#         # print("Data:\n{}".format(json.dumps(data, sort_keys=True, indent=4)))
#         data = json.loads(json.dumps(data))
#         settings.maybePrint("Data: {}".format(data))
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
#         settings.maybePrint('ext: '+str(ext))
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
#         settings.maybePrint(e)
#         return False
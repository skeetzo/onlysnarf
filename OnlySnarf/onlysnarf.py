#!/usr/bin/python3
# 3/28/2019 Skeetzo

import random
import os
import shutil
import datetime
import json
import sys
import pathlib
import time
from OnlySnarf.settings import SETTINGS as settings
from OnlySnarf import google as Google
from OnlySnarf import driver as OnlySnarf
from OnlySnarf.user import User
from OnlySnarf import cron as Cron

#################################################################
#################################################################
#################################################################

FIFTY_MEGABYTES = 50000000

####################
##### Discount #####
####################

def discount(choice, depth=1, amount=None, months=None):
    if not amount: amount = input("Discount: ")
    if not months: months = input("Months: ")
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
        # try:
        success = OnlySnarf.discount_user(user.id, depth=depth, discount=amount, months=months)
        if not success: print("Error: There was an error discounting - {}/{}".format(user.id, user.username))
        # except Exception as e:
            # settings.maybePrint(e)
        depth = int(depth) + 1
    OnlySnarf.exit()
    return True

####################
##### Download #####
####################

def download(fileChoice, methodChoice="random", file=None, folderName=None, parent=None):
    if methodChoice == "random":
        return Google.random_download(fileChoice)
    elif methodChoice == "choose" and file is not None:
        if fileChoice == 'image' or fileChoice == 'video':
            return Google.download_file(file)
        elif fileChoice == 'gallery':
            return Google.download_gallery(file)
        elif fileChoice == 'performer':
            if "folder" in file.get("mimeType"):
                return Google.download_content(file)
            else:          
                return Google.download_file(file)  
#################################################################
        elif fileChoice == 'scene':
            return Google.download_scene(file)
#################################################################
    else:
        print("Error: Unable to Download")
        return None

###################
##### Message #####
###################

def message(choice, message=None, image=None, price=None, username=None):
    if str(choice) == "all":
        print("Messaging: All")
        users = User.get_all_users()
    elif str(choice) == "recent":
        print("Messaging: Recent")
        users = User.get_recent_users()
    elif str(choice) == "favorites":
        print("Messaging: Recent")
        users = User.get_favorite_users()
    elif str(choice) == "new":
        print("Messaging: New")
        users = User.get_new_users()
    elif str(choice) == "user":
        print("Messaging: User - {}".format(username))
        if username is None:
            print("Error: Missing Username")
            return
        users = [User.get_user_by_username(str(username))]
    else:
        print("Error: Missing Message Choice")
        return
    if image == None and str(settings.METHOD) == "random": 
        images = Google.get_images()
        image = random.choice(images)
        image = Google.download_file(image[1]).get("path")
    success = False
    backup = False
    for user in users:
        if user:
            try:
                success = user.sendMessage(message=message, image=image, price=price)
                if not success: print("Error: There was an error messaging - {}/{}".format(user.id, user.username))
                if success: backup = True
            except Exception as e:
                settings.maybePrint(e)
    if backup:
        Google.upload_input(image)
    OnlySnarf.exit()
    return success
                
################
##### Post #####
################

def post(text=None, override=False):
    expires = settings.EXPIRES or ""
    schedule = settings.getSchedule()
    poll = None
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
        successful = OnlySnarf.post(text, expires=expires, schedule=schedule, poll=poll)
        # if successful: print("Post Successful")
        # else: print("Post Failed")
        OnlySnarf.exit()
        return successful
    except Exception as e:
        settings.maybePrint(e)
    
#####################
##### Promotion #####
#####################

def give_trial(user):
    print("Applying Promotion: "+user)
    link = OnlySnarf.get_new_trial_link()
    text = "Here's your free trial link!\n"+link
    settings.maybePrint("Link: "+str(text))
    send_email(email, text)

def send_email(email, text):
    print("Sending Email: "+str(email))
    pass

#################
##### Reset #####
#################

# Deletes local file
def remove_local():
    try:
        if str(settings.SKIP_DELETE) == "True" or str(settings.INPUT) != "None":
            settings.maybePrint("Skipping Local Remove")
            return
        # print('Deleting Local File(s)')
        # delete /tmp
        tmp = settings.getTmp()
        if os.path.exists(tmp):
            shutil.rmtree(tmp)
            print('Local File(s) Removed')
        else:
            print('Local Files Not Found')
    except Exception as e:
        settings.maybePrint(e)

###################
##### Release #####
###################

def release(opt, methodChoice="random", file=None, folderName=None, parent=None):
    try:
        if str(methodChoice) != "input":
            print("0/3 : Deleting Locals")
            remove_local()
        sys.stdout.flush()
        print("1/3 : Running - {}".format(opt))
        released = release_(opt, methodChoice=methodChoice, file=file, folderName=folderName, parent=parent)
        # if released == False: print("Upload Failed")
        # else: print("Upload Successful")
        sys.stdout.flush()
        print('2/3 : Cleaning Up Files')
        remove_local()
        print('Files Cleaned ')
        print('3/3 : Google Drive to OnlyFans Upload Complete')
        OnlySnarf.exit()
        sys.stdout.flush()
        return released
    except Exception as e:
        settings.maybePrint(e)

def release_(opt, methodChoice="random", file=None, folderName=None, parent=None):
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
            data = download(opt, methodChoice=methodChoice, file=file)
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
            print("- Expiration: {}".format(expires)) # name of performers
            print("- Schedule: {}".format(schedule)) # name of performers
            print("- Poll: {}".format(poll)) # name of performers
        successful_upload = upload(path, text=text, keywords=keywords, performers=performers, expires=expires, schedule=schedule, poll=poll)
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
    
# upload a file or gallery
# send a message to [recent, all, user] w/ a preview image
def release_scene(methodChoice="random", file=None, folderName=None, parent=None):
    try:
        print("Releasing Scene")
        response = download("scene", methodChoice=methodChoice, file=file)
        if response == None:
            print("Error: Failure Releasing Scene")
            return False
        # settings.maybePrint("Scene: {}".format(response))
        content = response[0]
        preview = response[1]
        data = response[2]
        google_folder = response[3]
        # print("Data:\n{}".format(json.dumps(data, sort_keys=True, indent=4)))
        data = json.loads(json.dumps(data))
        settings.maybePrint("Data: {}".format(data))
        title = None
        message = None
        price = None
        text = None
        performers = None
        keywords = None
        users = None
        title = data["title"]
        message = data["message"]
        price = data["price"]
        text = data["text"]
        performers = data["performers"]
        keywords = data["keywords"]
        if str(keywords) == " " or str(keywords[0]) == " ":
            keywords = []
        users = data["users"]
        if title == None:
            print("Error: Missing Scene Title")
            return False
        if message == None:
            print("Error: Missing Scene Message")
            return False
        if price == None:
            print("Error: Missing Scene Price")
            return False
        if text == None:
            print("Error: Missing Scene Text")
            return False
        print("Scene:")
        print("- Title: {}".format(title)) # name of scene
        print("- Text: {}".format(text)) # text entered into file upload
        print("- Price: {}".format(price)) # price of messages sent
        print("- Message: {}".format(message)) # text sent in messages
        print("- Keywords: {}".format(keywords)) # text sent in messages
        print("- Performers: {}".format(performers)) # text sent in messages
        print("- Preview: {}".format(preview)) # image sent in messages
        print("- Content: {}".format(content)) # the file(s) to upload
        print("- Users: {}".format(users)) # the file(s) to upload 
        files = os.listdir(content)
        file = files[0]
        ext = str(os.path.splitext(file)[1].lower())
        settings.maybePrint('ext: '+str(ext))
        successful_upload = upload(path, text, keywords, performers)
        if successful_upload:
            if str(users[0]) == "all" or str(users[0]) == str("recent") or str(users[0]) == str("favorites"):
                users = users[0]
            if not users or str(users).lower() == "none":
                print("Warning: Missing User Choice")
            elif str(users) == "all" or str(users) == "recent" or str(users) == "favorites":
                successful_message = OnlySnarf.message(choice=str(users), message=message, image=preview, price=price)
            else:
                for user in users:
                    successful_message = OnlySnarf.message(choice="user", message=message, image=preview, price=price, username=user)
            if successful_message:
                Google.move_file(google_folder)
            else:
                print("Error: Failure Messaging")
                return False
        else:
            print("Error: Failure Uploading")
            return False
        return True
    except Exception as e:
        settings.maybePrint(e)
        return False

#################
##### Reset #####
#################

def reset():
    OnlySnarf.reset()

##################
##### Upload #####
##################

def upload(path, text="", keywords=[], performers=[], expires=None, schedule=None, poll=None):
    # settings.maybePrint("Uploading: {}".format(path))
    try:
        if not schedule: schedule = settings.getSchedule()
        if not poll: poll = settings.getPoll()
        successful = OnlySnarf.upload_to_OnlyFans(path=path, text=text, keywords=keywords, performers=performers, expires=expires, schedule=schedule, poll=poll)
        # if successful: print("Upload Successful")
        # else: print("Upload Failed")
        return successful
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Unable to Upload")
        return False

#################
##### Users #####
#################

def get_users():
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

def test(TYPE, methodChoice="random", file=None, folderName=None, parent=None):
    print('0/3 : Deleting Locals')
    remove_local()
    print('1/3 : Testing')

    # ### Promotion ###
    print('TESTING: Cron')
    response = Cron.test()
    if not response or response == None:
        print("Error: Failed to test crons")
    reset_ = reset()
    if not reset_:
        return print("Error: Failed to Reset")
    return

################################################################################################################################################

def main():
    try:
        # os.system('clear')
        settings.initialize()
        success = False
        if str(settings.ACTION) == "upload":
            success = release(settings.TYPE, methodChoice=settings.METHOD)
        elif str(settings.ACTION) == "post":
            success = post(text=settings.TEXT, override=True)
        elif str(settings.ACTION) == "message":
            METHOD_ = settings.METHOD
            settings.METHOD = "random"
            success = message(METHOD_, message=settings.TEXT, image=settings.IMAGE, price=settings.PRICE, username=settings.USER)
        elif str(settings.ACTION) == "discount":
            if str(settings.USER) == "" or str(settings.USER) == "None": settings.USER = "all"
            success = discount(settings.USER, amount=settings.AMOUNT, months=settings.MONTHS)
        else:
            print("Warning: Missing Method")
        if success and str(settings.CRON) != "False":
            Cron.delete(settings.CRON)
    except Exception as e:
        print(e)
        print("Shnarf!")
    finally:
        sys.exit(0)

if __name__ == "__main__":
    main()
else:
    try:
        settings.initialize()
    except Exception as e:
        print(e)
        print("Shnnarf?")
#!/usr/bin/python3
# 3/28/2019: Skeetzo
import re
import random
import os
import shutil
# import datetime
import json
import sys
import pathlib
import threading
import chromedriver_binary
import time
from datetime import date, datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from OnlySnarf.user import User
from OnlySnarf.settings import SETTINGS as settings

###################
##### Globals #####
###################

BROWSER = None
USER_CACHE = None
USER_CACHE_TIMEOUT = 600 # ten minutes
USER_CACHE_LOCKED = False
settings.PATH_USERS = None
INITIALIZED = False
OnlyFans_USERNAME = None        
OnlyFans_PASSWORD = None
OnlyFans_USER_ID = None

def initialize():
    try:
        # settings.maybePrint("Initializing OnlySnarf")
        global INITIALIZED
        if INITIALIZED:
            # settings.maybePrint("Already Initialized, Skipping")
            return
        with open(settings.PATH_CONFIG) as config_file:    
            config = json.load(config_file)
        global OnlyFans_USERNAME
        global OnlyFans_PASSWORD
        OnlyFans_USERNAME = config['username']
        OnlyFans_PASSWORD = config['password']
        # settings.maybePrint("Initialized OnlySnarf: Driver")
        INITIALIZED = True
    except Exception as e:
        print('Error: Unable to Start, run `onlysnarf-config`')
        settings.maybePrint(e)
        sys.exit(0)
    except FileNotFoundError:
        print('Error: Missing Config, run `onlysnarf-config`')
        sys.exit(0)

#####################
##### Functions #####
#####################

# Upload to OnlyFans
def log_into_OnlyFans():
    print('Logging into OnlyFans')
    options = webdriver.ChromeOptions()
    if str(settings.SHOW_WINDOW) != "True":
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.setExperimentalOption('useAutomationExtension', false);
    options.add_argument('--disable-gpu')
    # BROWSER = webdriver.Chrome(binary=CHROMEDRIVER_PATH, chrome_options=options)
    CHROMEDRIVER_PATH = chromedriver_binary.chromedriver_filename
    os.environ["webdriver.chrome.driver"] = CHROMEDRIVER_PATH
    global BROWSER
    try:
        BROWSER = webdriver.Chrome(chrome_options=options)
    except Exception as e:
        settings.maybePrint(e)
        print("Warning: Missing chromedriver_path, retrying")
        try:
            BROWSER = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
        except Exception as e:
            settings.maybePrint(e)
            print("Error: Missing chromedriver_path, exiting")
            return False
    BROWSER.implicitly_wait(10) # seconds
    BROWSER.set_page_load_timeout(1200)    
    def login(opt):
        try:
            BROWSER.get(('https://onlyfans.com'))
            # login via Twitter
            if int(opt)==0:
                twitter = BROWSER.find_element_by_xpath('//a[@class="g-btn m-rounded m-flex m-lg"]').click()
            elif int(opt)==1:
                twitter = BROWSER.find_element_by_xpath('//a[@class="g-btn m-rounded m-flex m-lg btn-twitter"]').click()
            elif int(opt)==2:
                twitter = BROWSER.find_element_by_xpath('//a[@class="btn btn-default btn-block btn-lg btn-twitter"]').click()
        except NoSuchElementException as e:
            print("Warning: Login Failure, Retrying")
            login(opt+1)
    try:
        login(0)
        # fill in username
        username = BROWSER.find_element_by_xpath('//input[@id="username_or_email"]').send_keys(str(OnlyFans_USERNAME))
        # fill in password and hit the login button 
        password = BROWSER.find_element_by_xpath('//input[@id="password"]')
        password.send_keys(str(OnlyFans_PASSWORD))
        password.send_keys(Keys.ENTER)
        print('Login Successful')
        return True
    except Exception as e:
        settings.maybePrint(e)
        print('Error: Login Failure')
        return False

# Reset to home
def reset():
    global BROWSER
    if not BROWSER or BROWSER == None:
        print('OnlyFans Not Open, Skipping Reset')
        return True
    try:
        BROWSER.get(('https://onlyfans.com'))
        print('OnlyFans Reset')
        return True
    except Exception as e:
        settings.maybePrint(e)
        print('Error: Failure Resetting OnlyFans')
        return False

##################
##### Upload #####
##################

# Uploads a directory with a video file or image files to OnlyFans
def upload_to_OnlyFans(path=None, text=None, keywords=None, performers=None):
    try:
        logged_in = False
        global BROWSER
        if not BROWSER or BROWSER == None:
            logged_in = log_into_OnlyFans()
        else:
            logged_in = True
        if logged_in == False:
            print("Error: Not Logged In")
            return False
        if not path:
            print("Error: Missing Upload Path")
            return False
        if not text:
            print("Error: Missing Upload Text")
            return False
        text = text.replace(".mp4","")
        text = text.replace(".MP4","")
        text = text.replace(".jpg","")
        text = text.replace(".jpeg","")
        if performers:
            text += " w/ @"+" @".join(performers)
        if keywords:
            text += " #"+" #".join(keywords)
        print("Uploading:")
        settings.maybePrint("- Path: {}".format(path))
        print("- Keywords: {}".format(keywords))
        print("- Performers: {}".format(performers))
        print("- Text: {}".format(text))
        print("- Tweeting: {}".format(settings.TWEETING))
        WAIT = WebDriverWait(BROWSER, 600, poll_frequency=10)
        if str(settings.TWEETING) == "True":
            WAIT.until(EC.element_to_be_clickable((By.XPATH, '//label[@for="new_post_tweet_send"]'))).click()
        files = []
        if os.path.isfile(str(path)):
            files = [str(path)]
        elif os.path.isdir(str(path)):
            # files = os.listdir(str(path))
            for file in os.listdir(str(path)):
                files.append(os.path.join(os.path.abspath(str(path)),file))
        else:
            print("Error: Unable to parse path")
            return False
        for file in files:  
            print('Uploading: '+str(file))
            BROWSER.find_element_by_id("fileupload_photo").send_keys(str(file))
        maxUploadCount = 12 # 2 hours max attempt time
        i = 0
        while True:
            try:                
                WAIT.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]')))
                break
            except Exception as e:
                # try: 
                #     # check for existence of "thumbnail is fucked up" modal and hit ok button
                #     BROWSER.switchTo().frame("iframe");
                #     BROWSER.find_element_by_class("g-btn m-rounded m-border").send_keys(Keys.ENTER)
                #     print("Error: Thumbnail Missing")
                #     break
                # except Exception as ef:
                #     settings.maybePrint(ef)
                print('uploading...')
                settings.maybePrint(e)
                i+=1
                if i == maxUploadCount and settings.FORCE_UPLOAD is not True:
                    print('Error: Max Upload Time Reached')
                    return False
        try:
            BROWSER.find_element_by_id("new_post_text_input").send_keys(str(text))
        except:
            settings.maybePrint("Warning: Upload Error Message, Closing")
            try:
                buttons = BROWSER.find_elements_by_class_name("g-btn.m-rounded.m-border")
                for butt in buttons:
                    if butt.get_attribute("innerHTML").strip() == "Close":
                        butt.click()
                        settings.maybePrint("Success: Upload Error Message Closed")
                        BROWSER.find_element_by_id("new_post_text_input").send_keys(str(text))
            except Exception as e:
                print("Error: Unable to Upload Images")
                settings.maybePrint(e)
                return False
        # first one is disabled
        sends = BROWSER.find_elements_by_class_name("send_post_button")
        # send = BROWSER.find_element_by_class_name("send_post_button")
        for i in range(len(sends)):
            if sends[i].is_enabled():
                sends = sends[i]
        if str(settings.DEBUG) == "True" and str(settings.DEBUG_DELAY) == "True":
            time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
        if str(settings.DEBUG) == "True":
            print('Skipped: OnlyFans upload')
            return True
        sends.click()
        # send[1].click() # the 0th one is disabled
        print('File Uploaded Successfully')
        return True
    except Exception as e:
        settings.maybePrint(e)
        print("Error: File Upload Failure")
        return False

####################
##### Messages #####
####################

def message(choice=None, message=None, image=None, price=None, username=None):
    if str(choice) == "all":
        print("Messaging: All")
        users = get_users()
    elif str(choice) == "recent":
        print("Messaging: Recent")
        users = get_recent_users()
    elif str(choice) == "favorites":
        print("Messaging: Recent")
        users = get_favorite_users()
    elif str(choice) == "new":
        print("Messaging: New")
        users = get_new_users()
    elif str(choice) == "user":
        print("Messaging: User - {}".format(username))
        if username is None:
            print("Error: Missing Username")
            return
        users = [get_user_by_username(str(username))]
    else:
        print("Error: Missing Message Choice")
        return
    for user in users:
        success = user.sendMessage(message, image, price)
        if not success:
            print("Error: There was an error messaging - {}/{}".format(user.id, user.username))
                
def goto_user(user):
    try:
        userid = user.id
        if not userid or userid == None:
            print("Warning: Missing User ID")
            if not user.username or user.username == None:
                print("Error: Missing User ID & Username")
                return False
            userid = str(user.username).replace("@u","").replace("@","")
            if len(re.findall("[A-Za-z]", userid)) > 0:  
                print("Warning: Invalid User ID")
                if str(settings.DEBUG) == "False":
                    return False
        settings.maybePrint("goto -> /my/chats/chat/%s" % userid)
        global BROWSER
        BROWSER.get(('https://onlyfans.com/my/chats/chat/'+str(userid)))
        return True
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failure to Goto User - {}/{}".format(user.id, user.username))
        return False

def enter_message(text):
    try:
        print("Enter text: %s" % text)
        if not text or text == None:
            print("Error: Missing Text")
            return False
        global BROWSER
        message = BROWSER.find_element_by_css_selector(".form-control.b-chat__message-input")        
        message.send_keys(str(text))
        print("Message Entered")
        return True
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failure to Enter Message")
        return False

def enter_image(image):
    try:
        print("Enter image: %s" % image)
        if not image or image == None:
            print("Error: Missing Image")
            return False
        global BROWSER
        BROWSER.find_element_by_id("cm_fileupload_photo").send_keys(str(image))
        print("Image Entered")
        return True
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failure to Enter Image")
        return False

def enter_price(price):
    try:
        print("Enter price: %s" % price)
        if not price or price == None:
            print("Error: Missing Price")
            return False
        global BROWSER
        BROWSER.find_element_by_css_selector(".b-chat__btn-set-price").click()
        BROWSER.find_elements_by_css_selector(".form-control.b-chat__panel__input")[1].send_keys(str(price))
        BROWSER.find_elements_by_css_selector(".g-btn.m-rounded")[4].click()
        print("Price Entered")
        return True
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failure to Enter Price")
        return False

def confirm_message():
    try:
        global BROWSER
        send = WebDriverWait(BROWSER, 60, poll_frequency=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".g-btn.m-rounded.b-chat__btn-submit")))
        if str(settings.DEBUG) == "True":
            print('OnlyFans Message: Skipped (debug)')
            return True
        send.click()
        print('OnlyFans Message: Sent')
        return True
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failure to Confirm Message")
        return False

def read_chat(user):
    try:
        logged_in = False
        global BROWSER
        if not BROWSER or BROWSER == None:
            logged_in = log_into_OnlyFans()
        else:
            logged_in = True
        if logged_in == False:
            print("Error: Login Failure")
            return [[],[],[]]
        # go to onlyfans.com/my/subscribers/active
        goto_user(user)
        messages_from_ = BROWSER.find_elements_by_class_name("m-from-me")
        # print("first message: {}".format(messages_to_[0].get_attribute("innerHTML")))
        # messages_to_.pop(0) # drop self user at top of page
        messages_all_ = BROWSER.find_elements_by_class_name("b-chat__message__text")
        messages_all = []
        messages_to = []
        messages_from = []
        # timestamps_ = BROWSER.find_elements_by_class_name("b-chat__message__time")
        # timestamps = []
        # for timestamp in timestamps_:
            # settings.maybePrint("timestamp1: {}".format(timestamp))
            # timestamp = timestamp["data-timestamp"]
            # timestamp = timestamp.get_attribute("innerHTML")
            # settings.maybePrint("timestamp: {}".format(timestamp))
            # timestamps.append(timestamp)
        for message in messages_all_:
            settings.maybePrint("all: {}".format(message.get_attribute("innerHTML")))
            messages_all.append(message.get_attribute("innerHTML"))
        messages_and_timestamps = []
        # messages_and_timestamps = [j for i in zip(timestamps,messages_all) for j in i]
        # settings.maybePrint("Chat Log:")
        # for f in messages_and_timestamps:
            # settings.maybePrint(": {}".format(f))
        for message in messages_from_:
            # settings.maybePrint("from1: {}".format(message.get_attribute("innerHTML")))
            message = message.find_element_by_class_name("b-chat__message__text")
            settings.maybePrint("from: {}".format(message.get_attribute("innerHTML")))
            messages_from.append(message.get_attribute("innerHTML"))

        i = 0
        for message in messages_all:
            from_ = False
            to_ = False
            for mess in messages_from:
                if str(message) == str(mess):
                    from_ = True
            for mess in messages_to:
                if str(message) == str(mess):
                    to_ = True
            if not from_:
                # settings.maybePrint("to_: {}".format(message))
                # messages_to[i] = [timestamps[i], message]
                # messages_to[i] = message
                messages_to.append(message)
                # settings.maybePrint("to_: {}".format(messages_to[i]))
            # elif from_:
                # settings.maybePrint("from_: {}".format(message))
                # messages_from[i] = [timestamps[i], message]
                # messages_from[i] = message
                # settings.maybePrint("from_: {}".format(messages_from[i]))
            i += 1
        settings.maybePrint("to: {}".format(messages_to))
        settings.maybePrint("from: {}".format(messages_from))
        settings.maybePrint("Messages From: {}".format(len(messages_from)))
        settings.maybePrint("Messages To: {}".format(len(messages_to)))
        settings.maybePrint("Messages All: {}".format(len(messages_all)))
        return [messages_all, messages_and_timestamps, messages_to, messages_from]
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failure to Read Chat - {}".format(user.username))
        return [[],[],[]]

# update chat logs for all users
def update_chat_logs():
    global USER_CACHE_LOCKED
    USER_CACHE_LOCKED = True
    print("Updating User Chats")
    users = get_users()
    for user in users:
        update_chat_log(user)
    USER_CACHE_LOCKED = False


def update_chat_log(user):
    print("Updating Chat: {} - {}".format(user.username, user.id))
    if not user:
        return print("Error: Missing User")
    user.readChat()


######################
##### Promotions #####
######################

# or email
def get_new_trial_link():
    global BROWSER
    if not BROWSER or BROWSER == None:
        logged_in = log_into_OnlyFans()
    else:
        logged_in = True
    if logged_in == False:
        print("Error: Login Failure")
        return USER_CACHE
    # go to onlyfans.com/my/subscribers/active
    try:
        settings.maybePrint("goto -> /my/promotions")
        BROWSER.get(('https://onlyfans.com/my/promotions'))
        trial = BROWSER.find_elements_by_class_name("g-btn.m-rounded.m-sm")[0].click()
        create = BROWSER.find_elements_by_class_name("g-btn.m-rounded")
        for i in range(len(create)):
            if create[i].get_attribute("innerHTML").strip() == "Create":
                create[i].click()
                break

        # copy to clipboard? email to user by email?
        # count number of links
        # div class="b-users__item.m-fans"
        trials = BROWSER.find_elements_by_class_name("b-users__item.m-fans")
        # print("trials")
        # find last one in list of trial link buttons
        # button class="g-btn m-sm m-rounded" Copy trial link
        # trials = BROWSER.find_elements_by_class_name("g-btn.m-sm.m-rounded")
        # print("trials: "+str(len(trials)))
        # trials[len(trials)-1].click()
        # for i in range(len(create)):
        #     print(create[i].get_attribute("innerHTML"))
       
        # find the css for the email / user
        # which there isn't, so, create a 1 person limited 7 day trial and send it to their email
        # add a fucking emailing capacity
        # send it
        link = "https://onlyfans.com/action/trial/$number"
        return link
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failed to Apply Promotion")
        return None

#################
##### Users #####
#################

# gets a list of all user_ids subscribed to profile
def get_users():
    # gets users from cache or refreshes from onlyfans.com
    global USER_CACHE
    if USER_CACHE:
        return USER_CACHE
    USER_CACHE = read_users_local()
    if settings.PREFER_LOCAL == "True":
        return USER_CACHE
    logged_in = False
    global BROWSER
    if not BROWSER or BROWSER == None:
        logged_in = log_into_OnlyFans()
    else:
        logged_in = True
    if logged_in == False:
        print("Error: Login Failure")
        return USER_CACHE
    # go to onlyfans.com/my/subscribers/active
    try:
        settings.maybePrint("goto -> /my/subscribers/active")
        BROWSER.get(('https://onlyfans.com/my/subscribers/active'))
        num = BROWSER.find_element_by_class_name("l-sidebar__user-data__item__count").get_attribute("innerHTML")
        settings.maybePrint("User count: %s" % num)
        for n in range(int(int(int(num)/10)+1)):
            settings.maybePrint("scrolling...")
            BROWSER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failed to Count Users")
        return []
    avatars = BROWSER.find_elements_by_class_name('b-avatar')
    user_ids = BROWSER.find_elements_by_class_name("g-btn.m-rounded.m-border.m-sm")
    starteds = BROWSER.find_elements_by_class_name("b-fans__item__list__item")
    # users = BROWSER.find_elements_by_class_name('g-user-name')
    users = BROWSER.find_elements_by_class_name('g-user-name__wrapper')
    usernames = BROWSER.find_elements_by_class_name('g-user-username')
    active_users = []
    global OnlyFans_USERNAME
    # settings.maybePrint("user_ids: "+str(len(user_ids)))
    # settings.maybePrint("starteds: "+str(len(starteds)))
    settings.maybePrint("Found: ")
    useridsFailed = False
    startedsFailed = False
    if len(user_ids) == 0:
        print("Warning: Unable to find user ids")
        useridsFailed = True
    if len(starteds) == 0:
        print("Warning: Unable to find starting dates")
        startedsFailed = True
    try:
        user_ids_ = []
        starteds_ = []
        for i in range(len(user_ids)):
            if user_ids[i].get_attribute("href"):
                user_ids_.append(user_ids[i].get_attribute("href"))
        for i in range(len(starteds)):
            text = starteds[i].get_attribute("innerHTML")
            match = re.findall("Started.*([A-Za-z]{3}\s[0-9]{1,2},\s[0-9]{4})", text)
            if len(match) > 0:
                starteds_.append(match[0])
        settings.maybePrint("ids vs starteds: "+str(len(user_ids_))+" - "+str(len(starteds_)))
        for i in range(len(avatars)-1):
            if not startedsFailed:
                start = starteds_[i]
            else:
                start = datetime.now().strftime("%b %d, %Y")
            if not useridsFailed:
                user_id = user_ids_[i][35:]
            else:
                user_id = None
            name = users[i]
            username = usernames[i]
            name = str(name.get_attribute("innerHTML")).strip()
            username = str(username.get_attribute("innerHTML")).strip()
            # settings.maybePrint("name: "+str(name))
            # settings.maybePrint("username: "+str(username))
            # settings.maybePrint("user_id: "+str(user_id))
            if str(OnlyFans_USERNAME).lower() in str(username).lower():
                settings.maybePrint("(self): %s = %s" % (OnlyFans_USERNAME, username))
                # first user is always active user but just in case find it in list of users
                global OnlyFans_USER_ID
                OnlyFans_USER_ID = username
                continue
            user = User(name=name, username=username, id=user_id, started=start)
            user = skipUserCheck(user)
            if user is None: continue
            active_users.append(user)
        for user in active_users:
            existing = False
            for user_ in USER_CACHE:
                if user.equals(user_):
                    existing = True
            if not existing:
                USER_CACHE.append(user)
    except Exception as e:
        settings.maybePrint(e)
    # start cache timeout
    start_user_cache()
    return USER_CACHE

def get_user_by_username(username):
    if not username or username == None:
        print("Error: Missing Username")
        return None
    users = get_users()
    for user in users:
        if str(user.username) == str(username):
            return user
    return None

def get_favorite_users():
    return []

# returns users that have no messages sent to them
def get_new_users():
    settings.maybePrint("Getting New Users")
    users = get_users()
    newUsers = []
    date_ = datetime.today() - timedelta(days=10)
    for user in users:
        started = datetime.strptime(user.started,"%b %d, %Y")
        # settings.maybePrint("date: "+str(date_)+" - "+str(started))
        if started < date_: continue
        settings.maybePrint("New User: %s" % user.username)
        user = skipUserCheck(user)
        if user is None: continue
        newUsers.append(user)
    return newUsers

def get_never_messaged_users():
    settings.maybePrint("Getting New Users")
    update_chat_logs()
    users = get_users()
    newUsers = []
    for user in users:
        if len(user.messages_to) == 0:
            settings.maybePrint("Never Messaged User: %s" % user.username)
            user = skipUserCheck(user)
            if user is None: continue
            newUsers.append(user)
    return newUsers

def get_recent_users():
    settings.maybePrint("Getting Recent Users")
    users = get_users()
    i = 0
    users_ = []
    for user in users:
        settings.maybePrint("Recent User: %s" % user.username)
        user = skipUserCheck(user)
        if user is None: continue
        users_.append(user)
        i += 1
        if i == settings.RECENT_USER_COUNT:
            return users_
    return users_

# gets a list of all subscribed user_ids from local txt
def read_users_local():
    settings.maybePrint("Getting Local Users")
    users = []
    users_ = []
    try:
        with open(settings.PATH_USERS) as json_file:  
            users = json.load(json_file)
        for user in users['users']:
            user = User(name=user['name'], username=user['username'], id=user['id'], messages_from=user['messages_from'], messages_to=user['messages_to'], messages=user['messages'], preferences=user['preferences'], last_messaged_on=user['last_messaged_on'], sent_images=user['sent_images'], subscribed_on=user['subscribed_on'], isFavorite=user['isFavorite'], statement_history=user['statement_history'])
            settings.maybePrint('Loaded: %s' % user.username)
            settings.maybePrint('')
            users_.append(user)
    except FileNotFoundError:
        print("Error: Missing Local Users")
    except OSError:
        print("Error: Missing Local Path")
    finally:
        return users_

def skipUserCheck(user):
    if str(user.id).lower() in settings.SKIP_USERS or str(user.username).lower() in settings.SKIP_USERS:
        settings.maybePrint("skipping: %s" % user.username)
        return None
    return user

def reset_user_cache():
    global USER_CACHE_LOCKED
    if USER_CACHE_LOCKED:
        settings.maybePrint("User Cache: locked, skipping reset")
        return
    global USER_CACHE
    USER_CACHE = False
    settings.maybePrint("User Cache: reset")

def start_user_cache():
    settings.maybePrint("User Cache: starting")
    # write_users_local()
    global USER_CACHE_TIMEOUT
    try:
        threading.Timer(USER_CACHE_TIMEOUT, reset_user_cache).start() # after 10 minutes
        settings.maybePrint("User Cache: started")
    except:
        settings.maybePrint("User Cache: error starting")
        settings.maybePrint(sys.exc_info()[0])

# writes user list to local txt
def write_users_local():
    users = get_users()
    print("Saving Users Locally")
    settings.maybePrint("local data path: "+str(settings.PATH_USERS))
    data = {}
    data['users'] = []
    for user in users:
        settings.maybePrint("Saving: "+str(user.username))
        data['users'].append(user.toJSON())
    try:
        with open(settings.PATH_USERS, 'w') as outfile:  
            json.dump(data, outfile, indent=4, sort_keys=True)
    except FileNotFoundError:
        print("Error: Missing Local Users")
    except OSError:
        print("Error: Missing Local Path")

################
##### Exit #####
################

def exit(force=False):
    if str(settings.SAVE_USERS) == "True":
        print("Saving and Exiting OnlyFans")
        write_users_local()
    else:
        print("Exiting OnlyFans")
    global BROWSER
    BROWSER.quit()
    BROWSER = None
    print("Browser Closed")
    global logged_in
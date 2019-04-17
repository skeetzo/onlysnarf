#!/usr/bin/python3
# 3/28/2019: Skeetzo

import random
import os
import shutil
import datetime
import json
import sys
import pathlib
import threading
import chromedriver_binary
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from .user import User
from .settings import SETTINGS as settings

###################
##### Globals #####
###################

BROWSER = None
USER_CACHE = None
LOCAL_DATA = None
INITIALIZED = False

def initialize():
    try:
        # print("Initializing OnlySnarf")
        global INITIALIZED
        if INITIALIZED:
            # print("Already Initialized, Skipping")
            return
        global LOCAL_DATA
        if settings.USERS_PATH is not None and settings.MOUNT_PATH is not None:
            LOCAL_DATA = os.path.join(settings.MOUNT_PATH, settings.USERS_PATH)
        elif settings.USERS_PATH is not None:
            LOCAL_DATA = settings.USERS_PATH
        elif settings.MOUNT_PATH is not None:
            LOCAL_DATA = os.path.join(settings.MOUNT_PATH, "users.json")
        else:
            LOCAL_DATA = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'users.json')
        # print("Initialized OnlySnarf")
        INITIALIZED = True
    except Exception as e:
        print(e)
##################
##### Config #####
##################

CONFIG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')

OnlyFans_USERNAME = None        
OnlyFans_PASSWORD = None
OnlyFans_USER_ID = None

try:
    with open(CONFIG_FILE) as config_file:    
        config = json.load(config_file)
    OnlyFans_USERNAME = config['username']        
    OnlyFans_PASSWORD = config['password']
    OnlyFans_USER_ID = "409408"
except FileNotFoundError:
    print('Missing Config, run `onlysnarf-config`')
    sys.exit(0)

#####################
##### Functions #####
#####################

# Upload to OnlyFans
def log_into_OnlyFans():
    print('Logging into OnlyFans...')
    options = webdriver.ChromeOptions()
    if str(settings.SHOW_WINDOW) != "True":
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # options.setExperimentalOption('useAutomationExtension', false);
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    # BROWSER = webdriver.Chrome(binary=CHROMEDRIVER_PATH, chrome_options=options)
    CHROMEDRIVER_PATH = chromedriver_binary.chromedriver_filename
    os.environ["webdriver.chrome.driver"] = CHROMEDRIVER_PATH
    global BROWSER
    try:
        BROWSER = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
    except WebDriverException as e:
        settings.maybePrint(e)
        settings.maybePrint("Warning: Missing chromedriver_path, retrying")
        try:
            BROWSER = webdriver.Chrome(chrome_options=options)
        except Exception as e:
            settings.maybePrint(e)
            print("Error: Missing chromedriver_path, exiting")
            return False
    try:
        BROWSER.implicitly_wait(10) # seconds
        BROWSER.set_page_load_timeout(1200)
        BROWSER.get(('https://onlyfans.com'))
        # login via Twitter
        twitter = BROWSER.find_element_by_xpath('//a[@class="btn btn-default btn-block btn-lg btn-twitter"]').click()
        # fill in username
        username = BROWSER.find_element_by_xpath('//input[@id="username_or_email"]').send_keys(str(OnlyFans_USERNAME))
        # fill in password and hit the login button 
        password = BROWSER.find_element_by_xpath('//input[@id="password"]')
        password.send_keys(str(OnlyFans_PASSWORD))
        password.send_keys(Keys.ENTER)
        print('Login Success')
        return True
    except Exception as e:
        settings.maybePrint(e)
        print('Login Failure')
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

# Uploads a file to OnlyFans
def upload_file_to_OnlyFans(path=None, text=None, keywords=None, performers=None, tweeting=True):
    try:
        logged_in = False
        global BROWSER
        if not BROWSER or BROWSER == None:
            logged_in = log_into_OnlyFans()
        if not path:
            print("Error: Missing Upload Path")
            return
        if not text:
            print("Error: Missing Upload Text")
            return
        text = text.replace(".mp4","")
        text = text.replace(".MP4","")
        text = text.replace(".jpg","")
        text = text.replace(".jpeg","")
        if performers:
            text += " w/ @"+" @".join(performers)
        if keywords:
            text += " #"+" #".join(keywords)
        settings.maybePrint("Uploading:")
        settings.maybePrint("Path: {}".format(path))
        settings.maybePrint("Keywords: {}".format(keywords))
        settings.maybePrint("Performers: {}".format(performers))
        settings.maybePrint("Text: {}".format(text))
        WAIT = WebDriverWait(BROWSER, 600, poll_frequency=10)
        if not tweeting:
            WAIT.until(EC.element_to_be_clickable((By.XPATH, '//label[@for="new_post_tweet_send"]'))).click()
        BROWSER.find_element_by_id("new_post_text_input").send_keys(str(text))
        BROWSER.find_element_by_id("fileupload_photo").send_keys(str(path))
        maxUploadCount = 12 # 2 hours max attempt time
        i = 0
        while True:
            try:
                WAIT.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]')))
                if str(settings.DEBUG) == "True":
                    print('skipping OnlyFans upload')
                    return
                # send.click()
                send = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]'))).click()
                break
            except:
                try: 
                    # check for existence of "thumbnail is fucked up" modal and hit ok button
                    BROWSER.switchTo().frame("iframe");
                    BROWSER.find_element_by_class("g-btn m-rounded m-border").send_keys(Keys.ENTER)
                    print("Error: Thumbnail Missing")
                    break
                except:
                    settings.maybePrint(sys.exc_info()[0])
                print('uploading...')
                settings.maybePrint(sys.exc_info()[0])
                i+=1
                if i == maxUploadCount and settings.FORCE_UPLOAD is not True:
                    print('max upload wait reached, breaking..')
                    break
        print('File Uploaded Successfully')
    except Exception as e:
        settings.maybePrint(e)
        print("Error: File Upload Failure")

# Uploads a folder to OnlyFans
def upload_directory_to_OnlyFans(path=None, text=None, keywords=None, performers=None, tweeting=True):
    try:
        logged_in = False
        global BROWSER
        if not BROWSER or BROWSER == None:
            logged_in = log_into_OnlyFans()
        if not path:
            print("Error: Missing Upload Path")
            return
        if not text:
            print("Error: Missing Upload Text")
            return
        if performers and len(performers) > 1:
            text += " w/ @"+" @".join(performers)
        elif performers and len(performers) == 1:
            text += " w/ @{}".format(performers[0])
        if keywords:
            text += " #"+" #".join(keywords)
        settings.maybePrint("Uploading:")
        settings.maybePrint("Path: {}".format(path))
        settings.maybePrint("Keywords: {}".format(keywords))
        settings.maybePrint("Performers: {}".format(performers))
        settings.maybePrint("Text: {}".format(text))
        files_path = []
        for file in pathlib.Path(str(path)).iterdir():  
            files_path.append(str(file))
        settings.maybePrint('Files: '+str(files_path))
        BROWSER.find_element_by_id("new_post_text_input").send_keys(str(text))
        WAIT = WebDriverWait(BROWSER, 600, poll_frequency=10)
        if not tweeting:
            WAIT.until(EC.element_to_be_clickable((By.XPATH, '//label[@for="new_post_tweet_send"]'))).click()
        for file in files_path:
            settings.maybePrint('uploading: '+str(file))
            BROWSER.find_element_by_id("fileupload_photo").send_keys(str(file))
            send = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]')))
        send = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]')))
        if str(settings.DEBUG) == "True":
            print('skipping OnlyFans upload')
            return
        send = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]'))).click()
        print('Directory Uploaded Successfully')
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Directory Upload Failure")

####################################################################################################################

def uploadPerformer(args, dirName, path, folderName):
    pass

####################
##### Messages #####
####################

def message(choice=None, message=None, image=None, price=None):
    if str(choice) == "all":
        users = get_users()
    elif str(choice) == "recent":
        print("Messaging: Recent")
        users = get_recent_users()
    elif str(choice) == "favorites":
        print("Messaging: Recent")
        users = get_favorite_users()
    elif str(choice) != "None":
        print("Messaging: User - %s" % username)
        users = [get_user_by_username(str(username))]
    else:
        print("Error: Missing Message Choice")
        return
    for user in users:
        user.sendMessage(message, image, price)

def goto_user(username):
    try:
        if not username or username == None:
            print("Missing Username")
            return
        username = str(username).replace("@u","").replace("@","")
        print("goto -> /my/chats/chat/%s" % username)
        BROWSER.get(('https://onlyfans.com/my/chats/chat/'+str(username)))
    except:
        settings.maybePrint(sys.exc_info()[0])

def enter_message(text):
    try:
        print("Enter text: %s" % text)
        if not text or text == None:
            print("Missing Text")
            return
        global BROWSER
        message = BROWSER.find_element_by_css_selector(".form-control.unlimsize.b-chat__message-input")        
        message.send_keys(str(text))
        print("Message Entered")
    except:
        settings.maybePrint(sys.exc_info()[0])

def enter_image(image):
    try:
        print("Enter image: %s" % image)
        if not image or image == None:
            print("Missing Image")
            return
        global BROWSER
        BROWSER.find_element_by_id("cm_fileupload_photo").send_keys(str(image))
        print("Image Entered")
    except:
        settings.maybePrint(sys.exc_info()[0])

def enter_price(price):
    try:
        print("Enter price: %s" % price)
        if not price or price == None:
            print("Error: Missing Price")
            return
        global BROWSER
        BROWSER.find_element_by_css_selector(".b-chat__btn-set-price.js-chat__btn-set-price").click()
        BROWSER.find_element_by_css_selector(".form-control.js-chat__price-input.b-chat__panel__input.js-input").send_keys(str(price))
        BROWSER.find_element_by_css_selector(".g-btn.m-rounded.js-panel__btn-save.js-chat__price-btn-save").click()
        print("Price Entered")
    except:
        settings.maybePrint(sys.exc_info()[0])

def confirm_message():
    try:
        global BROWSER
        send = WebDriverWait(BROWSER, 60, poll_frequency=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".g-btn.m-rounded.b-chat__btn-submit")))
        if str(settings.DEBUG) == "True":
            print('OnlyFans Message: Skipped')
            return
        send.click()
        print('OnlyFans Message: Sent')
    except:
        settings.maybePrint(sys.exc_info()[0])

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
        print(e)

# update chat logs for all users
def update_chat_logs():
    print("Updating User Chats")
    users = get_users()
    for user in users:
        update_chat_log(user)

def update_chat_log(user):
    print("Updating Chat: {} - {}".format(user.username, user.id))
    if not user:
        return print("Error: Missing User")
    user.readChat()

#################
##### Users #####
#################

# gets a list of all user_ids subscribed to profile
def get_users():
    # gets users from cache or refreshes from onlyfans.com
    global USER_CACHE
    if USER_CACHE:
        return USER_CACHE
    USER_CACHE = get_users_local()
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
        print("goto -> /my/subscribers/active")
        BROWSER.get(('https://onlyfans.com/my/subscribers/active'))
        num = BROWSER.find_element_by_class_name("b-tabs__nav__item__count").get_attribute("innerHTML")
        settings.maybePrint("User count: %s" % num)
        for n in range(int(int(int(num)/10)+1)):
            settings.maybePrint("scrolling...")
            BROWSER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failed to Count Users")
        return []
    user_ids = BROWSER.find_elements_by_class_name('b-avatar')
    users = BROWSER.find_elements_by_class_name('g-user-name')
    usernames = BROWSER.find_elements_by_class_name('g-user-username')
    # settings.maybePrint(users)
    # return []
    # add to list of users
    active_users = []
    global OnlyFans_USERNAME
    settings.maybePrint("Found: ")
    for i in range(len(user_ids)):
        user_id = user_ids[i]
        name = users[i]
        username = usernames[i]
        user_id = str(user_id.get_attribute("user_id")).strip()
        name = str(name.get_attribute("innerHTML")).strip()
        username = str(username.get_attribute("innerHTML")).strip()
        if str(OnlyFans_USERNAME).lower() in str(username).lower():
            settings.maybePrint("skipping self: %s = %s" % (OnlyFans_USERNAME, username))
            continue
        if str(OnlyFans_USER_ID).lower() in str(user_id).lower():
            settings.maybePrint("skipping self: %s" % (OnlyFans_USER_ID, user_id))
            continue
        if str(user_id).lower() in settings.SKIP_USERS:
            settings.maybePrint("skipping: %s" % user_id)
            continue
        active_users.append(User(name=name, username=username, id=user_id)) # update this with correct values
    for user in active_users:
        existing = False
        for user_ in USER_CACHE:
            if user.equals(user_):
                existing = True
        if not existing:
            USER_CACHE.append(user)
    # start cache timeout
    start_user_cache()
    return USER_CACHE

# gets a list of all subscribed user_ids from local txt
def get_users_local():
    print("Getting Local Users")
    users = []
    users_ = []
    try:
        with open(LOCAL_DATA) as json_file:  
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

def get_recent_user():
    users = get_users()
    return users[0]

def get_recent_users():
    users = get_users()
    i = 0
    users_ = []
    for user in users:
        # settings.maybePrint("user: %s" % user.username)
        if str(user.username).lower() in settings.SKIP_USERS:
            settings.maybePrint("skipping: %s" % user.username)
            continue
        users_.append(user)
        i += 1
        if i == settings.RECENT_USER_COUNT:
            return users_
    return users_

def reset_user_cache():
    global USER_CACHE
    USER_CACHE = False
    settings.maybePrint("User Cache: reset")

def start_user_cache():
    settings.maybePrint("User Cache: starting")
    try:
        threading.Timer(600.0, reset_user_cache).start() # after 10 minutes
        settings.maybePrint("User Cache: started")
    except:
        settings.maybePrint("User Cache: error starting")
        settings.maybePrint(sys.exc_info()[0])

# writes user list to local txt
def write_users_local():
    users = get_users()
    print("Writing Local Users")
    settings.maybePrint("local data path: "+str(LOCAL_DATA))
    data = {}
    data['users'] = []
    for user in users:
        settings.maybePrint("Saving: "+str(user.username))
        data['users'].append(user.toJSON())
    try:
        with open(LOCAL_DATA, 'w') as outfile:  
            json.dump(data, outfile, indent=4, sort_keys=True)
    except FileNotFoundError:
        print("Error: Missing Local Users")
    except OSError:
        print("Error: Missing Local Path")

################
##### Exit #####
################

def exit(force=False):
    if not force:
        print("Saving and Exiting OnlyFans")
        write_users_local()
    global BROWSER
    BROWSER.quit()
    print("Browser Closed")
#!/usr/bin/python
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
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .user import User
from . import settings

###################
##### Globals #####
###################

BROWSER = None
USER_CACHE = None
LOCAL_DATA = None
if settings.USERS_PATH is not None:
    LOCAL_DATA = os.path.join(os.path.dirname(os.path.realpath(__file__)), settings.USERS_PATH)
else:
    LOCAL_DATA = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'users.json')

##################
##### Config #####
##################

CONFIG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')
try:
    with open(CONFIG_FILE) as config_file:    
        config = json.load(config_file)
except FileNotFoundError:
    print('Missing Config, run `onlysnarf-config`')
    sys.exit(0)

OnlyFans_USERNAME = config['username']        
OnlyFans_PASSWORD = config['password']
OnlyFans_USER_ID = "409408"

#####################
##### Functions #####
#####################

# Upload to OnlyFans
def log_into_OnlyFans():
    print('Logging into OnlyFans...')
    options = webdriver.ChromeOptions()
    if not settings.SHOW_WINDOW:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    # options.setExperimentalOption('useAutomationExtension', false);
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    global BROWSER
    # CHROMEDRIVER_PATH = chromedriver_binary.chromedriver_filename
    # BROWSER = webdriver.Chrome(binary=CHROMEDRIVER_PATH, chrome_options=options)
    BROWSER = webdriver.Chrome(chrome_options=options)
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

##################
##### Upload #####
##################

# Uploads a file to OnlyFans
def upload_file_to_OnlyFans(fileName, path, folderName):
    fileName = os.path.splitext(str(fileName))[0]
    print('Uploading: '+str(fileName))
    print('path: '+path)
    if settings.HASHTAGGING:
        postText = str(fileName)+" #"+" #".join(str(folderName).split(' '))
    else:
        postText = str(folderName)+" "+str(fileName)
    settings.maybePrint('text: '+str(postText))
    global BROWSER
    if not settings.TWEETING:
        WebDriverWait(BROWSER, 10, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//label[@for="new_post_tweet_send"]'))).click()
    BROWSER.find_element_by_id("new_post_text_input").send_keys(str(postText))
    BROWSER.find_element_by_id("fileupload_photo").send_keys(str(path))
    maxUploadCount = 12 # 2 hours max attempt time
    i = 0
    while True:
        try:
            WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]')))
            if settings.DEBUG:
                print('skipping OnlyFans upload')
                return
            # send.click()
            send = WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]'))).click()
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

# Failed to resize image (thumb) ????????????
# check / add / fix thumbnail for mp4

# Uploads a folder to OnlyFans
def upload_directory_to_OnlyFans(dirName, path, folderName):
    if settings.HASHTAGGING:
        postText = str(dirName)+" #"+" #".join(str(folderName).split(' '))
    else:    
        postText = str(folderName)+" "+str(dirName)
    print('Uploading: '+str(postText))
    settings.maybePrint('path: '+str(path))
    files_path = []
    for file in pathlib.Path(str(path)).iterdir():  
        files_path.append(str(file))
    settings.maybePrint('files: '+str(files_path))
    global BROWSER
    BROWSER.find_element_by_id("new_post_text_input").send_keys(str(postText))
    WAIT = WebDriverWait(BROWSER, 600, poll_frequency=10)
    if not settings.TWEETING:
        WAIT.until(EC.element_to_be_clickable((By.XPATH, '//label[@for="new_post_tweet_send"]'))).click()
    
    ############
    # files_path = "[\""+"\",\"".join(files_path)+"\"]"
    # print("files_path: "+files_path)
    # files_path = "home/skeetzo/Projects/onlysnarf/OnlySnarf/tmp"
    # BROWSER.find_element_by_id("fileupload_photo").send_keys(files_path)
    # WebDriverWait(BROWSER, 600).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="send_post_button"]')))
    ############

    for file in files_path:
        settings.maybePrint('uploading: '+str(file))
        BROWSER.find_element_by_id("fileupload_photo").send_keys(str(file))
        send = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]')))
    send = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]')))
    if settings.DEBUG:
        print('skipping OnlyFans upload')
        return
    send = WAIT.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]'))).click()
    print('Directory Uploaded Successfully')

####################################################################################################################

def uploadPerformer(args, dirName, path, folderName):
    pass

####################
##### Messages #####
####################

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
            print("Missing Price")
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
        if settings.DEBUG:
            print('OnlyFans Message: Skipped')
            return
        send.click()
        print('OnlyFans Message: Sent')
    except:
        settings.maybePrint(sys.exc_info()[0])

# update chat logs for all users
def update_chat_logs():
    pass
def update_chat_log(user):
    pass

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
    global BROWSER
    if not BROWSER or BROWSER == None:
        log_into_OnlyFans()
    # go to onlyfans.com/my/subscribers/active
    print("goto -> /my/subscribers/active")
    BROWSER.get(('https://onlyfans.com/my/subscribers/active'))
    num = BROWSER.find_element_by_class_name("b-tabs__nav__item__count").get_attribute("innerHTML")
    settings.maybePrint("User count: %s" % num)
    for n in range(int(int(int(num)/10)+1)):
        settings.maybePrint("scrolling...")
        BROWSER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
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
    # save users locally
    write_users_local()
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

# gets a list of all subscribed user_ids from local txt
def get_users_local():
    print("Getting Local Users")
    users = []
    users_ = []
    try:
        with open(LOCAL_DATA) as json_file:  
            users = json.load(json_file)
        for user in users['users']:
            user = User(name=user['name'], username=user['username'], id=user['id'])
            settings.maybePrint('Loaded: %s' % user.username)
            settings.maybePrint('')
            users_.append(user)
    except FileNotFoundError:
        print("Error: Missing Local Users")
    finally:
        return users_

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
    with open(LOCAL_DATA, 'w') as outfile:  
        json.dump(data, outfile, indent=4, sort_keys=True)

def exit():
    print("Saving and Exiting OnlyFans")
    write_users_local()
    global BROWSER
    BROWSER.quit()
    print("Browser Closed")

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

# debugging
def maybePrint(text):
    if settings.DEBUG:
        print(text);

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
    # maybePrint('path: '+path)
    if settings.HASHTAGGING:
        postText = str(fileName)+" #"+" #".join(str(folderName).split(' '))
    else:
        postText = str(folderName)+" "+str(fileName)
    maybePrint('text: '+str(postText))
    global BROWSER
    BROWSER.find_element_by_id("new_post_text_input").send_keys(str(postText))
    BROWSER.find_element_by_id("fileupload_photo").send_keys(str(path))
    if not settings.TWEETING:
        WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//label[@for="new_post_tweet_send"]'))).click()
    maxUploadCount = 12 # 2 hours max attempt time
    i = 0
    while True:
        try:
            WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="btn btn-xs btn-default send_post_button"]')))
            # WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]')))
            if settings.DEBUG:
                print('skipping OnlyFans upload')
                return
            send = WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="btn btn-xs btn-default send_post_button"]'))).click()
            # send = WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]'))).click()
            break
        except Exception as e:
            print('uploading...')
            i+=1
            if i == maxUploadCount and settings.FORCE_UPLOAD is not True:
                print('max upload wait reached, breaking..')
                break
    print('File Uploaded Successfully')

# Uploads a folder to OnlyFans
def upload_directory_to_OnlyFans(dirName, path, folderName):
    if settings.HASHTAGGING:
        postText = str(dirName)+" #"+" #".join(str(folderName).split(' '))
    else:    
        postText = str(folderName)+" "+str(dirName)
    print('Uploading: '+str(postText))
    maybePrint('path: '+str(path))
    files_path = []
    for file in pathlib.Path(str(path)).iterdir():  
        files_path.append(str(file))
    maybePrint('files: '+str(files_path))
    global BROWSER
    BROWSER.find_element_by_id("new_post_text_input").send_keys(str(postText))
    if not settings.TWEETING:
        WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//label[@for="new_post_tweet_send"]'))).click()
    
    ############
    # files_path = "[\""+"\",\"".join(files_path)+"\"]"
    # print("files_path: "+files_path)
    # files_path = "home/skeetzo/Projects/onlysnarf/OnlySnarf/tmp"
    # BROWSER.find_element_by_id("fileupload_photo").send_keys(files_path)
    # WebDriverWait(BROWSER, 600).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="btn btn-xs btn-default send_post_button"]')))
    ############

    for file in files_path:
        maybePrint('uploading: '+str(file))
        BROWSER.find_element_by_id("fileupload_photo").send_keys(str(file))
        WebDriverWait(BROWSER, 600).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]')))
    send = WebDriverWait(BROWSER, 600).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]')))
    if settings.DEBUG:
        print('skipping OnlyFans upload')
        return
    send.click()
    print('Directory Uploaded Successfully')

####################################################################################################################

def uploadPerformer(args, dirName, path, folderName):
    pass


#################
##### Users #####
#################

def goto_user(username):
    print("Goto user: %s" % username)
    global BROWSER
    if not BROWSER:
        log_into_OnlyFans()
    username = str(username).replace("@u","").replace("@","")
    BROWSER.get(('https://onlyfans.com/my/chats/chat/'+str(username)))
    print("goto -> /my/chats/chat/$%s" % username)

def enter_message(text):
    try:
        print("Enter text: %s" % text)
        if not text or text == None:
            print("Missing Text")
            return
        global BROWSER
        message = BROWSER.find_element_by_class("form-control unlimsize b-chat__message-input").sendKeys(Keys.TAB);
        message.clear();
        message.send_keys(str(text))
        print("Message Entered")
    except:
        print(sys.exc_info()[0])

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
        print(sys.exc_info()[0])

def enter_price(price):
    try:
        print("Enter price: %s" % price)
        if not price or price == None:
            print("Missing Price")
            return
        global BROWSER
        BROWSER.find_element_by_class("b-chat__btn-set-price js-chat__btn-set-price").click()
        BROWSER.find_element_by_class("form-control js-chat__price-input b-chat__panel__input js-input").send_keys(str(price))
        BROWSER.find_element_by_class("g-btn m-rounded js-panel__btn-save js-chat__price-btn-save").click()
        print("Price Entered")
    except:
        print(sys.exc_info()[0])

def confirm_message():
    try:
        if settings.DEBUG:
            print('skipping OnlyFans message')
            return
        global BROWSER
        BROWSER.find_element_by_class("g-btn m-rounded b-chat__btn-submit").click()
    except:
        print(sys.exc_info()[0])

# gets a list of all user_ids subscribed to profile
def get_users():
    # gets users from cache or refreshes from onlyfans.com
    global USER_CACHE
    if USER_CACHE:
        return USER_CACHE
    USER_CACHE = get_users_local()
    global BROWSER
    if not BROWSER:
        log_into_OnlyFans()
    # go to onlyfans.com/my/subscribers/active
    BROWSER.get(('https://onlyfans.com/my/subscribers/active'))
    print("goto -> /my/subscribers/active")
    # scrape all  <span class="g-user-username">@u6279283</span>
    # users = BROWSER.find_elements_by_xpath(By.XPATH, '//span[@class="g-user-username"]')
    users = BROWSER.find_elements_by_class_name('g-user-username')
    # maybePrint(users)
    # return []
    # add to list of users
    active_users = []
    global OnlyFans_USERNAME
    for user in users:
        name = str(user.get_attribute("innerHTML")).strip()
        if str(name) == "@"+str(OnlyFans_USERNAME):
            continue
        print("username: "+str(name))
        active_users.append(str(name)) # update this with correct values
    for user in active_users:
        existing = False
        for user_ in USER_CACHE:
            if str(user) == str(user_):
                existing = True
        if not existing:
            USER_CACHE.append(User(str(user)))
        user = User(user)
    # start cache timeout
    start_user_cache()
    # save users locally
    write_users_local(USER_CACHE)
    return USER_CACHE

def get_user_by_username(username):
    users = get_users()
    for user in users:
        if str(user.username) == str(username):
            return user
    return None

def get_recent_users():
    users = get_users()
    i = 0
    users_ = []
    for user in users:
        users_.append(user)
        i += 1
        if i == 10:
            return users_
    return users_

def reset_user_cache():
    global USER_CACHE
    USER_CACHE = False
    maybePrint("User Cache: reset")

def start_user_cache():
    maybePrint("User Cache: starting")
    try:
        threading.Timer(600.0, reset_user_cache).start() # after 10 minutes
        maybePrint("User Cache: started")
    except:
        maybePrint("User Cache: error starting")
        print(sys.exc_info()[0])

# gets a list of all subscribed user_ids from local txt
def get_users_local():
    print("Getting Local Users")
    users = []
    users_ = []
    try:
        with open(LOCAL_DATA) as json_file:  
            users = json.load(json_file)
        for p in users['users']:
            maybePrint('Username: ' + str(p))
            maybePrint('')
            users_.append(User(str(p)))
    except FileNotFoundError:
        print("Missing File: Local Users")
    finally:
        return users_

# writes user list to local txt
def write_users_local(users):
    print("Writing Local Users")
    maybePrint("local data path: "+str(LOCAL_DATA))
    data = {}
    data['users'] = []
    for user in users:
        maybePrint("saving: "+str(user.username))
        data['users'].append({  
            'username': str(user.username),
        })
    with open(LOCAL_DATA, 'w') as outfile:  
        json.dump(data, outfile)



# go to user chat at
# /my/chats/chat/$user_id

# upload photo
# input   id="cm_fileupload_photo"

# click button for setting price
# button     class="b-chat__btn-set-price js-chat__btn-set-price"
# set price
# class="form-control js-chat__price-input b-chat__panel__input js-input"
# save price
# class="g-btn m-rounded js-panel__btn-save js-chat__price-btn-save"

# wait until button is available and then send
# class="g-btn m-rounded b-chat__btn-submit"

# handles the price modal that pops up
def enterPrice(price):
    pass
    # driver.click on price entry and enter the price amount
    # driver.click on confirm

def enterMessage(text, image, price):
    pass
    # doesn't check for login or if on correct page, just searches for generic stuff
    # search for driver.text and enter text
    # search for driver.image and click on upload and upload image file location
    # search for driver.price and click on price then call setPrice(price) which handles the generic price modal


# message recent messages
def message_recent():
    pass
    # login if not
    # open url for /my/chats
    # driver.click on last message by class search
    # call function enterMessage(message, image, price)
    # driver.click on send button
# go to /my/chats

# click on last message
# class="b-chats__item__last-message js-chats__item__last-message"

# or change this to scrape for last 5-10 recent
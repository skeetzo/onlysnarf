#!/usr/bin/python
# 3/18/2019: Skeetzo

import random
import os
import shutil
import datetime
import json
import sys
import pathlib

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Thread

###################
##### Globals #####
###################

CONFIG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.json')
CHROMEDRIVER_PATH = chromedriver_binary.chromedriver_filename
BROWSER = None
DEBUG = False
# Twitter hashtags
HASHTAGGING = False
# -f -> force / ignore upload max wait
FORCE_UPLOAD = False
# -show -> shows window
SHOW_WINDOW = False
# -q -> quiet / no tweet
TWEETING = True

##################
##### Config #####
##################

try:
    with open(CONFIG_FILE) as config_file:    
        config = json.load(config_file)
except FileNotFoundError:
    print('Missing Config, run `onlysnarf-config`')
    sys.exit(0)

OnlyFans_USERNAME = config['username']        
OnlyFans_PASSWORD = config['password']   

def updateDefaults(args):
    for arg in args:
        if arg[0] == "Debug":
            global DEBUG
            DEBUG = arg[1]
        if arg[0] == "Debug Skip Download":
            global DEBUG_SKIP_DOWNLOAD
            DEBUG_SKIP_DOWNLOAD = arg[1]
        if arg[0] == "Hashtag":
            global HASHTAGGING
            HASHTAGGING = arg[1]
        if arg[0] == "Force Upload":
            global FORCE_UPLOAD
            FORCE_UPLOAD = arg[1]
        if arg[0] == "Show Window":
            global SHOW_WINDOW
            SHOW_WINDOW = arg[1]
        if arg[0] == "Tweeting":
            global TWEETING        
            TWEETING = arg[1]

# debugging
def maybePrint(text):
    if DEBUG:
        print(text);

#####################
##### Functions #####
#####################

# Upload to OnlyFans
def log_into_OnlyFans(SHOW_WINDOW):
    print('Logging into OnlyFans...')
    options = webdriver.ChromeOptions()
    if not SHOW_WINDOW:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    # options.setExperimentalOption('useAutomationExtension', false);
    options.add_argument('--disable-gpu')  # Last I checked this was necessary.
    global BROWSER
    # BROWSER = webdriver.Chrome(binary=CHROMEDRIVER_PATH, chrome_options=options)
    BROWSER = webdriver.Chrome(chrome_options=options)
    BROWSER.implicitly_wait(10) # seconds
    BROWSER.set_page_load_timeout(1200)
    BROWSER.get(('https://onlyfans.com'))
    # login via Twitter
    twitter = BROWSER.find_element_by_xpath('//a[@class="btn btn-default btn-block btn-lg btn-twitter"]').click()
    # fill in username
    username = BROWSER.find_element_by_xpath('//input[@id="username_or_email"]').send_keys(OnlyFans_USERNAME)
    # fill in password and hit the login button 
    password = BROWSER.find_element_by_xpath('//input[@id="password"]')
    password.send_keys(OnlyFans_PASSWORD)
    password.send_keys(Keys.ENTER)
    print('Login Success')

##################
##### Upload #####
##################

# Uploads a file to OnlyFans
def upload_file_to_OnlyFans(args, fileName, path, folderName):
    updateDefaults(args)
    fileName = os.path.splitext(fileName)[0]
    print('Uploading: '+fileName)
    # maybePrint('path: '+path)
    if HASHTAGGING:
        postText = str(fileName)+" #"+" #".join(folderName.split(' '))
    else:
        postText = folderName+" "+fileName
    maybePrint('text: '+postText)
    global BROWSER
    BROWSER.find_element_by_id("new_post_text_input").send_keys(postText)
    BROWSER.find_element_by_id("fileupload_photo").send_keys(path)
    if not TWEETING:
        WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//label[@for="new_post_tweet_send"]'))).click()
    maxUploadCount = 12 # 2 hours max attempt time
    i = 0
    while True:
        try:
            WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="btn btn-xs btn-default send_post_button"]')))
            # WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]')))
            if DEBUG:
                print('skipping OnlyFans upload')
                return
            send = WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="btn btn-xs btn-default send_post_button"]'))).click()
            # send = WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]'))).click()
            break
        except Exception as e:
            print('uploading...')
            i+=1
            if i == maxUploadCount and FORCE_UPLOAD is not True:
                print('max upload wait reached, breaking..')
                break
    print('File Uploaded Successfully')

# Uploads a folder to OnlyFans
def upload_directory_to_OnlyFans(args, dirName, path, folderName):
    updateDefaults(args)
    if HASHTAGGING:
        postText = str(dirName)+" #"+" #".join(folderName.split(' '))
    else:    
        postText = str(folderName)+" "+str(dirName)
    print('Uploading: '+postText)
    maybePrint('path: '+path)
    files_path = []
    for file in pathlib.Path(path).iterdir():  
        files_path.append(str(file))
    maybePrint('files: '+str(files_path))
    global BROWSER
    BROWSER.find_element_by_id("new_post_text_input").send_keys(postText)
    if not TWEETING:
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
        BROWSER.find_element_by_id("fileupload_photo").send_keys(file)
        WebDriverWait(BROWSER, 600).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]')))
    send = WebDriverWait(BROWSER, 600).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="g-btn m-rounded send_post_button"]')))
    if DEBUG:
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
# code User.py
from . import user as User

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
    # scrape all  <span class="g-user-username">@u6279283</span>
    users = BROWSER.find_elements_by_class_name('//span[@class="g-user-username"]')
    maybePrint(users)
    return []
    # add to list of users
    active_users = []
    for user in users:
        active_users.append("") # update this with correct values
    for user in active_users:
        existing = False
        for user_ in USER_CACHE:
            if user == user_:
                existing = True
        if not existing:
            USER_CACHE.append(user)
    # start cache timeout
    start_user_cache()
    # save users locally
    write_users_local(USER_CACHE)
    return USER_CACHE


def reset_user_cache():
    global USER_CACHE
    USER_CACHE = False
    print("User Cache Reset")

def start_user_cache():
    t = Timer(600.0, reset_user_cache)
    t.start() # after 10 minutes

# gets a list of all subscribed user_ids from local txt
def get_users_local():
    print("Getting Local Users")
    with open(LOCAL_DATA) as json_file:  
    users = json.load(json_file)
    for p in users['users']:
        print('Name: ' + p['name'])
        print('Username: ' + p['username'])
        print('')
    return users

# writes user list to local txt
def write_users_local(users):
    print("Writing Local Users")
    data = {}
    data['users'] = []
    for user in users:
        data['users'].append({  
            'name': user['name'],
            'username': user['username']
        })
    with open(LOCAL_DATA, 'w') as outfile:  
        json.dump(data, outfile)

####################
##### Messages #####
####################

# sends message to all users
def mass_message_all(message, image, price):
    print("Sending Mass Message")
    users = get_users()
    for user in users:
        user.sendMessage(message, image, price)

#### NEEDED?
# sends an image at price to user_id recipient
def send_message(message, image, price, recipient):
    print("Sending Message to User: "+recipient)
    recipient.sendMessage(message, image, price)

#################
##### Crons ##### -> move to onlysnarf.py
#################

# sends a message to all recent subscribers
def greet_new_subscribers():
    pass



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
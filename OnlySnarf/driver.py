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
            if DEBUG:
                print('skipping OnlyFans upload')
                return
            send = WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="btn btn-xs btn-default send_post_button"]'))).click()
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
    # maybePrint('path: '+path)
    files_path = []
    for file in pathlib.Path(path).iterdir():  
        files_path.append(str(file))
    # maybePrint('files: '+str(files_path))
    global BROWSER
    BROWSER.find_element_by_id("new_post_text_input").send_keys(postText)
    if not TWEETING:
        WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.XPATH, '//label[@for="new_post_tweet_send"]'))).click()
    for file in files_path:
        maybePrint('uploading: '+str(file))
        BROWSER.find_element_by_id("fileupload_photo").send_keys(file)
        WebDriverWait(BROWSER, 600).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="btn btn-xs btn-default send_post_button"]')))
    if DEBUG:
        print('skipping OnlyFans upload')
        return
    send = WebDriverWait(BROWSER, 600).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit" and @class="btn btn-xs btn-default send_post_button"]'))).click()
    print('Directory Uploaded Successfully')




####################################################################################################################

def uploadPerformer(args, dirName, path, folderName):
	pass


#################
##### Users #####
#################
# code User.py
from . import User

# gets a list of all user_ids subscribed to profile
def get_users():
	pass
# gets a list of all subscribed user_ids from local txt
def get_users_local():
	pass
# writes user list to local txt
def write_users_local():
	pass

####################
##### Messages #####
####################

# sends message to all users
def mass_message_all(message, image, price):
	pass

# sends an image at price to user_id recipient
def send_priced_image(message, image, price, recipient):
	pass

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






# message recent messages
def message_recent():
	pass
# go to /my/chats

# click on last message
# class="b-chats__item__last-message js-chats__item__last-message"

# or change this to scrape for last 5-10 recent
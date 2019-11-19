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
import chromedriver_binary
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from OnlySnarf.user import User
from OnlySnarf.settings import SETTINGS as settings

###################
##### Globals #####
###################

BROWSER = None
ONLYFANS_HOME_URL = 'https://onlyfans.com/'
ONLYFANS_USERS_ACTIVE_URL = "https://onlyfans.com/my/subscribers/active"
SEND_BUTTON_XPATH = "//button[@type='submit' and @class='g-btn m-rounded send_post_button']"
SEND_BUTTON_CLASS = "g-btn.m-rounded.send_post_button"
TWITTER_LOGIN0 = "//a[@class='g-btn m-rounded m-flex m-lg']"
TWITTER_LOGIN1 = "//a[@class='g-btn m-rounded m-flex m-lg btn-twitter']"
TWITTER_LOGIN2 = "//a[@class='btn btn-default btn-block btn-lg btn-twitter']"
USERNAME_XPATH = "//input[@id='username_or_email']"
PASSWORD_XPATH = "//input[@id='password']"
MESSAGE_INPUT_CLASS = ".form-control.b-chat__message-input"
MESSAGE_CONFIRM = "g-btn.m-rounded.b-chat__btn-submit"
MONTHS_INPUT = "form-control.b-fans__trial__select"
DISCOUNT_INPUT = "form-control.b-fans__trial__select"
DISCOUNT_TEXT = "form-control.b-fans__trial__select"
DISCOUNT_USER_BUTTONS = "g-btn.m-rounded.m-border.m-sm"
DISCOUNT_USER_BUTTONS1 = "g-btn.m-rounded"
DISCOUNT_USERS = "g-btn.m-rounded.m-border.m-sm"
DISCOUNT_USERS_ = "b-users__item.m-fans"
EXPIRATION = "g-btn.m-flat.b-make-post__expire-period-btn"
EXPIRATION_PERIODS = "b-make-post__expire__label"
EXPIRATION_SAVE = "g-btn.m-rounded.js-make-post-poll-duration-save"
EXPIRATION_CANCEL = "g-btn.m-rounded.m-border"
ONLYFANS_TWEET = "//label[@for='new_post_tweet_send']"
ONLYFANS_UPLOAD_PHOTO = "fileupload_photo"
ONLYFANS_UPLOAD_MESSAGE_PHOTO = "cm_fileupload_photo"
ONLYFANS_USER_COUNT = "l-sidebar__user-data__item__count"
ONLYFANS_USERS_IDS = "a.g-btn.m-rounded.m-border.m-sm"
ONLYFANS_USERS_STARTEDS = "b-fans__item__list__item"
ONLYFANS_USERS = "g-user-name__wrapper"
ONLYFANS_USERSNAMES = "g-user-username"
ONLYFANS_POST_TEXT_CLASS = "new_post_text_input"
ONLYFANS_PRICE = ".b-chat__btn-set-price"
ONLYFANS_PRICE_INPUT = ".form-control.b-chat__panel__input"
ONLYFANS_PRICE_CLICK = ".g-btn.m-rounded"
ONLYFANS_CHAT_URL = "https://onlyfans.com/my/chats/chat/"
ONLYFANS_UPLOAD_BUTTON = "g-btn.m-rounded.m-border"
ONLYFANS_MESSAGES_FROM = "m-from-me"
ONLYFANS_MESSAGES_ALL = "b-chat__message__text"
ONLYFANS_MESSAGES = "b-chat__message__text"
ONLYFANS_MORE = "g-btn.m-flat.b-make-post__more-btn"
SCHEDULE = "g-btn.m-flat.b-make-post__datepicker-btn"
SCHEDULE_EXISTING_DATE = "vdatetime-calendar__current--month"
SCHEDULE_NEXT_MONTH = "vdatetime-calendar__navigation--next"
SCHEDULE_DAYS = "vdatetime-calendar__month__day"
SCHEDULE_SAVE = "g-btn.m-rounded"
SCHEDULE_HOURS = "vdatetime-time-picker__item.vdatetime-time-picker__item"
SCHEDULE_MINUTES = "vdatetime-time-picker__item"
POLL = "g-btn.m-flat.b-make-post__voting-btn"
POLL_DURATION = "g-btn.m-flat.b-make-post__voting__duration"
POLL_ADD_QUESTION = "g-btn.m-flat.new_vote_add_option"
POLL_SAVE = "g-btn.m-rounded.js-make-post-poll-duration-save"
POLL_CANCEL = "b-dropzone__preview__delete"
POLL_INPUT_XPATH = "//input[@class='form-control']"

#####################
##### Functions #####
#####################

def auth():
    logged_in = False
    global BROWSER
    if not BROWSER or BROWSER == None: logged_in = log_into_OnlyFans()
    else: logged_in = True
    if logged_in == False: print("Error: Failure to Login")
    return logged_in

def goToHome():
    global BROWSER
    if BROWSER == None: return False
    if str(BROWSER.current_url) == str(ONLYFANS_HOME_URL):
        settings.maybePrint("at -> onlyfans.com")
    else:
        settings.maybePrint("goto -> onlyfans.com")
        BROWSER.get(ONLYFANS_HOME_URL)
        WebDriverWait(BROWSER, 60, poll_frequency=6).until(EC.visibility_of_element_located((By.XPATH, SEND_BUTTON_XPATH)))

# Login to OnlyFans
def log_into_OnlyFans():
    print('Logging into OnlyFans')
    username_ = str(settings.USERNAME)
    password_ = str(settings.PASSWORD)
    if not username_ or username_ == "":
        username_ = input("Twitter Username: ")
    if not password_ or password_ == "":
        password_ = input("Twitter Password: ")
        print("Save? y/n")
        save_ = input(">> ")
        if str(save_) != "n": settings.PASSWORD = password__
    if username_ == "" or password_ == "":
        print("Error: Missing Login Info")
        return False
    if str(settings.USERNAME) == "" or settings.USERNAME == None: settings.USERNAME = username_
    if str(settings.PASSWORD) == "" or settings.PASSWORD == None: settings.PASSWORD = password_
    settings.maybePrint("Opening Web Browser")
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
            BROWSER.get(ONLYFANS_HOME_URL)
            # login via Twitter
            if int(opt)==0:
                twitter = BROWSER.find_element_by_xpath(TWITTER_LOGIN0).click()
            elif int(opt)==1:
                twitter = BROWSER.find_element_by_xpath(TWITTER_LOGIN1).click()
            elif int(opt)==2:
                twitter = BROWSER.find_element_by_xpath(TWITTER_LOGIN2).click()
        except NoSuchElementException as e:
            print("Warning: Login Failure, Retrying")
            login(opt+1)
    try:
        login(0)
        # fill in username
        username = BROWSER.find_element_by_xpath(USERNAME_XPATH).send_keys(username_)
        # fill in password and hit the login button 
        password = BROWSER.find_element_by_xpath(PASSWORD_XPATH)
        password.send_keys(password_)
        password.send_keys(Keys.ENTER)
        WebDriverWait(BROWSER, 60, poll_frequency=6).until(EC.visibility_of_element_located((By.XPATH, SEND_BUTTON_XPATH)))
        print('Login Successful')
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
        BROWSER.get(ONLYFANS_HOME_URL)
        print('OnlyFans Reset')
        return True
    except Exception as e:
        settings.maybePrint(e)
        print('Error: Failure Resetting OnlyFans')
        return False

####################
##### Discount #####
####################

# maximum discount = 55%
def discount_user(user, depth=0, discount=10, months=1, tryAll=False):
    if not auth(): return False
    if int(discount) > 55:
        print("Warning: Discount Too High, Max -> 55%")
        discount = 55
    elif int(discount) < 5:
        print("Warning: Discount Too Low, Min -> 5%")
        discount = 5
    if int(months) > 12:
        print("Warning: Months Too High, Max -> 12")
        months = 12
    global BROWSER
    try:
        if str(BROWSER.current_url) == str(ONLYFANS_USERS_ACTIVE_URL):
            settings.maybePrint("at -> /my/subscribers/active")
            BROWSER.execute_script("window.scrollTo(0, 0);")
        else:
            settings.maybePrint("goto -> /my/subscribers/active")
            BROWSER.get(ONLYFANS_USERS_ACTIVE_URL)
        if tryAll: depth = BROWSER.find_element_by_class_name(ONLYFANS_USER_COUNT).get_attribute("innerHTML")
        # settings.maybePrint("Depth: {}".format(depth))
        for n in range(int(int(int(depth)/10)+1)):
            settings.maybePrint("scrolling...")
            BROWSER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failed to Find Users")
        return False
    users = BROWSER.find_elements_by_class_name(DISCOUNT_USERS_)
    print("Discounting User: {} - {}/{}".format(user, depth, len(users)))
    time.sleep(2)
    # get all the users
    user__ = users[0]
    for user_ in users:
        text = user_.get_attribute("innerHTML")
        buttons_ = user_.find_elements_by_class_name(DISCOUNT_USER_BUTTONS)
        if str(user) in text:
            user__ = user_
            break
    ActionChains(BROWSER).move_to_element(user_).perform()
    buttons = user__.find_elements_by_class_name(DISCOUNT_USER_BUTTONS)
    for button in buttons:
        if "Discount" in button.get_attribute("innerHTML"):
            try:
                button.click()
                break
            except Exception as e:
                print("Warning: Unable To Find User, retrying")
                settings.maybePrint(e)
                return discount_user(user, depth=depth, discount=discount, months=months, tryAll=True)
    time.sleep(1)
    buttons_ = BROWSER.find_elements_by_class_name(DISCOUNT_USER_BUTTONS1)
    try:
        (months_, discount_) = BROWSER.find_elements_by_class_name(DISCOUNT_INPUT)
        # removed in 2.10, inputs changed to above
        # months_ = BROWSER.find_element_by_class_name(MONTHS_INPUT)
        # if discount_.get_attribute("value") != "":
            # print("Warning: Existing Discount")
        # discount_.clear()
        for n in range(11):
            discount_.send_keys(str(Keys.UP))
        # if str(settings.DEBUG) == "True" and str(settings.DEBUG_DELAY) == "True":
        #     time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
        for n in range(round(int(discount)/5)-1):
            discount_.send_keys(Keys.DOWN)
        for n in range(11):
            months_.send_keys(str(Keys.UP))
        for n in range(int(months)-1):
            months_.send_keys(Keys.DOWN)
        if str(settings.DEBUG) == "True" and str(settings.DEBUG_DELAY) == "True":
            time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
        for button in buttons_:
            if "Cancel" in button.get_attribute("innerHTML") and str(settings.DEBUG) == "True":
                button.click()
                print("Skipping: Save Discount (Debug)")
                return True
            elif "Apply" in button.get_attribute("innerHTML") and str(settings.DEBUG) == "False":
                button.click()
                print("Discounted User: {}".format(user))
                return True
    except Exception as e:
        settings.maybePrint(e)
        for button in buttons_:
            if "Cancel" in button.get_attribute("innerHTML"):
                button.click()
                print("Skipping: Save Discount")
                return True

######################
##### Expiration #####
######################

def expiration(period):
    if not auth(): return False
    if int(period) != 1 and int(period) != 3 and int(period) != 7 and int(period) != 30 and int(period) != 99 and str(period) != "No limit":
        print("Error: Missing Expiration")
        return False
    global BROWSER
    try:
        # goToHome()
        if isinstance(period,str) and str(period) == "No limit": period = 99
        print("Expiration:")
        print("- Period: {}".format(period))
        try:
            BROWSER.find_element_by_class_name(ONLYFANS_MORE).click()
        except Exception as e:
            pass
        BROWSER.find_element_by_class_name(EXPIRATION).click()
        nums = BROWSER.find_elements_by_class_name(EXPIRATION_PERIODS)
        for num in nums:
            inner = num.get_attribute("innerHTML")
            if str(inner) == "1 day" and int(period) == 1: num.click()
            if str(inner) == "3 days" and int(period) == 3: num.click()
            if str(inner) == "7 days" and int(period) == 7: num.click()
            if str(inner) == "30 days" and int(period) == 30: num.click()
            if "No limit" in str(inner) and int(period) == 99: num.click()
        if str(settings.DEBUG) == "True" and str(settings.DEBUG_DELAY) == "True":
            time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
        save = BROWSER.find_element_by_class_name(EXPIRATION_SAVE)
        if str(settings.DEBUG) == "True":
            print("Skipping Expiration (debug)")
            cancels = BROWSER.find_elements_by_class_name(EXPIRATION_CANCEL)
            cancels[1].click() # its the second cancel button
        else:
            save.click()
            print("Expiration Entered")
        return True
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failed to enter Expiration")
        return False

####################
##### Messages #####
####################
 
def message_confirm():
    try:
        global BROWSER
        sends = BROWSER.find_elements_by_class_name(MESSAGE_CONFIRM)
        for send in sends:
            print(send)
            print(send.get_attribute("value"))
        send = WebDriverWait(BROWSER, 60, poll_frequency=10).until(EC.element_to_be_clickable((By.CLASS_NAME, MESSAGE_CONFIRM)))
        if str(settings.DEBUG) == "True":
            if str(settings.DEBUG_DELAY) == "True":
                time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
            print('OnlyFans Message: Skipped (debug)')
            return True
        send.click()
        print('OnlyFans Message: Sent')
        return True
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failure to Confirm Message")
        return False

def message_text(text):
    try:
        if not text or text == None or str(text) == "None":
            print("Error: Missing Text")
            return False
        print("Enter text: {}".format(text))
        global BROWSER
        message = BROWSER.find_element_by_css_selector(MESSAGE_INPUT_CLASS)        
        message.send_keys(str(text))
        settings.maybePrint("Text Entered")
        return True
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failure to Enter Message")
        return False

def message_image(image):
    try:
        if not image or image == None or str(image) == "None":
            print("Error: Missing Image(s)")
            return False
        print("Enter image(s): {}".format(image))
        global BROWSER
        files = []
        if str(settings.SKIP_DOWNLOAD) == "True":
            print("Warning: Unable to upload, skipped download")
            return True
        if os.path.isfile(str(image)):
            files = [str(image)]
        elif os.path.isdir(str(image)):
            for file in os.listdir(str(image)):
                files.append(os.path.join(os.path.abspath(str(image)),file))
        else:
            print("Error: Missing Image File(s)")
            return False
        if str(settings.SKIP_UPLOAD) == "True":
            print("Skipping Upload")
            return True
        files = files[:int(settings.IMAGE_UPLOAD_MAX_MESSAGES)]
        for file in files:  
            print('Uploading: '+str(file))
            BROWSER.find_element_by_id(ONLYFANS_UPLOAD_MESSAGE_PHOTO).send_keys(str(file))
        try:
            buttons = BROWSER.find_elements_by_class_name(ONLYFANS_UPLOAD_BUTTON)
            if len(buttons) > 0: settings.maybePrint("Warning: Upload Error Message, Closing")
            for butt in buttons:
                if butt.get_attribute("innerHTML").strip() == "Close":
                    butt.click()
                    settings.maybePrint("Success: Upload Error Message Closed")
                    time.sleep(1)
        except Exception as e:
            print("Error: Unable to Upload Images")
            settings.maybePrint(e)
            return False
        settings.maybePrint("Image(s) Entered")
        if str(settings.DEBUG) == "True" and str(settings.DEBUG_DELAY) == "True":
            time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
        return True
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failure to Enter Image(s)")
        return False

def message_price(price):
    try:
        if not price or price == None or str(price) == "None":
            print("Error: Missing Price")
            return False
        print("Enter price: {}" .format(price))

        global BROWSER
        WAIT = WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ONLYFANS_PRICE))).click()
        # BROWSER.find_element_by_css_selector(ONLYFANS_PRICE)
        BROWSER.find_elements_by_css_selector(ONLYFANS_PRICE_INPUT)[1].send_keys(str(price))
        BROWSER.find_elements_by_css_selector(ONLYFANS_PRICE_CLICK)[4].click()
        settings.maybePrint("Price Entered")
        if str(settings.DEBUG) == "True" and str(settings.DEBUG_DELAY) == "True":
            time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
        return True
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failure to Enter Price")
        return False

def message_user(user):
    try:
        if not auth(): return False
        userid = user.id
        if not userid or userid == None or str(userid) == "None":
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
        BROWSER.get(str(ONLYFANS_CHAT_URL)+str(userid))
        return True
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failure to Goto User - {}/{}".format(user.id, user.username))
        return False

def read_user_messages(user):
    try:
        if not auth(): return False
        global BROWSER
        # go to onlyfans.com/my/subscribers/active
        message_user(user)
        messages_from_ = BROWSER.find_elements_by_class_name(ONLYFANS_MESSAGES_FROM)
        # print("first message: {}".format(messages_to_[0].get_attribute("innerHTML")))
        # messages_to_.pop(0) # drop self user at top of page
        messages_all_ = BROWSER.find_elements_by_class_name(ONLYFANS_MESSAGES_ALL)
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
            message = message.find_element_by_class_name(ONLYFANS_MESSAGES)
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

################
##### Poll #####
################

def polling(poll):
    period = poll.get("period")
    questions = poll.get("questions")
    if isinstance(questions, str): questions = questions.split(",\"*\"")
    questions = [n.strip() for n in questions]
    if not auth(): return False
    if int(period) != 1 and int(period) != 3 and int(period) != 7 and int(period) != 30 and int(period) != 99 and str(period) != "No limit":
        print("Error: Missing Duration")
        return False
    if not questions or len(questions) == 0:
        print("Error: Missing Questions")
        return False
    global BROWSER
    try:
        print("Poll:")
        print("- Duration: {}".format(period))
        print("- Questions:\n> {}".format("\n> ".join(questions)))
        try:
            BROWSER.find_element_by_class_name(ONLYFANS_MORE).click()
        except Exception as e:
            pass
        BROWSER.find_element_by_class_name(POLL).click()
        BROWSER.find_element_by_class_name(POLL_DURATION).click()
        nums = BROWSER.find_elements_by_class_name(EXPIRATION_PERIODS)
        for num in nums:
            inner = num.get_attribute("innerHTML")
            if str(inner) == "1 day" and int(period) == 1: num.click()
            if str(inner) == "3 days" and int(period) == 3: num.click()
            if str(inner) == "7 days" and int(period) == 7: num.click()
            if str(inner) == "30 days" and int(period) == 30: num.click()
            if "No limit" in str(inner) and int(period) == 99: num.click()
        save = BROWSER.find_element_by_class_name(POLL_SAVE).click()
        time.sleep(1)
        if len(questions) > 2:
            for question in questions[2:]:
                BROWSER.find_element_by_class_name(POLL_ADD_QUESTION).click()
        questions_ = BROWSER.find_elements_by_xpath(POLL_INPUT_XPATH)
        i = 0
        # print("questions: {}".format(questions))
        for question in list(questions):
            questions_[i].send_keys(str(question))
            time.sleep(1)
            i+=1
        if str(settings.DEBUG) == "True" and str(settings.DEBUG_DELAY) == "True":
            time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
        if str(settings.DEBUG) == "True":
            print("Skipping Poll (debug)")
            cancel = BROWSER.find_element_by_class_name(POLL_CANCEL)
            cancel.click() # its the second cancel button
        else:
            print("Poll Entered")
        return True
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failed to enter Poll")
        return False

# b-dropzone__preview__delete


################
##### Post #####
################

def post(text, expires=None, schedule=False, poll=False):
    try:
        if not auth(): return False
        global BROWSER
        goToHome()
        print("Posting:")
        print("- Text: {}".format(text))
        if expires: expiration(expires)
        if schedule: scheduling(schedule)
        if poll: polling(poll)
        BROWSER.find_element_by_id(ONLYFANS_POST_TEXT_CLASS).send_keys(str(text))
        sends = BROWSER.find_elements_by_class_name(SEND_BUTTON_CLASS)
        for i in range(len(sends)):
            if sends[i].is_enabled():
                sends = sends[i]
        if str(settings.DEBUG) == "True" and str(settings.DEBUG_DELAY) == "True":
            time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
        if str(settings.DEBUG) == "True":
            print('Skipped: OnlyFans Post (debug)')
            return True
        sends.click()
        # send[1].click() # the 0th one is disabled
        print('OnlyFans Post Complete')
        return True
    except Exception as e:
        settings.maybePrint(e)
        print("Error: OnlyFans Post Failure")
        return False

######################
##### Promotions #####
######################

# or email
def get_new_trial_link():
    if not auth(): return False
    global BROWSER
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

####################
##### Schedule #####
####################

def scheduling(schedule_):
    if not auth(): return False
    global BROWSER
    try:
        if not schedule_:
            print("Error: Missing Schedule")
            return False
        tehdate = datetime.strptime(schedule_, "%m/%d/%Y:%H:%M")
        date = datetime.strptime(schedule_, "%m/%d/%Y:%H:%M").date()
        month_ = tehdate.strftime("%B")
        day_ = tehdate.day
        year_ = tehdate.year
        time_ = datetime.strptime(schedule_, "%m/%d/%Y:%H:%M").time()
        hour_ = datetime.strptime(schedule_, "%m/%d/%Y:%H:%M").hour
        minute_ = datetime.strptime(schedule_, "%m/%d/%Y:%H:%M").minute
        print("Schedule:")
        print("- Date: {}".format(date))
        print("- Time: {}".format(time_))
        try:
            BROWSER.find_element_by_class_name(ONLYFANS_MORE).click()
        except Exception as e:
            pass
        # click schedule
        BROWSER.find_element_by_class_name(SCHEDULE).click()
        searching = True
        while searching:
            existingDate = BROWSER.find_element_by_class_name(SCHEDULE_EXISTING_DATE).get_attribute("innerHTML")
            if str(month_) in str(existingDate) and str(year_) in str(existingDate):
                searching = False
            else:
                BROWSER.find_element_by_class_name(SCHEDULE_NEXT_MONTH).click()
        days = BROWSER.find_elements_by_class_name(SCHEDULE_DAYS)
        for day in days:
            inner = day.get_attribute("innerHTML").replace("<span><span>","").replace("</span></span>","")
            if str(day_) == str(inner):
                day.click()
        if str(settings.DEBUG) == "True" and str(settings.DEBUG_DELAY) == "True":
            time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
        saves = BROWSER.find_elements_by_class_name(SCHEDULE_SAVE)
        for save in saves:
            if "Save" in str(save.get_attribute("innerHTML")):
                save.click()
                break
        hours = BROWSER.find_elements_by_class_name(SCHEDULE_HOURS)
        for hour in hours:
            inner = hour.get_attribute("innerHTML")
            if str(hour_) in str(inner) and hour.is_enabled():
                hour.click()
        minutes = BROWSER.find_elements_by_class_name(SCHEDULE_MINUTES)
        for minute in minutes:
            inner = minute.get_attribute("innerHTML")
            if str(minute_) in str(inner) and minute.is_enabled():
                minute.click()
        if str(settings.DEBUG) == "True":
            print("Skipping Schedule (debug)")
            cancel = BROWSER.find_element_by_class_name(EXPIRATION_CANCEL)
            cancel.click() # its the first cancel button
        else:
            saves = BROWSER.find_elements_by_class_name(SCHEDULE_SAVE)
            for save in saves:
                if "Save" in str(save.get_attribute("innerHTML")):
                    save.click()
                    break
            print("Schedule Entered")
        return True
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failed to enter Schedule")
        return False

##################
##### Upload #####
##################

# Uploads a directory with a video file or image files to OnlyFans
def upload_to_OnlyFans(path=None, text="", keywords=[], performers=[], expires=False, schedule=False, poll=False):
    try:
        if not auth(): return False
        global BROWSER
        goToHome()
        if not path:
            print("Error: Missing Upload Path")
            return False
        if not text or text == None or str(text) == "None":
            print("Warning: Missing Upload Text")
            text = ""
        text = text.replace(".mov","")
        text = text.replace(".mp4","")
        text = text.replace(".MP4","")
        text = text.replace(".jpg","")
        text = text.replace(".jpeg","")
        if isinstance(performers, list) and len(performers) > 0: text += " w/ @"+" @".join(performers)
        if isinstance(keywords, list) and len(keywords) > 0: text += " #"+" #".join(keywords)
        text = text.strip()
        print("Uploading:")
        settings.maybePrint("- Path: {}".format(path))
        print("- Keywords: {}".format(keywords))
        print("- Performers: {}".format(performers))
        print("- Text: {}".format(text))
        print("- Tweeting: {}".format(settings.TWEETING))
        if expires: expiration(expires)
        if schedule: scheduling(schedule)
        if poll: polling(poll)
        WAIT = WebDriverWait(BROWSER, 600, poll_frequency=10)
        if str(settings.TWEETING) == "True":
            WAIT.until(EC.element_to_be_clickable((By.XPATH, ONLYFANS_TWEET))).click()
        files = []
        if str(settings.SKIP_DOWNLOAD) == "True":
            print("Warning: Unable to upload, skipped download")
            return True
        if os.path.isfile(str(path)):
            files = [str(path)]
        elif os.path.isdir(str(path)):
            # files = os.listdir(str(path))
            for file in os.listdir(str(path)):
                files.append(os.path.join(os.path.abspath(str(path)),file))
        else:
            print("Error: Unable to parse path")
            return False
        if str(settings.SKIP_UPLOAD) == "True":
            print("Skipping Upload")
            return True
        files = files[:int(settings.IMAGE_UPLOAD_MAX)]
        for file in files:  
            print('Uploading: '+str(file))
            BROWSER.find_element_by_id(ONLYFANS_UPLOAD_PHOTO).send_keys(str(file))
        maxUploadCount = 12 # 2 hours max attempt time
        i = 0
        while True:
            try:                
                WAIT.until(EC.element_to_be_clickable((By.XPATH, SEND_BUTTON_XPATH)))
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
            BROWSER.find_element_by_id(ONLYFANS_POST_TEXT_CLASS).send_keys(str(text))
            # first one is disabled
            sends = BROWSER.find_elements_by_class_name(SEND_BUTTON_CLASS)
            for i in range(len(sends)):
                if sends[i].is_enabled():
                    sends = sends[i]
            if str(settings.DEBUG) == "True" and str(settings.DEBUG_DELAY) == "True":
                time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
            if str(settings.DEBUG) == "True":
                print('Skipped: OnlyFans Upload (debug)')
                return True
            sends.click()
        except:
            settings.maybePrint("Warning: Upload Error Message, Closing")
            try:
                buttons = BROWSER.find_elements_by_class_name(ONLYFANS_UPLOAD_BUTTON)
                for butt in buttons:
                    if butt.get_attribute("innerHTML").strip() == "Close":
                        butt.click()
                        settings.maybePrint("Success: Upload Error Message Closed")
                        send_text = BROWSER.find_element_by_id(ONLYFANS_POST_TEXT_CLASS)
                        send_text.clear()
                        send_text.send_keys(str(text))
                        # first one is disabled
                        sends = BROWSER.find_elements_by_class_name(SEND_BUTTON_CLASS)
                        for i in range(len(sends)):
                            if sends[i].is_enabled():
                                sends = sends[i]
                        if str(settings.DEBUG) == "True" and str(settings.DEBUG_DELAY) == "True":
                            time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
                        if str(settings.DEBUG) == "True":
                            print('Skipped: OnlyFans Upload (debug)')
                            return True
                        sends.click()
            except Exception as e:
                print("Error: Unable to Upload Images")
                settings.maybePrint(e)
                return False
        # send[1].click() # the 0th one is disabled
        print('OnlyFans Upload Complete')
        return True
    except Exception as e:
        settings.maybePrint(e)
        print("Error: OnlyFans Upload Failure")
        return False

#################
##### Users #####
#################

def get_users():
    if not auth(): return False
    global BROWSER
    try:
        if str(BROWSER.current_url) == str(ONLYFANS_USERS_ACTIVE_URL):
            settings.maybePrint("at -> /my/subscribers/active")
        else:
            settings.maybePrint("goto -> /my/subscribers/active")
            BROWSER.get(ONLYFANS_USERS_ACTIVE_URL)
            num = BROWSER.find_element_by_class_name(ONLYFANS_USER_COUNT).get_attribute("innerHTML")
            settings.maybePrint("User count: {}".format(num))
            for n in range(int(int(int(num)/10)+1)):
                settings.maybePrint("scrolling...")
                BROWSER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
    except Exception as e:
        settings.maybePrint(e)
        print("Error: Failed to Find Users")
        return []
    # avatars = BROWSER.find_elements_by_class_name('b-avatar')
    user_ids = BROWSER.find_elements_by_css_selector(ONLYFANS_USERS_IDS)
    starteds = BROWSER.find_elements_by_class_name(ONLYFANS_USERS_STARTEDS)
    # users = BROWSER.find_elements_by_class_name('g-user-name')
    users = BROWSER.find_elements_by_class_name(ONLYFANS_USERS)
    usernames = BROWSER.find_elements_by_class_name(ONLYFANS_USERSNAMES)
    usernames.pop(0)
    active_users = []
    # settings.maybePrint("user_ids: "+str(len(user_ids)))
    # settings.maybePrint("starteds: "+str(len(starteds)))
    useridsFailed = False
    startedsFailed = False
    if len(user_ids) == 0:
        print("Warning: Unable to find user ids")
        useridsFailed = True
    if len(starteds) == 0:
        print("Warning: Unable to find starting dates")
        startedsFailed = True
    users_ = []
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
        if len(user_ids_) == 0:
            print("Warning: Unable to find user ids")
            useridsFailed = True
        if len(starteds_) == 0:
            print("Warning: Unable to find starting dates")
            startedsFailed = True
        # settings.maybePrint("ids vs starteds vs avatars: "+str(len(user_ids_))+" - "+str(len(starteds_))+" - "+str(len(avatars)))
        settings.maybePrint("ids vs starteds vs usernames:"+str(len(user_ids_))+" - "+str(len(starteds_))+" - "+str(len(usernames)))
        for i in range(len(users)): # the first is you and doesn't count towards total
            try:
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
                if str(settings.USERNAME).lower() in str(username).lower():
                    settings.maybePrint("(self): %s = %s" % (settings.USERNAME, username))
                    # first user is always active user but just in case find it in list of users
                    settings.USER_ID = username
                    continue
                users_.append({"name":name, "username":username, "id":user_id, "started":start})
            except Exception as e:
                settings.maybePrint(e)
    except Exception as e:
        settings.maybePrint(e)
    settings.maybePrint("Found: {}".format(len(users_)))
    return users_

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
    if BROWSER:
        BROWSER.quit()
    BROWSER = None
    print("Browser Closed")
    global logged_in
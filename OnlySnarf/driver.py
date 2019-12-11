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
##
from OnlySnarf.settings import SETTINGS as settings

###################
##### Globals #####
###################

ONLYFANS_HOME_URL = 'https://onlyfans.com/'
ONLYFANS_SETTINGS_URL = "https://onlyfans.com/my/settings"
ONLYFANS_USERS_ACTIVE_URL = "https://onlyfans.com/my/subscribers/active"
SEND_BUTTON_XPATH = "//button[@type='submit' and @class='g-btn m-rounded']"
SEND_BUTTON_CLASS = "g-btn.m-rounded"
LIVE_BUTTON_CLASS = "b-make-post__streaming-link"
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
ONLYFANS_POST_TEXT_ID = "new_post_text_input"
ONLYFANS_PRICE = "b-chat__btn-set-price"
ONLYFANS_PRICE_INPUT = "form-control.g-input"
ONLYFANS_PRICE_CLICK = "g-btn.m-rounded"
ONLYFANS_CHAT_URL = "https://onlyfans.com/my/chats/chat"
ONLYFANS_UPLOAD_BUTTON = "g-btn.m-rounded.m-border"
ONLYFANS_MESSAGE_SEND_BUTTON = "g-btn.m-rounded.b-chat__btn-submit"
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
# POLL = "g-btn.m-flat.b-make-post__voting-btn.has-tooltip"
POLL_DURATION = "g-btn.m-flat.b-make-post__voting__duration"
POLL_ADD_QUESTION = "g-btn.m-flat.new_vote_add_option"
POLL_SAVE = "g-btn.m-rounded"
POLL_CANCEL = "b-dropzone__preview__delete"
POLL_INPUT_XPATH = "//input[@class='form-control']"
REMEMBERME_CHECKBOX_XPATH = "//input[@id='remember']"

ONLYFANS_ELEMENTS = [
    {
        "name": "confirm",
        "class_name": MESSAGE_CONFIRM,
        "text": "",
        "id": None
    },
    {
        "name": "post",
        "class_name": SEND_BUTTON_CLASS,
        "text": "Post",
        "id": None
    },
    {
        "name": "uploadImage",
        "class_name": "",
        "text": None,
        "id": ONLYFANS_UPLOAD_PHOTO
    },
    {
        "name": "uploadImageMessage",
        "class_name": "",
        "text": None,
        "id": ONLYFANS_UPLOAD_MESSAGE_PHOTO
    },
    {
        "name": "errorUpload",
        "class_name": "g-btn.m-rounded.m-border",
        "text": None,
        "id": None
    },
    {
        "name": "poll",
        "class_name": POLL,
        "text": "<svg class=\"g-icon\" aria-hidden=\"true\"><use xlink:href=\"#icon-more\" href=\"#icon-more\"></use></svg>",
        "id": None
    },
    {
        "name": "pollCancel",
        "class_name": POLL_CANCEL,
        "text": "Cancel",
        "id": None
    },
    {
        "name": "pollDuration",
        "class_name": POLL_DURATION,
        "text": None,
        "id": None
    },
    {
        "name": "pollDurations",
        "class_name": EXPIRATION_PERIODS,
        "text": None,
        "id": None
    },
    {
        "name": "pollSave",
        "class_name": POLL_SAVE,
        "text": "Save",
        "id": None
    },
    {
        "name": "pollQuestionAdd",
        "class_name": POLL_ADD_QUESTION,
        "text": None,
        "id": None
    },
    {
        "name": "moreOptions",
        "class_name": ONLYFANS_MORE,
        "text": "<svg class=\"g-icon\" aria-hidden=\"true\"><use xlink:href=\"#icon-more\" href=\"#icon-more\"></use></svg>",
        "id": None
    },
    {
        "name": "expiration",
        "class_name": EXPIRATION,
        "text": None,
        "id": None
    },
    {
        "name": "expirationPeriods",
        "class_name": EXPIRATION_PERIODS,
        "text": None,
        "id": None
    },
    {
        "name": "expirationSave",
        "class_name": EXPIRATION_SAVE,
        "text": None,
        "id": None
    },
    {
        "name": "priceEnter",
        "class_name": ONLYFANS_PRICE_INPUT,
        "text": "Free",
        "id": None
    },
    {
        "name": "saveSchedule",
        "class_name": SCHEDULE_SAVE,
        "text": "Save",
        "id": None
    },
    {
        "name": "login",
        "class_name": LIVE_BUTTON_CLASS,
        "text": "",
        "id": None
    }

    
    
]


def error_checker(e):
    if "Unable to locate element" in str(e):
        print("Warning: OnlySnarf may require an update")
    if str(settings.DEBUG) == "True" and str(settings.VERBOSE) == "True":
        print(e)
    elif "Message: " not in str(e):
        settings.maybePrint(e)

def get_element_by_name(name):
    settings.devPrint("getting element: {}".format(name))
    if name == None:
        settings.maybePrint("Error: Missing Element Name")
        return None
    global ONLYFANS_ELEMENTS
    for element in ONLYFANS_ELEMENTS:
        if str(element["name"]) == str(name): return element
    return None

class Driver:

    def __init__(self):
        self.browser = None

    #####################
    ##### Functions #####
    #####################

    def auth(self):
        logged_in = False
        if not self.browser or self.browser == None: logged_in = self.login()
        else: logged_in = True
        if logged_in == False: print("Error: Failure to Login")
        return logged_in

    def error_window_upload(self):
        try:
            element = get_element_by_name("errorUpload")
            error_buttons = self.browser.find_elements_by_class_name(element["class_name"])
            settings.devPrint("errors btns: {}".format(len(error_buttons)))
            for butt in error_buttons:
                if butt.get_attribute("innerHTML").strip() == "Close" and butt.is_enabled():
                    settings.maybePrint("Warning: Upload Error Message, Closing")
                    butt.click()
                    settings.maybePrint("Success: Upload Error Message Closed")
                    return True
            return False
        except Exception as e:
            error_checker(e)
            return False

    # should already be logged in
    def find_element_by_name(self, name):
        if self.browser == None: return False
        try:
            element = get_element_by_name(name)
            if not element:
                print("Error: Unable to find Element Reference")
                return False
            element = self.browser.find_element_by_class_name(element["class_name"])
            if not element: print("Warning Message About Element Not Found")
            return element
        except Exception as e:
            settings.maybePrint(e)
            print("Error: Element not found")
            return None

    def get_element_to_click(self, name):
        global ONLYFANS_ELEMENTS
        element = get_element_by_name(name)
        eles = self.browser.find_elements_by_class_name(element["class_name"])
        settings.devPrint("clickable eles: {}".format(len(eles)))
        for i in range(len(eles)):
            settings.devPrint("ele: {} -> {}".format(eles[i].get_attribute("innerHTML").strip(), element["text"]))
            if (element["text"] and str(element["text"]) == eles[i].get_attribute("innerHTML").strip()) and eles[i].is_enabled():
                settings.devPrint("found matching ele: {}".format(eles[i].get_attribute("innerHTML").strip()))
                return eles[i]
            elif (element["text"] and str(element["text"]) == eles[i].get_attribute("innerHTML").strip()):
                settings.devPrint("found text ele: {}".format(eles[i].get_attribute("innerHTML").strip()))
                return eles[i]
            elif not element["text"] and eles[i].is_enabled():
                settings.devPrint("found enabled ele: {}".format(eles[i].get_attribute("innerHTML").strip()))
                return eles[i]
        return eles[0] or None

    def go_to_home(self):
        if self.browser == None: return False
        if str(self.browser.current_url) == str(ONLYFANS_HOME_URL):
            settings.maybePrint("at -> onlyfans.com")
        else:
            settings.maybePrint("goto -> onlyfans.com")
            self.browser.get(ONLYFANS_HOME_URL)
            WebDriverWait(self.browser, 60, poll_frequency=6).until(EC.visibility_of_element_located((By.CLASS_NAME, LIVE_BUTTON_CLASS)))

    def upload_image_files(self, name="post", path=None):
        if path == None:
            print("Error: Missing Upload Path")
            return False
        if str(settings.SKIP_UPLOAD) == "True":
            print("Skipping Upload: Disabled")
            return True
        files = []
        if os.path.isfile(str(path)):
            files = [str(path)]
        elif os.path.isdir(str(path)):
            for file in os.listdir(str(path)):
                files.append(os.path.join(os.path.abspath(str(path)),file))
        else:
            print("Error: Missing Image File(s)")
            return False
        if len(files) == 0:
            print("Warning: Empty File Path")
            return False
        enter_file = self.browser.find_element_by_id(get_element_by_name(str(name))["id"])
        files = files[:int(settings.IMAGE_UPLOAD_LIMIT_MESSAGES)]
        for file in files:  
            print('Uploading: '+str(file))
            enter_file.send_keys(str(file))
            if self.error_window_upload():
                # move file to change its name
                filename = os.path.basename(file)
                filename = os.path.splitext(filename)[0]
                if "_fixed" in str(filename): continue
                print("Fixing Filename")
                filename += "_fixed"
                ext = os.path.splitext(filename)[1].lower()
                print("{} -> {}.{}".format(os.path.dirname(file), filename, ext))
                dst = "{}/{}.{}".format(os.path.dirname(file), filename, ext)
                shutil.move(file, dst)
                # add file to end of list so it gets retried
                files.append(dst)
                # if this doesn't force it then it'll loop forever without a stopper
            time.sleep(1)
         ## Wait for Confirm
        i = 0
        while True:
            try:                
                WebDriverWait(self.browser, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.CLASS_NAME, get_element_by_name(name)["class_name"])))
                settings.devPrint("upload complete")
                return True
            except Exception as e:
                # try: 
                #     # check for existence of "thumbnail is fucked up" modal and hit ok button
                #     # haven't seen in long enough time to properly add
                #     self.browser.switchTo().frame("iframe");
                #     self.browser.find_element_by_class("g-btn m-rounded m-border").send_keys(Keys.ENTER)
                #     print("Error: Thumbnail Missing")
                #     break
                # except Exception as ef:
                #     settings.maybePrint(ef)
                print('uploading...')
                error_checker(e)
                i+=1
                if i == int(settings.UPLOAD_MAX_DURATION) and settings.FORCE_UPLOAD is not True:
                    print('Error: Max Upload Time Reached')
                    return False
        return True

    ### Drivers

    ####################
    ##### Discount #####
    ####################

    # maximum discount = 55%
    def discount_user(self, user, depth=0, discount=10, months=1, tryAll=False):
        auth_ = self.auth()
        if not auth_: return False
        if int(discount) > 55:
            print("Warning: Discount Too High, Max -> 55%")
            discount = 55
        elif int(discount) < 5:
            print("Warning: Discount Too Low, Min -> 5%")
            discount = 5
        if int(months) > 12:
            print("Warning: Months Too High, Max -> 12")
            months = 12
        try:
            if str(self.browser.current_url) == str(ONLYFANS_USERS_ACTIVE_URL):
                settings.maybePrint("at -> /my/subscribers/active")
                self.browser.execute_script("window.scrollTo(0, 0);")
            else:
                settings.maybePrint("goto -> /my/subscribers/active")
                self.browser.get(ONLYFANS_USERS_ACTIVE_URL)
            if tryAll: depth = self.browser.find_element_by_class_name(ONLYFANS_USER_COUNT).get_attribute("innerHTML")
            # settings.maybePrint("Depth: {}".format(depth))
            for n in range(int(int(int(depth)/10)+1)):
                settings.maybePrint("scrolling...")
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
        except Exception as e:
            error_checker(e)
            print("Error: Failed to Find Users")
            return False
        try:
            users = self.browser.find_elements_by_class_name(DISCOUNT_USERS_)
            if int(len(users)) == 0:
                print("Error: Missing Users")
                return False
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
            ActionChains(self.browser).move_to_element(user_).perform()
            buttons = user__.find_elements_by_class_name(DISCOUNT_USER_BUTTONS)
            for button in buttons:
                if "Discount" in button.get_attribute("innerHTML"):
                    try:
                        button.click()
                        break
                    except Exception as e:
                        error_checker(e)
                        print("Warning: Unable To Find User, retrying")
                        return self.discount_user(user, depth=depth, discount=discount, months=months, tryAll=True)
            time.sleep(1)
            buttons_ = self.browser.find_elements_by_class_name(DISCOUNT_USER_BUTTONS1)
            (months_, discount_) = self.browser.find_elements_by_class_name(DISCOUNT_INPUT)
            # removed in 2.10, inputs changed to above
            # months_ = self.browser.find_element_by_class_name(MONTHS_INPUT)
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
            settings.debug_delay_check()
            for button in buttons_:
                # if "Cancel" in button.get_attribute("innerHTML") and str(settings.DEBUG) == "True":
                #     button.click()
                #     print("Skipping: Save Discount (Debug)")
                #     return True
                if "Apply" in button.get_attribute("innerHTML") and str(settings.DEBUG) == "False":
                    button.click()
                    print("Discounted User: {}".format(user))
                    return True
        except Exception as e:
            error_checker(e)
            for button in buttons_:
                if "Cancel" in button.get_attribute("innerHTML"):
                    button.click()
                    return False
            return False

    def enter_text(self, text):
        try:
            settings.devPrint("finding text")
            sendText = self.browser.find_element_by_id(ONLYFANS_POST_TEXT_ID)
            settings.devPrint("found text")
            sendText.clear()
            settings.devPrint("sending text")
            sendText.send_keys(str(text))
            return True
        except Exception as e:
            settings.maybePrint(e)
            return False

    ######################
    ##### Expiration #####
    ######################

    def expiration(self, period):
        settings.devPrint("expiration")   
        if int(period) != 1 and int(period) != 3 and int(period) != 7 and int(period) != 30 and int(period) != 99 and str(period) != "No limit":
            print("Error: Missing Expiration")
            return False
        auth_ = self.auth()
        if not auth_: return False
        try:
            # go_to_home() # this should be run only from upload anyways
            if isinstance(period,str) and str(period) == "No limit": period = 99
            print("Expiration:")
            print("- Period: {}".format(period))
            try:
                settings.devPrint("opening options")
                self.get_element_to_click("moreOptions").click()
            except Exception as e:
                pass
            # open expiration window
            settings.devPrint("adding expiration")
            self.get_element_to_click("expiration").click()
            # select duration
            settings.devPrint("selecting expiration")
            nums = self.browser.find_elements_by_class_name(get_element_by_name("expirationPeriods")["class_name"])
            for num in nums:
                inner = num.get_attribute("innerHTML")
                ##
                # <span class="g-first-letter">1</span> day
                # <span class="g-first-letter">3</span> days
                # <span class="g-first-letter">7</span> days
                # <span class="g-first-letter">30</span> days
                # <span><span class="g-first-letter">N</span>o limit</span>
                ##
                if ">1<" in str(inner) and int(period) == 1: num.click()
                if ">3<" in str(inner) and int(period) == 3: num.click()
                if ">7<" in str(inner) and int(period) == 7: num.click()
                if ">30<" in str(inner) and int(period) == 30: num.click()
                if ">o limit<" in str(inner) and int(period) == 99: num.click()
            settings.debug_delay_check()
            # save
            settings.devPrint("saving expiration")
            save = self.get_element_to_click("expirationSave")
            if str(settings.DEBUG) == "True":
                print("Skipping Expiration (debug)")
                cancels = self.browser.find_elements_by_class_name(EXPIRATION_CANCEL)
                cancels[1].click() # its the second cancel button
            else:
                save.click()
                print("Expiration Entered")
            return True
        except Exception as e:
            error_checker(e)
            print("Error: Failed to enter Expiration")
            return False

    ##################
    ###### Login #####
    ##################

    def login(self):
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
        # self.browser = webdriver.Chrome(binary=CHROMEDRIVER_PATH, chrome_options=options)
        CHROMEDRIVER_PATH = chromedriver_binary.chromedriver_filename
        os.environ["webdriver.chrome.driver"] = CHROMEDRIVER_PATH
        try:
            self.browser = webdriver.Chrome(chrome_options=options)
        except Exception as e:
            error_checker(e)
            print("Warning: Missing chromedriver_path, retrying")
            try:
                self.browser = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
            except Exception as e:
                error_checker(e)
                print("Error: Missing chromedriver_path, exiting")
                return False
        self.browser.implicitly_wait(10) # seconds
        self.browser.set_page_load_timeout(1200)    
        def attempt_login(opt):
            try:
                self.browser.get(ONLYFANS_HOME_URL)
                # login via Twitter
                if int(opt)==0:
                    twitter = self.browser.find_element_by_xpath(TWITTER_LOGIN0).click()
                elif int(opt)==1:
                    twitter = self.browser.find_element_by_xpath(TWITTER_LOGIN1).click()
                elif int(opt)==2:
                    twitter = self.browser.find_element_by_xpath(TWITTER_LOGIN2).click()
            except NoSuchElementException as e:
                opt+=1
                print("Warning: Login Failure, Retrying ({})".format(opt))
                attempt_login(opt)
        try:
            attempt_login(0)
            # rememberMe checkbox doesn't actually cause login to be remembered
            rememberMe = self.browser.find_element_by_xpath(REMEMBERME_CHECKBOX_XPATH)
            if not rememberMe.is_selected():
                rememberMe.click()
            # fill in username
            username = self.browser.find_element_by_xpath(USERNAME_XPATH).send_keys(username_)
            # fill in password and hit the login button 
            password = self.browser.find_element_by_xpath(PASSWORD_XPATH)
            password.send_keys(password_)
            password.send_keys(Keys.ENTER)
            try:
                WebDriverWait(self.browser, 120, poll_frequency=6).until(EC.visibility_of_element_located((By.CLASS_NAME, get_element_by_name("login")["class_name"])))
                print("OnlyFans Login Successful")
                return True
            except TimeoutException as te:
                settings.devPrint(te)
                print("Login Failure: Timed Out! Please check your Twitter credentials.")
                print(": If the problem persists, OnlySnarf may require an update.")
            except Exception as e:
                error_checker(e)
                print("Login Failure: OnlySnarf may require an update")
            return False
        except Exception as e:
            error_checker(e)
            print("OnlyFans Login Failed")
            return False

    ####################
    ##### Messages #####
    ####################
     
    def message_confirm(self):
        try:
            WAIT = WebDriverWait(self.browser, 120, poll_frequency=30)
            i = 0
            while True:
                try:                
                    WAIT.until(EC.element_to_be_clickable((By.CLASS_NAME, MESSAGE_CONFIRM)))
                    break
                except Exception as e:
                    print('uploading...')
                    error_checker(e)
                    i += 1
                    if i == int(settings.UPLOAD_MAX_DURATION) and settings.FORCE_UPLOAD is not True:
                        print('Error: Max Upload Time Reached')
                        return False
            confirm = self.get_element_to_click("confirm")
            # confirm = WebDriverWait(self.browser, 60, poll_frequency=10).until(EC.element_to_be_clickable((By.CLASS_NAME, MESSAGE_CONFIRM)))
            if str(settings.DEBUG) == "True":
                if str(settings.DEBUG_DELAY) == "True":
                    time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
                print('OnlyFans Message: Skipped (debug)')
                return True
            confirm.click()
            print('OnlyFans Message: Sent')
            return True
        except Exception as e:
            error_checker(e)
            print("Error: Failure to Confirm Message")
            return False

    def message_text(self, text):
        try:
            if not text or text == None or str(text) == "None":
                print("Error: Missing Text")
                return False
            print("Enter text: {}".format(text))
            message = self.browser.find_element_by_css_selector(MESSAGE_INPUT_CLASS)        
            message.send_keys(str(text))
            settings.maybePrint("Text Entered")
            return True
        except Exception as e:
            error_checker(e)
            print("Error: Failure to Enter Message")
            return False

    def message_image(self, path):
        try:
            if not path or path == None or str(path) == "None":
                print("Error: Missing Image(s)")
                return False
            print("Enter image(s): {}".format(path))
            try:
                self.upload_image_files(name="confirm", path=path)
                settings.maybePrint("Image(s) Entered")
                settings.debug_delay_check()
                return True
            except Exception as e:
                error_checker(e)
                print("Error: Unable to Upload Images")
                return False
        except Exception as e:
            error_checker(e)
            print("Error: Failure to Enter Image(s)")
            return False

    def message_price(self, price):
        try:
            if not price or price == None or str(price) == "None":
                print("Error: Missing Price")
                return False
            print("Enter price: {}".format(price))
            WAIT = WebDriverWait(self.browser, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ONLYFANS_PRICE))).click()
            # self.browser.find_element_by_css_selector(ONLYFANS_PRICE)
            settings.devPrint("entering price")
            eles = self.browser.find_elements_by_css_selector(ONLYFANS_PRICE_INPUT)
            print(len(eles))
            self.browser.find_elements_by_css_selector(ONLYFANS_PRICE_INPUT)[1].send_keys(str(price))
            price = get_element_by_name("priceEnter")
            print(price)
            print(price.get_attribute("innerHTML"))
            settings.devPrint("saving price")
            submits = self.browser.find_elements_by_css_selector(ONLYFANS_PRICE_CLICK)
            found = False
            for submit in submits:
                # print(submit.get_attribute("innerHTML"))
                # print(submit.is_enabled())
                if submit.get_attribute("innerHTML").strip() == "Save" and submit.is_enabled():
                    submit.click()
                    settings.maybePrint("Price Entered")
                    found = True
                    settings.devPrint("saved price")
                    break
            settings.debug_delay_check()
            if not found:
                print("Warning: Unable to Enter Price")
                return False
            return True
        except Exception as e:
            error_checker(e)
            print("Error: Failure to Enter Price")
            return False

    def message_user(self, user):
        try:
            auth_ = self.auth()
            if not auth_: return False
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
            self.browser.get("{}/{}".format(ONLYFANS_CHAT_URL,userid))
            return True
        except Exception as e:
            error_checker(e)
            print("Error: Failure to Goto User - {}/{}".format(user.id, user.username))
            return False

    def read_user_messages(self, user):
        try:
            auth_ = self.auth()
            if not auth_: return False
            # go to onlyfans.com/my/subscribers/active
            self.message_user(user)
            messages_from_ = self.browser.find_elements_by_class_name(ONLYFANS_MESSAGES_FROM)
            # print("first message: {}".format(messages_to_[0].get_attribute("innerHTML")))
            # messages_to_.pop(0) # drop self user at top of page
            messages_all_ = self.browser.find_elements_by_class_name(ONLYFANS_MESSAGES_ALL)
            messages_all = []
            messages_to = []
            messages_from = []
            # timestamps_ = self.browser.find_elements_by_class_name("b-chat__message__time")
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
            error_checker(e)
            print("Error: Failure to Read Chat - {}".format(user.username))
            return [[],[],[]]

    # update chat logs for all users
    def update_chat_logs(self):
        global USER_CACHE_LOCKED
        USER_CACHE_LOCKED = True
        print("Updating User Chats")
        users = self.get_users()
        for user in users:
            self.update_chat_log(user)
        USER_CACHE_LOCKED = False

    def update_chat_log(self, user):
        print("Updating Chat: {} - {}".format(user.username, user.id))
        if not user:
            return print("Error: Missing User")
        user.readChat()

    ################
    ##### Poll #####
    ################

    def polling(self, poll):
        settings.devPrint("polling")
        period = poll.get("period")
        questions = poll.get("questions")
        if isinstance(questions, str): questions = questions.split(",\"*\"")
        questions = [n.strip() for n in questions]
        auth_ = self.auth()
        if not auth_: return False
        if int(period) != 1 and int(period) != 3 and int(period) != 7 and int(period) != 30 and int(period) != 99 and str(period) != "No limit":
            print("Error: Missing Duration")
            return False
        if not questions or len(questions) == 0:
            print("Error: Missing Questions")
            return False
        try:
            print("Poll:")
            print("- Duration: {}".format(period))
            print("- Questions:\n> {}".format("\n> ".join(questions)))
            # make sure the extra options are shown
            try:
                settings.devPrint("opening options")
                self.get_element_to_click("moreOptions").click()
            except Exception as e:
                pass
            # add a poll
            settings.devPrint("adding poll")
            self.get_element_to_click("poll").click()
            # open the poll duration
            settings.devPrint("adding duration")
            self.get_element_to_click("pollDuration").click()
            # click on the correct duration number
            settings.devPrint("setting duration")
            nums = self.browser.find_elements_by_class_name(get_element_by_name("pollDurations")["class_name"])
            for num in nums:
                inner = num.get_attribute("innerHTML")
                ##
                # <span class="g-first-letter">1</span> day
                # <span class="g-first-letter">3</span> days
                # <span class="g-first-letter">7</span> days
                # <span class="g-first-letter">30</span> days
                # <span><span class="g-first-letter">N</span>o limit</span>
                ##
                if ">1<" in str(inner) and int(period) == 1: num.click()
                if ">3<" in str(inner) and int(period) == 3: num.click()
                if ">7<" in str(inner) and int(period) == 7: num.click()
                if ">30<" in str(inner) and int(period) == 30: num.click()
                if ">o limit<" in str(inner) and int(period) == 99: num.click()
            # save the duration
            settings.devPrint("### this is not working ###")
            settings.devPrint("saving duration")
            save = self.get_element_to_click("pollSave").click()
            settings.devPrint("saved duration")
            # add extra question space
            if len(questions) > 2:
                for question in questions[2:]:
                    settings.devPrint("adding question")
                    question_ = self.get_element_to_click("pollQuestionAdd").click()
                    settings.devPrint("added question")
            # find the question inputs
            settings.devPrint("locating question paths")
            questions_ = self.browser.find_elements_by_xpath(POLL_INPUT_XPATH)
            settings.devPrint("question paths: {}".format(len(questions_)))
            # enter the questions
            i = 0
            # print("questions: {}".format(questions))
            for question in list(questions):
                settings.devPrint("entering question: {}".format(question))
                questions_[i].send_keys(str(question))
                settings.devPrint("entered question")
                time.sleep(1)
                i+=1
            settings.debug_delay_check()
            if str(settings.DEBUG) == "True":
                print("Skipping Poll (debug)")
                cancel = self.get_element_to_click("pollCancel")
                cancel.click()
                settings.devPrint("canceled poll")
            else:
                print("Poll Entered")
            return True
        except Exception as e:
            error_checker(e)
            print("Error: Failed to enter Poll")
            return False

    ################
    ##### Post #####
    ################

    def post(self, text, expires=None, schedule=False, poll=False):
        try:
            auth_ = self.auth()
            if not auth_: return False
            self.go_to_home()
            print("Posting:")
            print("- Text: {}".format(text))
            if expires: self.expiration(expires)
            if schedule: self.scheduling(schedule)
            if poll: self.polling(poll)
            settings.devPrint("entering text")
            self.browser.find_element_by_id(ONLYFANS_POST_TEXT_ID).send_keys(str(text))
            settings.devPrint("entered text")
            settings.devPrint("finding send")
            # sends = self.browser.find_elements_by_class_name(SEND_BUTTON_CLASS)
            # for i in range(len(sends)):
                # if sends[i].is_enabled():
                    # sends = sends[i]
                    # settings.devPrint("found send")
            send = self.get_element_to_click("post")
            print("send btn: {}".format(send))
            settings.debug_delay_check()
            if str(settings.DEBUG) == "True":
                print('Skipped: OnlyFans Post (debug)')
                return True
            settings.devPrint("sending post")
            send.click()
            # send[1].click() # the 0th one is disabled
            print('OnlyFans Post Complete')
            return True
        except Exception as e:
            error_checker(e)
            print("Error: OnlyFans Post Failure")
            return False

    ######################
    ##### Promotions #####
    ######################

    # or email
    def get_new_trial_link(self):
        auth_ = self.auth()
        if not auth_: return False
        # go to onlyfans.com/my/subscribers/active
        try:
            settings.maybePrint("goto -> /my/promotions")
            self.browser.get(('https://onlyfans.com/my/promotions'))
            trial = self.browser.find_elements_by_class_name("g-btn.m-rounded.m-sm")[0].click()
            create = self.browser.find_elements_by_class_name("g-btn.m-rounded")
            for i in range(len(create)):
                if create[i].get_attribute("innerHTML").strip() == "Create":
                    create[i].click()
                    break

            # copy to clipboard? email to user by email?
            # count number of links
            # div class="b-users__item.m-fans"
            trials = self.browser.find_elements_by_class_name("b-users__item.m-fans")
            # print("trials")
            # find last one in list of trial link buttons
            # button class="g-btn m-sm m-rounded" Copy trial link
            # trials = self.browser.find_elements_by_class_name("g-btn.m-sm.m-rounded")
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
            error_checker(e)
            print("Error: Failed to Apply Promotion")
            return None

    #################
    ##### Reset #####
    #################

    # Reset to home
    def reset(self):
        if not self.browser or self.browser == None:
            print('OnlyFans Not Open, Skipping Reset')
            return True
        try:
            self.browser.get(ONLYFANS_HOME_URL)
            print('OnlyFans Reset')
            return True
        except Exception as e:
            error_checker(e)
            print('Error: Failure Resetting OnlyFans')
            return False

    ####################
    ##### Settings #####
    ####################

    # onlyfans.com/my/settings
    def go_to_settings(self, settingsTab):
        if self.browser == None: return False
        if str(self.browser.current_url) == str(ONLYFANS_SETTINGS_URL) and str(settingsTab) == "profile":
            settings.maybePrint("at -> onlyfans.com/settings/{}".format(settingsTab))
        else:
            settings.maybePrint("goto -> onlyfans.com/settings/{}".format(settingsTab))
            self.browser.get("{}/{}".format(ONLYFANS_SETTINGS_URL, settingsTab))
            # WebDriverWait(self.browser, 60, poll_frequency=6).until(EC.visibility_of_element_located((By.XPATH, SEND_BUTTON_XPATH)))
            # fix above with correct element to locate

    def settings_get(self, key):
         # find the var from the list of var names in settingsVariables
        var = None
        settingsVariables = settings.get_settings_variables()
        for key in settingsVariables:
            if str(var) == str(key[0]):
                var = key
        if not var or var == None:
            print("Error: Unable to Find Variable")
            return False
        #
        key_ = var[0]
        page_ = var[1]
        class_ = var[2]
        type_ = var[3]
        self.go_to_settings(page_)
        self.find_element_by_name(class_)
        if str(type_) == "text":
            # get attr text
            pass
        elif str(type_) == "toggle":
            # get state true|false
            pass
        # other stuff
        settings_save()

    def settings_set(self, key, value):
        # find the var from the list of var names in settingsVariables
        var = None
        settingsVariables = settings.get_settings_variables()
        for key in settingsVariables:
            if str(var) == str(key[0]):
                var = key
        if not var or var == None:
            print("Error: Unable to Find Variable")
            return False
        #
        key_ = var[0]
        page_ = var[1]
        class_ = var[2]
        type_ = var[3]
        self.go_to_settings(page_)
        self.find_element_by_name(class_)
        # text, path, state, list (text), price 
        if str(type_) == "text":
            # set attr text
            pass
        elif str(type_) == "toggle":
            # set state == value
            pass
        # other stuff
        settings_save()

    # saves the settings page
    def settings_save(self):
        pass

    ####################
    ##### Schedule #####
    ####################

    def scheduling(self, schedule_):
        auth_ = self.auth()
        if not auth_: return False
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
                self.get_element_to_click("moreOptions").click()
            except Exception as e:
                pass
            # click schedule
            settings.devPrint("adding schedule")
            self.browser.find_element_by_class_name(SCHEDULE).click()
            searching = True
            while searching:
                settings.devPrint("getting date")
                existingDate = self.browser.find_element_by_class_name(SCHEDULE_EXISTING_DATE).get_attribute("innerHTML")
                if str(month_) in str(existingDate) and str(year_) in str(existingDate):
                    searching = False
                else:
                    self.browser.find_element_by_class_name(SCHEDULE_NEXT_MONTH).click()
            settings.devPrint("setting days")
            days = self.browser.find_elements_by_class_name(SCHEDULE_DAYS)
            for day in days:
                inner = day.get_attribute("innerHTML").replace("<span><span>","").replace("</span></span>","")
                if str(day_) == str(inner):
                    day.click()
                    settings.devPrint("clicked day")
            settings.debug_delay_check()
            saves = self.browser.find_elements_by_class_name(SCHEDULE_SAVE)
            for save in saves:
                if "Save" in str(save.get_attribute("innerHTML")):
                    save.click()
                    settings.devPrint("clicked save")
                    break
            settings.devPrint("setting hours")
            hours = self.browser.find_elements_by_class_name(SCHEDULE_HOURS)
            for hour in hours:
                inner = hour.get_attribute("innerHTML")
                if str(hour_) in str(inner) and hour.is_enabled():
                    hour.click()
                    settings.devPrint("hours set")
            settings.devPrint("setting minutes")
            minutes = self.browser.find_elements_by_class_name(SCHEDULE_MINUTES)
            for minute in minutes:
                inner = minute.get_attribute("innerHTML")
                if str(minute_) in str(inner) and minute.is_enabled():
                    minute.click()
                    settings.devPrint("minutes set")
            # if str(settings.DEBUG) == "True":
                # print("Skipping Schedule (debug)")
                # cancel = self.browser.find_element_by_class_name(EXPIRATION_CANCEL)
                # cancel.click() # its the first cancel button
            # else:

            # self.get_element_to_click("saveSchedule").click()
            settings.devPrint("saving schedule")
            saves = self.browser.find_elements_by_class_name(SCHEDULE_SAVE)
            settings.devPrint("saves: {}".format(len(saves)))
            for save in saves:
                settings.devPrint("save: {}".format(save.get_attribute("innerHTML")))
                settings.devPrint("enabled: {}".format(save.is_enabled()))
                if "Save" in str(save.get_attribute("innerHTML")) and save.is_enabled():
                    save.click()
                    settings.devPrint("schedule saved")
                    break
            print("Schedule Entered")
            return True
        except Exception as e:
            error_checker(e)
            print("Error: Failed to enter Schedule")
            return False

    ##################
    ##### Upload #####
    ##################

    # Uploads a directory with a video file or image files to OnlyFans
    def upload(self, path=None, text="", keywords=[], performers=[], expires=False, schedule=False, poll=False):
        settings.devPrint("uploading")
        try:
            auth_ = self.auth()
            if not auth_: return False
            self.go_to_home()
            if not path:
                print("Error: Missing Upload Path")
                return False
            if not text or text == None or str(text) == "None":
                print("Warning: Missing Upload Text")
                text = ""
            text = text.replace(".mp4","").replace(".MP4","").replace(".jpg","").replace(".jpeg","")
            if isinstance(performers, list) and len(performers) > 0: text += " w/ @"+" @".join(performers)
            if isinstance(keywords, list) and len(keywords) > 0: text += " #"+" #".join(keywords)
            text = text.strip()
            print("Uploading:")
            settings.maybePrint("- Path: {}".format(path))
            print("- Keywords: {}".format(keywords))
            print("- Performers: {}".format(performers))
            print("- Text: {}".format(text))
            print("- Tweeting: {}".format(settings.TWEETING))
            ## Expires, Schedule, Poll
            if expires: self.expiration(expires)
            if schedule: self.scheduling(schedule)
            if poll: 
                self.polling(poll)
                time.sleep(3)
            WAIT = WebDriverWait(self.browser, 600, poll_frequency=10)
            ## Tweeting
            if str(settings.TWEETING) == "True":
                settings.devPrint("tweeting")
                WAIT.until(EC.element_to_be_clickable((By.XPATH, ONLYFANS_TWEET))).click()
            else:
                settings.devPrint("not tweeting")
            ## Text
            successful_text = self.enter_text(text)
            if not successful_text:
                print("Error: Unable to Enter Text")
                return False
            ## Images
            try:
                settings.devPrint("uploading files")
                successful_upload = self.upload_image_files("uploadImage", path)
            except Exception as e:
                error_checker(e)
                print("Error: Unable to Upload Images")
                return False
            ## Confirm
            try:
                send = self.get_element_to_click("post")
                if send:
                    if str(settings.DEBUG) == "True" and str(settings.DEBUG_DELAY) == "True":
                        time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
                    if str(settings.DEBUG) == "True":
                        print('Skipped: OnlyFans Upload (debug)')
                        return True
                    settings.devPrint("confirming upload")
                    send.click()
                else:
                    settings.maybePrint("Error: Unable to locate 'Send Post' button")
                    return False
            except Exception as e:
                print("Error: Unable to Send Post")
                settings.maybePrint(e)
                return False
            # send[1].click() # the 0th one is disabled
            print('OnlyFans Upload Complete')
            return True
        except Exception as e:
            error_checker(e)
            print("Error: OnlyFans Upload Failure")
            return False

    #################
    ##### Users #####
    #################

    def get_users(self):
        auth_ = self.auth()
        if not auth_: return False
        try:
            if str(self.browser.current_url) == str(ONLYFANS_USERS_ACTIVE_URL):
                settings.maybePrint("at -> /my/subscribers/active")
            else:
                settings.maybePrint("goto -> /my/subscribers/active")
                self.browser.get(ONLYFANS_USERS_ACTIVE_URL)
                num = self.browser.find_element_by_class_name(ONLYFANS_USER_COUNT).get_attribute("innerHTML")
                settings.maybePrint("User count: {}".format(num))
                for n in range(int(int(int(num)/10)+1)):
                    settings.maybePrint("scrolling...")
                    self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
        except Exception as e:
            error_checker(e)
            print("Error: Failed to Find Users")
            return []
        # avatars = self.browser.find_elements_by_class_name('b-avatar')
        user_ids = self.browser.find_elements_by_css_selector(ONLYFANS_USERS_IDS)
        starteds = self.browser.find_elements_by_class_name(ONLYFANS_USERS_STARTEDS)
        # users = self.browser.find_elements_by_class_name('g-user-name')
        users = self.browser.find_elements_by_class_name(ONLYFANS_USERS)
        usernames = self.browser.find_elements_by_class_name(ONLYFANS_USERSNAMES)
        # usernames.pop(0)
        # print("My User Id: {}".format(user_ids[0]))
        # user_ids.pop(0)
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
            settings.maybePrint("users vs ids vs starteds vs usernames:"+str(len(users))+" - "+str(len(user_ids_))+" - "+str(len(starteds_))+" - "+str(len(usernames)))
            # first 2 usernames are self
            usernames.pop(0)
            usernames.pop(0)
            for i in range(len(users)): # the first is you and doesn't count towards total
                try:
                    if not startedsFailed:
                        start = starteds_[i]
                    else:
                        start = datetime.now().strftime("%b %d, %Y")
                    if not useridsFailed:
                        user_id = user_ids_[i][35:] # cuts out initial chars instead of unwieldy regex
                    else:
                        user_id = None
                    name = users[i]
                    username = usernames[i]
                    name = str(name.get_attribute("innerHTML")).strip()
                    username = str(username.get_attribute("innerHTML")).strip()
                    # settings.maybePrint("name: "+str(name))
                    # settings.maybePrint("username: "+str(username))
                    # settings.maybePrint("user_id: "+str(user_id))
                    # if str(settings.USERNAME).lower() in str(username).lower():
                    #     settings.maybePrint("(self): %s = %s" % (settings.USERNAME, username))
                    #     # first user is always active user but just in case find it in list of users
                    #     settings.USER_ID = username
                    # else:
                    users_.append({"name":name, "username":username, "id":user_id, "started":start})
                except Exception as e:
                    settings.maybePrint(e)
        except Exception as e:
            error_checker(e)
        settings.maybePrint("Found: {}".format(len(users_)))
        return users_

    ################
    ##### Exit #####
    ################

    def exit(self):
        if str(settings.SAVE_USERS) == "True":
            print("Saving and Exiting OnlyFans")
            write_users_local()
        else:
            print("Exiting OnlyFans")
        
        if self.browser:
            self.browser.quit()
        self.browser = None
        print("Browser Closed")
        global logged_in
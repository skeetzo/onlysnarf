#!/usr/bin/python3
# 3/28/2019: Skeetzo
import re
import random
import os
import shutil
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
from OnlySnarf.colorize import colorize
from OnlySnarf.settings import SETTINGS as settings
from OnlySnarf.element import Element
from OnlySnarf.profile import Profile

###################
##### Globals #####
###################
BROWSER = None
LOGGED_IN = False

# Urls
ONLYFANS_HOME_URL = 'https://onlyfans.com'
ONLYFANS_MESSAGES_URL = "/my/chats/"
ONLYFANS_NEW_MESSAGE_URL = "/my/chats/send"
ONLYFANS_CHAT_URL = "/my/chats/chat"
ONLYFANS_SETTINGS_URL = "/my/settings"
ONLYFANS_USERS_ACTIVE_URL = "/my/subscribers/active"
ONLYFANS_USERS_FOLLOWING_URL = "/my/subscriptions/active"
#
LOGIN_FORM = "b-loginreg__form"
SEND_BUTTON_XPATH = "//button[@type='submit' and @class='g-btn m-rounded']"
SEND_BUTTON_CLASS = "g-btn.m-rounded"
SEND_BUTTON_CLASS2 = "button.g-btn.m-rounded"
# Login References
LIVE_BUTTON_CLASS = "b-make-post__streaming-link"
TWITTER_LOGIN0 = "//a[@class='g-btn m-rounded m-flex m-lg']"
TWITTER_LOGIN1 = "//a[@class='g-btn m-rounded m-flex m-lg btn-twitter']"
TWITTER_LOGIN2 = "//a[@class='btn btn-default btn-block btn-lg btn-twitter']"
TWITTER_LOGIN3 = "//a[@class='g-btn m-rounded m-flex m-lg m-with-icon']"
USERNAME_XPATH = "//input[@id='username_or_email']"
PASSWORD_XPATH = "//input[@id='password']"
# IDs and xpaths not yet required fancy element sorting
ONLYFANS_POST_TEXT_ID = "new_post_text_input"
ONLYFANS_MESSAGES = "b-chat__message__text"
MESSAGE_CONFIRM = "g-btn.m-rounded.b-chat__btn-submit"
DISCOUNT_INPUT = "form-control.b-fans__trial__select"
ONLYFANS_TWEET = "//label[@for='new_post_tweet_send']"
ONLYFANS_PRICE2 = "button.b-chat__btn-set-price"
POLL_INPUT_XPATH = "//input[@class='form-control']"
REMEMBERME_CHECKBOX_XPATH = "//input[@id='remember']"
DISCOUNT_USER_BUTTONS = "g-btn.m-rounded.m-border.m-sm"

def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()

class Driver:

    def __init__():
        # BROWSER = None

    @staticmethod
    def auth():
        spawned = Driver.check_spawn()
        if not spawned: return False
        logged_in = False
        global LOGGED_IN
        if not LOGGED_IN or LOGGED_IN == None:
            logged_in = self.login()
        else: logged_in = True
        if logged_in == False: print("Error: Failure to Login")
        LOGGED_IN = logged_in
        return logged_in

    @staticmethod
    def check_spawn():
        global BROWSER
        spawned = False
        if not BROWSER or BROWSER == None:
            spawned = Driver.spawn_browser()
        else: spawned = True
        if spawned == False: print("Error: Failure to Spawn Browser")
        return spawned

    ####################
    ##### Discount #####
    ####################

    @staticmethod
    def discount_user(user, discount=10, months=1):
        auth_ = Driver.auth()
        if not auth_: return False
        if int(expiration) > int(settings.DISCOuNT_MAX_AMOUNT):
            print("Warning: Discount Too High, Max -> {}%".format(settings.DISCOuNT_MAX_AMOUNT))
            discount = settings.DISCOuNT_MAX_AMOUNT
        elif int(expiration) > int(settings.DISCOuNT_MIN_AMOUNT):
            print("Warning: Discount Too Low, Min -> {}%".format(settings.DISCOuNT_MIN_AMOUNT))
            discount = settings.DISCOuNT_MIN_AMOUNT
        if int(months) > int(settings.DISCOUNT_MAX_MONTHS):
            print("Warning: Duration Too High, Max -> {} days".format(settings.DISCOUNT_MAX_MONTHS))
            months = settings.DISCOUNT_MAX_MONTHS
        elif int(months) < int(settings.DISCOUNT_MIN_MONTHS):
            print("Warning: Duration Too Low, Min -> {} days".format(settings.DISCOUNT_MIN_MONTHS))
            months = settings.DISCOUNT_MIN_MONTHS
        try:
            print("Discounting User: {}".format(user))
            Driver.go_to_page(ONLYFANS_USERS_ACTIVE_URL)
            end_ = True
            count = 0
            while end_:
                elements = BROWSER.find_elements_by_class_name("m-fans")
                for ele in elements:
                    username = ele.find_element_by_class_name("g-user-username").get_attribute("innerHTML").strip()
                    if str(user) == str(username): 
                        BROWSER.execute_script("arguments[0].scrollIntoView();", ele)
                        end_ = False
                if not end_: continue
                if len(elements) == int(count): break
                print_same_line("({}/{}) scrolling...".format(count, len(elements)))
                count = len(elements)
                BROWSER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            print()
            users = Driver.find_elements_by_name("discountUsers")
            if int(len(users)) == 0:
                print("Error: Missing Users")
                return False
            # get all the users
            settings.devPrint("finding user")
            user__ = None
            for user_ in users:
                text = user_.get_attribute("innerHTML")
                # settings.devPrint("user text: {}".format(text))
                if str(user) in text:
                    user__ = user_
                    settings.devPrint("found user: {} - {}".format(user__, user_))
                    break
            if user__ == None:
                print("Warning: Unable to Find User")
                return False
            ActionChains(BROWSER).move_to_element(user__).perform()
            settings.devPrint("moved to user")
            settings.devPrint("finding discount btn")
            buttons = user__.find_elements_by_class_name(DISCOUNT_USER_BUTTONS)
            for button in buttons:
                if "Discount" in button.get_attribute("innerHTML") and button.is_enabled() and button.is_displayed():
                    try:
                        settings.devPrint("clicking discount btn")
                        button.click()
                        settings.devPrint("clicked discount btn")
                        break
                    except Exception as e:
                        Driver.error_checker(e)
                        print("Warning: Unable To Find User, retrying")
                        return Driver.discount_user(user, discount=discount, months=months)
            time.sleep(1)
            settings.devPrint("finding months and discount amount btns")
            (months_, discount_) = BROWSER.find_elements_by_class_name(DISCOUNT_INPUT)
            settings.devPrint("found months and discount amount")
            # removed in 2.10, inputs changed to above
            # months_ = BROWSER.find_element_by_class_name(MONTHS_INPUT)
            # if discount_.get_attribute("value") != "":
                # print("Warning: Existing Discount")
            # discount_.clear()
            settings.devPrint("entering discount amount")
            for n in range(11):
                discount_.send_keys(str(Keys.UP))
            for n in range(round(int(discount)/5)-1):
                discount_.send_keys(Keys.DOWN)
            settings.devPrint("entered discount amount")
            settings.devPrint("entering discount months")
            for n in range(11):
                months_.send_keys(str(Keys.UP))
            for n in range(int(months)-1):
                months_.send_keys(Keys.DOWN)
            settings.devPrint("entered discount months")
            settings.debug_delay_check()
            settings.devPrint("applying discount")
            buttons_ = Driver.find_elements_by_name("discountUserButton")
            for button in buttons_:
                if not button.is_enabled() and not button.is_displayed(): continue
                if "Cancel" in button.get_attribute("innerHTML") and str(settings.DEBUG) == "True" and str(settings.DEBUG_FORCE) == "False":
                    button.click()
                    print("Skipping: Save Discount (Debug)")
                    settings.devPrint("### Discount Successfully Canceled ###")
                    return True
                elif "Apply" in button.get_attribute("innerHTML"):
                    button.click()
                    print("Discounted User: {}".format(user))
                    settings.devPrint("### Discount Successful ###")
                    return True
            settings.devPrint("### Discount Failure ###")
        except Exception as e:
            print(e)
            Driver.error_checker(e)
            buttons_ = Driver.find_elements_by_name("discountUserButtons")
            for button in buttons_:
                if "Cancel" in button.get_attribute("innerHTML"):
                    button.click()
                    settings.devPrint("### Discount Successful Failure ###")
                    return False
            settings.devPrint("### Discount Failure ###")
            return False

    @staticmethod
    def enter_text(text):
        try:
            settings.devPrint("finding text")
            sendText = BROWSER.find_element_by_id(ONLYFANS_POST_TEXT_ID)
            settings.devPrint("found text")
            sendText.clear()
            settings.devPrint("sending text")
            sendText.send_keys(str(text))
            return True
        except Exception as e:
            settings.maybePrint(e)
            return False

    @staticmethod
    def error_checker(e):
        if "Unable to locate element" in str(e):
            print("Warning: OnlySnarf may require an update")
        if "Message: " in str(e): return
        if str(settings.VERBOSER) == "True":
            print(e)
        else:
            settings.maybePrint(e)

    @staticmethod
    def error_window_upload():
        try:
            element = Element.get_element_by_name("errorUpload")
            error_buttons = BROWSER.find_elements_by_class_name(element.getClass())
            settings.devPrint("errors btns: {}".format(len(error_buttons)))
            for butt in error_buttons:
                if butt.get_attribute("innerHTML").strip() == "Close" and butt.is_enabled():
                    settings.maybePrint("Warning: Upload Error Message, Closing")
                    butt.click()
                    settings.maybePrint("Success: Upload Error Message Closed")
                    return True
            return False
        except Exception as e:
            Driver.error_checker(e)
            return False

    ######################
    ##### Expiration #####
    ######################

    @staticmethod
    def expires(period):
        settings.devPrint("expires")
        if period == None or str(period) == "": return False
        if int(period) != 1 and int(period) != 3 and int(period) != 7 and int(period) != 30 and int(period) != 99 and str(period) != "No limit":
            print("Error: Missing Expiration")
            return False
        auth_ = Driver.auth()
        if not auth_: return False
        try:
            # go_to_home() # this should be run only from upload anyways
            if isinstance(period,str) and str(period) == "No limit": period = 99
            print("Expiration:")
            print("- Period: {}".format(period))
            Driver.open_more_options()
            # open expires window
            settings.devPrint("adding expires")
            Driver.get_element_to_click("expiresAdd").click()
            # select duration
            settings.devPrint("selecting expires")
            nums = Driver.find_elements_by_name("expiresPeriods")
            for num in nums:
                ##
                # <span class="g-first-letter">1</span> day
                # <span class="g-first-letter">3</span> days
                # <span class="g-first-letter">7</span> days
                # <span class="g-first-letter">30</span> days
                # <span><span class="g-first-letter">N</span>o limit</span>
                ##
                inner = num.get_attribute("innerHTML")
                if ">1<" in str(inner) and int(period) == 1: num.click()
                if ">3<" in str(inner) and int(period) == 3: num.click()
                if ">7<" in str(inner) and int(period) == 7: num.click()
                if ">30<" in str(inner) and int(period) == 30: num.click()
                if ">o limit<" in str(inner) and int(period) == 99: num.click()
            settings.devPrint("selected expires")
            settings.debug_delay_check()
            # save
            if str(settings.DEBUG) == "True" and str(settings.DEBUG_FORCE) == "False":
                print("Skipping: Expiration (debug)")
                settings.devPrint("skipping expires")
                Driver.get_element_to_click("expiresCancel").click()
                settings.devPrint("canceled expires")
                settings.devPrint("### Expiration Successfully Canceled ###")
            else:
                settings.devPrint("saving expires")
                Driver.get_element_to_click("expiresSave").click()
                settings.devPrint("saved expires")
                print("Expiration Entered")
                settings.devPrint("### Expiration Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failed to Enter Expiration")
            try:
                settings.devPrint("canceling expires")
                Driver.get_element_to_click("expiresCancel").click()
                settings.devPrint("canceled expires")
                settings.devPrint("### Expiration Successful Failure ###")
            except: 
                settings.devPrint("### Expiration Failure Failure")
            return False

    ######################################################################

    # should already be logged in
    @staticmethod
    def find_element_by_name(name):
        if BROWSER == None: return False
        element = Element.get_element_by_name(name)
        if not element:
            print("Error: Unable to find Element Reference")
            return False
        # prioritize id over class name
        eleID = None
        try: eleID = BROWSER.find_element_by_id(element.getId())
        except: eleID = None
        if eleID: return eleID
        for className in element.getClasses():
            ele = None
            eleCSS = None
            try: ele = BROWSER.find_element_by_class_name(className)
            except: ele = None
            try: eleCSS = BROWSER.find_element_by_css_selector(className)
            except: eleCSS = None
            settings.devPrint("class: {} - {}:css".format(ele, eleCSS))
            if ele: return ele
            if eleCSS: return eleCSS
        raise Exception("Error: Unable to Locate Element")

    @staticmethod
    def find_elements_by_name(name):
        if BROWSER == None: return False
        element = Element.get_element_by_name(name)
        if not element:
            print("Error: Unable to find Element Reference")
            return False
        eles = []
        for className in element.getClasses():
            eles_ = []
            elesCSS_ = []
            try: eles_ = BROWSER.find_elements_by_class_name(className)
            except: eles_ = []
            try: elesCSS_ = BROWSER.find_elements_by_css_selector(className)
            except: elesCSS_ = []
            settings.devPrint("class: {} - {}:css".format(len(eles_), len(elesCSS_)))
            eles.extend(eles_)
            eles.extend(elesCSS_)
        eles_ = []
        for i in range(len(eles)):
            # settings.devPrint("ele: {} -> {}".format(eles[i].get_attribute("innerHTML").strip(), element.getText()))
            if eles[i].is_displayed():
                settings.devPrint("found displayed ele: {}".format(eles[i].get_attribute("innerHTML").strip()))
                eles_.append(eles[i])
        if len(eles_) == 0:
            raise Exception("Error: Unable to Locate Elements")
        return eles_

    @staticmethod
    def get_element_to_click(name):
        settings.devPrint("finding click: {}".format(name))
        element = Element.get_element_by_name(name)
        if not element:
            print("Error: Unable to find Element Reference")
            return False
        for className in element.getClasses():
            eles = []
            elesCSS = []
            try: eles = BROWSER.find_elements_by_class_name(className)
            except: eles = []
            try: elesCSS = BROWSER.find_elements_by_css_selector(className)
            except: elesCSS = []
            settings.devPrint("class: {} - {}:css".format(len(eles), len(elesCSS)))
            eles.extend(elesCSS)
            for i in range(len(eles)):
                # settings.devPrint("ele: {} -> {}".format(eles[i].get_attribute("innerHTML").strip(), element.getText()))
                if (eles[i].is_displayed() and element.getText() and str(element.getText().lower()) == eles[i].get_attribute("innerHTML").strip().lower()) and eles[i].is_enabled():
                    settings.devPrint("found matching ele")
                    # settings.devPrint("found matching ele: {}".format(eles[i].get_attribute("innerHTML").strip()))
                    return eles[i]
                elif (eles[i].is_displayed() and element.getText() and str(element.getText().lower()) == eles[i].get_attribute("innerHTML").strip().lower()):
                    settings.devPrint("found text ele")
                    # settings.devPrint("found text ele: {}".format(eles[i].get_attribute("innerHTML").strip()))
                    return eles[i]
                elif eles[i].is_displayed() and not element.getText() and eles[i].is_enabled():
                    settings.devPrint("found enabled ele")
                    # settings.devPrint("found enabled ele: {}".format(eles[i].get_attribute("innerHTML").strip()))
                    return eles[i]
            if len(eles) > 0: return eles[0]
            settings.devPrint("unable to find element - {}".format(className))
        raise Exception("Error Locating Element")

    ######################################################################

    @staticmethod
    def go_to_page(page):
        auth_ = Driver.auth()
        if not auth_: return False
        if str(BROWSER.current_url) == str(page) or str(page) in str(BROWSER.current_url):
            settings.maybePrint("at -> {}".format(page))
            BROWSER.execute_script("window.scrollTo(0, 0);")
        else:
            settings.maybePrint("goto -> {}".format(page))
            BROWSER.get("{}/{}".format(ONLYFANS_HOME_URL, page))

    @staticmethod
    def go_to_home():
        auth_ = Driver.auth()
        if not auth_: return False
        if str(BROWSER.current_url) == str(ONLYFANS_HOME_URL):
            settings.maybePrint("at -> onlyfans.com")
        else:
            settings.maybePrint("goto -> onlyfans.com")
            BROWSER.get(ONLYFANS_HOME_URL)
            WebDriverWait(BROWSER, 60, poll_frequency=6).until(EC.visibility_of_element_located((By.CLASS_NAME, LIVE_BUTTON_CLASS)))

    # onlyfans.com/my/settings
    @staticmethod
    def go_to_settings(settingsTab):
        auth_ = Driver.auth()
        if not auth_: return False
        if str(BROWSER.current_url) == str(ONLYFANS_SETTINGS_URL) and str(settingsTab) == "profile":
            settings.maybePrint("at -> onlyfans.com/settings/{}".format(settingsTab))
        else:
            if str(settingsTab) == "profile": settingsTab = ""
            settings.maybePrint("goto -> onlyfans.com/settings/{}".format(settingsTab))
            BROWSER.get("{}/{}".format(ONLYFANS_SETTINGS_URL, settingsTab))
            # fix above with correct element to locate

    ##################
    ###### Login #####
    ##################

    @staticmethod
    def login():
        print('Logging into OnlyFans')
        username_ = str(settings.USERNAME)
        password_ = str(settings.PASSWORD)
        if not username_ or username_ == "": username_ = input("Twitter Username: ")
        if not password_ or password_ == "": password_ = input("Twitter Password: ")
        if str(username_) == "" or str(password_) == "":
            print("Error: Missing Login Info")
            return False
        if str(settings.USERNAME) == "" or settings.USERNAME == None: settings.USERNAME = username_
        if str(settings.PASSWORD) == "" or settings.PASSWORD == None: settings.PASSWORD = password_
        try:
            BROWSER.get(ONLYFANS_HOME_URL)
            settings.devPrint("logging in")
            twitter = BROWSER.find_element_by_xpath(TWITTER_LOGIN3).click()
            settings.devPrint("twitter login clicked")
            # rememberMe checkbox doesn't actually cause login to be remembered
            # rememberMe = BROWSER.find_element_by_xpath(REMEMBERME_CHECKBOX_XPATH)
            # if not rememberMe.is_selected():
                # rememberMe.click()
            # if str(settings.MANUAL) == "True":
                # print("Please Login")
            [elem for elem in elements if '/twitter/auth' in str(elem.get_attribute('href'))][0].click()
            # twitter = self.driver.find_element_by_xpath("//a[@class='g-btn m-rounded m-flex m-lg m-with-icon']").click()    
            username = self.driver.find_element_by_xpath("//input[@id='username_or_email']").send_keys(username_)
            settings.devPrint("username entered")
            # fill in password and hit the login button 
            password = self.driver.find_element_by_xpath("//input[@id='password']")
            password.send_keys(self.password)
            settings.devPrint("password entered")
            password.send_keys(Keys.ENTER)
            try:
                settings.devPrint("waiting for loginCheck")
                WebDriverWait(BROWSER, 120, poll_frequency=6).until(EC.visibility_of_element_located((By.CLASS_NAME, Element.get_element_by_name("loginCheck").getClass())))
                print("OnlyFans Login Successful")
                return True
            except TimeoutException as te:
                settings.devPrint(str(te))
                print("Login Failure: Timed Out! Please check your Twitter credentials.")
                print(": If the problem persists, OnlySnarf may require an update.")
            except Exception as e:
                Driver.error_checker(e)
                print("Login Failure: OnlySnarf may require an update")
            return False
        except Exception as e:
            settings.devPrint("login failure")
            Driver.error_checker(e)
            print("OnlyFans Login Failed")
            return False

    ####################
    ##### Messages #####
    ####################

    @staticmethod
    def message(username):
        try:
            auth_ = Driver.auth()
            if not auth_: return False
            type__ = None # default
            if str(username) == "all": type__ = "messageAll"
            elif str(username) == "recent": type__ = "messageRecent"
            elif str(username) == "favorite": type__ = "messageFavorite"
            successful = False
            if type__ != None:
                Driver.go_to_page(ONLYFANS_NEW_MESSAGE_URL)
                settings.devPrint("clicking message type: {}".format(username))
                Driver.get_element_to_click(type__).click()
                successful = True
            else:
                successful = Driver.message_user(username)
            settings.devPrint("successfully started message: {}".format(username))
            return successful
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failure to Message All")
            return False
     
    @staticmethod
    def message_confirm():
        try:
            WAIT = WebDriverWait(BROWSER, 120, poll_frequency=30)
            i = 0
            settings.devPrint("waiting for message confirm to be clickable")
            while True:
                try:                
                    WAIT.until(EC.element_to_be_clickable((By.CLASS_NAME, MESSAGE_CONFIRM)))
                    settings.devPrint("message confirm is clickable")
                    break
                except Exception as e:
                    print('uploading...')
                    Driver.error_checker(e)
                    i += 1
                    if i == int(settings.UPLOAD_MAX_DURATION) and settings.FORCE_UPLOAD is not True:
                        print('Error: Max Upload Time Reached')
                        return False
            settings.devPrint("getting confirm to click")
            confirm = Driver.get_element_to_click("new_post")
            if str(settings.DEBUG) == "True":
                print('OnlyFans Message: Skipped (debug)')
                settings.devPrint("### Message Successful (debug) ###")
                settings.debug_delay_check()
                return True
            settings.devPrint("clicking confirm")
            confirm.click()
            print('OnlyFans Message: Sent')
            settings.devPrint("### Message Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failure to Confirm Message")
            settings.devPrint("### Message Failure ###")
            return False

    @staticmethod
    def message_files(path):
        try:
            if not path or path == None or str(path) == "None":
                print("Error: Missing File(s)")
                return False
            print("Entering image(s): {}".format(path))
            try:
                settings.devPrint("uploading file")
                Driver.upload_image_files(name="uploadImageMessage", path=path)
                settings.maybePrint("Image(s) Entered")
                settings.debug_delay_check()
                return True
            except Exception as e:
                Driver.error_checker(e)
                print("Error: Unable to Upload Images")
                return False
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failure to Enter Image(s)")
            return False

    @staticmethod
    def message_price(price):
        try:
            if not price or price == None or str(price) == "None":
                print("Error: Missing Price")
                return False
            print("Enter price: {}".format(price))
            settings.devPrint("waiting for price area to enter price")
            priceElement = WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ONLYFANS_PRICE2)))
            settings.devPrint("entering price")
            priceElement.click()
            actions = ActionChains(BROWSER)
            actions.send_keys(str(price)) 
            actions.perform()
            settings.devPrint("entered price")
            # settings.debug_delay_check()
            settings.devPrint("saving price")
            Driver.get_element_to_click("priceClick").click()    
            settings.devPrint("saved price")
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failure to Enter Price")
            return False

    @staticmethod
    def message_text(text):
        try:
            # auth_ = Driver.auth()
            # if not auth_: return False
            # Driver.go_to_page(ONLYFANS_HOME_URL)
            if not text or text == None or str(text) == "None":
                print("Error: Missing Text")
                return False
            print("Enter text: {}".format(text))
            settings.devPrint("finding text area")
            message = Driver.find_element_by_name("messageText")     
            settings.devPrint("entering text")
            message.send_keys(str(text))
            settings.devPrint("entered text")
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failure to Enter Message")
            return False

    @staticmethod
    def message_user(username):
        try:
            auth_ = Driver.auth()
            if not auth_: return False
            username = str(username).replace("@u","").replace("@","")
            if not username or username == None or str(username) == "None":
                print("Warning: Missing Username")
                return False
            # settings.maybePrint("goto -> /my/chats/chat/{}".format(username))
            Driver.go_to_page("{}/{}".format(ONLYFANS_CHAT_URL, username))
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failure to Goto User - {}".format(user.username))
            return False

    ####################################################################################################
    ####################################################################################################
    ####################################################################################################

    # tries both and throws error for not found element internally
    @staticmethod
    def open_more_options():
        def option_one():
            # click on '...' element
            settings.devPrint("opening options (1)")
            moreOptions = Driver.get_element_to_click("moreOptions")
            if not moreOptions: return False    
            moreOptions.click()
            return True
        def option_two():
            # click in empty space
            settings.devPrint("opening options (2)")
            moreOptions = BROWSER.find_element_by_id(ONLYFANS_POST_TEXT_ID)
            if not moreOptions: return False    
            moreOptions.click()
            return True
        try:
            successful = option_one()
            if not successful: return option_two()
        except Exception as e:
            try:
                return option_two()
            except Exception as e:    
                Driver.error_checker(e)
                raise Exception("Error: Unable to Locate 'More Options' Element")

    ################
    ##### Poll #####
    ################

    @staticmethod
    def poll(poll):
        settings.devPrint("poll")
        period = poll.get("period")
        questions = poll.get("questions")
        if period == None or str(period) == "": return False
        if isinstance(questions, str): questions = questions.split(",\"*\"")
        questions = [n.strip() for n in questions]
        auth_ = Driver.auth()
        if not auth_: return False
        if int(period) != 1 and int(period) != 3 and int(period) != 7 and int(period) != 30 and int(period) != 99:
            try:
                if str(period) != "No limit":
                    print("Error: Missing Duration")
                    return False
            except Exception as e:
                return False
        if not questions or len(questions) == 0:
            print("Error: Missing Questions")
            return False
        try:
            print("Poll:")
            print("- Duration: {}".format(period))
            print("- Questions:\n> {}".format("\n> ".join(questions)))
            # make sure the extra options are shown
            Driver.open_more_options()
            # add a poll
            settings.devPrint("adding poll")
            Driver.get_element_to_click("poll").click()
            # open the poll duration
            settings.devPrint("adding duration")
            Driver.get_element_to_click("pollDuration").click()
            # click on the correct duration number
            settings.devPrint("setting duration")
            # nums = BROWSER.find_elements_by_class_name(Element.get_element_by_name("pollDurations").getClass())
            nums = Driver.find_elements_by_name("pollDurations")
            for num in nums:
                ##
                # <span class="g-first-letter">1</span> day
                # <span class="g-first-letter">3</span> days
                # <span class="g-first-letter">7</span> days
                # <span class="g-first-letter">30</span> days
                # <span><span class="g-first-letter">N</span>o limit</span>
                ##
                inner = num.get_attribute("innerHTML")
                if ">1<" in str(inner) and int(period) == 1: num.click()
                if ">3<" in str(inner) and int(period) == 3: num.click()
                if ">7<" in str(inner) and int(period) == 7: num.click()
                if ">30<" in str(inner) and int(period) == 30: num.click()
                if ">o limit<" in str(inner) and int(period) == 99: num.click()
            # save the duration
            settings.devPrint("saving duration")
            Driver.get_element_to_click("pollSave").click()
            settings.devPrint("saved duration")
            # add extra question space
            if len(questions) > 2:
                for question in questions[2:]:
                    settings.devPrint("adding question")
                    question_ = Driver.get_element_to_click("pollQuestionAdd").click()
                    settings.devPrint("added question")
            # find the question inputs
            settings.devPrint("locating question paths")
            questions_ = BROWSER.find_elements_by_xpath(POLL_INPUT_XPATH)
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
            if str(settings.DEBUG) == "True" and str(settings.DEBUG_FORCE) == "False":
                print("Skipping: Poll (debug)")
                cancel = Driver.get_element_to_click("pollCancel")
                cancel.click()
                settings.devPrint("canceled poll")
            else:
                print("Poll Entered")
            settings.devPrint("### Poll Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failed to Enter Poll")
            return False

    ################
    ##### Post #####
    ################

    @staticmethod
    def post(message):
        settings.devPrint("posting")
        try:
            auth_ = Driver.auth()
            if not auth_: return False
            Driver.go_to_home()
            path = message.get_files()
            text = message.get_text()
            keywords = message.get_keywords()
            performers = message.get_performers()
            tags = message.get_tags()
            expires = message.get_expiration()
            schedule = message.get_schedule()
            poll = message.get_poll()
            if not text or text == None or str(text) == "None":
                print("Warning: Missing Upload Text")
                text = ""
            # if isinstance(performers, list) and len(performers) > 0: text += " w/ @"+" @".join(performers)
            if isinstance(tags, list) and len(tags) > 0: text += " @"+" @".join(tags)
            if isinstance(keywords, list) and len(keywords) > 0: text += " #"+" #".join(keywords)
            text = text.strip()
            print("Posting:")
            settings.maybePrint("- Path: {}".format(path))
            print("- Keywords: {}".format(keywords))
            print("- Performers: {}".format(performers))
            print("- Tags: {}".format(tags))
            print("- Text: {}".format(text))
            print("- Tweeting: {}".format(settings.TWEETING))
            ## Expires, Schedule, Poll
            if expires: Driver.expires(expires)
            if schedule: Driver.schedule(schedule)
            if poll: 
                Driver.poll(poll)
                time.sleep(3)
            WAIT = WebDriverWait(BROWSER, 600, poll_frequency=10)
            ## Tweeting
            if str(settings.TWEETING) == "True":
                settings.devPrint("tweeting")
                WAIT.until(EC.element_to_be_clickable((By.XPATH, ONLYFANS_TWEET))).click()
            else:
                settings.devPrint("not tweeting")
            ## Images
            try:
                settings.devPrint("uploading files")
                successful_upload = Driver.upload_image_files("image_upload", path)
            except Exception as e:
                Driver.error_checker(e)
                print("Error: Unable to Upload Images")
                return False
            ## Text
            successful_text = Driver.enter_text(text)
            if not successful_text:
                print("Error: Unable to Enter Text")
                return False
            ## Confirm
            i = 0
            while True:
                try:
                    WebDriverWait(BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.CLASS_NAME, SEND_BUTTON_CLASS)))
                    settings.devPrint("upload complete")
                    break
                except Exception as e:
                    # try: 
                    #     # check for existence of "thumbnail is fucked up" modal and hit ok button
                    #     # haven't seen in long enough time to properly add
                    #     BROWSER.switchTo().frame("iframe");
                    #     BROWSER.find_element_by_class("g-btn m-rounded m-border").send_keys(Keys.ENTER)
                    #     print("Error: Thumbnail Missing")
                    #     break
                    # except Exception as ef:
                    #     settings.maybePrint(ef)
                    print('uploading...')
                    Driver.error_checker(e)
                    i+=1
                    if i == int(settings.UPLOAD_MAX_DURATION) and settings.FORCE_UPLOAD is not True:
                        print('Error: Max Upload Time Reached')
                        return False
            try:
                send = Driver.get_element_to_click("new_post")
                if send:
                    settings.debug_delay_check()
                    if str(settings.DEBUG) == "True":
                        print('Skipped: OnlyFans Post (debug)')
                        settings.devPrint("### Post Maybe Successful ###")
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
            settings.devPrint("### Post Successful ###")
            print('OnlyFans Post Complete')
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: OnlyFans Post Failure")
            return False

    ######################
    ##### Promotions #####
    ######################

    # or email
    @staticmethod
    def promotional_trial_link(user, depth=0, limit=1, expiration=1, duration=1, tryAll=False):
        auth_ = Driver.auth()
        if not auth_: return False
        # go to onlyfans.com/my/subscribers/active
        try:
            settings.maybePrint("goto -> /my/promotions")
            BROWSER.get(('https://onlyfans.com/my/promotions'))

            settings.devPrint("creating promotional trial")
            Driver.get_element_to_click("promotionalTrial").click()

            # limit dropdown
            settings.devPrint("setting trial count")
            limitDropwdown = Driver.find_element_by_name("promotionalTrialCount")
            for n in range(11): # 11 max subscription limits
                limitDropwdown.send_keys(str(Keys.UP))
            settings.debug_delay_check()
            if int(limit) == 99: limit = 1
            for n in range(int(limit)-1):
                limitDropwdown.send_keys(Keys.DOWN)

            settings.debug_delay_check()

            # expiration dropdown
            settings.devPrint("settings trial expiration")
            expirationDropdown = Driver.find_element_by_name("promotionalTrialExpiration")
            for n in range(11): # 31 max days
                expirationDropdown.send_keys(str(Keys.UP))
            settings.debug_delay_check()
            if int(expiration) == 99: expiration = 1
            for n in range(int(expiration)-1):
                expirationDropdown.send_keys(Keys.DOWN)

            settings.debug_delay_check()

            # duration dropdown
            settings.devPrint("settings trial duration")
            durationDropwdown = Driver.find_element_by_name("promotionalTrialDuration")
            for n in range(11): # 32 max duration
                durationDropwdown.send_keys(str(Keys.UP))
            settings.debug_delay_check()
            if int(duration) == 99: duration = 1
            for n in range(int(duration)-1):
                durationDropwdown.send_keys(Keys.DOWN)

            settings.debug_delay_check()

            # find and click promotionalTrialConfirm
            if str(settings.DEBUG) == "True":
                settings.devPrint("finding trial cancel")
                Driver.get_element_to_click("promotionalTrialCancel").click()
                print("Skipping: Promotion (debug)")
                settings.devPrint("Successful trial cancellation")
                return True
            settings.devPrint("finding trial save")
            save_ = Driver.get_element_to_click("promotionalTrialConfirm")
            settings.devPrint("saving promotion")
            save_.click()
            settings.devPrint("promotion saved")
            settings.devPrint("copying trial link")
            Driver.find_element_by_name("promotionalTrialLink").click()
            settings.devPrint("copied trial link")

            # go to /home
            # enter copied paste into new post
            # get text in new post
            # email link to user
            
            # Actions actions = new Actions(Driver.driver);
            # actions.sendKeys(Keys.chord(Keys.LEFT_CONTROL, "v")).build().perform();
            # sendemail(from_addr    = 'python@RC.net', 
            #   to_addr_list = ['RC@gmail.com'],
            #   cc_addr_list = ['RC@xx.co.uk'], 
            #   subject      = 'Howdy', 
            #   message      = 'Howdy from a python function', 
            #   login        = 'pythonuser', 
            #   password     = 'XXXXX')

            settings.devPrint("Successful Promotion")
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failed to Apply Promotion")
            return None

    @staticmethod
    def promotion_user_directly(user, expiration=10, months=1, message=""):
        auth_ = Driver.auth()
        if not auth_: return False
        if int(expiration) > int(settings.DISCOuNT_MAX_AMOUNT):
            print("Warning: Discount Too High, Max -> {}%".format(settings.DISCOuNT_MAX_AMOUNT))
            discount = settings.DISCOuNT_MAX_AMOUNT
        elif int(expiration) > int(settings.DISCOuNT_MIN_AMOUNT):
            print("Warning: Discount Too Low, Min -> {}%".format(settings.DISCOuNT_MIN_AMOUNT))
            discount = settings.DISCOuNT_MIN_AMOUNT
        if int(months) > int(settings.DISCOUNT_MAX_MONTHS):
            print("Warning: Duration Too High, Max -> {} days".format(settings.DISCOUNT_MAX_MONTHS))
            months = settings.DISCOUNT_MAX_MONTHS
        elif int(months) < int(settings.DISCOUNT_MIN_MONTHS):
            print("Warning: Duration Too Low, Min -> {} days".format(settings.DISCOUNT_MIN_MONTHS))
            months = settings.DISCOUNT_MIN_MONTHS
        try:
            settings.maybePrint("goto -> /{}".format(user.username))
            Driver.go_to_page.get(user.username)
            # click discount button
            Driver.get_element_to_click("discountUser").click()
            # enter expiration
            expirations = Driver.find_element_by_name("promotionalTrialExpirationUser")
            # enter duration
            durations = Driver.find_element_by_name("promotionalTrialDurationUser")
            # enter message
            message = Driver.find_element_by_name("promotionalTrialMessageUser")
            # save
            settings.devPrint("entering expiration")
            for n in range(11):
                expirations.send_keys(str(Keys.UP))
            for n in range(round(int(expiration)/5)-1):
                expirations.send_keys(Keys.DOWN)
            settings.devPrint("entered expiration")
            settings.devPrint("entering duration")
            for n in range(11):
                durations.send_keys(str(Keys.UP))
            for n in range(int(months)-1):
                durations.send_keys(Keys.DOWN)
            settings.devPrint("entered duration")
            settings.debug_delay_check()
            settings.devPrint("entering message")
            message.clear()
            message.send_keys(message)
            settings.devPrint("entered message")
            settings.devPrint("applying discount")
            save = Driver.find_element_by_name("promotionalTrialApply")
            if str(settings.DEBUG) == "True":
                Driver.find_element_by_name("promotionalTrialCancel").click()
                print("Skipping: Save Discount (Debug)")
                settings.devPrint("### Discount Successfully Canceled ###")
                cancel.click()
                return True
            save.click()
            print("Discounted User: {}".format(user.username))
            settings.devPrint("### User Discount Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            try:
                Driver.find_element_by_name("promotionalTrialCancel").click()
                settings.devPrint("### Discount Successful Failure ###")
                return False
            except Exception as e:
                Driver.error_checker(e)
            settings.devPrint("### Discount Failure ###")
            return False

    ######################################################################

    @staticmethod
    def read_user_messages(user):
        try:
            auth_ = Driver.auth()
            if not auth_: return False
            # go to onlyfans.com/my/subscribers/active
            Driver.message_user(user)
            messages_from_ = Driver.find_elements_by_name("messagesFrom")
            # print("first message: {}".format(messages_to_[0].get_attribute("innerHTML")))
            # messages_to_.pop(0) # drop self user at top of page
            messages_all_ = Driver.find_elements_by_name("messagesAll")
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
            Driver.error_checker(e)
            print("Error: Failure to Read Chat - {}".format(user.username))
            return [[],[],[]]

    #################
    ##### Reset #####
    #################

    # Reset to home
    @staticmethod
    def reset():
        if not BROWSER or BROWSER == None:
            print('OnlyFans Not Open, Skipping Reset')
            return True
        try:
            BROWSER.get(ONLYFANS_HOME_URL)
            print('OnlyFans Reset')
            return True
        except Exception as e:
            Driver.error_checker(e)
            print('Error: Failure Resetting OnlyFans')
            return False

    ####################
    ##### Settings #####
    ####################

    # gets all settings from whichever page its on
    # or get a specific setting
    # probably just way easier and resourceful to do it all at once
    # though it would be ideal to also be able to update individual settings without risking other settings

    # goes through the settings and get all the values
    @staticmethod
    def settings_get_all():
        print("Getting All Settings")
        try:
            auth_ = Driver.auth()
            if not auth_: return False
            pages = Profile.get_pages()
            for page in pages:
                variables = Profile.get_variables_for_page(page)
                settings.devPrint("going to settings page: {}".format(page))
                Driver.go_to_settings(page)
                settings.devPrint("reached settings: {}".format(page))
                data = Profile({})
                for var in variables:
                    name = var[0]
                    page_ = var[1]
                    type_ = var[2]
                    status = None
                    settings.devPrint("searching: {} - {}".format(name, type_))
                    try:
                        element = Driver.find_element_by_name(name)
                        settings.devPrint("Successful ele: {}".format(name))
                    except Exception as e:
                        Driver.error_checker(e)
                        continue
                    if str(type_) == "text":
                        # get attr text
                        status = element.get_attribute("innerHTML").strip() or None
                        status2 = element.get_attribute("value").strip() or None
                        print("{} - {}".format(status, status2))
                        if not status and status2: status = status2
                    elif str(type_) == "toggle":
                        # get state true|false
                        status = element.is_selected()
                    elif str(type_) == "dropdown":
                        ele = Driver.find_element_by_name(name)
                        Select(driver.find_element_by_id(ele.getId()))
                        status = element.first_selected_option
                    elif str(type_) == "list":
                        status = element.get_attribute("innerHTML")
                    elif str(type_) == "file":
                        # can get file from image above
                        # can set once found
                        # status = element.get_attribute("innerHTML")
                        pass
                    elif str(type_) == "checkbox":
                        status = element.is_selected()
                    if status is not None: settings.devPrint("Successful value: {}".format(status))
                    settings.maybePrint("{} : {}".format(name, status))
                    data.set(name, status)
            settings.devPrint("Successfully got settings")
            print("Settings Retrieved")
            return data
        except Exception as e:
            Driver.error_checker(e)

    # goes through each page and sets all the values
    @staticmethod
    def settings_set_all(data):
        print("Updating All Settings")
        try:
            auth_ = Driver.auth()
            if not auth_: return False
            # Driver.go_to_home()
            pages = Profile.get_pages()
            for page in pages:
                variables = Profile.get_variables_for_page(page)
                settings.devPrint("going to settings page: {}".format(page))
                Driver.go_to_settings(page)
                settings.devPrint("reached settings: {}".format(page))
                for var in variables:
                    name = var[0]
                    page_ = var[1]
                    type_ = var[2]
                    status = None
                    settings.devPrint("searching: {} - {}".format(name, type_))
                    try:
                        element = Driver.find_element_by_name(name)
                        settings.devPrint("Successful ele: {}".format(name))
                    except Exception as e:
                        Driver.error_checker(e)
                        continue
                    if str(type_) == "text":
                        element.send_keys(data.get(name))
                    elif str(type_) == "toggle":
                        # somehow set the other toggle state
                        pass
                    elif str(type_) == "dropdown":
                        ele = Driver.find_element_by_name(name)
                        Select(driver.find_element_by_id(ele.getId()))
                        # go to top
                        # then go to matching value
                        pass
                    elif str(type_) == "list":
                        element.send_keys(data.get(name))
                    elif str(type_) == "file":
                        element.send_keys(data.get(name))
                    elif str(type_) == "checkbox":
                        element.click()
                    # settings.devPrint("Successful value: {}".format(status))
                Driver.settings_save(page=page)
            settings.devPrint("Successfully set settings")
            print("Settings Updated")
        except Exception as e:
            Driver.error_checker(e)

    # saves the settings page if it is a page that needs to be saved
        # has save:
        # profile
        # account
        # security
        ##
        # doesn't have save:
        # story
        # notifications
        # other
    @staticmethod
    def settings_save(pa@staticmethodge=None):
        if str(page) not in ["profile", "account", "security"]:
            settings.devPrint("not saving: {}".format(page))
            return
        try:
            settings.devPrint("saving: {}".format(page))
            element = Driver.find_element_by_name("profileSave")
            settings.devPrint("derp")
            element = Driver.get_element_to_click("profileSave")
            settings.devPrint("found page save")
            if str(settings.DEBUG) == "True":
                print("Skipping: Save (debug)")
            else:
                settings.devPrint("saving page")
                element.click()
                settings.devPrint("page saved")
        except Exception as e:
            Driver.error_checker(e)

    ####################
    ##### Schedule #####
    ####################

    @staticmethod
    def schedule(schedule_):
        auth_ = Driver.auth()
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
            # add check for if date is before today
            today = datetime.now()
            todaysMonth = today.strftime("%B")
            todaysYear = today.strftime("%Y")
            settings.devPrint("today: {} {}".format(todaysMonth, todaysYear))
            if tehdate < today:
                print("Error: Unable to Schedule Earlier Date")
                return False
            print("Schedule:")
            print("- Date: {}".format(date))
            print("- Time: {}".format(time_))
            Driver.open_more_options()
            # click schedule
            settings.devPrint("adding schedule")
            Driver.get_element_to_click("scheduleAdd").click()
            # find and click month w/ correct date
            while True:
                settings.devPrint("getting date")
                existingDate = Driver.find_element_by_name("scheduleDate").get_attribute("innerHTML")
                settings.devPrint("date: {} - {} {}".format(existingDate, month_, year_))
                if str(month_) in str(existingDate) and str(year_) in str(existingDate): break
                else: Driver.get_element_to_click("scheduleNextMonth").click()
            # set day in month
            settings.devPrint("setting days")
            days = Driver.find_elements_by_name("scheduleDays")
            for day in days:
                inner = day.get_attribute("innerHTML").replace("<span><span>","").replace("</span></span>","")
                if str(day_) == str(inner):
                    day.click()
                    settings.devPrint("clicked day")
            settings.debug_delay_check()
            # save schedule date
            saves = Driver.get_element_to_click("scheduleSave").click()
            # set hours
            settings.devPrint("setting hours")
            hours = Driver.find_elements_by_name("scheduleHours")
            for hour in hours:
                inner = hour.get_attribute("innerHTML")
                if str(hour_) in str(inner) and hour.is_enabled():
                    hour.click()
                    settings.devPrint("hours set")
            # set minutes
            settings.devPrint("setting minutes")
            minutes = Driver.find_elements_by_name("scheduleMinutes")
            for minute in minutes:
                inner = minute.get_attribute("innerHTML")
                if str(minute_) in str(inner) and minute.is_enabled():
                    minute.click()
                    settings.devPrint("minutes set")
            # save time
            settings.devPrint("saving schedule")
            settings.debug_delay_check()
            if str(settings.DEBUG) == "True" and str(settings.DEBUG_FORCE) == "False":
                print("Skipping: Schedule (debug)")
                Driver.get_element_to_click("scheduleCancel").click()
                settings.devPrint("canceled schedule")
            else:
                Driver.get_element_to_click("scheduleSave").click()
                settings.devPrint("saved schedule")
                print("Schedule Entered")
            settings.devPrint("### Schedule Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failed to Enter Schedule")
            return False

    @staticmethod
    def spawn_browser(self):      
        global BROWSER
        if BROWSER: return True
        print("Spawning Browser")
        CHROMEDRIVER_PATH = chromedriver_binary.chromedriver_filename
        options = webdriver.ChromeOptions()
        # options.setExperimentalOption('useAutomationExtension', false);
        # options.binary_location = chromedriver_binary.chromedriver_filename
        if str(SHOW_WINDOW) != "True":
            options.add_argument('--headless')
            #
            options.add_argument('--disable-smooth-scrolling')
            options.add_argument('--disable-software-rasterizer')
            options.add_argument("disable-infobars") # disabling infobars
            options.add_argument("--disable-extensions") # disabling extensions
            options.add_argument("--disable-gpu") # applicable to windows os only
        #
        options.add_argument('--disable-login-animations')
        options.add_argument('--disable-modal-animations')
        options.add_argument('--disable-sync')
        # options.add_argument('--incognito')
        options.add_argument('--user-agent=MozillaYerMomFox')
        #
        options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems
        options.add_argument("--no-sandbox") # Bypass OS security model
        # options.add_experimental_option("prefs", {
        #   "download.default_directory": str(DOWNLOAD_PATH),
        #   "download.prompt_for_download": False,
        #   "download.directory_upgrade": True,
        #   "safebrowsing.enabled": True
        # })
        driver = None
        try:
            driver = webdriver.Chrome(chrome_options=options)
        except Exception as e:
            # print(e)
            print("Warning: Missing Chromedriver")
            return False
        driver.implicitly_wait(30) # seconds
        driver.set_page_load_timeout(1200)
        print("Browser Spawned")
        BROWSER = driver
        return True

    # update chat logs for all users
    @staticmethod
    def update_chat_logs():
        global USER_CACHE_LOCKED
        USER_CACHE_LOCKED = True
        print("Updating User Chats")
        users = Driver.users_get()
        for user in users:
            Driver.update_chat_log(user)
        USER_CACHE_LOCKED = False

    @staticmethod
    def update_chat_log(user):
        print("Updating Chat: {}".format(user.username))
        if not user:
            return print("Error: Missing User")
        user.readChat()

    ##################
    ##### Upload #####
    ##################

    # uploads image into post or message
    @staticmethod
    def upload_image_files(name="image_upload", path=None):
        settings.devPrint("uploading image files: {} - {}".format(name, path))
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
        files = files[:int(settings.IMAGE_UPLOAD_LIMIT_MESSAGES)]
        for file in files:  
            print('Uploading: '+str(file))
            enter_file = BROWSER.find_element_by_id(Element.get_element_by_name(str(name)).getId())
            enter_file.send_keys(str(file))
            time.sleep(1)
            Driver.error_window_upload()
            ###
            def fix_filename(file):
                # move file to change its name
                filename = os.path.basename(file)
                filename = os.path.splitext(filename)[0]
                if "_fixed" in str(filename): return
                settings.devPrint("fixing filename...")
                filename += "_fixed"
                ext = os.path.splitext(filename)[1].lower()
                settings.devPrint("{} -> {}.{}".format(os.path.dirname(file), filename, ext))
                dst = "{}/{}.{}".format(os.path.dirname(file), filename, ext)
                shutil.move(file, dst)
                # add file to end of list so it gets retried
                files.append(dst)
                # if this doesn't force it then it'll loop forever without a stopper
            ###
        # one last final check
        Driver.error_window_upload()
        settings.debug_delay_check()
        settings.devPrint("files uploaded")
        return True

    #################
    ##### Users #####
    #################

    # returns list of accounts you follow
    @staticmethod
    def following_get():
        users = []
        try:
            Driver.go_to_page(ONLYFANS_USERS_FOLLOWING_URL)
            count = 0
            while True:
                elements = BROWSER.find_elements_by_class_name("m-subscriptions")
                if len(elements) == count: break
                print_same_line("({}/{}) scrolling...".format(count, len(elements)))
                count = len(elements)
                BROWSER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            print()
            elements = BROWSER.find_elements_by_class_name("m-subscriptions")
            for ele in elements:
                username = ele.find_element_by_class_name("g-user-username").get_attribute("innerHTML").strip()
                name = ele.find_element_by_class_name("g-user-name").get_attribute("innerHTML")
                name = re.sub("<!-*>", "", name)
                name = re.sub("<.*\">", "", name)
                name = re.sub("</.*>", "", name).strip()
                # print("username: {}".format(username))
                # print("name: {}".format(name))
                users.append({"name":name, "username":username}) 
            settings.maybePrint("Found: {}".format(len(users)))
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failed to Find Subscriptions")
        return users

    # returns list of accounts that follow you
    @staticmethod
    def users_get():
        users = []
        try:
            Driver.go_to_page(ONLYFANS_USERS_ACTIVE_URL)
            count = 0
            while True:
                elements = BROWSER.find_elements_by_class_name("m-fans")
                if len(elements) == int(count): break
                print_same_line("({}/{}) scrolling...".format(count, len(elements)))
                count = len(elements)
                BROWSER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            print()
            elements = BROWSER.find_elements_by_class_name("m-fans")
            for ele in elements:
                username = ele.find_element_by_class_name("g-user-username").get_attribute("innerHTML").strip()
                name = ele.find_element_by_class_name("g-user-name").get_attribute("innerHTML")
                name = re.sub("<!-*>", "", name)
                name = re.sub("<.*\">", "", name)
                name = re.sub("</.*>", "", name).strip()
                # print("username: {}".format(username))
                # print("name: {}".format(name))
                users.append({"name":name, "username":username}) # ,"id":user_id, "started":start})
            settings.maybePrint("Found: {}".format(len(users)))
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failed to Find Users")
        return users

    ################
    ##### Exit #####
    ################

    @staticmethod
    def exit():
        if BROWSER == None: return
        if str(settings.SAVE_USERS) == "True":
            print("Saving and Exiting OnlyFans")
            write_users_local()
        else:
            print("Exiting OnlyFans")
        BROWSER.quit()
        BROWSER = None
        print("Browser Closed")

##################################################################################

def parse_users(user_ids, starteds, users, usernames):
    # usernames.pop(0)
    # print("My User Id: {}".format(user_ids[0]))
    # user_ids.pop(0)
    settings.devPrint("user_ids: "+str(len(user_ids)))
    settings.devPrint("starteds: "+str(len(starteds)))
    useridsFailed = False
    startedsFailed = False
    if len(user_ids) == 0:
        settings.maybePrint("Warning: Unable to find user ids")
        useridsFailed = True
    if len(starteds) == 0:
        settings.maybePrint("Warning: Unable to find starting dates")
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
            settings.maybePrint("Warning: Unable to find user ids")
            useridsFailed = True
        if len(starteds_) == 0:
            settings.maybePrint("Warning: Unable to find starting dates")
            startedsFailed = True
        # settings.maybePrint("ids vs starteds vs avatars: "+str(len(user_ids_))+" - "+str(len(starteds_))+" - "+str(len(avatars)))
        settings.maybePrint("users vs ids vs starteds vs usernames:"+str(len(users))+" - "+str(len(user_ids_))+" - "+str(len(starteds_))+" - "+str(len(usernames)))
        # for user in usernames:
            # print(user.get_attribute("innerHTML"))
        if len(usernames) > 2:
            # first 2 usernames are self
            usernames.pop(0)
            usernames.pop(0)
        if len(users) > 2:
            users.pop(0)
            users.pop(0)
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
                name = str(name.get_attribute("innerHTML"))
                # print("name: "+name)
                # if "<!" in str(name):
                name = re.sub("<!-*>", "", name)
                # print(name)
                # if "<" in str(name) and ">" in str(name):
                name = re.sub("<.*\">", "", name).strip()
                # print(name)
                name = re.sub("</.*>", "", name).strip()
                # print(name)
                # name = re.sub(name, "<.*>", "").strip()
                # print(name)
                # name = re.sub(name, "<!-*>", "")
                username = str(username.get_attribute("innerHTML"))
                # print("username: "+username)
                # if "<!" in str(username):
                username = re.sub("<!-*>", "", username)
                # print(username)
                # if "<" in str(username) and ">" in str(username):
                username = re.sub("<.*\">", "", username).strip()
                # print(username)
                username = re.sub("</.*>", "", username).strip()
                username = username.replace("@","")
                # print(username)
                # username = re.sub("<.*>", "", username).strip()
                # print(username)
                # username = re.sub(username, "<!-*>", "")
                # settings.maybePrint("name: "+str(name))
                # settings.maybePrint("username: "+str(username))
                # settings.maybePrint("user_id: "+str(user_id))
                # if str(settings.USERNAME).lower() in str(username).lower():
                #     settings.maybePrint("(): %s = %s" % (settings.USERNAME, username))
                #     # first user is always active user but just in case find it in list of users
                #     settings.USER_ID = username
                # else:
                users_.append({"name":name, "username":username, "id":user_id, "started":start})
            except Exception as e: settings.maybePrint(e)
    except Exception as e: Driver.error_checker(e)
    return users_



import smtplib

def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    return problems
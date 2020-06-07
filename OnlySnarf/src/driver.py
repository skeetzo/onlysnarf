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
from .colorize import colorize
from .settings import Settings
from .element import Element

###################
##### Globals #####
###################

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
    BROWSER = None
    LOGGED_IN = False

    def __init__():
        pass
        # BROWSER = None

    @staticmethod
    def auth():
        spawned = Driver.check_spawn()
        if not spawned: return False
        logged_in = False
        if not Driver.LOGGED_IN or Driver.LOGGED_IN == None:
            logged_in = Driver.login()
        else: logged_in = True
        if logged_in == False: print("Error: Failure to Login")
        Driver.LOGGED_IN = logged_in
        return logged_in

    @staticmethod
    def check_spawn():
        spawned = False
        if not Driver.BROWSER or Driver.BROWSER == None:
            spawned = Driver.spawn_browser()
        else: spawned = True
        if spawned == False: print("Error: Failure to Spawn Browser")
        return spawned

    ####################
    ##### Discount #####
    ####################

    @staticmethod
    def discount_user(discount=None):
        if not discount:
            print("Error: Missing Discount")
            return False
        auth_ = Driver.auth()
        if not auth_: return False
        discount.get()
        months = discount.months
        amount = discount.amount
        user = discount.username
        if int(months) > int(Settings.get_discount_max_months()):
            print("Warning: Months Too High, Max -> {} days".format(Settings.get_discount_max_months()))
            months = Settings.get_discount_max_months()
        elif int(months) < int(Settings.get_discount_min_months()):
            print("Warning: Months Too Low, Min -> {} days".format(Settings.get_discount_min_months()))
            months = Settings.get_discount_min_months()
        if int(amount) > int(Settings.get_discount_max_amount()):
            print("Warning: Amount Too High, Max -> {} days".format(Settings.get_discount_max_months()))
            amount = Settings.get_discount_max_amount()
        elif int(amount) < int(Settings.get_discount_min_amount()):
            print("Warning: Amount Too Low, Min -> {} days".format(Settings.get_discount_min_months()))
            amount = Settings.get_discount_min_amount()
        try:
            print("Discounting User: {}".format(user))
            Driver.go_to_page(ONLYFANS_USERS_ACTIVE_URL)
            end_ = True
            count = 0
            while end_:
                elements = Driver.BROWSER.find_elements_by_class_name("m-fans")
                for ele in elements:
                    username = ele.find_element_by_class_name("g-user-username").get_attribute("innerHTML").strip()
                    if str(user) == str(username): 
                        Driver.BROWSER.execute_script("arguments[0].scrollIntoView();", ele)
                        end_ = False
                if not end_: continue
                if len(elements) == int(count): break
                print_same_line("({}/{}) scrolling...".format(count, len(elements)))
                count = len(elements)
                Driver.BROWSER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            print()
            users = Driver.find_elements_by_name("discountUsers")
            if int(len(users)) == 0:
                print("Error: Missing Users")
                return False
            # get all the users
            Settings.dev_print("finding user")
            user__ = None
            for user_ in users:
                text = user_.get_attribute("innerHTML")
                # Settings.dev_print("user text: {}".format(text))
                if str(user) in text:
                    user__ = user_
                    Settings.dev_print("found user: {} - {}".format(user__, user_))
                    break
            if user__ == None:
                print("Warning: Unable to Find User")
                return False
            ActionChains(Driver.BROWSER).move_to_element(user__).perform()
            Settings.dev_print("moved to user")
            Settings.dev_print("finding discount btn")
            buttons = user__.find_elements_by_class_name(DISCOUNT_USER_BUTTONS)
            for button in buttons:
                if "Discount" in button.get_attribute("innerHTML") and button.is_enabled() and button.is_displayed():
                    try:
                        Settings.dev_print("clicking discount btn")
                        button.click()
                        Settings.dev_print("clicked discount btn")
                        break
                    except Exception as e:
                        Driver.error_checker(e)
                        print("Warning: Unable To Find User")
                        return False
            time.sleep(1)
            Settings.dev_print("finding months and discount amount btns")
            (months_, discount_) = Driver.BROWSER.find_elements_by_class_name(DISCOUNT_INPUT)
            Settings.dev_print("found months and discount amount")
            # removed in 2.10, inputs changed to above
            # months_ = Driver.BROWSER.find_element_by_class_name(MONTHS_INPUT)
            # if discount_.get_attribute("value") != "":
                # print("Warning: Existing Discount")
            # discount_.clear()
            Settings.dev_print("entering discount amount")
            for n in range(11):
                discount_.send_keys(str(Keys.UP))
            for n in range(round(int(amount)/5)-1):
                discount_.send_keys(Keys.DOWN)
            Settings.dev_print("entered discount amount")
            Settings.dev_print("entering discount months")
            for n in range(11):
                months_.send_keys(str(Keys.UP))
            for n in range(int(months)-1):
                months_.send_keys(Keys.DOWN)
            Settings.dev_print("entered discount months")
            Settings.debug_delay_check()
            Settings.dev_print("applying discount")
            buttons_ = Driver.find_elements_by_name("discountUserButton")
            for button in buttons_:
                if not button.is_enabled() and not button.is_displayed(): continue
                if "Cancel" in button.get_attribute("innerHTML") and Settings.is_debug():
                    button.click()
                    print("Skipping: Save Discount (Debug)")
                    Settings.dev_print("### Discount Successfully Canceled ###")
                    return True
                elif "Apply" in button.get_attribute("innerHTML"):
                    button.click()
                    print("Discounted User: {}".format(user))
                    Settings.dev_print("### Discount Successful ###")
                    return True
            Settings.dev_print("### Discount Failure ###")
        except Exception as e:
            print(e)
            Driver.error_checker(e)
            buttons_ = Driver.find_elements_by_name("discountUserButtons")
            for button in buttons_:
                if "Cancel" in button.get_attribute("innerHTML"):
                    button.click()
                    Settings.dev_print("### Discount Successful Failure ###")
                    return False
            Settings.dev_print("### Discount Failure ###")
            return False

    @staticmethod
    def enter_text(text):
        try:
            Settings.dev_print("finding text")
            sendText = Driver.BROWSER.find_element_by_id(ONLYFANS_POST_TEXT_ID)
            Settings.dev_print("found text")
            sendText.clear()
            Settings.dev_print("sending text")
            sendText.send_keys(str(text))
            return True
        except Exception as e:
            print(e)
            Settings.dev_print(e)
            return False

    @staticmethod
    def error_checker(e):
        if "Unable to locate element" in str(e):
            print("Warning: OnlySnarf may require an update")
        if "Message: " in str(e): return
        Settings.dev_print(e)
        Settings.dev_print(e)

    @staticmethod
    def error_window_upload():
        try:
            element = Element.get_element_by_name("errorUpload")
            error_buttons = Driver.BROWSER.find_elements_by_class_name(element.getClass())
            Settings.dev_print("errors btns: {}".format(len(error_buttons)))
            for butt in error_buttons:
                if butt.get_attribute("innerHTML").strip() == "Close" and butt.is_enabled():
                    Settings.maybe_print("Warning: Upload Error Message, Closing")
                    butt.click()
                    Settings.maybe_print("Success: Upload Error Message Closed")
                    return True
            return False
        except Exception as e:
            Driver.error_checker(e)
            return False

    ######################
    ##### Expiration #####
    ######################

    @staticmethod
    def expires(expiration=None):
        if not expiration:
            print("Error: Missing Expiration")
            return False
        auth_ = Driver.auth()
        if not auth_: return False
        Settings.dev_print("expires")
        try:
            # go_to_home() # this should be run only from upload anyways
            print("Expiration:")
            print("- Period: {}".format(expiration))
            Driver.open_more_options()
            # open expires window
            Settings.dev_print("adding expires")
            Driver.get_element_to_click("expiresAdd").click()
            # select duration
            Settings.dev_print("selecting expires")
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
                if ">1<" in str(inner) and int(expiration) == 1: num.click()
                if ">3<" in str(inner) and int(expiration) == 3: num.click()
                if ">7<" in str(inner) and int(expiration) == 7: num.click()
                if ">30<" in str(inner) and int(expiration) == 30: num.click()
                if ">o limit<" in str(inner) and int(expiration) == 99: num.click()
            Settings.dev_print("selected expires")
            Settings.debug_delay_check()
            # save
            if Settings.is_debug():
                print("Skipping: Expiration (debug)")
                Settings.dev_print("skipping expires")
                Driver.get_element_to_click("expiresCancel").click()
                Settings.dev_print("canceled expires")
                Settings.dev_print("### Expiration Successfully Canceled ###")
            else:
                Settings.dev_print("saving expires")
                Driver.get_element_to_click("expiresSave").click()
                Settings.dev_print("saved expires")
                print("Expiration Entered")
                Settings.dev_print("### Expiration Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failed to Enter Expiration")
            try:
                Settings.dev_print("canceling expires")
                Driver.get_element_to_click("expiresCancel").click()
                Settings.dev_print("canceled expires")
                Settings.dev_print("### Expiration Successful Failure ###")
            except: 
                Settings.dev_print("### Expiration Failure Failure")
            return False

    ######################################################################

    # should already be logged in
    @staticmethod
    def find_element_by_name(name):
        if Driver.BROWSER == None: return False
        element = Element.get_element_by_name(name)
        if not element:
            print("Error: Unable to find Element Reference")
            return False
        # prioritize id over class name
        eleID = None
        try: eleID = Driver.BROWSER.find_element_by_id(element.getId())
        except: eleID = None
        if eleID: return eleID
        for className in element.getClasses():
            ele = None
            eleCSS = None
            try: ele = Driver.BROWSER.find_element_by_class_name(className)
            except: ele = None
            try: eleCSS = Driver.BROWSER.find_element_by_css_selector(className)
            except: eleCSS = None
            Settings.dev_print("class: {} - {}:css".format(ele, eleCSS))
            if ele: return ele
            if eleCSS: return eleCSS
        raise Exception("Error: Unable to Locate Element")

    @staticmethod
    def find_elements_by_name(name):
        if Driver.BROWSER == None: return False
        element = Element.get_element_by_name(name)
        if not element:
            print("Error: Unable to find Element Reference")
            return False
        eles = []
        for className in element.getClasses():
            eles_ = []
            elesCSS_ = []
            try: eles_ = Driver.BROWSER.find_elements_by_class_name(className)
            except: eles_ = []
            try: elesCSS_ = Driver.BROWSER.find_elements_by_css_selector(className)
            except: elesCSS_ = []
            Settings.dev_print("class: {} - {}:css".format(len(eles_), len(elesCSS_)))
            eles.extend(eles_)
            eles.extend(elesCSS_)
        eles_ = []
        for i in range(len(eles)):
            # Settings.dev_print("ele: {} -> {}".format(eles[i].get_attribute("innerHTML").strip(), element.getText()))
            if eles[i].is_displayed():
                Settings.dev_print("found displayed ele: {}".format(eles[i].get_attribute("innerHTML").strip()))
                eles_.append(eles[i])
        if len(eles_) == 0:
            raise Exception("Error: Unable to Locate Elements")
        return eles_

    @staticmethod
    def get_element_to_click(name):
        Settings.dev_print("finding click: {}".format(name))
        element = Element.get_element_by_name(name)
        if not element:
            print("Error: Unable to find Element Reference")
            return False
        for className in element.getClasses():
            eles = []
            elesCSS = []
            try: eles = Driver.BROWSER.find_elements_by_class_name(className)
            except: eles = []
            try: elesCSS = Driver.BROWSER.find_elements_by_css_selector(className)
            except: elesCSS = []
            Settings.dev_print("class: {} - {}:css".format(len(eles), len(elesCSS)))
            eles.extend(elesCSS)
            for i in range(len(eles)):
                # Settings.dev_print("ele: {} -> {}".format(eles[i].get_attribute("innerHTML").strip(), element.getText()))
                if (eles[i].is_displayed() and element.getText() and str(element.getText().lower()) in eles[i].get_attribute("innerHTML").strip().lower()) and eles[i].is_enabled():
                    Settings.dev_print("found matching ele")
                    # Settings.dev_print("found matching ele: {}".format(eles[i].get_attribute("innerHTML").strip()))
                    return eles[i]
                elif (eles[i].is_displayed() and element.getText() and str(element.getText().lower()) in eles[i].get_attribute("innerHTML").strip().lower()):
                    Settings.dev_print("found text ele")
                    # Settings.dev_print("found text ele: {}".format(eles[i].get_attribute("innerHTML").strip()))
                    return eles[i]
                elif eles[i].is_displayed() and not element.getText() and eles[i].is_enabled():
                    Settings.dev_print("found enabled ele")
                    # Settings.dev_print("found enabled ele: {}".format(eles[i].get_attribute("innerHTML").strip()))
                    return eles[i]
            if len(eles) > 0: return eles[0]
            Settings.dev_print("unable to find element - {}".format(className))
        raise Exception("Error Locating Element")

    ######################################################################

    ##############
    ### Go Tos ###
    ##############


    # waits for page load
    def get_page_load():
        time.sleep(5)
        # try: WebDriverWait(Driver.BROWSER, 120, poll_frequency=10).until(EC.visibility_of_element_located((By.CLASS_NAME, "main-wrapper")))
        # except Exception as e: pass

    def handle_alert():
        try:
            alert_obj = Driver.BROWSER.switch_to.alert or None
            if alert_obj:
                alert_obj.accept()
        except: pass
        # alert = WebDriverWait(s.mydriver, 3).until(EC.alert_is_present(),"Enter Party Name")
        # alert.send_keys() – used to enter a value in the Alert text box.
        # alert.accept()
        # Settings.dev_print("alert accepted")

    @staticmethod
    def go_to_page(page):
        auth_ = Driver.auth()
        if not auth_: return False
        if str(Driver.BROWSER.current_url) == str(page) or str(page) in str(Driver.BROWSER.current_url):
            Settings.maybe_print("at -> {}".format(page))
            Driver.BROWSER.execute_script("window.scrollTo(0, 0);")
        else:
            Settings.maybe_print("goto -> {}".format(page))
            Driver.BROWSER.get("{}/{}".format(ONLYFANS_HOME_URL, page))
        Driver.handle_alert()
        Driver.get_page_load()

    @staticmethod
    def go_to_home():
        auth_ = Driver.auth()
        if not auth_: return False
        if str(Driver.BROWSER.current_url) == str(ONLYFANS_HOME_URL):
            Settings.maybe_print("at -> onlyfans.com")
            Driver.BROWSER.execute_script("window.scrollTo(0, 0);")
        else:
            Settings.maybe_print("goto -> onlyfans.com")
            Driver.BROWSER.get(ONLYFANS_HOME_URL)
        Driver.get_page_load()

    # onlyfans.com/my/settings
    @staticmethod
    def go_to_settings(settingsTab):
        auth_ = Driver.auth()
        if not auth_: return False
        if str(Driver.BROWSER.current_url) == str(ONLYFANS_SETTINGS_URL) and str(settingsTab) == "profile":
            Settings.maybe_print("at -> onlyfans.com/settings/{}".format(settingsTab))
            Driver.BROWSER.execute_script("window.scrollTo(0, 0);")
        else:
            if str(settingsTab) == "profile": settingsTab = ""
            Settings.maybe_print("goto -> onlyfans.com/settings/{}".format(settingsTab))
            Driver.go_to_page("{}/{}".format(ONLYFANS_SETTINGS_URL, settingsTab))
            # fix above with correct element to locate
        Driver.get_page_load()

    ##################
    ###### Login #####
    ##################

    @staticmethod
    def login():
        print('Logging into OnlyFans')
        username = str(Settings.get_username())
        password = str(Settings.get_password())
        if not username or username == "":
            username = Settings.prompt_username()
        if not password or password == "":
            password = Settings.prompt_password()
        if str(username) == "" or str(password) == "":
            print("Error: Missing Login Info")
            return False
        try:
            Driver.BROWSER.get(ONLYFANS_HOME_URL)
            Settings.dev_print("logging in")
            # twitter = Driver.BROWSER.find_element_by_xpath(TWITTER_LOGIN3).click()
            # Settings.dev_print("twitter login clicked")
            # rememberMe checkbox doesn't actually cause login to be remembered
            # rememberMe = Driver.BROWSER.find_element_by_xpath(REMEMBERME_CHECKBOX_XPATH)
            # if not rememberMe.is_selected():
                # rememberMe.click()
            # if str(Settings.MANUAL) == "True":
                # print("Please Login")
            elements = Driver.BROWSER.find_elements_by_tag_name("a")
            [elem for elem in elements if '/twitter/auth' in str(elem.get_attribute('href'))][0].click()
            # twitter = Driver.BROWSER.find_element_by_xpath("//a[@class='g-btn m-rounded m-flex m-lg m-with-icon']").click()    
            Driver.BROWSER.find_element_by_xpath("//input[@id='username_or_email']").send_keys(username)
            Settings.dev_print("username entered")
            # fill in password and hit the login button 
            password_ = Driver.BROWSER.find_element_by_xpath("//input[@id='password']")
            password_.send_keys(password)
            Settings.dev_print("password entered")
            password_.send_keys(Keys.ENTER)
            try:
                Settings.dev_print("waiting for loginCheck")
                WebDriverWait(Driver.BROWSER, 120, poll_frequency=6).until(EC.visibility_of_element_located((By.CLASS_NAME, Element.get_element_by_name("loginCheck").getClass())))
                print("OnlyFans Login Successful")
                return True
            except TimeoutException as te:
                Settings.dev_print(str(te))
                print("Login Failure: Timed Out! Please check your Twitter credentials.")
                print(": If the problem persists, OnlySnarf may require an update.")
            except Exception as e:
                Driver.error_checker(e)
                print("Login Failure: OnlySnarf may require an update")
            return False
        except Exception as e:
            Settings.dev_print("login failure")
            Driver.error_checker(e)
            print("OnlyFans Login Failed")
            return False

    ####################
    ##### Messages #####
    ####################

    @staticmethod
    def message(username=None, user_id=None):
        if not username and not user_id:
            print("Error: Missing User to Message")
            return False
        auth_ = Driver.auth()
        if not auth_: return False
        try:
            type__ = None # default
            if str(username).lower() == "all": type__ = "messageAll"
            elif str(username).lower() == "recent": type__ = "messageRecent"
            elif str(username).lower() == "favorite": type__ = "messageFavorite"
            elif str(username).lower() == "renew on": type__ = "messageRenewers"
            successful = False
            if type__ != None:
                Driver.go_to_page(ONLYFANS_NEW_MESSAGE_URL)
                Settings.dev_print("clicking message type: {}".format(username))
                Driver.get_element_to_click(type__).click()
                successful = True
            else:
                successful = Driver.message_user(username=username, user_id=user_id)
            Settings.dev_print("successfully started message: {}".format(username))
            return successful
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failure to Message - {}".format(username))
            return False
     
    @staticmethod
    def message_confirm():
        try:
            WAIT = WebDriverWait(Driver.BROWSER, 600, poll_frequency=10)
            i = 0
            Settings.dev_print("waiting for message confirm to be clickable")
            while True:
                try:                
                    WAIT.until(EC.element_to_be_clickable((By.CLASS_NAME, MESSAGE_CONFIRM)))
                    Settings.dev_print("message confirm is clickable")
                    break
                except Exception as e:
                    print('uploading...')
                    Driver.error_checker(e)
                    i += 1
                    if i == int(Settings.get_upload_max_duration()):
                        print('Error: Max Upload Time Reached')
                        return False
            Settings.dev_print("getting confirm to click")
            confirm = Driver.get_element_to_click("new_post")
            if Settings.is_debug():
                print('OnlyFans Message: Skipped (debug)')
                Settings.dev_print("### Message Successful (debug) ###")
                Settings.debug_delay_check()
                return True
            Settings.dev_print("clicking confirm")
            confirm.click()
            print('OnlyFans Message: Sent')
            Settings.dev_print("### Message Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failure to Confirm Message")
            Settings.dev_print("### Message Failure ###")
            return False

    @staticmethod
    def message_files(files=[]):
        if len(files) == 0: return True
        try:
            print("Uploading file(s): {}".format(len(files)))
            Settings.dev_print("uploading files")
            Driver.upload_files(files=files)
            Settings.maybe_print("file(s) Entered")
            Settings.debug_delay_check()
            return True
        except Exception as e:
            print(e)
            Driver.error_checker(e)
            print("Error: Failure to Upload File(s)")
            return False

    @staticmethod
    def message_price(price):
        try:
            if not price or price == None or str(price) == "None":
                print("Error: Missing Price")
                return False
            print("Enter price: {}".format(price))
            Settings.dev_print("waiting for price area to enter price")
            priceElement = WebDriverWait(Driver.BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ONLYFANS_PRICE2)))
            Settings.dev_print("entering price")
            priceElement.click()
            actions = ActionChains(Driver.BROWSER)
            actions.send_keys(str(price)) 
            actions.perform()
            Settings.dev_print("entered price")
            # Settings.debug_delay_check()
            Settings.dev_print("saving price")
            Driver.get_element_to_click("priceClick").click()    
            Settings.dev_print("saved price")
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
            Settings.dev_print("finding text area")
            message = Driver.find_element_by_name("messageText")     
            # message = Driver.BROWSER.find_element_by_name("message")     
            Settings.dev_print("entering text")
            message.send_keys(str(text))
            Settings.dev_print("entered text")
            return True
        except Exception as e:
            print(e)
            Driver.error_checker(e)
            print("Error: Failure to Enter Message")
            return False

    @staticmethod
    def message_user_by_id(user_id=None):
        user_id = str(user_id).replace("@u","").replace("@","")
        if not user_id or user_id == None or str(user_id) == "None":
            print("Warning: Missing User ID")
            return False
        try:
            auth_ = Driver.auth()
            if not auth_: return False
            Driver.go_to_page("{}/{}".format(ONLYFANS_CHAT_URL, user_id))
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failure to Goto User - {}".format(user_id))
            return False

    @staticmethod
    def message_user(username=None, user_id=None):
        auth_ = Driver.auth()
        if not auth_: return None
        if user_id: return Driver.message_user_by_id(user_id=user_id)
        if not username:
            print("Error: Missing Username to Message")
            return False
        try:
            Driver.go_to_page(username)
            elements = Driver.BROWSER.find_elements_by_tag_name("a")
            ele = [ele for ele in elements
                    if "/my/chats/chat/" in str(ele.get_attribute("href"))]
            if len(ele) == 0: 
                print("Warning: User Cannot Be Messaged")
                return False
            ele = ele[0]
            Settings.dev_print("clicking send message")
            ele.click()
            Settings.dev_print("messaging username: {}".format(username))
        except Exception as e:
            print(e)
            Driver.error_checker(e)
            print("Error: Failed to Message User")
            return False
        return True

    ####################################################################################################
    ####################################################################################################
    ####################################################################################################

    # tries both and throws error for not found element internally
    @staticmethod
    def open_more_options():
        def option_one():
            # click on '...' element
            Settings.dev_print("opening options (1)")
            moreOptions = Driver.get_element_to_click("moreOptions")
            if not moreOptions: return False    
            moreOptions.click()
            return True
        def option_two():
            # click in empty space
            Settings.dev_print("opening options (2)")
            moreOptions = Driver.BROWSER.find_element_by_id(ONLYFANS_POST_TEXT_ID)
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
    def poll(poll=None):
        if not poll:
            print("Error: Missing Poll")
            return False
        auth_ = Driver.auth()
        if not auth_: return False
        Settings.dev_print("poll")
        poll.get()
        duration = poll.duration
        questions = poll.questions
        try:
            print("Poll:")
            print("- Duration: {}".format(duration))
            print("- Questions:\n> {}".format("\n> ".join(questions)))
            # make sure the extra options are shown
            Driver.open_more_options()
            # add a poll
            Settings.dev_print("adding poll")
            Driver.get_element_to_click("poll").click()
            # open the poll duration
            Settings.dev_print("adding duration")
            Driver.get_element_to_click("pollDuration").click()
            # click on the correct duration number
            Settings.dev_print("setting duration")
            # nums = Driver.BROWSER.find_elements_by_class_name(Element.get_element_by_name("pollDurations").getClass())
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
                if ">1<" in str(inner) and int(duration) == 1: num.click()
                if ">3<" in str(inner) and int(duration) == 3: num.click()
                if ">7<" in str(inner) and int(duration) == 7: num.click()
                if ">30<" in str(inner) and int(duration) == 30: num.click()
                if ">o limit<" in str(inner) and int(duration) == 99: num.click()
            # save the duration
            Settings.dev_print("saving duration")
            Driver.get_element_to_click("pollSave").click()
            Settings.dev_print("saved duration")
            # add extra question space
            if len(questions) > 2:
                for question in questions[2:]:
                    Settings.dev_print("adding question")
                    question_ = Driver.get_element_to_click("pollQuestionAdd").click()
                    Settings.dev_print("added question")
            # find the question inputs
            Settings.dev_print("locating question paths")
            questions_ = Driver.BROWSER.find_elements_by_xpath(POLL_INPUT_XPATH)
            Settings.dev_print("question paths: {}".format(len(questions_)))
            # enter the questions
            i = 0
            # print("questions: {}".format(questions))
            for question in list(questions):
                Settings.dev_print("entering question: {}".format(question))
                questions_[i].send_keys(str(question))
                Settings.dev_print("entered question")
                time.sleep(1)
                i+=1
            Settings.debug_delay_check()
            if Settings.is_debug():
                print("Skipping: Poll (debug)")
                cancel = Driver.get_element_to_click("pollCancel")
                cancel.click()
                Settings.dev_print("canceled poll")
            else:
                print("Poll Entered")
            Settings.dev_print("### Poll Successful ###")
            time.sleep(3)
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failed to Enter Poll")
            return False

    ################
    ##### Post #####
    ################

    @staticmethod
    def post(message=None):
        if not message:
            print("Error: Missing Message")
            return False
        auth_ = Driver.auth()
        if not auth_: return False
        Settings.dev_print("posting")
        try:
            Driver.go_to_home()
            # message.get_post()
            files = message.get_files()
            text = message.format_text()
            keywords = message.get_keywords()
            performers = message.get_performers()
            tags = message.get_tags()
            expires = message.get_expiration()
            schedule = message.get_schedule()
            poll = message.get_poll()
            if str(text) == "None": text = ""
            print("Posting:")
            print("- Files: {}".format(len(files)))
            print("- Keywords: {}".format(keywords))
            print("- Performers: {}".format(performers))
            print("- Tags: {}".format(tags))
            print("- Text: {}".format(text))
            print("- Tweeting: {}".format(Settings.is_tweeting()))
            ## Expires, Schedule, Poll
            if expires: Driver.expires(expires)
            if schedule: Driver.schedule(schedule)
            if poll: Driver.poll(poll)
            WAIT = WebDriverWait(Driver.BROWSER, 600, poll_frequency=10)
            ## Tweeting
            if Settings.is_tweeting():
                Settings.dev_print("tweeting")
                WAIT.until(EC.element_to_be_clickable((By.XPATH, ONLYFANS_TWEET))).click()
            else:
                Settings.dev_print("not tweeting")
            ## Files
            successful_upload = False
            try:
                Settings.dev_print("uploading files")
                successful_upload = Driver.upload_files(files) or False
            except Exception as e:
                print(e)
            ## Text
            successful_text = Driver.enter_text(text)
            if not successful_text:
                print("Error: Unable to Enter Text")
                return False
            ## Confirm
            i = 0
            while successful_upload:
                try:
                    WebDriverWait(Driver.BROWSER, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.CLASS_NAME, SEND_BUTTON_CLASS)))
                    Settings.dev_print("upload complete")
                    break
                except Exception as e:
                    # try: 
                    #     # check for existence of "thumbnail is fucked up" modal and hit ok button
                    #     # haven't seen in long enough time to properly add
                    #     Driver.BROWSER.switchTo().frame("iframe");
                    #     Driver.BROWSER.find_element_by_class("g-btn m-rounded m-border").send_keys(Keys.ENTER)
                    #     print("Error: Thumbnail Missing")
                    #     break
                    # except Exception as ef:
                    #     Settings.maybe_print(ef)
                    print('uploading...')
                    Driver.error_checker(e)
                    i+=1
                    if i == int(Settings.get_upload_max_duration()) and not Settings.is_force_upload():
                        print('Error: Max Upload Time Reached')
                        return False
            try:
                send = Driver.get_element_to_click("new_post")
                if send:
                    Settings.debug_delay_check()
                    if Settings.is_debug():
                        print('Skipped: OnlyFans Post (debug)')
                        Settings.dev_print("### Post Maybe Successful ###")
                        return True
                    Settings.dev_print("confirming upload")
                    send.click()
                else:
                    Settings.maybe_print("Error: Unable to locate 'Send Post' button")
                    return False
            except Exception as e:
                print("Error: Unable to Send Post")
                Settings.dev_print(e)
                return False
            # send[1].click() # the 0th one is disabled
            Settings.dev_print("### Post Successful ###")
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
    def promotional_trial_link(promotion=None):
        if not promotion:
            print("Error: Missing Promotion")
            return False
        auth_ = Driver.auth()
        if not auth_: return False
        # go to onlyfans.com/my/subscribers/active
        try:
            promotion.get()
            limit = promotion.limit
            expiration = promotion.expiration
            months = promotion.months
            user = promotion.user
            Settings.maybe_print("goto -> /my/promotions")
            Driver.BROWSER.get(('https://onlyfans.com/my/promotions'))
            Settings.dev_print("creating promotional trial")
            Driver.get_element_to_click("promotionalTrial").click()
            # limit dropdown
            Settings.dev_print("setting trial count")
            limitDropwdown = Driver.find_element_by_name("promotionalTrialCount")
            for n in range(11): # 11 max subscription limits
                limitDropwdown.send_keys(str(Keys.UP))
            Settings.debug_delay_check()
            if int(limit) == 99: limit = 1
            for n in range(int(limit)-1):
                limitDropwdown.send_keys(Keys.DOWN)
            Settings.debug_delay_check()
            # expiration dropdown
            Settings.dev_print("settings trial expiration")
            expirationDropdown = Driver.find_element_by_name("promotionalTrialExpiration")
            for n in range(11): # 31 max days
                expirationDropdown.send_keys(str(Keys.UP))
            Settings.debug_delay_check()
            if int(expiration) == 99: expiration = 1
            for n in range(int(expiration)-1):
                expirationDropdown.send_keys(Keys.DOWN)
            Settings.debug_delay_check()
            # months dropdown
            Settings.dev_print("settings trial months")
            durationDropwdown = Driver.find_element_by_name("promotionalTrialDuration")
            for n in range(11): # 32 max months
                durationDropwdown.send_keys(str(Keys.UP))
            Settings.debug_delay_check()
            if int(months) == 99: months = 1
            for n in range(int(months)-1):
                durationDropwdown.send_keys(Keys.DOWN)
            Settings.debug_delay_check()
            # find and click promotionalTrialConfirm
            if Settings.is_debug():
                Settings.dev_print("finding trial cancel")
                Driver.get_element_to_click("promotionalTrialCancel").click()
                print("Skipping: Promotion (debug)")
                Settings.dev_print("Successful trial cancellation")
                return True
            Settings.dev_print("finding trial save")
            save_ = Driver.get_element_to_click("promotionalTrialConfirm")
            Settings.dev_print("saving promotion")
            save_.click()
            Settings.dev_print("promotion saved")
            Settings.dev_print("copying trial link")
            Driver.find_element_by_name("promotionalTrialLink").click()
            Settings.dev_print("copied trial link")

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

            Settings.dev_print("Successful Promotion")
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failed to Apply Promotion")
            return None

    @staticmethod
    def promotion_user_directly(promotion=None):
        if not promotion:
            print("Error: Missing Promotion")
            return False
        auth_ = Driver.auth()
        if not auth_: return False
        # go to onlyfans.com/my/subscribers/active
        promotion.get()
        expiration = promotion.expiration
        months = promotion.duration
        user = promotion.user
        message = promotion.message
        if int(expiration) > int(Settings.get_discount_max_amount()):
            print("Warning: Discount Too High, Max -> {}%".format(Settings.get_discount_max_amount()))
            discount = Settings.get_discount_max_amount()
        elif int(expiration) > int(Settings.get_discount_min_amount()):
            print("Warning: Discount Too Low, Min -> {}%".format(Settings.get_discount_min_amount()))
            discount = Settings.get_discount_min_amount()
        if int(months) > int(Settings.get_discount_max_months()):
            print("Warning: Duration Too High, Max -> {} days".format(Settings.get_discount_max_months()))
            months = Settings.get_discount_max_months()
        elif int(months) < int(Settings.get_discount_min_months()):
            print("Warning: Duration Too Low, Min -> {} days".format(Settings.get_discount_min_months()))
            months = Settings.get_discount_min_months()
        try:
            Settings.maybe_print("goto -> /{}".format(user.username))
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
            Settings.dev_print("entering expiration")
            for n in range(11):
                expirations.send_keys(str(Keys.UP))
            for n in range(round(int(expiration)/5)-1):
                expirations.send_keys(Keys.DOWN)
            Settings.dev_print("entered expiration")
            Settings.dev_print("entering duration")
            for n in range(11):
                durations.send_keys(str(Keys.UP))
            for n in range(int(months)-1):
                durations.send_keys(Keys.DOWN)
            Settings.dev_print("entered duration")
            Settings.debug_delay_check()
            Settings.dev_print("entering message")
            message.clear()
            message.send_keys(message)
            Settings.dev_print("entered message")
            Settings.dev_print("applying discount")
            save = Driver.find_element_by_name("promotionalTrialApply")
            if Settings.is_debug():
                Driver.find_element_by_name("promotionalTrialCancel").click()
                print("Skipping: Save Discount (Debug)")
                Settings.dev_print("### Discount Successfully Canceled ###")
                cancel.click()
                return True
            save.click()
            print("Discounted User: {}".format(user.username))
            Settings.dev_print("### User Discount Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            try:
                Driver.find_element_by_name("promotionalTrialCancel").click()
                Settings.dev_print("### Discount Successful Failure ###")
                return False
            except Exception as e:
                Driver.error_checker(e)
            Settings.dev_print("### Discount Failure ###")
            return False

    ######################################################################

    @staticmethod
    def read_user_messages(user):
        auth_ = Driver.auth()
        if not auth_: return False
        try:
            # go to onlyfans.com/my/subscribers/active
            Driver.message_user(user)
            messages_from_ = Driver.find_elements_by_name("messagesFrom")
            # print("first message: {}".format(messages_to_[0].get_attribute("innerHTML")))
            # messages_to_.pop(0) # drop self user at top of page
            messages_all_ = Driver.find_elements_by_name("messagesAll")
            messages_all = []
            messages_to = []
            messages_from = []
            # timestamps_ = Driver.BROWSER.find_elements_by_class_name("b-chat__message__time")
            # timestamps = []
            # for timestamp in timestamps_:
                # Settings.maybe_print("timestamp1: {}".format(timestamp))
                # timestamp = timestamp["data-timestamp"]
                # timestamp = timestamp.get_attribute("innerHTML")
                # Settings.maybe_print("timestamp: {}".format(timestamp))
                # timestamps.append(timestamp)
            for message in messages_all_:
                Settings.maybe_print("all: {}".format(message.get_attribute("innerHTML")))
                messages_all.append(message.get_attribute("innerHTML"))
            messages_and_timestamps = []
            # messages_and_timestamps = [j for i in zip(timestamps,messages_all) for j in i]
            # Settings.maybe_print("Chat Log:")
            # for f in messages_and_timestamps:
                # Settings.maybe_print(": {}".format(f))
            for message in messages_from_:
                # Settings.maybe_print("from1: {}".format(message.get_attribute("innerHTML")))
                message = message.find_element_by_class_name(ONLYFANS_MESSAGES)
                Settings.maybe_print("from: {}".format(message.get_attribute("innerHTML")))
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
                    # Settings.maybe_print("to_: {}".format(message))
                    # messages_to[i] = [timestamps[i], message]
                    # messages_to[i] = message
                    messages_to.append(message)
                    # Settings.maybe_print("to_: {}".format(messages_to[i]))
                # elif from_:
                    # Settings.maybe_print("from_: {}".format(message))
                    # messages_from[i] = [timestamps[i], message]
                    # messages_from[i] = message
                    # Settings.maybe_print("from_: {}".format(messages_from[i]))
                i += 1
            Settings.maybe_print("to: {}".format(messages_to))
            Settings.maybe_print("from: {}".format(messages_from))
            Settings.maybe_print("Messages From: {}".format(len(messages_from)))
            Settings.maybe_print("Messages To: {}".format(len(messages_to)))
            Settings.maybe_print("Messages All: {}".format(len(messages_all)))
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
        if not Driver.BROWSER or Driver.BROWSER == None:
            print('OnlyFans Not Open, Skipping Reset')
            return True
        try:
            Driver.BROWSER.get(ONLYFANS_HOME_URL)
            print('OnlyFans Reset')
            return True
        except Exception as e:
            Driver.error_checker(e)
            print('Error: Failure Resetting OnlyFans')
            return False

    ####################
    ##### Schedule #####
    ####################

    @staticmethod
    def schedule(theSchedule=None):
        if not theSchedule:
            print("Error: Missing Schedule")
            return False
        auth_ = Driver.auth()
        if not auth_: return False
        try:
            theSchedule.get()
            month_ = theSchedule.month
            day_ = theSchedule.day
            year_ = theSchedule.year
            hour_ = theSchedule.hour
            minute_ = theSchedule.minute
            today = datetime.now()
            Settings.dev_print("today: {} {}".format(today.strftime("%B"), today.strftime("%Y")))
            date__ = datetime.strptime(str(theSchedule.date), "%Y-%m-%d %H:%M:%S")
            if date__ < today:
                print("Error: Unable to Schedule Earlier Date")
                return False
            print("Schedule:")
            print("- Date: {}".format(theSchedule.date))
            print("- Time: {}".format(theSchedule.time))
            Driver.open_more_options()
            # click schedule
            Settings.dev_print("adding schedule")
            Driver.get_element_to_click("scheduleAdd").click()
            # find and click month w/ correct date
            while True:
                Settings.dev_print("getting date")
                existingDate = Driver.find_element_by_name("scheduleDate").get_attribute("innerHTML")
                Settings.dev_print("date: {} - {} {}".format(existingDate, month_, year_))
                if str(month_) in str(existingDate) and str(year_) in str(existingDate): break
                else: Driver.get_element_to_click("scheduleNextMonth").click()
            # set day in month
            Settings.dev_print("setting days")
            days = Driver.find_elements_by_name("scheduleDays")
            for day in days:
                inner = day.get_attribute("innerHTML").replace("<span><span>","").replace("</span></span>","")
                if str(day_) == str(inner):
                    day.click()
                    Settings.dev_print("clicked day")
            Settings.debug_delay_check()
            # save schedule date
            saves = Driver.get_element_to_click("scheduleSave")
            Settings.dev_print("found save button, clicking")
            saves.click()
            Settings.dev_print("clicked save button")
            # set hours
            Settings.dev_print("setting hours")
            hours = Driver.find_elements_by_name("scheduleHours")
            for hour in hours:
                inner = hour.get_attribute("innerHTML")
                if str(hour_) in str(inner) and hour.is_enabled():
                    hour.click()
                    Settings.dev_print("hours set")
            # set minutes
            Settings.dev_print("setting minutes")
            minutes = Driver.find_elements_by_name("scheduleMinutes")
            for minute in minutes:
                inner = minute.get_attribute("innerHTML")
                if str(minute_) in str(inner) and minute.is_enabled():
                    minute.click()
                    Settings.dev_print("minutes set")
            # save time
            Settings.dev_print("saving schedule")
            Settings.debug_delay_check()
            if Settings.is_debug():
                print("Skipping: Schedule (debug)")
                Driver.get_element_to_click("scheduleCancel").click()
                Settings.dev_print("canceled schedule")
            else:
                Driver.get_element_to_click("scheduleSave").click()
                Settings.dev_print("saved schedule")
                print("Schedule Entered")
            Settings.dev_print("### Schedule Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failed to Enter Schedule")
            return False

    ####################
    ##### Settings #####
    ####################

    # gets all settings from whichever page its on
    # or get a specific setting
    # probably just way easier and resourceful to do it all at once
    # though it would be ideal to also be able to update individual settings without risking other settings

    @staticmethod
    def sync_from_settings_page(page=None):
        auth_ = Driver.auth()
        if not auth_: return False
        print("Getting Settings: {}".format(page))
        from .profile import Profile
        try:
            variables = Profile.get_variables_for_page(page)
            Settings.dev_print("going to settings page: {}".format(page))
            Driver.go_to_settings(page)
            Settings.dev_print("reached settings: {}".format(page))
            data = Profile({})
            for var in variables:
                name = var[0]
                page_ = var[1]
                type_ = var[2]
                status = None
                Settings.dev_print("searching: {} - {}".format(name, type_))
                try:
                    element = Driver.find_element_by_name(name)
                    Settings.dev_print("Successful ele: {}".format(name))
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
                if status is not None: Settings.dev_print("Successful value: {}".format(status))
                Settings.maybe_print("{} : {}".format(name, status))
                data[name] = status
            Settings.dev_print("Successfully got settings page: {}".format(page))
            print("Settings Page Retrieved: {}".format(page))
            return data
        except Exception as e:
            Driver.error_checker(e)

    # goes through the settings and get all the values
    # @staticmethod
    # def settings_get_all():
    #     auth_ = Driver.auth()
    #     if not auth_: return False
    #     print("Getting All Settings")
    #     profile = Profile({})
    #     try:
    #         pages = Profile.get_pages()
    #         for page in pages:
    #             data = Driver.sync_from_settings_page(page)
    #             for key, value in data:
    #                 profile[key] = value
    #         Settings.dev_print("Successfully got settings")
    #         print("Settings Retrieved")
    #     except Exception as e:
    #         Driver.error_checker(e)
    #     return profile

    # goes through each page and sets all the values
    @staticmethod
    def sync_to_settings_page(Profile, page):
        auth_ = Driver.auth()
        if not auth_: return False
        print("Updating Page Settings: {}".format(page))
        from .profile import Profile
        try:
            variables = Profile.get_variables_for_page(page)
            Settings.dev_print("going to settings page: {}".format(page))
            Driver.go_to_settings(page)
            Settings.dev_print("reached settings: {}".format(page))
            for var in variables:
                name = var[0]
                page_ = var[1]
                type_ = var[2]
                status = None
                Settings.dev_print("searching: {} - {}".format(name, type_))
                try:
                    element = Driver.find_element_by_name(name)
                    Settings.dev_print("Successful ele: {}".format(name))
                except Exception as e:
                    Driver.error_checker(e)
                    continue
                if str(type_) == "text":
                    element.send_keys(Profile.get(name))
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
                    element.send_keys(Profile.get(name))
                elif str(type_) == "file":
                    element.send_keys(Profile.get(name))
                elif str(type_) == "checkbox":
                    element.click()
                # Settings.dev_print("Successful value: {}".format(status))
            Driver.settings_save(page=page)
            Settings.dev_print("Successfully set settings page: {}".format(page))
            print("Settings Page Updated: {}".format(page))
        except Exception as e:
            Driver.error_checker(e)

    # @staticmethod
    # def settings_set_all(Profile):
    #     auth_ = Driver.auth()
    #     if not auth_: return False
    #     print("Updating All Settings")
    #     try:
    #         pages = Profile.TABS
    #         for page in pages:
    #             Driver.sync_to_settings_page(Profile, page)
    #         Settings.dev_print("Successfully set settings")
    #         print("Settings Updated")
    #     except Exception as e:
    #         Driver.error_checker(e)

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
    def settings_save(page=None):
        if str(page) not in ["profile", "account", "security"]:
            Settings.dev_print("not saving: {}".format(page))
            return
        try:
            Settings.dev_print("saving: {}".format(page))
            element = Driver.find_element_by_name("profileSave")
            Settings.dev_print("derp")
            element = Driver.get_element_to_click("profileSave")
            Settings.dev_print("found page save")
            if Settings.is_debug():
                print("Skipping: Save (debug)")
            else:
                Settings.dev_print("saving page")
                element.click()
                Settings.dev_print("page saved")
        except Exception as e:
            Driver.error_checker(e)

    @staticmethod
    def spawn_browser():      
        if Driver.BROWSER: return True
        print("Spawning Browser")
        driver = None

        def google():
            try:
                options = webdriver.ChromeOptions()
                options.add_argument("--no-sandbox") # Bypass OS security model
                options.add_argument("--disable-setuid-sandbox")
                options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems
                options.add_argument("--disable-gpu") # applicable to windows os only
                if not Settings.is_show_window():
                    options.add_argument('--headless')
                    # options.add_argument('--disable-smooth-scrolling')
                    # options.add_argument('--disable-software-rasterizer')
                #
                # options.add_argument("--disable-extensions") # disabling extensions
                # options.add_argument("--disable-infobars") # disabling infobars
                # options.add_argument("--start-maximized")
                # options.add_argument("--window-size=1920,1080")
                # options.add_argument("--user-data-dir=/tmp/");
                # options.add_argument('--disable-login-animations')
                # options.add_argument('--disable-modal-animations')
                # options.add_argument('--disable-sync')
                # options.add_argument('--disable-background-networking')
                # options.add_argument('--disable-web-resources')
                # options.add_argument('--ignore-certificate-errors')
                # options.add_argument('--disable-logging')
                # options.add_argument('--no-experiments')
                # options.add_argument('--incognito')
                # options.add_argument('--user-agent=MozillaYerMomFox')
                options.add_argument("--remote-debugging-address=localhost")
                options.add_argument("--remote-debugging-port=9222")
                #
                # options.add_experimental_option("prefs", {
                  # "download.default_directory": str(DOWNLOAD_PATH),
                  # "download.prompt_for_download": False,
                  # "download.directory_upgrade": True,
                  # "safebrowsing.enabled": True
                # })
                # capabilities = {
                #   'browserName': 'chrome',
                #   'chromeOptions':  {
                #     'useAutomationExtension': False,
                #     'forceDevToolsScreenshot': True,
                #     'args': ['--start-maximized', '--disable-infobars']
                #   }
                # }  
                service_args = []
                if Settings.is_debug():
                    service_args = ["--verbose", "--log-path=/var/log/onlysnarf/debug.txt"]
                # desired_capabilities = capabilities
                Settings.dev_print("executable_path: {}".format(chromedriver_binary.chromedriver_filename))
                # options.binary_location = chromedriver_binary.chromedriver_filename
                driver = webdriver.Chrome(executable_path=chromedriver_binary.chromedriver_filename, chrome_options=options, service_args=service_args)
            except Exception as e:
                print(e)
                print("Warning: Missing Chromedriver")

        def firefox():
            try:
                import geckodriver_autoinstaller
                geckodriver_autoinstaller.install()
                # options = webdriver.FirefoxOptions()
                # options.binary_location = "/usr/local/bin/geckodriver"
                driver = webdriver.Firefox(firefox_binary="/usr/local/bin/geckodriver")
            except Exception as e:
                print(e)
                print("Warning: Missing Geckodriver")
                return False

        def remote():
            try:
                from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

                host = Settings.get_remote_host()
                port = Settings.get_remote_port()
                link = 'http://{}:{}/wd/hub'.format(host, port)

                driver = webdriver.Remote(
                   command_executor=link,
                   desired_capabilities=DesiredCapabilities.CHROME)

                # driver = webdriver.Remote(
                #    command_executor=link,
                #    desired_capabilities=DesiredCapabilities.FIREFOX)
            except:
                print(e)
                print("Warning: Unable to connect remotely")

        BROWSER_TYPE = Settings.get_browser_type()

        if BROWSER_TYPE == "remote":
            remote()
        elif BROWSER_TYPE == "google":
            google()
        elif BROWSER_TYPE == "firefox":
            firefox()
        elif BROWSER_TYPE == "auto":
            successful = google()
            if not successful:
                firefox()

        if not driver: 
            print("Error: Unable to spawn browser")
            return

        driver.implicitly_wait(30) # seconds
        driver.set_page_load_timeout(1200)
        print("Browser Spawned")
        Driver.BROWSER = driver
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
    def upload_files(files=[]):
        if Settings.is_skip_download(): 
            print("Skipping Upload (download)")
            return True
        elif Settings.is_skip_upload(): 
            print("Skipping Upload (upload)")
            return True
        if len(files) == 0: return False
        if Settings.is_skip_upload():
            print("Skipping Upload: Disabled")
            return False
        files = files[:int(Settings.get_upload_max())]
        Settings.dev_print("uploading image files: {}".format(len(files)))

        ####

        import threading
        import concurrent.futures

        files_ = []

        def prepare(file):
            uploadable = file.prepare() # downloads if Google_File
            if not uploadable:
                print("Error: Unable to Upload - {}".format(file.get_title()))
            else: files_.append(file)    

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.map(prepare, files)

        ####

        i = 1
        for file in files_:
            print('Uploading: {} - {}/{}'.format(file.get_title(), i, len(files)))
            i += 1
            enter_file = Driver.BROWSER.find_element_by_id("fileupload_photo")
            enter_file.send_keys(str(file.get_path()))
            time.sleep(1)
            Driver.error_window_upload()
            ###
            def fix_filename(file):
                # move file to change its name
                filename = os.path.basename(file.get_path())
                filename = os.path.splitext(filename)[0]
                if "_fixed" in str(filename): return
                Settings.dev_print("fixing filename...")
                filename += "_fixed"
                ext = os.path.splitext(filename)[1].lower()
                Settings.dev_print("{} -> {}.{}".format(os.path.dirname(file.get_path()), filename, ext))
                dst = "{}/{}.{}".format(os.path.dirname(file), filename, ext)
                shutil.move(file.get_path(), dst)
                file.path = dst
                # add file to end of list so it gets retried
                files.append(file)
                # if this doesn't force it then it'll loop forever without a stopper
            ###
        # one last final check
        Driver.error_window_upload()
        Settings.debug_delay_check()
        Settings.dev_print("### Files Upload Successful ###")
        return True

    #################
    ##### Users #####
    #################

    # returns list of accounts you follow
    @staticmethod
    def following_get():
        auth_ = Driver.auth()
        if not auth_: return False
        users = []
        try:
            Driver.go_to_page(ONLYFANS_USERS_FOLLOWING_URL)
            count = 0
            while True:
                elements = Driver.BROWSER.find_elements_by_class_name("m-subscriptions")
                if len(elements) == count: break
                print_same_line("({}/{}) scrolling...".format(count, len(elements)))
                count = len(elements)
                Driver.BROWSER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            print()
            elements = Driver.BROWSER.find_elements_by_class_name("m-subscriptions")
            for ele in elements:
                username = ele.find_element_by_class_name("g-user-username").get_attribute("innerHTML").strip()
                name = ele.find_element_by_class_name("g-user-name").get_attribute("innerHTML")
                name = re.sub("<!-*>", "", name)
                name = re.sub("<.*\">", "", name)
                name = re.sub("</.*>", "", name).strip()
                # print("username: {}".format(username))
                # print("name: {}".format(name))
                users.append({"name":name, "username":username}) 
            Settings.maybe_print("Found: {}".format(len(users)))
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failed to Find Subscriptions")
        return users

    # returns list of accounts that follow you
    @staticmethod
    def users_get():
        auth_ = Driver.auth()
        if not auth_: return False
        users = []
        try:
            Driver.go_to_page(ONLYFANS_USERS_ACTIVE_URL)
            count = 0
            while True:
                elements = Driver.BROWSER.find_elements_by_class_name("m-fans")
                if len(elements) == int(count): break
                print_same_line("({}/{}) scrolling...".format(count, len(elements)))
                count = len(elements)
                Driver.BROWSER.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            print()
            elements = Driver.BROWSER.find_elements_by_class_name("m-fans")
            for ele in elements:
                username = ele.find_element_by_class_name("g-user-username").get_attribute("innerHTML").strip()
                name = ele.find_element_by_class_name("g-user-name").get_attribute("innerHTML")
                name = re.sub("<!-*>", "", name)
                name = re.sub("<.*\">", "", name)
                name = re.sub("</.*>", "", name).strip()
                # print("username: {}".format(username))
                # print("name: {}".format(name))
                # start = datetime.strptime(str(datetime.now()), "%m-%d-%Y:%H:%M")
                users.append({"name":name, "username":username}) # ,"id":user_id, "started":start})
            Settings.maybe_print("Found: {}".format(len(users)))
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failed to Find Users")
        return users

    @staticmethod
    def user_get_id(username):
        auth_ = Driver.auth()
        if not auth_: return None
        user_id = None
        try:
            Driver.go_to_page(username)
            time.sleep(3) # this should realistically only fail if they're no longer subscribed but it fails often from loading
            elements = Driver.BROWSER.find_elements_by_tag_name("a")
            ele = [ele.get_attribute("href") for ele in elements
                    if "/my/chats/chat/" in str(ele.get_attribute("href"))]
            if len(ele) == 0: 
                print("Warning: User Cannot Be Messaged")
                return None
            ele = ele[0]
            ele = ele.replace("https://onlyfans.com/my/chats/chat/", "")
            user_id = ele
            Settings.maybe_print("found user id: {}".format(user_id))
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failed to Find User ID")
        return user_id

    ################
    ##### Exit #####
    ################

    @staticmethod
    def exit():
        if Driver.BROWSER == None: return
        if Settings.is_save_users():
            print("Saving and Exiting OnlyFans")
            User.write_users_local()
        else:
            print("Exiting OnlyFans")
        Driver.BROWSER.quit()
        Driver.BROWSER = None
        print("Browser Closed")

##################################################################################

def parse_users(user_ids, starteds, users, usernames):
    # usernames.pop(0)
    # print("My User Id: {}".format(user_ids[0]))
    # user_ids.pop(0)
    Settings.dev_print("user_ids: "+str(len(user_ids)))
    Settings.dev_print("starteds: "+str(len(starteds)))
    useridsFailed = False
    startedsFailed = False
    if len(user_ids) == 0:
        Settings.maybe_print("Warning: Unable to find user ids")
        useridsFailed = True
    if len(starteds) == 0:
        Settings.maybe_print("Warning: Unable to find starting dates")
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
            Settings.maybe_print("Warning: Unable to find user ids")
            useridsFailed = True
        if len(starteds_) == 0:
            Settings.maybe_print("Warning: Unable to find starting dates")
            startedsFailed = True
        # Settings.maybe_print("ids vs starteds vs avatars: "+str(len(user_ids_))+" - "+str(len(starteds_))+" - "+str(len(avatars)))
        Settings.maybe_print("users vs ids vs starteds vs usernames:"+str(len(users))+" - "+str(len(user_ids_))+" - "+str(len(starteds_))+" - "+str(len(usernames)))
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
                # Settings.maybe_print("name: "+str(name))
                # Settings.maybe_print("username: "+str(username))
                # Settings.maybe_print("user_id: "+str(user_id))
                # if str(Settings.get_username()).lower() in str(username).lower():
                #     Settings.maybe_print("(): %s = %s" % (Settings.get_username(), username))
                #     # first user is always active user but just in case find it in list of users
                #     Settings.USER_ID = username
                # else:
                users_.append({"name":name, "username":username, "id":user_id, "started":start})
            except Exception as e: Settings.dev_print(e)
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
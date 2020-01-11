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
from OnlySnarf.settings import SETTINGS as settings
from OnlySnarf.element import Element
from OnlySnarf.profile import Profile

###################
##### Globals #####
###################

ONLYFANS_HOME_URL = 'https://onlyfans.com'
ONLYFANS_CHAT_URL = "{}/my/chats/chat".format(ONLYFANS_HOME_URL)
ONLYFANS_SETTINGS_URL = "{}/my/settings".format(ONLYFANS_HOME_URL)
ONLYFANS_USERS_ACTIVE_URL = "{}/my/subscribers/active".format(ONLYFANS_HOME_URL)
LOGIN_FORM = "b-loginreg__form"
SEND_BUTTON_XPATH = "//button[@type='submit' and @class='g-btn m-rounded']"
SEND_BUTTON_CLASS = "g-btn.m-rounded"
SEND_BUTTON_CLASS2 = "button.g-btn.m-rounded"
# Login References
LIVE_BUTTON_CLASS = "b-make-post__streaming-link"
TWITTER_LOGIN0 = "//a[@class='g-btn m-rounded m-flex m-lg']"
TWITTER_LOGIN1 = "//a[@class='g-btn m-rounded m-flex m-lg btn-twitter']"
TWITTER_LOGIN2 = "//a[@class='btn btn-default btn-block btn-lg btn-twitter']"
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
class Driver:

    def __init__(self):
        self.browser = None

    def auth(self):
        logged_in = False
        if not self.browser or self.browser == None: logged_in = self.login()
        else: logged_in = True
        if logged_in == False: print("Error: Failure to Login")
        return logged_in

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
            if tryAll: depth = self.find_element_by_name("usersCount").get_attribute("innerHTML")
            settings.devPrint("scrolling: {}".format(int(int(int(depth)/10)+1)))
            for n in range(int(int(int(depth)/10)+1)):
                settings.maybePrint("scrolling...")
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failed to Find Users")
            return False
        try:
            users = self.find_elements_by_name("discountUsers")
            if int(len(users)) == 0:
                print("Error: Missing Users")
                return False
            print("Discounting User: {} - {}/{}".format(user, depth, len(users)))
            time.sleep(2)
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
            ActionChains(self.browser).move_to_element(user__).perform()
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
                        return self.discount_user(user, depth=depth, discount=discount, months=months, tryAll=True)
            time.sleep(1)
            settings.devPrint("finding months and discount amount btns")
            (months_, discount_) = self.browser.find_elements_by_class_name(DISCOUNT_INPUT)
            settings.devPrint("found months and discount amount")
            # removed in 2.10, inputs changed to above
            # months_ = self.browser.find_element_by_class_name(MONTHS_INPUT)
            # if discount_.get_attribute("value") != "":
                # print("Warning: Existing Discount")
            # discount_.clear()
            settings.devPrint("entering discount amount")
            for n in range(11):
                discount_.send_keys(str(Keys.UP))
            # if str(settings.DEBUG) == "True" and str(settings.DEBUG_DELAY) == "True":
            #     time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
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
            buttons_ = self.find_elements_by_name("discountUserButton")
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
            Driver.error_checker(e)
            buttons_ = self.find_elements_by_name("discountUserButtons")
            for button in buttons_:
                if "Cancel" in button.get_attribute("innerHTML"):
                    button.click()
                    settings.devPrint("### Discount Successful Failure ###")
                    return False
            settings.devPrint("### Discount Failure ###")
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

    @staticmethod
    def error_checker(e):
        if "Unable to locate element" in str(e):
            print("Warning: OnlySnarf may require an update")
        if str(settings.DEBUG) == "True" and str(settings.VERBOSE) == "True":
            print(e)
        elif "Message: " not in str(e):
            settings.maybePrint(e)

    def error_window_upload(self):
        try:
            element = Element.get_element_by_name("errorUpload")
            error_buttons = self.browser.find_elements_by_class_name(element.getClass())
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
            self.open_more_options()
            # open expiration window
            settings.devPrint("adding expiration")
            self.get_element_to_click("expirationAdd").click()
            # select duration
            settings.devPrint("selecting expiration")
            nums = self.find_elements_by_name("expirationPeriods")
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
            settings.devPrint("selected expiration")
            settings.debug_delay_check()
            # save
            if str(settings.DEBUG) == "True" and str(settings.DEBUG_FORCE) == "False":
                print("Skipping: Expiration (debug)")
                settings.devPrint("skipping expiration")
                self.get_element_to_click("expirationCancel").click()
                settings.devPrint("canceled expiration")
                settings.devPrint("### Expiration Successfully Canceled ###")
            else:
                settings.devPrint("saving expiration")
                self.get_element_to_click("expirationSave").click()
                settings.devPrint("saved expiration")
                print("Expiration Entered")
                settings.devPrint("### Expiration Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failed to Enter Expiration")
            try:
                settings.devPrint("canceling expiration")
                self.get_element_to_click("expirationCancel").click()
                settings.devPrint("canceled expiration")
                settings.devPrint("### Expiration Successful Failure ###")
            except: 
                settings.devPrint("### Expiration Failure Failure")
            return False

    ###################################

    # should already be logged in
    def find_element_by_name(self, name):
        if self.browser == None: return False
        element = Element.get_element_by_name(name)
        if not element:
            print("Error: Unable to find Element Reference")
            return False
        for className in element.getClasses():
            ele = None
            eleCSS = None
            try: ele = self.browser.find_element_by_class_name(className)
            except: ele = None
            try: eleCSS = self.browser.find_element_by_css_selector(className)
            except: eleCSS = None
            settings.devPrint("class: {} - {}:css".format(ele, eleCSS))
            if ele: return ele
            if eleCSS: return eleCSS
        raise Exception("Error: Unable to Locate Element")

    def find_elements_by_name(self, name):
        if self.browser == None: return False
        element = Element.get_element_by_name(name)
        if not element:
            print("Error: Unable to find Element Reference")
            return False
        eles = []
        for className in element.getClasses():
            eles_ = []
            elesCSS_ = []
            try: eles_ = self.browser.find_elements_by_class_name(className)
            except: eles_ = []
            try: elesCSS_ = self.browser.find_elements_by_css_selector(className)
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

    def get_element_to_click(self, name):
        settings.devPrint("finding click: {}".format(name))
        element = Element.get_element_by_name(name)
        if not element:
            print("Error: Unable to find Element Reference")
            return False
        for className in element.getClasses():
            eles = []
            elesCSS = []
            try: eles = self.browser.find_elements_by_class_name(className)
            except: eles = []
            try: elesCSS = self.browser.find_elements_by_css_selector(className)
            except: elesCSS = []
            settings.devPrint("class: {} - {}:css".format(len(eles), len(elesCSS)))
            eles.extend(elesCSS)
            for i in range(len(eles)):
                # settings.devPrint("ele: {} -> {}".format(eles[i].get_attribute("innerHTML").strip(), element.getText()))
                if (eles[i].is_displayed() and element.getText() and str(element.getText()) == eles[i].get_attribute("innerHTML").strip()) and eles[i].is_enabled():
                    settings.devPrint("found matching ele")
                    # settings.devPrint("found matching ele: {}".format(eles[i].get_attribute("innerHTML").strip()))
                    return eles[i]
                elif (eles[i].is_displayed() and element.getText() and str(element.getText()) == eles[i].get_attribute("innerHTML").strip()):
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

    ###################################

    def go_to_home(self):
        if self.browser == None: return False
        if str(self.browser.current_url) == str(ONLYFANS_HOME_URL):
            settings.maybePrint("at -> onlyfans.com")
        else:
            settings.maybePrint("goto -> onlyfans.com")
            self.browser.get(ONLYFANS_HOME_URL)
            WebDriverWait(self.browser, 60, poll_frequency=6).until(EC.visibility_of_element_located((By.CLASS_NAME, LIVE_BUTTON_CLASS)))

    # onlyfans.com/my/settings
    def go_to_settings(self, settingsTab):
        if self.browser == None: return False
        if str(self.browser.current_url) == str(ONLYFANS_SETTINGS_URL) and str(settingsTab) == "profile":
            settings.maybePrint("at -> onlyfans.com/settings/{}".format(settingsTab))
        else:
            settings.maybePrint("goto -> onlyfans.com/settings/{}".format(settingsTab))
            self.browser.get("{}/{}".format(ONLYFANS_SETTINGS_URL, settingsTab))
            # fix above with correct element to locate

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
        options.add_argument('--disable-gpu')
        # options.setExperimentalOption('useAutomationExtension', false);
        CHROMEDRIVER_PATH = chromedriver_binary.chromedriver_filename
        try:
            self.browser = webdriver.Chrome(chrome_options=options)
        except Exception as e:
            Driver.error_checker(e)
            print("Warning: Missing chromedriver_path, retrying")
            try:
                self.browser = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
            except Exception as e:
                Driver.error_checker(e)
                print("Error: Missing chromedriver_path, exiting")
                try:
                    self.browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH)
                except Exception as e:
                    print(e)
                    print("Super Fucked")
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
                WebDriverWait(self.browser, 120, poll_frequency=6).until(EC.visibility_of_element_located((By.CLASS_NAME, Element.get_element_by_name("loginCheck").getClass())))
                print("OnlyFans Login Successful")
                return True
            except TimeoutException as te:
                settings.devPrint(te)
                print("Login Failure: Timed Out! Please check your Twitter credentials.")
                print(": If the problem persists, OnlySnarf may require an update.")
            except Exception as e:
                Driver.error_checker(e)
                print("Login Failure: OnlySnarf may require an update")
            return False
        except Exception as e:
            Driver.error_checker(e)
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
                    Driver.error_checker(e)
                    i += 1
                    if i == int(settings.UPLOAD_MAX_DURATION) and settings.FORCE_UPLOAD is not True:
                        print('Error: Max Upload Time Reached')
                        return False
            confirm = self.get_element_to_click("new_post")
            # confirm = WebDriverWait(self.browser, 60, poll_frequency=10).until(EC.element_to_be_clickable((By.CLASS_NAME, MESSAGE_CONFIRM)))
            if str(settings.DEBUG) == "True":
                if str(settings.DEBUG_DELAY) == "True":
                    time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
                print('OnlyFans Message: Skipped (debug)')
                settings.devPrint("### Message Maybe Successful ###")
                return True
            confirm.click()
            print('OnlyFans Message: Sent')
            settings.devPrint("### Message Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failure to Confirm Message")
            settings.devPrint("### Message Failure ###")
            return False

    def message_image(self, path):
        try:
            if not path or path == None or str(path) == "None":
                print("Error: Missing Image(s)")
                return False
            print("Enter image(s): {}".format(path))
            try:
                self.upload_image_files(name="uploadImageMessage", path=path)
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

    def message_price(self, price):
        try:
            if not price or price == None or str(price) == "None":
                print("Error: Missing Price")
                return False
            print("Enter price: {}".format(price))
            priceElement = WebDriverWait(self.browser, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ONLYFANS_PRICE2)))
            settings.devPrint("entering price")
            priceElement.click()
            actions = ActionChains(self.browser)
            actions.send_keys(str(price)) 
            actions.perform()
            settings.devPrint("entered price")
            # settings.debug_delay_check()
            settings.devPrint("saving price")
            self.get_element_to_click("priceClick").click()    
            settings.devPrint("saved price")
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failure to Enter Price")
            return False

    def message_text(self, text):
        try:
            if not text or text == None or str(text) == "None":
                print("Error: Missing Text")
                return False
            print("Enter text: {}".format(text))
            message = self.find_element_by_name("messageText")        
            message.send_keys(str(text))
            settings.maybePrint("Text Entered")
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failure to Enter Message")
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
            Driver.error_checker(e)
            print("Error: Failure to Goto User - {}/{}".format(user.id, user.username))
            return False

    # tries both and throws error for not found element internally
    def open_more_options(self):
        def option_one():
            # click on '...' element
            settings.devPrint("opening options (1)")
            moreOptions = self.get_element_to_click("moreOptions")
            if not moreOptions: return False    
            moreOptions.click()
            return True
        def option_two():
            # click in empty space
            settings.devPrint("opening options (2)")
            moreOptions = self.browser.find_element_by_id(ONLYFANS_POST_TEXT_ID)
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
            self.open_more_options()
            # add a poll
            settings.devPrint("adding poll")
            self.get_element_to_click("poll").click()
            # open the poll duration
            settings.devPrint("adding duration")
            self.get_element_to_click("pollDuration").click()
            # click on the correct duration number
            settings.devPrint("setting duration")
            # nums = self.browser.find_elements_by_class_name(Element.get_element_by_name("pollDurations").getClass())
            nums = self.find_elements_by_name("pollDurations")
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
            self.get_element_to_click("pollSave").click()
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
            if str(settings.DEBUG) == "True" and str(settings.DEBUG_FORCE) == "False":
                print("Skipping: Poll (debug)")
                cancel = self.get_element_to_click("pollCancel")
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
            send = self.get_element_to_click("new_post")
            settings.debug_delay_check()
            if str(settings.DEBUG) == "True":
                print('Skipped: OnlyFans Post (debug)')
                settings.devPrint("### Post Maybe Successful ###")
                return True
            settings.devPrint("sending post")
            send.click()
            # send[1].click() # the 0th one is disabled
            print('OnlyFans Post Complete')
            settings.devPrint("### Post Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: OnlyFans Post Failure")
            settings.devPrint("### Post Failure ###")
            return False

    ######################
    ##### Promotions #####
    ######################

    # or email
    def promotional_trial_link(self):
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
            Driver.error_checker(e)
            print("Error: Failed to Apply Promotion")
            return None

    def read_user_messages(self, user):
        try:
            auth_ = self.auth()
            if not auth_: return False
            # go to onlyfans.com/my/subscribers/active
            self.message_user(user)
            messages_from_ = self.find_elements_by_name("messagesFrom")
            # print("first message: {}".format(messages_to_[0].get_attribute("innerHTML")))
            # messages_to_.pop(0) # drop self user at top of page
            messages_all_ = self.find_elements_by_name("messagesAll")
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
            Driver.error_checker(e)
            print("Error: Failure to Read Chat - {}".format(user.username))
            return [[],[],[]]

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
            Driver.error_checker(e)
            print('Error: Failure Resetting OnlyFans')
            return False

    ####################
    ##### Settings #####
    ####################

    # has save:
    # profile
    # account
    # security

    # doesn't have save:
    # story
    # notifications
    # other

    # goes through the settings and get all the values
    def settings_get_all(self):
         # find the var from the list of var names in settingsVariables
        settingsVariables = Profile.get_settings_variables()
        for var in settingsVariables:
            name = var[0]
            page_ = var[1]
            type_ = var[2]
            settings.devPrint("going to settings page: {}".format(page_))
            self.go_to_settings(page_)
            settings.devPrint("reached settings: {}".format(page_))
            element = self.find_element_by_name(name)
            settings.devPrint("getting gotten of type: {}".format(type_))
            status = ""
            if str(type_) == "text":
                # get attr text
                status = element.get_attribute("innerHTML")
            elif str(type_) == "toggle":
                # get state true|false
                status = element.is_selected()
            elif str(type_) == "dropdown":
                Select(driver.find_element_by_id("mySelectID"))
                status = element.first_selected_option
            elif str(type_) == "list":
                status = element.get_attribute("innerHTML")
            elif str(type_) == "file":
                status = element.get_attribute("innerHTML")
            elif str(type_) == "checkbox":
                status = element.is_selected()
            settings.maybePrint("{} : {}".format(var, status))
            settings.update_value(var, status)

    def settings_set_all(self):
        # goes through each page and sets all the values
        

        # dropdown
        # select by visible text
        select.select_by_visible_text('Banana')
        # select by value 
        select.select_by_value('1')

        self.settings_save()

    def settings_set(self, key, value):
        # find the var from the list of var names in settingsVariables
        var = None
        settingsVariables = Profile.get_settings_variables()
        for key in settingsVariables:
            if str(var) == str(key[0]):
                var = key
        if not var or var == None:
            print("Error: Unable to Find Variable")
            return False
        #
        name = var[0]
        page_ = var[1]
        type_ = var[2]
        settings.devPrint("going to settings page: {}".format(page))
        self.go_to_settings(page_)
        settings.devPrint("reached settings: {}".format(page))
        self.find_element_by_name(name)
        # text, path, state, list (text), price 
        if str(type_) == "text":
            # set attr text
            pass
        elif str(type_) == "toggle":
            # set state == value
            pass
        # other stuff
        self.settings_save()

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
            self.open_more_options()
            # click schedule
            settings.devPrint("adding schedule")
            self.get_element_to_click("scheduleAdd").click()
            # find and click month w/ correct date
            while True:
                settings.devPrint("getting date")
                existingDate = self.find_element_by_name("scheduleDate").get_attribute("innerHTML")
                settings.devPrint("date: {} - {} {}".format(existingDate, month_, year_))
                if str(month_) in str(existingDate) and str(year_) in str(existingDate): break
                else: self.get_element_to_click("scheduleNextMonth").click()
            # set day in month
            settings.devPrint("setting days")
            days = self.find_elements_by_name("scheduleDays")
            for day in days:
                inner = day.get_attribute("innerHTML").replace("<span><span>","").replace("</span></span>","")
                if str(day_) == str(inner):
                    day.click()
                    settings.devPrint("clicked day")
            settings.debug_delay_check()
            # save schedule date
            saves = self.get_element_to_click("scheduleSave").click()
            # set hours
            settings.devPrint("setting hours")
            hours = self.find_elements_by_name("scheduleHours")
            for hour in hours:
                inner = hour.get_attribute("innerHTML")
                if str(hour_) in str(inner) and hour.is_enabled():
                    hour.click()
                    settings.devPrint("hours set")
            # set minutes
            settings.devPrint("setting minutes")
            minutes = self.find_elements_by_name("scheduleMinutes")
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
                self.get_element_to_click("scheduleCancel").click()
                settings.devPrint("canceled schedule")
            else:
                self.get_element_to_click("scheduleSave").click()
                settings.devPrint("saved schedule")
                print("Schedule Entered")
            settings.devPrint("### Schedule Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failed to Enter Schedule")
            return False

    # update chat logs for all users
    def update_chat_logs(self):
        global USER_CACHE_LOCKED
        USER_CACHE_LOCKED = True
        print("Updating User Chats")
        users = self.users_get()
        for user in users:
            self.update_chat_log(user)
        USER_CACHE_LOCKED = False

    def update_chat_log(self, user):
        print("Updating Chat: {} - {}".format(user.username, user.id))
        if not user:
            return print("Error: Missing User")
        user.readChat()


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
            ## Images
            try:
                settings.devPrint("uploading files")
                successful_upload = self.upload_image_files("image_upload", path)
            except Exception as e:
                Driver.error_checker(e)
                print("Error: Unable to Upload Images")
                return False
            ## Text
            successful_text = self.enter_text(text)
            if not successful_text:
                print("Error: Unable to Enter Text")
                return False
            ## Confirm
            i = 0
            while True:
                try:
                    WebDriverWait(self.browser, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.CLASS_NAME, SEND_BUTTON_CLASS)))
                    settings.devPrint("upload complete")
                    break
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
                    Driver.error_checker(e)
                    i+=1
                    if i == int(settings.UPLOAD_MAX_DURATION) and settings.FORCE_UPLOAD is not True:
                        print('Error: Max Upload Time Reached')
                        return False
            try:
                send = self.get_element_to_click("new_post")
                if send:
                    if str(settings.DEBUG) == "True" and str(settings.DEBUG_DELAY) == "True":
                        time.sleep(int(settings.DEBUG_DELAY_AMOUNT))
                    if str(settings.DEBUG) == "True":
                        print('Skipped: OnlyFans Upload (debug)')
                        settings.devPrint("### Upload Maybe Successful ###")
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
            settings.devPrint("### Upload Successful ###")
            print('OnlyFans Upload Complete')
            return True
        except Exception as e:
            Driver.error_checker(e)
            print("Error: OnlyFans Upload Failure")
            return False

    # uploads image into post or message
    def upload_image_files(self, name="image_upload", path=None):
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
            enter_file = self.browser.find_element_by_id(Element.get_element_by_name(str(name)).getId())
            enter_file.send_keys(str(file))
            time.sleep(1)
            self.error_window_upload()
            # if self.error_window_upload(): fix_filename(file)
            
            def fix_filename(file):
                # move file to change its name
                filename = os.path.basename(file)
                filename = os.path.splitext(filename)[0]
                if "_fixed" in str(filename): return
                print("Fixing Filename")
                filename += "_fixed"
                ext = os.path.splitext(filename)[1].lower()
                print("{} -> {}.{}".format(os.path.dirname(file), filename, ext))
                dst = "{}/{}.{}".format(os.path.dirname(file), filename, ext)
                shutil.move(file, dst)
                # add file to end of list so it gets retried
                files.append(dst)
                # if this doesn't force it then it'll loop forever without a stopper

            # time.sleep(1)
         ## Wait for Confirm
        self.error_window_upload()
        settings.debug_delay_check()
        settings.devPrint("files uploaded")
        return True

    #################
    ##### Users #####
    #################

    def users_get(self):
        auth_ = self.auth()
        if not auth_: return False
        try:
            if str(self.browser.current_url) == str(ONLYFANS_USERS_ACTIVE_URL):
                settings.maybePrint("at -> /my/subscribers/active")
            else:
                settings.maybePrint("goto -> /my/subscribers/active")
                self.browser.get(ONLYFANS_USERS_ACTIVE_URL)
                num = self.find_element_by_name("usersCount").get_attribute("innerHTML")
                settings.maybePrint("User count: {}".format(num))
                for n in range(int(int(int(num)/10)+1)):
                    settings.maybePrint("scrolling...")
                    self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
        except Exception as e:
            Driver.error_checker(e)
            print("Error: Failed to Find Users")
            return []
        # avatars = self.browser.find_elements_by_class_name('b-avatar')
        user_ids = self.find_elements_by_name("usersIds")
        starteds = self.find_elements_by_name("usersStarteds")
        users = self.find_elements_by_name("usersUsers")
        usernames = self.find_elements_by_name("usersUsernames")
        # usernames.pop(0)
        # print("My User Id: {}".format(user_ids[0]))
        # user_ids.pop(0)
        active_users = []
        settings.devPrint("user_ids: "+str(len(user_ids)))
        settings.devPrint("starteds: "+str(len(starteds)))
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
            Driver.error_checker(e)
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










    
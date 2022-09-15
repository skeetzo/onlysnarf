import re
import random
import os
import shutil
import json
import pathlib
import chromedriver_binary
import time
import wget
import pickle
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.file_detector import LocalFileDetector
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from pathlib import Path
##
from ..classes.element import Element
from ..util.config import config
from ..util.settings import Settings

###################
##### Globals #####
###################

# Urls
ONLYFANS_HOME_URL = "https://onlyfans.com"
ONLYFANS_HOME_URL2 = "https://onlyfans.com/"
# ONLYFANS_MESSAGES_URL = "/my/chats/"
ONLYFANS_NEW_MESSAGE_URL = "/my/chats/send"
ONLYFANS_CHAT_URL = "/my/chats/chat/"
ONLYFANS_SETTINGS_URL = "/my/settings/"
ONLYFANS_USERS_ACTIVE_URL = "/my/subscribers/active"
ONLYFANS_USERS_FOLLOWING_URL = "/my/subscriptions/active"
ONLYFANS_LISTS_URL = "/my/lists/"
# ONLYFANS_CHATS_URL_FULL = "{}{}".format(ONLYFANS_HOME_URL, ONLYFANS_CHAT_URL)
# ONLYFANS_LISTS_URL_FULL = "{}{}".format(ONLYFANS_HOME_URL, ONLYFANS_LISTS_URL)

class Driver:
    """Driver class for Selenium management"""

    BROWSER = None
    BROWSERS = []
    #
    DOWNLOADING = True
    DOWNLOADING_MAX = False
    DOWNLOAD_MAX_IMAGES = 1000
    DOWNLOAD_MAX_VIDEOS = 1000
    #
    MAX_TABS = 20
    NOT_INFORMED_KEPT = False # whether or not "Keep"ing the Driver.browser session has been printed once upon exit
    NOT_INFORMED_CLOSED = False # same dumb shit as above

    # selenium web driver
    browser = None
    browsers = []

    # browser tabs cache
    tabs = []
    # OnlyFans discovered lists cache
    lists = []
    # save login state
    logged_in = False
    # web browser session id and url for reconnecting
    session_id = None
    session_url = None

    _initialized_ = False

    def init():
        """
        Initiliaze the web driver aspect.

        Parameters
        ----------
        browser : Selenium.webdriver
            An existing selenium webdriver object / web browser

        """

        if Driver._initialized_: return
        Driver.spawn_browser(Settings.get_browser_type())
        ## Cookies
        if Settings.is_cookies() == "True": Driver.cookies_load()
        Driver.tabs.append([Driver.browser.current_url, Driver.browser.current_window_handle, 0])
        Driver._initialized_ = True

        
    def auth():
        """
        Authorization check

        Logs in with provided runtime creds if not logged in

        Returns
        -------
        bool
            Whether or not the login attempt was successful

        """

        if not Driver.login(): os._exit(1)
        ## Cookies
        if Settings.is_cookies() == "True": Driver.cookies_save()
        return True

    ###################
    ##### Cookies #####
    ###################

    def cookies_load():
        """Loads existing web browser cookies from local source"""

        if os.path.exists(Settings.get_cookies_path()):
            # must be at onlyfans.com to load cookies of onlyfans.com
            Driver.go_to_home()
            file = open(Settings.get_cookies_path(), "rb")
            cookies = pickle.load(file)
            file.close()
            for cookie in cookies:
                Driver.browser.add_cookie(cookie)
            Settings.dev_print("successfully loaded cookies")
            Driver.refresh()
        else: 
            Settings.dev_print("failed to load cookies")
            Settings.dev_print(e)

    def cookies_save():
        """Saves existing web browser cookies to local source"""

        try:
            # must be at onlyfans.com to save cookies of onlyfans.com
            Driver.go_to_home()
            file = open(Settings.get_cookies_path(), "wb")
            pickle.dump(Driver.browser.get_cookies(), file) # "cookies.pkl"
            file.close()
            Settings.dev_print("successfully saved cookies")
        except Exception as e:
            Settings.dev_print("failed to save cookies")
            Settings.dev_print(e)

    ####################
    ##### Discount #####
    ####################

    def discount_user(discount):
        """
        Enter and apply discount to user

        Discount object requires:
        - duration (in months)
        - amount
        - username

        Parameters
        ----------
        discount : classes.Discount
            Discount object that contains or prompts for proper values

        Returns
        -------
        bool
            Whether or not the discount was applied successfully

        """

        if not discount:
            Settings.err_print("missing discount")
            return False
        Settings.dev_print("discounting user...")
        try:
            discount.get()
            months = int(discount.get_months())
            amount = int(discount.get_amount())
            username = str(discount.get_username())
            # ensure username is actually a username
            from ..classes.user import User
            if isinstance(discount.username, User):
                username = discount.username.username
            # check variable constraints
            if int(months) > int(Settings.get_discount_max_months()):
                Settings.warn_print("months too high, max -> {} months".format(Settings.get_discount_max_months()))
                months = int(Settings.get_discount_max_months())
            elif int(months) < int(Settings.get_discount_min_months()):
                Settings.warn_print("months too low, min -> {} months".format(Settings.get_discount_min_months()))
                months = int(Settings.get_discount_min_months())
            if int(amount) > int(Settings.get_discount_max_amount()):
                Settings.warn_print("amount too high, max -> {}%".format(Settings.get_discount_max_months()))
                amount = int(Settings.get_discount_max_amount())
            elif int(amount) < int(Settings.get_discount_min_amount()):
                Settings.warn_print("amount too low, min -> {}%".format(Settings.get_discount_min_months()))
                amount = int(Settings.get_discount_min_amount())
            Settings.print("discounting: {}".format(username))
            Driver.go_to_page(ONLYFANS_USERS_ACTIVE_URL)
            end_ = True
            count = 0
            user_ = None
            Settings.print("searching for user...")
            # scroll through users on page until user is found
            while end_:
                elements = Driver.browser.find_elements_by_class_name("m-fans")
                for ele in elements:
                    username_ = ele.find_element_by_class_name("g-user-username").get_attribute("innerHTML").strip()
                    if str(username) == str(username_).replace("@",""):
                        Driver.browser.execute_script("arguments[0].scrollIntoView();", ele)
                        user_ = ele
                        end_ = False
                if not end_: continue
                if len(elements) == int(count): break
                Settings.print_same_line("({}/{}) scrolling...".format(count, len(elements)))
                count = len(elements)
                Driver.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            Settings.print("")
            Settings.dev_print("successfully found fans")
            if not user_:
                Settings.err_print("unable to find user - {}".format(username))
                return False
            Settings.maybe_print("found: {}".format(username))
            ActionChains(Driver.browser).move_to_element(user_).perform()
            Settings.dev_print("successfully moved to user")
            Settings.dev_print("finding discount btn")
            buttons = user_.find_elements_by_class_name(Element.get_element_by_name("discountUser").getClass())
            clicked = False
            for button in buttons:
                # print(button.get_attribute("innerHTML"))
                if "Discount" in button.get_attribute("innerHTML") and button.is_enabled() and button.is_displayed():
                    try:
                        Settings.dev_print("clicking discount btn")
                        button.click()
                        Settings.dev_print("clicked discount btn")
                        clicked = True
                        break
                    except Exception as e:
                        Driver.error_checker(e)
                        Settings.warn_print("unable to click discount btn for: {}".format(username))
                        return False
            if not clicked:
                Settings.warn_print("unable to find discount btn for: {}".format(username))
                return False
            time.sleep(1)

            def apply_discount():
                Settings.maybe_print("attempting discount entry...")
                Settings.dev_print("finding months and discount amount btns")
                ## amount
                discountEle = Driver.browser.find_elements_by_class_name(Element.get_element_by_name("discountUserAmount").getClass())[0]
                discountAmount = int(discountEle.get_attribute("innerHTML").replace("% discount", ""))
                Settings.dev_print("amount: {}".format(discountAmount))
                Settings.dev_print("entering discount amount")
                if int(discountAmount) != int(amount):
                    up_ = int((discountAmount / 5) - 1)
                    down_ = int((int(amount) / 5) - 1)
                    Settings.dev_print("up: {}".format(up_))
                    Settings.dev_print("down: {}".format(down_))
                    action = ActionChains(Driver.browser)
                    action.click(on_element=discountEle)
                    action.pause(1)
                    for n in range(up_):
                        action.send_keys(Keys.UP)
                        action.pause(0.5)
                    for n in range(down_):
                        action.send_keys(Keys.DOWN)
                        action.pause(0.5)                
                    action.send_keys(Keys.TAB)
                    action.perform()
                Settings.dev_print("successfully entered discount amount")
                ## months
                monthsEle = Driver.browser.find_elements_by_class_name(Element.get_element_by_name("discountUserMonths").getClass())[1]
                monthsAmount = int(monthsEle.get_attribute("innerHTML").replace(" months", "").replace(" month", ""))
                Settings.dev_print("months: {}".format(monthsAmount))
                Settings.dev_print("entering discount months")
                if int(monthsAmount) != int(months):
                    up_ = int(monthsAmount - 1)
                    down_ = int(int(months) - 1)
                    Settings.dev_print("up: {}".format(up_))
                    Settings.dev_print("down: {}".format(down_))
                    action = ActionChains(Driver.browser)
                    action.click(on_element=monthsEle)
                    action.pause(1)
                    for n in range(up_):
                        action.send_keys(Keys.UP)
                        action.pause(0.5)
                    for n in range(down_):
                        action.send_keys(Keys.DOWN)
                        action.pause(0.5)
                    action.send_keys(Keys.TAB)
                    action.perform()
                Settings.dev_print("successfully entered discount months")
                discountEle = Driver.browser.find_elements_by_class_name(Element.get_element_by_name("discountUserAmount").getClass())[0]
                discountAmount = int(discountEle.get_attribute("innerHTML").replace("% discount", ""))
                monthsEle = Driver.browser.find_elements_by_class_name(Element.get_element_by_name("discountUserMonths").getClass())[1]
                monthsAmount = int(monthsEle.get_attribute("innerHTML").replace(" months", "").replace(" month", ""))
                return discountAmount, monthsAmount

            # discount method is repeated until values are correct because somehow it occasionally messes up...
            discountAmount, monthsAmount = apply_discount()
            while int(discountAmount) != int(amount) and int(monthsAmount) != int(months):
                # Settings.print("{} = {}    {} = {}".format(discountAmount, amount, monthsAmount, months))
                discountAmount, monthsAmount = apply_discount()

            Settings.debug_delay_check()
            ## apply
            Settings.dev_print("applying discount")
            buttons_ = Driver.find_elements_by_name("discountUserButton")
            for button in buttons_:
                if not button.is_enabled() and not button.is_displayed(): continue
                if "Cancel" in button.get_attribute("innerHTML") and Settings.is_debug() == "True":
                    Settings.print("skipping save discount (debug)")
                    button.click()
                    Settings.dev_print("successfully canceled discount")
                    Settings.dev_print("### Discount Successful ###")
                    return True
                elif "Cancel" in button.get_attribute("innerHTML") and int(discountAmount) == int(amount) and int(monthsAmount) == int(months):
                    Settings.print("skipping existing discount")
                    button.click()
                    Settings.dev_print("successfully skipped existing discount")
                    Settings.dev_print("### Discount Successful ###")
                    return True
                elif "Apply" in button.get_attribute("innerHTML"):
                    button.click()
                    Settings.print("discounted: {}".format(username))
                    Settings.dev_print("successfully applied discount")
                    Settings.dev_print("### Discount Successful ###")
                    return True
            Settings.dev_print("### Discount Failure ###")
            return False
        except Exception as e:
            Settings.print(e)
            Driver.error_checker(e)
            buttons_ = Driver.find_elements_by_name("discountUserButton")
            for button in buttons_:
                if "Cancel" in button.get_attribute("innerHTML"):
                    button.click()
                    Settings.dev_print("### Discount Successful Failure ###")
                    return False
            Settings.dev_print("### Discount Failure ###")
            return False

    def download_content():
        """Downloads all content (images and video) from the user's profile page"""

        Settings.print("downloading content...")
        def scroll_to_bottom():
            try:
                # go to profile page and scroll to bottom
                Driver.go_to_profile()
                # count number of content elements to scroll to bottom
                num = Driver.browser.find_element_by_class_name("b-profile__sections__count").get_attribute("innerHTML")
                Settings.maybe_print("content count: {}".format(num))
                for n in range(int(int(int(num)/5)+1)):
                    Settings.print_same_line("({}/{}) scrolling...".format(n,int(int(int(num)/5)+1)))
                    Driver.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                Settings.print("")
            except Exception as e:
                Settings.print(e)
                Settings.err_print("failed to find content to scroll")
        scroll_to_bottom()
        imagesDownloaded = Driver.download_images()
        videosDownloaded = Driver.download_videos()
        Settings.print("downloaded content")
        Settings.print("count: {}".format(len(imagesDownloaded)+len(videosDownloaded)))

    def download_images():
        """Downloads all images on the page"""

        imagesDownloaded = []
        try:
            images = Driver.browser.find_elements_by_tag_name("img")
            downloadPath = os.path.join(Settings.get_download_path(), "images")
            Path(downloadPath).mkdir(parents=True, exist_ok=True)
            i=1
            for image in images:
                if Driver.DOWNLOADING_MAX and i > Driver.DOWNLOAD_MAX_IMAGES: break
                src = str(image.get_attribute("src"))
                if not src or src == "" or src == "None" or "/thumbs/" in src or "_frame_" in src or "http" not in src: continue
                Settings.print_same_line("downloading image: {}/{}".format(i, len(images)))
                # Settings.print("Image: {}".format(src[:src.find(".jpg")+4]))
                # Settings.print("Image: {}".format(src))
                if Driver.DOWNLOADING:
                    try:
                        while os.path.isfile("{}/{}.jpg".format(downloadPath, i)):
                            i+=1
                        wget.download(src, "{}/{}.jpg".format(downloadPath, i), False)
                        imagesDownloaded.append(i)
                    except Exception as e: Settings.print(e)
                i+=1
            Settings.print("")
        except Exception as e:
            Settings.print(e)
        return imagesDownloaded

    def download_messages(user="all"):
        """
        Downloads all content in messages with the user

        Parameters
        ----------
        user : str or classes.User
            The user to download message content from

        """

        Settings.print("downloading messages: {}".format(user))
        try:
            if str(user) == "all":
                # from OnlySnarf.classes.user import User
                from ..classes.user import User
                user = random.choice(User.get_all_users())
            Driver.message_user(user.username)
            contentCount = 0
            while True:
                Driver.browser.execute_script("document.querySelector('div[id=chatslist]').scrollTop=1e100")
                time.sleep(1)
                Driver.browser.execute_script("document.querySelector('div[id=chatslist]').scrollTop=1e100")
                time.sleep(1)
                Driver.browser.execute_script("document.querySelector('div[id=chatslist]').scrollTop=1e100")
                time.sleep(1)
                images = Driver.browser.find_elements_by_tag_name("img")
                videos = Driver.browser.find_elements_by_tag_name("video")
                # Settings.print((len(images)+len(videos)))
                if contentCount == len(images)+len(videos): break
                contentCount = len(images)+len(videos)
            # download all images and videos
            imagesDownloaded = Driver.download_images()
            videosDownloaded = Driver.download_videos()
            Settings.print("downloaded messages")
            Settings.print("count: {}".format(len(imagesDownloaded)+len(videosDownloaded)))
        except Exception as e:
            Settings.maybe_print(e)

    def download_videos():
        """Downloads all videos on the page"""

        videosDownloaded = []
        try:
            # find all video elements on page
            videos = Driver.browser.find_elements_by_tag_name("video")
            downloadPath = os.path.join(Settings.get_download_path(), "videos")
            Path(downloadPath).mkdir(parents=True, exist_ok=True)
            i=1
            # download all video.src -> /arrrg/$username/videos            
            for video in videos:
                if Driver.DOWNLOADING_MAX and i > Driver.DOWNLOAD_MAX_VIDEOS: break
                src = str(video.get_attribute("src"))
                if not src or src == "" or src == "None" or "http" not in src: continue
                Settings.print_same_line("downloading video: {}/{}".format(i, len(videos)))
                # Settings.print("Video: {}".format(src[:src.find(".mp4")+4]))
                # Settings.print("Video: {}".format(src))
                if Driver.DOWNLOADING:
                    try:
                        while os.path.isfile("{}/{}.mp4".format(downloadPath, i)):
                            i+=1
                        wget.download(src, "{}/{}.mp4".format(downloadPath, i), False)
                        videosDownloaded.append(i)
                    except Exception as e: Settings.print(e)
                i+=1
            Settings.print("")
        except Exception as e:
            Settings.print(e)
        return videosDownloaded


    def drag_and_drop_file(drop_target, path):
        """
        Drag and drop the provided file path onto the provided element target.


        Parameters
        ----------
        drop_target : WebElement
            The web element to drop the file at path on

        path : str
            The file path to drag onto the web element


        """

        # https://stackoverflow.com/questions/43382447/python-with-selenium-drag-and-drop-from-file-system-to-webdriver
        JS_DROP_FILE = """
            var target = arguments[0],
                offsetX = arguments[1],
                offsetY = arguments[2],
                document = target.ownerDocument || document,
                window = document.defaultView || window;

            var input = document.createElement('INPUT');
            input.type = 'file';
            input.onchange = function () {
              var rect = target.getBoundingClientRect(),
                  x = rect.left + (offsetX || (rect.width >> 1)),
                  y = rect.top + (offsetY || (rect.height >> 1)),
                  dataTransfer = { files: this.files };

              ['dragenter', 'dragover', 'drop'].forEach(function (name) {
                var evt = document.createEvent('MouseEvent');
                evt.initMouseEvent(name, !0, !0, window, 0, 0, 0, x, y, !1, !1, !1, !1, 0, null);
                evt.dataTransfer = dataTransfer;
                target.dispatchEvent(evt);
              });

              setTimeout(function () { document.body.removeChild(input); }, 25);
            };
            document.body.appendChild(input);
            return input;
        """
        try:
            Settings.maybe_print("dragging and dropping...")
            Settings.dev_print("drop target: {}".format(drop_target.get_attribute("innerHTML")))
            # BUG: requires double to register file upload
            file_input = drop_target.parent.execute_script(JS_DROP_FILE, drop_target, 0, 0)
            file_input.send_keys(path)
            file_input = drop_target.parent.execute_script(JS_DROP_FILE, drop_target, 50, 50)
            file_input.send_keys(path)
            Settings.debug_delay_check()
        except Exception as e:
            Settings.err_print(e) 

    def enter_text(text):
        """
        Enter the provided text into the page's text area

        Must be ran on a page with an OnlyFans text area.


        Parameters
        ----------
        text : str
            The text to enter

        Returns
        -------
        bool
            Whether or not entering the text was successful

        """

        try:
            # click on open text area
            Settings.dev_print("finding text")
            enterText = Element.get_element_by_name("enterText").getId()
            sendText = Driver.browser.find_element_by_id(enterText)
            # action = webdriver.common.action_chains.ActionChains(Driver.browser)
            action = ActionChains(Driver.browser)
            action.move_to_element(sendText)
            action.click()
            action.perform()
            # action seperated for debugging
            sendText = Driver.browser.find_element_by_id(enterText)
            Settings.dev_print("found text")
            sendText.clear()
            Settings.dev_print("sending text")
            sendText.send_keys(str(text))
            Settings.dev_print("successfully entered text")
            return True
        except Exception as e:
            Settings.dev_print(e)
            return False

    @staticmethod
    def error_checker(e):
        """
        Custom error checker

        Parameters
        ----------
        e : str
            Error text

        """

        if "Unable to locate element" in str(e):
            Settings.warn_print("onlysnarf may require an update")
        if "Message: " in str(e): return
        Settings.dev_print(e)

    def error_window_upload():
        """Closes error window that appears during uploads for 'duplicate' files"""

        try:
            element = Element.get_element_by_name("errorUpload")
            error_buttons = Driver.browser.find_elements_by_class_name(element.getClass())
            Settings.dev_print("errors btns: {}".format(len(error_buttons)))
            if len(error_buttons) == 0: return True
            for butt in error_buttons:
                if butt.get_attribute("innerHTML").strip() == "Close" and butt.is_enabled():
                    Settings.maybe_print("upload error message, closing")
                    butt.click()
                    Settings.maybe_print("success: upload error message closed")
                    return True
            return False
        except Exception as e:
            Driver.error_checker(e)
        return False

    ######################
    ##### Expiration #####
    ######################

    def expires(expiration):
        """
        Enters the provided expiration duration for a post

        Must be on home page

        Parameters
        ----------
        expiration : int
            The duration (in days) until the post expires
        
        Returns
        -------
        bool
            Whether or not entering the expiration was successful

        """

        if not expiration: return True
        try:
            Settings.print("Expiration:")
            Settings.print("- Period: {}".format(expiration))
            # if expiration is 'no limit', then there's no expiration and hence no point here
            if expiration == 999: return True
            Driver.open_more_options()
            # open expires window
            Settings.dev_print("adding expiration")
            Driver.find_element_to_click("expiresAdd").click()
            # select duration
            Settings.dev_print("entering expiration")

            # leave in case needed again
            # nums = Driver.find_elements_by_name("expiresPeriods")
            # for num in nums:
            #     inner = num.get_attribute("innerHTML")
            #     if int(expiration) == 1  and ">1<" in str(inner): num.click()
            #     if int(expiration) == 3  and ">3<" in str(inner): num.click()
            #     if int(expiration) == 7  and ">7<" in str(inner): num.click()
            #     if int(expiration) == 30 and ">30<" in str(inner): num.click()
            #     if int(expiration) == 99 and ">o limit<" in str(inner): num.click()

            # expiration can now have any int, so update for entering any int less than 30
            Driver.browser.find_element_by_name("periodValue").send_keys(expiration)

            Settings.dev_print("successfully selected expiration")
            Settings.debug_delay_check()
            # save
            if Settings.is_debug() == "True":
                Settings.maybe_print("skipping expiration (debug)")
                Settings.dev_print("skipping expiration")
                Driver.find_element_to_click("expiresCancel").click()
                Settings.dev_print("successfully canceled expires")
                Settings.dev_print("### Expiration Successfully Canceled ###")
            else:
                Settings.dev_print("saving expiration")
                Driver.find_element_to_click("expiresSave").click()
                Settings.dev_print("successfully saved expires")
                Settings.dev_print("### Expiration Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to enter expiration")
            try:
                Settings.dev_print("canceling expiration")
                Driver.find_element_to_click("expiresCancel").click()
                Settings.dev_print("successfully canceled expiration")
                Settings.dev_print("### Expiration Successful Failure ###")
            except: 
                Settings.dev_print("### Expiration Failure Failure")
        return False

    ######################################################################

    def find_element_by_name(name):
        """
        Find element on page by name

        Does not auth check or otherwise change the focus

        Parameters
        ----------
        name : str
            The name of the element to reference from its /elements/element name

        Returns
        -------
        Selenium.WebDriver.WebElement
            The located web element if found by id, class name, or css selector

        """
        element = Element.get_element_by_name(name)
        if not element:
            Settings.err_print("unable to find element reference")
            return False
        # prioritize id over class name
        eleID = None
        try: eleID = Driver.browser.find_element_by_id(element.getId())
        except: eleID = None
        if eleID: return eleID
        for className in element.getClasses():
            ele = None
            eleCSS = None
            try: ele = Driver.browser.find_element_by_class_name(className)
            except: ele = None
            try: eleCSS = Driver.browser.find_element_by_css_selector(className)
            except: eleCSS = None
            Settings.dev_print("class: {} - {}:css".format(ele, eleCSS))
            if ele: return ele
            if eleCSS: return eleCSS
        raise Exception("unable to locate element")

    def find_elements_by_name(name):
        """
        Find elements on page by name. Does not change window focus.

        Parameters
        ----------
        name : str
            The name of the element to reference from its /elements/element name

        Returns
        -------
        list
            A list of the located Selenium.WebDriver.WebElements as found by id, class name, or css selector. 
            Elements must also be displayed

        """

        element = Element.get_element_by_name(name)
        if not element:
            Settings.err_print("unable to find element reference")
            return False
        eles = []
        for className in element.getClasses():
            eles_ = []
            elesCSS_ = []
            try: eles_ = Driver.browser.find_elements_by_class_name(className)
            except: eles_ = []
            try: elesCSS_ = Driver.browser.find_elements_by_css_selector(className)
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
            raise Exception("unable to locate elements")
        return eles_

    def find_element_to_click(name):
        """
        Find element on page by name to click

        Does not auth check or otherwise change the focus. Checks that located element is properly 
        capable of being clicked.

        Parameters
        ----------
        name : str
            The name of the element to click as referenced from its /elements/element name

        Returns
        -------
        Selenium.WebDriver.WebElements
            The located web element that can be clicked

        """

        Settings.dev_print("finding click: {}".format(name))
        element = Element.get_element_by_name(name)
        if not element:
            Settings.err_print("unable to find element reference")
            return False
        for className in element.getClasses():
            eles = []
            elesCSS = []
            try: eles = Driver.browser.find_elements_by_class_name(className)
            except: eles = []
            try: elesCSS = Driver.browser.find_elements_by_css_selector(className)
            except: elesCSS = []
            Settings.dev_print("class: {} - {}:css".format(len(eles), len(elesCSS)))
            eles.extend(elesCSS)
            for i in range(len(eles)):
                Settings.dev_print("ele: {} -> {}".format(eles[i].get_attribute("innerHTML").strip(), element.getText()))
                if (eles[i].is_displayed() and element.getText() and str(element.getText().lower()) == eles[i].get_attribute("innerHTML").strip().lower()) and eles[i].is_enabled():
                    Settings.dev_print("found matching ele")
                    # Settings.dev_print("found matching ele: {}".format(eles[i].get_attribute("innerHTML").strip()))
                    return eles[i]
                elif (eles[i].is_displayed() and element.getText() and str(element.getText().lower()) in eles[i].get_attribute("innerHTML").strip().lower()) and eles[i].is_enabled():
                    Settings.dev_print("found matching(ish) ele")
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
        raise Exception("unable to locate element")

    ######################################################################

    @staticmethod
    def get_browser():
        """
        Get the default WebDriver object in use or create one

        Returns
        -------
        Selenium.WebDriver
            The default WebDriver object in use or was created

        """
        try:
            if not Driver.browser: Driver.spawn_browser(Settings.get_browser_type())
            return Driver.browser
        except Exception as e:
            print(e)

    # waits for page load
    def get_page_load():
        """Attempt to generic page load"""

        time.sleep(2)
        try: WebDriverWait(Driver.browser, 60*3, poll_frequency=10).until(EC.visibility_of_element_located((By.CLASS_NAME, "main-wrapper")))
        except Exception as e: Settings.dev_print(e)

    def handle_alert():
        """Switch to alert pop up"""

        try:
            alert_obj = Driver.browser.switch_to.alert or None
            if alert_obj:
                alert_obj.accept()
        except: pass

    ##############
    ### Go Tos ###
    ##############

    def go_to_home(force=False):
        """
        Go to home page

        If already at home don't go unless forced

        Parameters
        ----------
        force : bool
            Force page goto even if already at url

        """

        Driver.init()
        def goto():
            Settings.maybe_print("goto -> onlyfans.com")
            Driver.browser.get(ONLYFANS_HOME_URL)
            # Driver.open_tab(ONLYFANS_HOME_URL)
            Driver.handle_alert()
            Driver.get_page_load()
        if force: return goto()
        if Driver.search_for_tab(ONLYFANS_HOME_URL):
            Settings.maybe_print("found -> /")
            return
        Settings.dev_print("current url: {}".format(Driver.browser.current_url))
        if str(Driver.browser.current_url) == str(ONLYFANS_HOME_URL):
            Settings.maybe_print("at -> onlyfans.com")
            Driver.browser.execute_script("window.scrollTo(0, 0);")
        else: goto()
        
    def go_to_page(page):
        """
        Go to page

        If already at page don't go

        Parameters
        ----------
        page : str
            The url of the OnlyFans 'page' to go to

        """

        Driver.auth()
        if Driver.search_for_tab(page):
            Settings.maybe_print("found -> {}".format(page))
            return
        if str(Driver.browser.current_url) == str(page) or str(page) in str(Driver.browser.current_url):
            Settings.maybe_print("at -> {}".format(page))
            Driver.browser.execute_script("window.scrollTo(0, 0);")
        else:
            Settings.maybe_print("goto -> {}".format(page))
            Driver.open_tab(page)
            Driver.handle_alert()
            Driver.get_page_load()

    def go_to_profile():
        """Go to OnlyFans profile page"""

        Driver.auth()
        username = Settings.get_username()
        if str(username) == "":
            username = Driver.get_username()
        page = "{}/{}".format(ONLYFANS_HOME_URL, username)
        if Driver.search_for_tab(page):
            Settings.maybe_print("found -> /{}".format(username))
            return
        if str(username) in str(Driver.browser.current_url):
            Settings.maybe_print("at -> {}".format(username))
            Driver.browser.execute_script("window.scrollTo(0, 0);")
        else:
            Settings.maybe_print("goto -> {}".format(username))
            # Driver.browser.get("{}{}".format(ONLYFANS_HOME_URL, username))
            Driver.open_tab(page)
            # Driver.handle_alert()
            # Driver.get_page_load()

    # onlyfans.com/my/settings
    def go_to_settings(settingsTab):
        """
        Go to settings tab on settings page

        If already at tab, stay

        Parameters
        ----------
        settingsTab : str
            The name of the Settings tab to go to

        """

        Driver.auth()
        if Driver.search_for_tab("{}{}".format(ONLYFANS_SETTINGS_URL, settingsTab)):  
            Settings.maybe_print("found -> settings/{}".format(settingsTab))
            return
        if str(ONLYFANS_SETTINGS_URL) in str(Driver.browser.current_url) and str(settingsTab) == "profile":
            Settings.maybe_print("at -> onlyfans.com/settings/{}".format(settingsTab))
            Driver.browser.execute_script("window.scrollTo(0, 0);")
        else:
            if str(settingsTab) == "profile": settingsTab = ""
            Settings.maybe_print("goto -> onlyfans.com/settings/{}".format(settingsTab))
            Driver.go_to_page("{}{}".format(ONLYFANS_SETTINGS_URL, settingsTab))

    def search_for_tab(page):
        """
        Search for (and goto if exists) tab in Driver.tabs cache

        Parameters
        ----------
        page : str
            The url of the OnlyFans 'page' to go to

        Returns
        -------
        bool
            Whether or not the tab exists


        """

        original_handle = Driver.browser.current_window_handle
        Settings.dev_print("tabs: {}".format(Driver.tabs))
        try:
            for page_, handle, value in Driver.tabs:
                # Settings.dev_print("{} = {}".format(page_, page))
                if str(page_) == str(page):
                    Driver.browser.switch_to.window(handle)
                    value += 1
                    Settings.dev_print("successfully located tab in cache: {}".format(page))
                    return True
            for handle in Driver.browser.window_handles[0]:
                Driver.browser.switch_to.window(handle)
                if str(page) in str(Driver.browser.current_url):
                    Settings.dev_print("successfully located tab: {}".format(page))
                    return True
            for handle in Driver.browser.window_handles:
                Driver.browser.switch_to.window(handle)
                if str(page) in str(Driver.browser.current_url):
                    Settings.dev_print("successfully located tab in windows: {}".format(page))
                    return True
            Settings.dev_print("failed to locate tab: {}".format(page))
            Driver.browser.switch_to.window(original_handle)
        except Exception as e:
            if "Unable to locate window" not in str(e):
                Settings.dev_print(e)
        return False

    def open_tab(url):
        """
        Open new tab of url

        Parameters
        ----------
        url : str
            The url to open in a new tab

        Returns
        -------
        bool
            Whether or not the tab was opened successfully

        """

        Settings.maybe_print("tab -> {}".format(url))
        # Driver.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
        # Driver.browser.get(url)
        # https://stackoverflow.com/questions/50844779/how-to-handle-multiple-windows-in-python-selenium-with-firefox-driver
        windows_before  = Driver.browser.current_window_handle
        Settings.dev_print("current window handle is : %s" %windows_before)
        windows = Driver.browser.window_handles
        Driver.browser.execute_script('''window.open("{}","_blank");'''.format(url))
        # Driver.browser.execute_script("window.open('{}')".format(url))
        Driver.handle_alert()
        Driver.get_page_load()
        # Driver.browser.execute_script("window.open('https://www.yahoo.com')")
        WebDriverWait(Driver.browser, 10).until(EC.number_of_windows_to_be(len(windows)+1))
        windows_after = Driver.browser.window_handles
        new_window = [x for x in windows_after if x not in windows][0]
        # Driver.browser.switch_to.window(new_window) <!---deprecated>
        Driver.browser.switch_to.window(new_window)
        Settings.dev_print("page title after tab switching is : %s" %Driver.browser.title)
        Settings.dev_print("new window handle is : %s" %new_window)
        # if len(Driver.tabs) >= Driver.MAX_TABS:
        #     least = Driver.tabs[0]
        #     for i, tab in enumerate(Driver.tabs):
        #         if int(tab[2]) < int(least[2]):
        #             least = tab
        #     Driver.tabs.remove(least)
        # Driver.tabs.append([url, new_window, 0]) # url, window_handle, use count
    
    ##################
    ###### Login #####
    ##################

    def login():
        """
        Logs into OnlyFans account provided via args and chosen method.

        Checks if already logged in first. Logs in via requested method or tries all available.

        Returns
        -------
        bool
            Whether or not the login was successful

        """

        if Driver.logged_in: return True
        Settings.print('logging into OnlyFans for {}...'.format(Settings.get_username()))

        def loggedin_check():
            """Check if already logged in before attempting to login again"""

            Driver.go_to_home(force=True)
            try:
                ele = Driver.browser.find_element_by_class_name(Element.get_element_by_name("loginCheck").getClass())
                if ele: 
                    Settings.print("already logged into OnlyFans!")
                    return True
            except Exception as e:
                Settings.dev_print(e)
            return False

        def login_check(which):
            """
            Check after login attempt for successful home page

            Returns
            -------
            bool
                Whether or not the login check was successful

            """

            try:
                Settings.dev_print("waiting for logincheck...")
                WebDriverWait(Driver.browser, 120, poll_frequency=6).until(EC.visibility_of_element_located((By.CLASS_NAME, Element.get_element_by_name("loginCheck").getClass())))
                Settings.print("OnlyFans login successful!")
                Settings.dev_print("login successful - {}".format(which))
                return True
            except TimeoutException as te:
                Settings.dev_print(str(te))
                Settings.print("Login Failure: Timed Out! Please check your credentials.")
                Settings.print(": If the problem persists, OnlySnarf may require an update.")
                return False
            except Exception as e:
                Driver.error_checker(e)
                Settings.print("OnlyFans login failure: OnlySnarf may require an update")
                return False
            return True
        
        def via_form():
            """
            Logs in via OnlyFans username & password form
            
            Returns
            -------
            bool
                Whether or not the login attempt was successful

            """

            try:
                Settings.maybe_print("logging in via form")
                username = str(Settings.get_username_onlyfans())
                password = str(Settings.get_password())
                if not username or username == "": username = Settings.prompt_email()
                if not password or password == "": password = Settings.prompt_password()
                if str(username) == "" or str(password) == "":
                    Settings.err_print("missing onlyfans login info")
                    return False
                Driver.go_to_home()
                Settings.dev_print("finding username")
                Driver.browser.find_element_by_name("email").send_keys(username)
                Settings.dev_print("username entered")
                # fill in password and hit the login button 
                Settings.dev_print("finding password")
                password_ = Driver.browser.find_element_by_name("password")
                password_.send_keys(password)
                Settings.dev_print("password entered")
                password_.send_keys(Keys.ENTER)
                def check_captcha():
                    try:
                        time.sleep(10) # wait extra long to make sure it doesn't verify obnoxiously
                        el = Driver.browser.find_element_by_name("password")
                        if not el: return # likely logged in without captcha
                        Settings.print("waiting for captcha completion by user...")
                        # action = webdriver.common.action_chains.ActionChains(Driver.browser)
                        action = ActionChains(Driver.browser)
                        action.move_to_element_with_offset(el, 40, 100)
                        action.click()
                        action.perform()
                        time.sleep(10)
                        sub = None
                        submit = Driver.browser.find_elements_by_class_name("g-btn.m-rounded.m-flex.m-lg")
                        for ele in submit:
                            if str(ele.get_attribute("innerHTML")) == "Login":
                                sub = ele
                        if sub and sub.is_enabled():
                            submit.click()
                        elif sub and not sub.is_enabled():
                            Settings.err_print("unable to login via form - captcha")
                    except Exception as e:
                        if "Unable to locate element: [name=\"password\"]" not in str(e):
                            Settings.dev_print(e)
                check_captcha()
                return login_check("form")
            except Exception as e:
                Settings.dev_print("form login failure")
                Driver.error_checker(e)
            return False

        def via_google():
            """
            Logs in via linked Google account. (doesn't work)
            
            Returns
            -------
            bool
                Whether or not the login attempt was successful

            """

            try:
                Settings.maybe_print("logging in via google")
                username = str(Settings.get_username_google())
                password = str(Settings.get_password_google())
                if not username or username == "":
                    username = Settings.prompt_username_google()
                if not password or password == "":
                    password = Settings.prompt_password_google()
                if str(username) == "" or str(password) == "":
                    Settings.err_print("missing google login info")
                    return False
                Driver.go_to_home()
                elements = Driver.browser.find_elements_by_tag_name("a")
                [elem for elem in elements if '/auth/google' in str(elem.get_attribute('href'))][0].click()
                time.sleep(5)
                username_ = Driver.browser.switch_to.active_element
                # then click username spot
                username_.send_keys(username)
                username_.send_keys(Keys.ENTER)
                Settings.dev_print("username entered")
                time.sleep(2)
                password_ = Driver.browser.switch_to.active_element
                # fill in password and hit the login button 
                password_.send_keys(password)
                Settings.dev_print("password entered")
                password_.send_keys(Keys.ENTER)
                return login_check("google")
            except Exception as e:
                Settings.dev_print("google login failure")
                Driver.error_checker(e)
            return False

        def via_twitter():
            """
            Logs in via linked Twitter account
            
            Returns
            -------
            bool
                Whether or not the login attempt was successful

            """

            try:
                Settings.maybe_print("logging in via twitter")
                username = str(Settings.get_username_twitter())
                password = str(Settings.get_password_twitter())
                if not username or username == "": username = Settings.prompt_username_twitter()
                if not password or password == "": password = Settings.prompt_password_twitter()
                if str(username) == "" or str(password) == "":
                    Settings.err_print("missing twitter login info")
                    return False
                Driver.go_to_home()
                # rememberMe checkbox doesn't actually cause login to be remembered
                # rememberMe = Driver.browser.find_element_by_xpath(Element.get_element_by_name("rememberMe").getXPath())
                # if not rememberMe.is_selected():
                    # rememberMe.click()
                # if str(Settings.MANUAL) == "True":
                    # Settings.print("Please Login")
                elements = Driver.browser.find_elements_by_tag_name("a")
                [elem for elem in elements if '/twitter/auth' in str(elem.get_attribute('href'))][0].click()
                Driver.browser.find_element_by_name("session[username_or_email]").send_keys(username)
                Settings.dev_print("username entered")
                # fill in password and hit the login button 
                password_ = Driver.browser.find_element_by_name("session[password]")
                password_.send_keys(password)
                Settings.dev_print("password entered")
                password_.send_keys(Keys.ENTER)
                return login_check("twitter")
            except Exception as e:
                Settings.dev_print("twitter login failure")
                Driver.error_checker(e)
            return False

        # TODO: remember to add auto here if it works again for auto reconnecting
        if Settings.get_browser_type() == "reconnect" or Settings.get_browser_type() == "remote":
            if loggedin_check():
                Driver.logged_in = True
                return True

        successful = False
        try:
            if Settings.get_login_method() == "auto":
                successful = via_form()
                if not successful: successful = via_twitter()
                if not successful: successful = via_google()
            elif Settings.get_login_method() == "onlyfans":
                successful = via_form()
            elif Settings.get_login_method() == "twitter":
                successful = via_twitter()
            elif Settings.get_login_method() == "google":
                successful = via_google()
            if not successful:
                Settings.print("OnlyFans login failed!")
            Driver.logged_in = True
            return True
        except Exception as e:
            Settings.dev_print("login failure")
            Driver.error_checker(e)
            Settings.print("OnlyFans login failed!")
        return False

    ####################
    ##### Messages #####
    ####################

    def message(username, user_id=None):
        """
        Start a message to the username (or group of users) or user_id.

        Parameters
        ----------
        username : str
            The username of the user to message
        user_id : str
            The user id of the user to message

        Returns
        -------
        bool
            Whether or not the message was successful

        """

        if not username and not user_id:
            Settings.err_print("missing user to message")
            return False
        try:
            Settings.dev_print("attempting to start message for {}...".format(username))
            type__ = None # default
            # if the username is a key string it will behave differently
            if str(username).lower() == "all": type__ = "messageAll"
            elif str(username).lower() == "recent": type__ = "messageRecent"
            elif str(username).lower() == "favorite": type__ = "messageFavorite"
            elif str(username).lower() == "renew on": type__ = "messageRenewers"
            successful = False
            if type__ != None:
                Driver.go_to_page(ONLYFANS_NEW_MESSAGE_URL)
                Settings.dev_print("clicking message type: {}".format(username))
                Driver.find_element_to_click(type__).click()
                successful = True
            else:
                successful = Driver.message_user(username, user_id=user_id)
            Settings.dev_print("successfully started message for {}".format(username))
            return successful
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failure to message - {}".format(username))
            return False
     
    def message_confirm():
        """
        Wait for the message open on the page's Confirm button to be clickable and click it

        Returns
        -------
        bool
            Whether or not the message confirmation was successful

        """

        try:
            WAIT = WebDriverWait(Driver.browser, 600, poll_frequency=10)
            i = 0
            Settings.dev_print("waiting for message confirm to be clickable")
            while True:
                try:                
                    WAIT.until(EC.element_to_be_clickable((By.CLASS_NAME, Element.get_element_by_name("uploadMessageConfirm").getClass())))
                    Settings.dev_print("message confirm is clickable")
                    break
                except Exception as e:
                    Settings.print('uploading...')
                    Driver.error_checker(e)
                    i += 1
                    if i == int(Settings.get_upload_max_duration()):
                        Settings.err_print("max upload time reached")
                        return False
            Settings.dev_print("getting confirm to click")
            confirm = Driver.find_element_to_click("new_post")
            if Settings.is_debug() == "True":
                Settings.print('skipped message (debug)')
                Settings.dev_print("### Message Successful (debug) ###")
                Settings.debug_delay_check()
                Driver.go_to_home()
                return True
            Settings.dev_print("clicking confirm")
            confirm.click()
            Settings.print('OnlyFans Message: Sent')
            Settings.dev_print("### Message Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failure to confirm message")
            Settings.dev_print("### Message Failure ###")
        return False

    def message_price(price):
        """
        Enter the provided price into the message on the page

        Parameters
        ----------
        price : str
            The price to enter in dollars

        Returns
        -------
        bool
            Whether or not entering the price was successful

        """

        try:
            if not price or price == None or str(price) == "None":
                Settings.err_print("missing price")
                return False
            time.sleep(1) # prevents delay from inputted text preventing buttom from being available to click
            # Settings.print("price: {}".format(price))
            Settings.dev_print("waiting for price area to enter price")
            # finds the button on the page with the #icon-price text
            priceElements = Driver.browser.find_elements_by_class_name(Element.get_element_by_name("priceClick").getClass())
            priceElement = None
            for ele in priceElements:
                # Settings.dev_print("{}  {}".format(ele.get_attribute("value")))
                if "#icon-price" in str(ele.get_attribute("innerHTML")):
                    priceElement = ele
            if not priceElement:
                Settings.dev_print("failed to find price button")
                Settings.err_print("failure to enter price")
                return False
            # priceElement = WebDriverWait(Driver.browser, 60, poll_frequency=10).until(EC.element_to_be_clickable(priceElement))
            Settings.dev_print("entering price")
            priceElement.click()
            actions = ActionChains(Driver.browser)
            actions.send_keys(str(price)) 
            actions.perform()
            Settings.dev_print("entered price")
            # Settings.debug_delay_check()
            Settings.dev_print("saving price")
            Driver.find_element_to_click("priceSave").click()    
            Settings.dev_print("successfully saved price")
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failure to enter price")
            return False

    def message_text(text):
        """
        Enter the provided text into the message on the page

        Parameters
        ----------
        text : str
            The text to enter

        Returns
        -------
        bool
            Whether or not entering the text was successful

        """

        try:
            # Driver.go_to_page(ONLYFANS_HOME_URL)
            if not text or text == None or str(text) == "None" or text == "":
                Settings.warn_print("missing text for message")
                return False
            # Settings.print("text: {}".format(text))
            Settings.dev_print("finding text area")
            # message = Driver.find_element_by_name("messageText")     
            message = Driver.browser.find_element_by_id("new_post_text_input")     
            # message = Driver.browser.find_element_by_name("message")     
            Settings.dev_print("entering text")
            message.send_keys(str(text))
            Settings.dev_print("successfully entered text")
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failure to enter message")
            return False

    def message_user_by_id(user_id=None):
        """
        Message the provided user id

        Parameters
        ----------
        user_id : str
            The user id of the user to message

        Returns
        -------
        bool
            Whether or not messaging the user was successful

        """

        user_id = str(user_id).replace("@u","").replace("@","")
        if not user_id or user_id == None or str(user_id) == "None":
            Settings.warn_print("missing user id")
            return False
        try:
            Driver.go_to_page("{}{}".format(ONLYFANS_CHAT_URL, user_id))
            Settings.dev_print("successfully messaging user id: {}".format(user_id))
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to message user by id")
            return False

    def message_user(username, user_id=None):
        """
        Message the matching username or user id

        Parameters
        ----------
        username : str
            The username of the user to message
        user_id : str
            The user id of the user to message

        Returns
        -------
        bool
            Whether or not messaging the user was successful

        """

        Settings.dev_print("username: {} : {}: user_id".format(username, user_id))
        if user_id and str(user_id) != "None": return Driver.message_user_by_id(user_id=user_id)
        if not username:
            Settings.err_print("missing username to message")
            return False
        try:
            Driver.go_to_page(username)
            time.sleep(5) # for whatever reason this constantly errors out from load times
            elements = Driver.browser.find_elements_by_tag_name("a")
            ele = [ele for ele in elements
                    if ONLYFANS_CHAT_URL in str(ele.get_attribute("href"))]
            if len(ele) == 0:
                Settings.warn_print("user cannot be messaged - unable to locate id")
                return False
            ele = ele[0]
            ele = ele.get_attribute("href").replace("https://onlyfans.com", "")
            # clicking no longer works? just open href in Driver.browser
            # Settings.dev_print("clicking send message")
            # ele.click()
            # Settings.dev_print(ele.get_attribute("href"))
            Settings.maybe_print("user id found: {}".format(ele.replace(ONLYFANS_HOME_URL2, "")))
            Driver.go_to_page(ele)
            Settings.dev_print("successfully messaging username: {}".format(username))
            # return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to message user")
            return False
        return True

    def messages_scan(num=0):
        """
        Scan messages page for recent users

        Parameters
        ----------
        num : int
            The number of users to consider recent (doesn't work)

        Returns
        -------
        list
            The list of users found

        """

        # go to /messages page
        # get top n users
        Settings.dev_print("scanning messages")
        # 

        # g-avatar online_status_class m-w50 -> username
        # b-chats__item__link -> id

        # if users found < n, scroll
        # g-section-title -> scroll this
        # if int(num) == 0: num = Settings.get_user_num()
        users = []
        try:
            Driver.go_to_page("/my/chats")

            # num += len(notusers)

            ## so none of the scrolling is working, might as well only return the top 10 every time
            # count = 0
            # while True:
                # elements = Driver.browser.find_elements_by_class_name("b-chats__item__link")
                # if len(elements) <= int(num): break
                # if len(elements) <= int(count): break
                # Settings.print_same_line("({}/{}) scrolling...".format(count, len(elements)))
                # count = len(elements)
                # elementToFocus = Driver.browser.find_element_by_class_name("g-section-title")
                # elementToFocus = elements[0]
                # Settings.print(elementToFocus.get_attribute("innerHTML"))
                # Driver.browser.execute_script("arguments[0].focus();", elementToFocus)
                # actions = ActionChains(Driver.browser)
                # actions.send_keys(Keys.PAGE_DOWN) 
                # actions.perform()
                # Driver.browser.execute_script("window.scrollBy(0,250)", "");
                # Driver.browser.execute_script("scroll(0, 250);");
                # elementToFocus.send_keys(Keys.END)
                # elementToFocus.sendKeys(Keys.PAGE_DOWN);
                # elementToFocus.sendKeys(Keys.PAGE_DOWN);
                # elementToFocus.sendKeys(Keys.PAGE_DOWN);
                # elementToFocus = elements[0]
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # Driver.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                # time.sleep(2)

            users_ = Driver.browser.find_elements_by_class_name("g-user-username")
            Settings.dev_print("users: {}".format(len(users_)))

            user_ids = Driver.browser.find_elements_by_class_name("b-chats__item__link")
            Settings.dev_print("ids: {}".format(len(user_ids)))


            # for user in users_:
            #     if not user.get_attribute("href") or str(user.get_attribute("href")) == "None": continue
            #     Settings.print(str(user.get_attribute("href")).replace(ONLYFANS_HOME_URL2, ""))

            #     users.append(str(user.get_attribute("href")).replace(ONLYFANS_HOME_URL2, ""))

            for user in user_ids:
                if not user or not user.get_attribute("href") or str(user.get_attribute("href")) == "None": continue
                # Settings.print(str(user.get_attribute("href")).replace("https://onlyfans.com/my/chats/chat/", ""))
                # Settings.print(str(user.get_attribute("innerHTML")))
                # for notuser in notusers:
                    # if str(notuser.id) == str(user.get_attribute("href")).replace("https://onlyfans.com/my/chats/chat/", ""): 
                        # Settings.print("skipping not user")
                        # continue
                users.append(str(user.get_attribute("href")).replace("https://onlyfans.com/my/chats/chat/", ""))


            return users[:10]
        except Exception as e:
            Settings.print(e)
            Driver.error_checker(e)
            Settings.err_print("failed to scan messages")
        return users


    def move_to_then_click_element(element):
        """
        Move to then click element.
        
        From: https://stackoverflow.com/questions/44777053/selenium-movetargetoutofboundsexception-with-firefox

        Parameters
        ----------
        element : Selenium.WebDriver.WebElement
            The element to move to then click

        """

        def scroll_shim(passed_in_driver, object):
            x = object.location['x']
            y = object.location['y']
            scroll_by_coord = 'window.scrollTo(%s,%s);' % (
                x,
                y
            )
            scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
            passed_in_driver.execute_script(scroll_by_coord)
            passed_in_driver.execute_script(scroll_nav_out_of_way)
        #
        try:
            ActionChains(Driver.browser).move_to_element(element).click().perform()
        except Exception as e:
            Settings.dev_print(e)
            if 'firefox' in Driver.browser.capabilities['browserName']:
                scroll_shim(Driver.browser, element)
            try:
                ActionChains(Driver.browser).move_to_element(element).click().perform()
            except Exception as e:
                Settings.dev_print(e)
            # Driver.browser.execute_script("arguments[0].scrollIntoView();", ele)
                Driver.browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
                ActionChains(Driver.browser).move_to_element(element).click().perform()


    ####################################################################################################
    ####################################################################################################
    ####################################################################################################

    # tries both and throws error for not found element internally
    def open_more_options():
        """
        Click to open more options on a post.

        Returns
        -------
        bool
            Whether or not opening more options was successful

        """

        def option_one():
            """Click on '...' element"""

            Settings.dev_print("opening options (1)")
            moreOptions = Driver.find_element_to_click("moreOptions")
            if not moreOptions: return False    
            moreOptions.click()
            Settings.dev_print("successfully opened more options (1)")
            return True
        def option_two():
            """Click in empty space"""

            Settings.dev_print("opening options (2)")
            moreOptions = Driver.browser.find_element_by_id(Element.get_element_by_name("enterText").getId())
            if not moreOptions: return False    
            moreOptions.click()
            Settings.dev_print("successfully opened more options (2)")
            return True
        try:
            successful = option_one()
            if not successful: return option_two()
        except Exception as e:
            try:
                return option_two()
            except Exception as e:    
                Driver.error_checker(e)
                raise Exception("unable to locate 'More Options' element")

    ################
    ##### Poll #####
    ################

    def poll(poll):
        """
        Enter the Poll object into the current post

        Parameters
        ----------
        poll : classes.Poll
            The poll object containing required values

        Returns
        -------
        bool
            Whether or not entering the poll was successful

        """

        if str(poll) == "None": return True
        poll.get()
        duration = poll["duration"]
        questions = poll["questions"]
        try:
            Settings.print("Poll:")
            Settings.print("- Duration: {}".format(duration))
            Settings.print("- Questions:\n> {}".format("\n> ".join(questions)))
            # make sure the extra options are shown
            Driver.open_more_options()
            # add a poll
            Settings.dev_print("adding poll")
            Driver.find_element_to_click("poll").click()
            # open the poll duration
            Settings.dev_print("adding duration")
            Driver.find_element_to_click("pollDuration").click()
            # click on the correct duration number
            Settings.dev_print("setting duration")
            # nums = Driver.browser.find_elements_by_class_name(Element.get_element_by_name("pollDurations").getClass())
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
            Driver.find_element_to_click("pollSave").click()
            Settings.dev_print("successfully saved duration")
            # add extra question space
            if len(questions) > 2:
                for question in questions[2:]:
                    Settings.dev_print("adding question")
                    question_ = Driver.find_element_to_click("pollQuestionAdd").click()
                    Settings.dev_print("added question")
            # find the question inputs
            Settings.dev_print("locating question paths")
            questions_ = Driver.browser.find_elements_by_xpath(Element.get_element_by_name("pollInput").getXPath())
            Settings.dev_print("question paths: {}".format(len(questions_)))
            # enter the questions
            i = 0
            Settings.dev_print("questions: {}".format(questions))
            for question in list(questions):
                Settings.dev_print("entering question: {}".format(question))
                questions_[i].send_keys(str(question))
                Settings.dev_print("entered question")
                time.sleep(1)
                i+=1
            Settings.dev_print("successfully entered questions")
            Settings.debug_delay_check()
            if Settings.is_debug() == "True":
                Settings.maybe_print("skipping poll (debug)")
                cancel = Driver.find_element_to_click("pollCancel")
                cancel.click()
                Settings.dev_print("### Poll Successfully Canceled ###")
            Settings.dev_print("### Poll Successful ###")
            time.sleep(3)
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to enter poll")
            return False

    ################
    ##### Post #####
    ################

    def post(message):
        """
        Post the message to OnlyFans.

        Optionally tweet if enabled. A message must contain text and can contain:
        - files
        - keywords
        - performers
        - expiration
        - schedule
        - poll

        Parameters
        ----------
        message : classes.Message
            The message to be entered into the post

        Returns
        -------
        bool
            Whether or not the post was successful

        """

        Settings.dev_print("posting...")
        try:
            Driver.go_to_home()
            Driver.auth()
            files = message["files"]
            text = message["text"]
            if str(text) == "None": text = ""
            #################### Formatted Text ####################
            Settings.print("====================")
            Settings.print("Posting:")
            Settings.print("- Files: {}".format(len(files)))
            # Settings.print("- Keywords: {}".format(message.get_keywords()))
            # Settings.print("- Performers: {}".format(message.get_performers()))
            Settings.print("- Text: {}".format(text))
            Settings.print("- Tweeting: {}".format(Settings.is_tweeting()))
            ## Expires, Schedule, Poll
            if not Driver.expires(message["expiration"]): return False
            if not Driver.schedule(message["schedule"]): return False
            if not Driver.poll(message["poll"]): return False
            Settings.print("====================")
            ############################################################
            WAIT = WebDriverWait(Driver.browser, 600, poll_frequency=10)
            ## Tweeting
            if Settings.is_tweeting() == "True":
                Settings.dev_print("tweeting")
                WAIT.until(EC.element_to_be_clickable((By.XPATH, Element.get_element_by_name("tweet").getXPath()))).click()
            else: Settings.dev_print("not tweeting")
            
            ## Upload Files
            try:
                successful_upload = Driver.upload_files(files) or False # neither of these are supposed to fail
                ## Text
                successful_text = Driver.enter_text(text) or False # neither of these are supposed to fail
                if not successful_text or not successful_upload:
                    Settings.err_print("unable to post")
                    return False
                ## Upload
                i = 0
                while True:
                    try:
                        WebDriverWait(Driver.browser, 600, poll_frequency=10).until(EC.element_to_be_clickable((By.CLASS_NAME, Element.get_element_by_name("sendButton").getClass())))
                        Settings.dev_print("upload complete")
                        break
                    except Exception as e:
                        # try: 
                        #     # check for existence of "thumbnail is fucked up" modal and hit ok button
                        #     # haven't seen in long enough time to properly add
                        #     Driver.browser.switchTo().frame("iframe");
                        #     Driver.browser.find_element_by_class_name("g-btn m-rounded m-border").send_keys(Keys.ENTER)
                        #     Settings.err_print("thumbnail missing")
                        #     break
                        # except Exception as ef:
                        #     Settings.maybe_print(ef)
                        Settings.print('uploading...')
                        Driver.error_checker(e)
                        i+=1
                        if i == int(Settings.get_upload_max_duration()) and Settings.is_force_upload() == "False":
                            Settings.err_print("max upload time reached")
                            return False

            except Exception as e:
                Settings.print(e)

            ## Confirm
            try:
                send = Driver.find_element_to_click("new_post")
                if send:
                    Settings.debug_delay_check()
                    if Settings.is_debug() == "True":
                        Settings.print('skipped post (debug)')
                        Settings.debug_delay_check()
                        Driver.go_to_home(force=True)
                        return True
                    Settings.dev_print("confirming upload")
                    send.click()
                    # send[1].click() # the 0th one is disabled
                else:
                    Settings.err_print("unable to locate 'Send Post' button")
                    return False
            except Exception as e:
                Settings.err_print("unable to send post")
                Settings.dev_print(e)
                return False

            Settings.print('posted to OnlyFans!')
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("onlyfans post failure")
            return False

    ######################
    ##### Promotions #####
    ######################

    def promotional_campaign(promotion=None):
        """
        Enter the promotion as a campaign.

        Parameters
        ----------
        promotion : classes.Promotion
            The promotion to enter as a campaign

        Returns
        -------
        bool
            Whether or not the promotion was successful

        """

        if not promotion:
            Settings.err_print("missing promotion")
            return False
        # go to onlyfans.com/my/subscribers/active
        try:
            promotion.get()
            limit = promotion["limit"]
            expiration = promotion["expiration"]
            duration = promotion["duration"]
            # user = promotion["user"]
            amount = promotion["amount"]
            text = promotion["message"]
            Settings.maybe_print("goto -> /my/promotions")
            Driver.go_to_page("my/promotions")
            Settings.dev_print("checking existing promotion")
            copies = Driver.browser.find_elements_by_class_name("g-btn.m-rounded.m-uppercase")
            for copy in copies:
                if "copy link to profile" in str(copy.get_attribute("innerHTML")).lower():
                # Settings.print("{}".format(copy.get_attribute("innerHTML")))
                    copy.click()
                    Settings.dev_print("successfully clicked early copy")
                    Settings.warn_print("a promotion already exists")
                    Settings.print("Copied existing promotion")
                    return True
            Settings.dev_print("clicking promotion campaign")
            Driver.find_element_to_click("promotionalCampaign").click()
            Settings.dev_print("successfully clicked promotion campaign")
            # Settings.debug_delay_check()
            time.sleep(10)
            # limit dropdown
            Settings.dev_print("setting campaign count")
            limitDropwdown = Driver.find_element_by_name("promotionalTrialCount")
            for n in range(11): # 11 max subscription limits
                limitDropwdown.send_keys(str(Keys.UP))
            Settings.debug_delay_check()
            if limit:
                for n in range(int(limit)):
                    limitDropwdown.send_keys(Keys.DOWN)
            Settings.dev_print("successfully set campaign count")
            Settings.debug_delay_check()
            # expiration dropdown
            Settings.dev_print("settings campaign expiration")
            expirationDropdown = Driver.find_element_by_name("promotionalTrialExpiration")
            for n in range(11): # 31 max days
                expirationDropdown.send_keys(str(Keys.UP))
            Settings.debug_delay_check()
            if expiration:
                for n in range(int(expiration)):
                    expirationDropdown.send_keys(Keys.DOWN)
            Settings.dev_print("successfully set campaign expiration")
            Settings.debug_delay_check()
            # duration dropdown
            # LIMIT_ALLOWED = ["1 day","3 days","7 days","14 days","1 month","3 months","6 months","12 months"]
            durationDropdown = Driver.find_element_by_name("promotionalCampaignAmount")
            Settings.dev_print("entering discount amount")
            for n in range(11):
                durationDropdown.send_keys(str(Keys.UP))
            for n in range(round(int(amount)/5)-1):
                durationDropdown.send_keys(Keys.DOWN)
            Settings.dev_print("successfully entered discount amount")
            # todo: add message to users
            message = Driver.find_element_by_name("promotionalTrialMessage")
            Settings.dev_print("found message text")
            message.clear()
            Settings.dev_print("sending text")
            message.send_keys(str(text))
            # todo: [] apply to expired subscribers checkbox
            Settings.debug_delay_check()
            # find and click promotionalTrialConfirm
            if Settings.is_debug() == "True":
                Settings.dev_print("finding campaign cancel")
                Driver.find_element_to_click("promotionalTrialCancel").click()
                Settings.maybe_print("skipping promotion (debug)")
                Settings.dev_print("successfully cancelled promotion campaign")
                return True
            Settings.dev_print("finding campaign save")
            save_ = Driver.find_element_to_click("promotionalTrialConfirm")
            # save_ = Driver.find_element_to_click("promotionalCampaignConfirm")
            save_ = Driver.browser.find_elements_by_class_name("g-btn.m-rounded")
            for save__ in save_:
                Settings.print(save__.get_attribute("innerHTML"))
            if len(save_) == 0:
                Settings.dev_print("unable to find promotion 'Create'")
                Settings.err_print("unable to save promotion")
                return False
            for save__ in save_:
                if save__.get_attribute("innerHTML").lower().strip() == "create":
                    save_ = save__    
            Settings.print(save_.get_attribute("innerHTML"))
            Settings.dev_print("saving promotion")
            save_.click()
            Settings.dev_print("successfully saved promotion")
            Settings.dev_print("successful promotion campaign")
            # todo: add copy link to profile
            Settings.debug_delay_check()
            Settings.dev_print("clicking copy")
            copies = Driver.browser.find_elements_by_class_name("g-btn.m-rounded.m-uppercase")
            for copy in copies:
                Settings.print("{}".format(copy.get_attribute("innerHTML")))
                if "copy link to profile" in str(copy.get_attribute("innerHTML")).lower():
                    copy.click()
                    Settings.dev_print("successfully clicked copy")
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to apply promotion")
            return None

    # or email
    def promotional_trial_link(promotion=None):
        """
        Enter the promotion as a trial link

        Parameters
        ----------
        promotion : classes.Promotion
            The promotion to enter as a link

        Returns
        -------
        bool
            Whether or not the promotion was successful

        """

        if not promotion:
            Settings.err_print("missing promotion")
            return False
        # go to onlyfans.com/my/subscribers/active
        try:
            promotion.get()
            limit = promotion["limit"]
            expiration = promotion["expiration"]
            duration = promotion["duration"]
            user = promotion["user"]
            Settings.maybe_print("goto -> /my/promotions")
            Driver.go_to_page("/my/promotions")
            Settings.dev_print("showing promotional trial link")
            Driver.find_element_to_click("promotionalTrialShow").click()
            Settings.dev_print("successfully showed promotional trial link")
            Settings.dev_print("creating promotional trial")
            Driver.find_element_to_click("promotionalTrial").click()
            Settings.dev_print("successfully clicked promotional trial")
            # limit dropdown
            Settings.dev_print("setting trial count")
            limitDropwdown = Driver.find_element_by_name("promotionalTrialCount")
            for n in range(11): # 11 max subscription limits
                limitDropwdown.send_keys(str(Keys.UP))
            Settings.debug_delay_check()
            if limit:
                for n in range(int(limit)):
                    limitDropwdown.send_keys(Keys.DOWN)
            Settings.dev_print("successfully set trial count")
            Settings.debug_delay_check()
            # expiration dropdown
            Settings.dev_print("settings trial expiration")
            expirationDropdown = Driver.find_element_by_name("promotionalTrialExpiration")
            for n in range(11): # 31 max days
                expirationDropdown.send_keys(str(Keys.UP))
            Settings.debug_delay_check()
            if expiration:
                for n in range(int(expiration)):
                    expirationDropdown.send_keys(Keys.DOWN)
            Settings.dev_print("successfully set trial expiration")
            Settings.debug_delay_check()
            # duration dropdown
            # LIMIT_ALLOWED = ["1 day","3 days","7 days","14 days","1 month","3 months","6 months","12 months"]
            Settings.dev_print("settings trial duration")
            durationDropwdown = Driver.find_element_by_name("promotionalTrialDuration")
            for n in range(11):
                durationDropwdown.send_keys(str(Keys.UP))
            Settings.debug_delay_check()
            num = 1
            if str(duration) == "1 day": num = 1
            if str(duration) == "3 day": num = 2
            if str(duration) == "7 days": num = 3
            if str(duration) == "14 days": num = 4
            if str(duration) == "1 month": num = 5
            if str(duration) == "3 months": num = 6
            if str(duration) == "6 months": num = 7
            if str(duration) == "12 months": num = 8
            for n in range(int(num)-1):
                durationDropwdown.send_keys(Keys.DOWN)
            Settings.dev_print("successfully set trial duration")
            Settings.debug_delay_check()
            # find and click promotionalTrialConfirm
            # if Settings.is_debug():
            #     Settings.dev_print("finding trial cancel")
            #     Driver.find_element_to_click("promotionalTrialCancel").click()
            #     Settings.print("skipping: Promotion (debug)")
            #     Settings.dev_print("successfully cancelled promotion trial")
            #     return True
            Settings.dev_print("finding trial save")
            save_ = Driver.find_element_to_click("promotionalTrialConfirm")
            # "g-btn.m-rounded"

            save_ = Driver.browser.find_elements_by_class_name("g-btn.m-rounded")
            for save__ in save_:
                Settings.print(save__.get_attribute("innerHTML"))
            if len(save_) == 0:
                Settings.dev_print("unable to find promotion 'Create'")
                Settings.err_print("unable to save promotion")
                return False
            for save__ in save_:
                if save__.get_attribute("innerHTML").lower().strip() == "create":
                    save_ = save__    
            Settings.print(save_.get_attribute("innerHTML"))
            Settings.dev_print("saving promotion")
            save_.click()
            Settings.dev_print("successfully saved promotion")
            ## TODO ##
            # finish this
            link = ""
            # Settings.dev_print("copying trial link")
            # Driver.find_element_by_name("promotionalTrialLink").click()
            # Settings.dev_print("successfully copied trial link")

            # in order for this to work accurately i need to figure out the number of trial things already on the page
            # then find the new trial thing
            # then get the link for the new trial thing
            # as of now it creates a new trial for the x duration so voila

            # todo maybe probably never:
            # go to /home
            # enter copied paste into new post
            # get text in new post
            # email link to user

            Settings.dev_print("successful promotion trial")
            Settings.debug_delay_check()
            return link
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to apply promotion")
            return None

    def promotion_user_directly(promotion=None):
        """
        Apply the promotion directly to the user.

        Parameters
        ----------
        promotion : classes.Promotion
            The promotion to provide to the user

        Returns
        -------
        bool
            Whether or not the promotion was successful

        """

        if not promotion:
            Settings.err_print("missing promotion")
            return False
        # go to onlyfans.com/my/subscribers/active
        promotion.get()
        expiration = promotion["expiration"]
        months = promotion["duration"]
        user = promotion["user"]
        message = promotion["message"]
        if int(expiration) > int(Settings.get_discount_max_amount()):
            Settings.warn_print("discount too high, max -> {}%".format(Settings.get_discount_max_amount()))
            discount = Settings.get_discount_max_amount()
        elif int(expiration) > int(Settings.get_discount_min_amount()):
            Settings.warn_print("discount too low, min -> {}%".format(Settings.get_discount_min_amount()))
            discount = Settings.get_discount_min_amount()
        if int(months) > int(Settings.get_discount_max_months()):
            Settings.warn_print("duration too high, max -> {} days".format(Settings.get_discount_max_months()))
            months = Settings.get_discount_max_months()
        elif int(months) < int(Settings.get_discount_min_months()):
            Settings.warn_print("duration too low, min -> {} days".format(Settings.get_discount_min_months()))
            months = Settings.get_discount_min_months()
        try:
            Settings.maybe_print("goto -> /{}".format(user))
            Driver.go_to_page(user)
            # click discount button
            Driver.find_element_to_click("discountUserPromotion").click()
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
            Settings.dev_print("successfully entered expiration")
            Settings.dev_print("entering duration")
            for n in range(11):
                durations.send_keys(str(Keys.UP))
            for n in range(int(months)-1):
                durations.send_keys(Keys.DOWN)
            Settings.dev_print("successfully entered duration")
            Settings.debug_delay_check()
            Settings.dev_print("entering message")
            message.clear()
            message.send_keys(message)
            Settings.dev_print("successfully entered message")
            Settings.dev_print("applying discount")
            save = Driver.find_element_by_name("promotionalTrialApply")
            if Settings.is_debug() == "True":
                Driver.find_element_by_name("promotionalTrialCancel").click()
                Settings.maybe_print("skipping save discount (debug)")
                Settings.dev_print("successfully canceled discount")
                cancel.click()
                return True
            save.click()
            Settings.print("discounted: {}".format(user.username))
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

    def read_user_messages(username, user_id=None):
        """
        Read the messages of the target user by username or user id.

        Parameters
        ----------
        username : str
            The username of the user to read messages of
        user_id : str
            The user id of the user to read messages of

        Returns
        -------
        list
            A list containing the messages read

        """

        try:
            # go to onlyfans.com/my/subscribers/active
            Driver.message_user(username, user_id=user_id)
            messages_sent_ = []
            try:
                messages_sent_ = Driver.find_elements_by_name("messagesFrom")
            except Exception as e:
                if "Unable to locate elements" in str(e):
                    pass
                else: Settings.dev_print(e)
            # Settings.print("first message: {}".format(messages_received_[0].get_attribute("innerHTML")))
            # messages_received_.pop(0) # drop self user at top of page
            messages_all_ = []
            try:
                messages_all_ = Driver.find_elements_by_name("messagesAll")
            except Exception as e:
                if "Unable to locate elements" in str(e):
                    pass
                else: Settings.dev_print(e)
            messages_all = []
            messages_received = []
            messages_sent = []
            # timestamps_ = Driver.browser.find_elements_by_class_name("b-chat__message__time")
            # timestamps = []
            # for timestamp in timestamps_:
                # Settings.maybe_print("timestamp1: {}".format(timestamp))
                # timestamp = timestamp["data-timestamp"]
                # timestamp = timestamp.get_attribute("innerHTML")
                # Settings.maybe_print("timestamp: {}".format(timestamp))
                # timestamps.append(timestamp)
            for message in messages_all_:
                message = message.get_attribute("innerHTML")
                message = re.sub(r'<[a-zA-Z0-9=\"\\/_\-!&;%@#$\(\)\.:\+\s]*>', "", message)
                Settings.maybe_print("all: {}".format(message))
                messages_all.append(message)
            messages_and_timestamps = []
            # messages_and_timestamps = [j for i in zip(timestamps,messages_all) for j in i]
            # Settings.maybe_print("chat log:")
            # for f in messages_and_timestamps:
                # Settings.maybe_print(": {}".format(f))
            for message in messages_sent_:
                # Settings.maybe_print("from1: {}".format(message.get_attribute("innerHTML")))
                message = message.find_element_by_class_name(Element.get_element_by_name("enterMessage").getClass()).get_attribute("innerHTML")
                message = re.sub(r'<[a-zA-Z0-9=\"\\/_\-!&;%@#$\(\)\.:\+\s]*>', "", message)
                Settings.maybe_print("sent: {}".format(message))
                messages_sent.append(message)
            i = 0

            # messages_all = list(set(messages_all))
            # messages_sent = list(set(messages_sent))
            # i really only want to remove duplicates if they're over a certain str length

            def remove_dupes(list_):
                """Remove duplicates from the list"""

                for i in range(len(list_)):
                    for j in range(len(list_)):
                        # if j >= len(list_): break
                        if i==j: continue
                        if str(list_[i]) == str(list_[j]) and len(str(list_[i])) > 10:
                            del list_[j]
                            remove_dupes(list_)
                            return
                            
            remove_dupes(messages_all)
            remove_dupes(messages_sent)

            for message in messages_all:
                if message not in messages_sent:
                    messages_received.append(message)
                i += 1
            Settings.maybe_print("received: {}".format(messages_received))
            Settings.maybe_print("sent: {}".format(messages_sent))
            Settings.maybe_print("messages sent: {}".format(len(messages_sent)))
            Settings.maybe_print("messages received: {}".format(len(messages_received)))
            Settings.maybe_print("messages all: {}".format(len(messages_all)))
            return [messages_all, messages_and_timestamps, messages_received, messages_sent]
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failure to read chat - {}".format(username))
            return [[],[],[],[]]

    ###################
    ##### Refresh #####
    ###################

    def refresh():
        """Refresh the web browser"""

        Settings.dev_print("refreshing browser...")
        Driver.browser.refresh()

    #################
    ##### Reset #####
    #################

    def reset():
        """
        Reset the web browser to home page

        Returns
        -------
        bool
            Whether or not the browser was reset successfully

        """

        if not Driver.browser:
            Settings.print('OnlyFans not open, skipping reset')
            return True
        try:
            Driver.go_to_home()
            Settings.print('OnlyFans reset')
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failure resetting onlyfans")
            return False

    ####################
    ##### Schedule #####
    ####################

    def schedule(schedule):
        """
        Enter the provided schedule

        Parameters
        ----------
        schedule : classes.Schedule
            The schedule object containing the values to enter

        Returns
        -------
        bool
            Whether or not the schedule was entered successfully

        """

        if str(schedule) == "None" or schedule: return True
        try:
            month_ = schedule["month"]
            day_ = schedule["day"]
            year_ = schedule["year"]
            hour_ = schedule["hour"]
            minute_ = schedule["minute"]
            Settings.print("Schedule:")
            Settings.print("- Date: {}".format(schedule["date"]))
            Settings.print("- Time: {}".format(schedule["time"]))
            Driver.open_more_options()
            # click schedule
            Settings.dev_print("opening schedule")
            Driver.find_element_to_click("scheduleAdd").click()
            Settings.dev_print("successfully opened schedule")

            # find and click month w/ correct date
            while True:
                Settings.dev_print("getting date")
                existingDate = Driver.find_element_by_name("scheduleDate").get_attribute("innerHTML")
                Settings.dev_print("date: {} - {} {}".format(existingDate, month_, year_))
                if str(month_) in str(existingDate) and str(year_) in str(existingDate): break
                else: Driver.find_element_to_click("scheduleNextMonth").click()
            Settings.dev_print("successfully set month")
            # set day in month
            Settings.dev_print("setting days")
            days = Driver.find_elements_by_name("scheduleDays")
            for day in days:
                inner = day.get_attribute("innerHTML").replace("<span><span>","").replace("</span></span>","")
                if str(day_) == str(inner):
                    day.click()
                    Settings.dev_print("clicked day")
            Settings.dev_print("successfully set day")
            Settings.debug_delay_check()
            
            # save schedule date
            saves = Driver.find_element_to_click("scheduleNext")
            Settings.dev_print("found next button, clicking")
            saves.click()
            Settings.dev_print("successfully saved date")
            # set hours
            # try:
            #     hours = Driver.browser.find_element_by_class_name("vdatetime-time-picker.vdatetime-time-picker__with-suffix")
            #     Settings.print(hours)
            #     for hour in hours:
            #         Settings.print(hour.get_attribute("class"))
            #         Settings.print(hour.get_attribute("innerHTML"))
            # except Exception as e:
            #     Settings.print(e)

                # try:
                #     Settings.print(2)
                #     hours = Driver.browser.find_element_by_class_name("vdatetime-time-picker__list--hours")
                #     Settings.print(hours)
                #     for hour in hours:
                #         Settings.print(hour.get_attribute("class"))
                #         Settings.print(hour.get_attribute("innerHTML"))
                # except Exception as e:
                #     Settings.print(e)


                # return False

            Settings.dev_print("setting hours")
            hours = Driver.find_elements_by_name("scheduleHours")
            # this finds both hours and minutes so just cut off first 12
            hours = hours[:12]
            for hour in hours:
                inner = hour.get_attribute("innerHTML")
                if str(hour_) in str(inner) and hour.is_enabled():
                    hour.click()
                    Settings.dev_print("successfully set hours")
                    break
            # set minutes
            Settings.dev_print("setting minutes")
            minutes = Driver.find_elements_by_name("scheduleMinutes")
            # and get ones after first 12 hours
            minutes = minutes[12:]
            for minute in minutes:
                inner = minute.get_attribute("innerHTML")
                if str(minute_) in str(inner) and minute.is_enabled():
                    minute.click()
                    Settings.dev_print("successfully set minutes")
                    break
            # set am/pm
            Settings.dev_print("setting suffix")
            # suffixes = Driver.find_elements_by_name("scheduleAMPM")
            suffixes = Driver.find_elements_by_name("scheduleMinutes")
            for suffix in suffixes:
                inner = suffix.get_attribute("innerHTML")
                if str(schedule["suffix"]).lower() in str(inner).lower() and suffix.is_enabled():
                    suffix.click()
                    Settings.dev_print("successfully set suffix")
                    break
            # save time
            Settings.dev_print("saving schedule")
            Settings.debug_delay_check()
            if Settings.is_debug() == "True":
                Settings.maybe_print("skipping schedule (debug)")
                Driver.find_element_to_click("scheduleCancel").click()
                Settings.dev_print("successfully canceled schedule")
            else:
                Driver.find_element_to_click("scheduleSave").click()
                Settings.dev_print("successfully saved schedule")
                Settings.print("schedule entered")
            Settings.dev_print("### Schedule Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to enter schedule")
            return False

    ####################
    ##### Settings #####
    ####################

    # gets all settings from whichever page its on
    # or get a specific setting
    # probably just way easier and resourceful to do it all at once
    # though it would be ideal to also be able to update individual settings without risking other settings

    # goes through the settings and get all the values
    # @staticmethod
    # def settings_get_all():
    #     Settings.print("Getting All Settings")
    #     profile = Profile()
    #     try:
    #         pages = Profile.get_pages()
    #         for page in pages:
    #             data = Driver.sync_from_settings_page(page)
    #             for key, value in data:
    #                 profile[key] = value
    #         Settings.dev_print("successfully got settings")
    #         Settings.print("Settings Retrieved")
    #     except Exception as e:
    #         Driver.error_checker(e)
    #     return profile

    def sync_from_settings_page(profile=None, page=None):
        """
        Sync values from settings page.

        Parameters
        ----------
        profile : Profile
            The profile object to sync from
        page : str
            The profile page to sync settings from

        Returns
        -------
        bool
            Whether or not the sync was successful

        """

        Settings.print("Getting Settings: {}".format(page))
        from ..classes.profile import Profile
        try:
            variables = Profile.get_variables_for_page(page)
            Settings.dev_print("going to settings page: {}".format(page))
            Driver.go_to_settings(page)
            Settings.dev_print("reached settings: {}".format(page))
            if profile == None:
                profile = Profile()
            for var in variables:
                name = var[0]
                page_ = var[1]
                type_ = var[2]
                status = None
                Settings.dev_print("searching: {} - {}".format(name, type_))
                try:
                    element = Driver.find_element_by_name(name)
                    Settings.dev_print("successful ele: {}".format(name))
                except Exception as e:
                    Driver.error_checker(e)
                    continue
                if str(type_) == "text":
                    # get attr text
                    status = element.get_attribute("innerHTML").strip() or None
                    status2 = element.get_attribute("value").strip() or None
                    Settings.print("{} - {}".format(status, status2))
                    if not status and status2: status = status2
                elif str(type_) == "toggle":
                    # get state true|false
                    status = element.is_selected()
                elif str(type_) == "dropdown":
                    ele = Driver.find_element_by_name(name)
                    Select(Driver.browser.find_element_by_id(ele.getId()))
                    status = element.first_selected_option
                elif str(type_) == "list":
                    status = element.get_attribute("innerHTML")
                elif str(type_) == "file":
                    Settings.print("NEED TO UPDATE THIS")
                    # can get file from image above
                    # can set once found
                    # status = element.get_attribute("innerHTML")
                    # pass
                elif str(type_) == "checkbox":
                    status = element.is_selected()
                if status is not None: Settings.dev_print("successful value: {}".format(status))
                Settings.maybe_print("{} : {}".format(name, status))
                setattr(profile, str(name), status)
            Settings.dev_print("successfully got settings page: {}".format(page))
            Settings.print("Settings Page Retrieved: {}".format(page))
        except Exception as e:
            Driver.error_checker(e)

    # goes through each page and sets all the values
    def sync_to_settings_page(profile=None, page=None):
        """
        Sync values to settings page.

        Parameters
        ----------
        profile : Profile
            The profile object to sync to
        page : str
            The profile page to sync settings to

        Returns
        -------
        bool
            Whether or not the sync was successful

        """

        Settings.print("Updating Page Settings: {}".format(page))
        from ..classes.profile import Profile
        try:
            variables = Profile.get_variables_for_page(page)
            Settings.dev_print("going to settings page: {}".format(page))
            Driver.go_to_settings(page)
            Settings.dev_print("reached settings: {}".format(page))
            if profile == None:
                profile = Profile()
            for var in variables:
                name = var[0]
                page_ = var[1]
                type_ = var[2]
                status = None
                Settings.dev_print("searching: {} - {}".format(name, type_))
                try:
                    element = Driver.find_element_by_name(name)
                    Settings.dev_print("successful ele: {}".format(name))
                except Exception as e:
                    Driver.error_checker(e)
                    continue
                if str(type_) == "text":

                    element.send_keys(getattr(profile, str(name)))
                elif str(type_) == "toggle":
                    # somehow set the other toggle state
                    pass
                elif str(type_) == "dropdown":
                    ele = Driver.find_element_by_name(name)
                    Select(Driver.browser.find_element_by_id(ele.getId()))
                    # go to top
                    # then go to matching value
                    pass
                elif str(type_) == "list":
                    element.send_keys(getattr(profile, str(name)))
                elif str(type_) == "file":
                    element.send_keys(getattr(profile, str(name)))
                elif str(type_) == "checkbox":
                    element.click()
            if Settings.is_debug() == "True":
                Settings.dev_print("successfully cancelled settings page: {}".format(page))
            else:
                Driver.settings_save(page=page)
                Settings.dev_print("successfully set settings page: {}".format(page))
            Settings.print("Settings Page Updated: {}".format(page))
        except Exception as e:
            Driver.error_checker(e)

    # @staticmethod
    # def settings_set_all(Profile):
    #     Settings.print("Updating All Settings")
    #     try:
    #         pages = Profile.TABS
    #         for page in pages:
    #             Driver.sync_to_settings_page(Profile, page)
    #         Settings.dev_print("successfully set settings")
    #         Settings.print("Settings Updated")
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
    def settings_save(page=None):
        """
        Save the provided settings page if it is a page that saves

        Parameters
        ----------
        page : str
            The settings page to check if saves
        
        """

        if str(page) not in ["profile", "account", "security"]:
            Settings.dev_print("not saving: {}".format(page))
            return
        try:
            Settings.dev_print("saving: {}".format(page))
            element = Driver.find_element_by_name("profileSave")
            Settings.dev_print("derp")
            element = Driver.find_element_to_click("profileSave")
            Settings.dev_print("found page save")
            if Settings.is_debug() == "True":
                Settings.print("skipping settings save (debug)")
            else:
                Settings.dev_print("saving page")
                element.click()
                Settings.dev_print("page saved")
        except Exception as e:
            Driver.error_checker(e)

    #################
    ##### Spawn #####
    #################

    @staticmethod
    def spawn_browser(browserType):
        """
        Spawns a browser according to args.

        Browser options can be: firefox, chrome

        Parameters
        ----------
        driver : Selenium.WebDriver
            Selenium Webdriver to attach a browser to

        Returns
        -------
        Selenium.WebDriver
            The created browser object

        """

        if Settings.is_debug("selenium") == "False":
            import logging
            from selenium.webdriver.remote.remote_connection import LOGGER as SeleniumLogger
            SeleniumLogger.setLevel(logging.ERROR)
            logging.getLogger("urllib3").setLevel(logging.ERROR)
            logging.getLogger("requests").setLevel(logging.ERROR)
            if Settings.get_verbosity() == 3:
                SeleniumLogger.setLevel(logging.WARNING)
                logging.getLogger("urllib3").setLevel(logging.WARNING)
                logging.getLogger("requests").setLevel(logging.WARNING)

        browser = None
        browserTypeFinal = None
        Settings.print("spawning web browser...")

        def attempt_chrome():
            """
            Spawn a Google browser
            
            Returns
            -------
            bool
                Whether or not the browser was created successfully

            """

            Settings.maybe_print("attempting chrome web browser...")
            browserAttempt = None
            try:
                options = webdriver.ChromeOptions()
                options.add_argument("--no-sandbox") # Bypass OS security model
                options.add_argument('--disable-software-rasterizer')
                if not Settings.is_show_window() == "True":
                    options.add_argument('--headless')
                options.add_argument("--disable-extensions") # disabling extensions
                options.add_argument("--disable-infobars") # disabling infobars
                options.add_argument("user-data-dir=selenium") 
                options.add_argument('--ignore-certificate-errors')
                options.add_argument("--remote-debugging-address=localhost")    
                options.add_argument("--remote-debugging-port=9223")
                options.add_argument("--allow-insecure-localhost")                
                capabilities = {
                  'browserName': 'chrome',
                  'platform': 'LINUX',
                  'chromeOptions':  {
                    'acceptInsecureCerts': True,
                    'useAutomationExtension': False,
                    'forceDevToolsScreenshot': True,
                    'args': ['--start-maximized', '--disable-infobars']
                  }
                }  
                service_args = []
                if Settings.is_debug("google"):
                    service_args = ["--verbose", "--log-path={}".format(Settings.get_logs_path("google"))]
                Settings.dev_print("executable_path: {}".format(chromedriver_binary.chromedriver_filename))
                # options.binary_location = chromedriver_binary.chromedriver_filename
                browserAttempt = webdriver.Chrome(desired_capabilities=capabilities, executable_path=chromedriver_binary.chromedriver_filename, chrome_options=options, service_args=service_args)
                Settings.print("browser created - chrome")
                browserTypeFinal = "chrome"
                return browserAttempt
            except Exception as e:
                Settings.warn_print("unable to launch chrome!")
                Settings.dev_print(e)
            return browserAttempt

        def attempt_firefox():
            """
            Spawn a Firefox browser
            
            Returns
            -------
            bool
                Whether or not the browser was created successfully

            """

            Settings.maybe_print("attempting firefox web browser...")
            # firefox needs non root
            if os.geteuid() == 0:
                Settings.print("You must run `onlysnarf` as non-root for Firefox to work correctly!")
                return False
            browserAttempt = None
            try:
                d = DesiredCapabilities.FIREFOX
                options = FirefoxOptions()
                if Settings.is_debug("firefox") == "True":
                    options.log.level = "trace"
                if Settings.is_show_window() == "False":
                    options.add_argument("--headless")
                options.add_argument("--enable-file-cookies")

                # BUG: cookies
                # added for cookies, doesn't seem to help
                # opts.add_argument("--user-data-dir=/tmp")

                # browserAttempt = webdriver.Firefox(options=options, log_path='/var/log/onlysnarf/geckodriver.log')
                # browserAttempt = webdriver.Firefox(firefox_binary="/usr/local/bin/geckodriver", options=options, capabilities=d)
                browserAttempt = webdriver.Firefox(options=options, desired_capabilities=d, service_log_path=Settings.get_logs_path("firefox"))
                Settings.print("browser created - firefox")
                browserTypeFinal = "firefox"
                return browserAttempt
            except Exception as e:
                Settings.warn_print("unable to launch firefox!")
                Settings.dev_print(e)
            return browserAttempt

        def attempt_reconnect():
            """
            Reconnect to the corresponding session id and url.

            Notes:
            https://stackoverflow.com/questions/8344776/can-selenium-interact-with-an-existing-browser-session
            https://stackoverflow.com/questions/47861813/how-can-i-reconnect-to-the-browser-opened-by-webdriver-with-selenium

            Parameters
            ----------
            browser : WebDriver
                An existing (for the running script) WebDriver browser to reconnect the session to, if it exists.
            reconnect_id : int
                The saved reconnect id to use
            url : str
                The saved url to reconnect with

            Returns
            -------
            bool
                Whether or not the reconnect was successful

            """

            reconnect_id, url, browserTypeFinal_ = Driver.read_session_data()
            if not reconnect_id and not url:
                Settings.maybe_print("unable to read session data")
                return None
            if not browserTypeFinal_:
                Settings.maybe_print("unable to read previous browser type")
                return None
            Settings.maybe_print("reconnecting to web browser...")
            Settings.dev_print("reconnect id: {}".format(reconnect_id))
            Settings.dev_print("reconnect url: {}".format(url))
            try:
                # original_execute = WebDriver.execute
                # def new_command_execute(command, params=None):
                #     if command == "newSession":
                #         # Mock the response
                #         return {'success': 0, 'value': None, 'sessionId': reconnect_id}
                #     else:
                #         return original_execute(command, params)
                # Patch the function before creating the browser object
                # WebDriver.execute = new_command_execute
                browserAttempt = webdriver.Remote(command_executor=url, desired_capabilities={})
                if browserAttempt.session_id != reconnect_id:   # this is pretty much guaranteed to be the case
                    browserAttempt.close()   # this closes the session's window - it is currently the only one, thus the session itself will be auto-killed, yet:
                    browserAttempt.quit()    # for remote connections (like ours), this deletes the session, but does not stop the SE server
                # take the session that's already running
                browserAttempt.session_id = reconnect_id
                # Replace the patched function with original function
                # WebDriver.execute = original_execute
                # necessary?
                browser.title # fails check with: 'NoneType' object has no attribute 'title'
                Settings.print("browser reconnected!")
            except Exception as e:
                Settings.warn_print("unable to reconnect!")
                Settings.dev_print(e)
            return browser

        def attempt_remote():
            """
            Connect to remote Selenium webdriver

            Returns
            -------
            bool
                Whether or not the remote connection was successful

            """

            link = 'http://{}:{}/wd/hub'.format(config["remote_browser_host"], config["remote_browser_port"])
            Settings.dev_print("remote url: {}".format(link))

            def attempt(dc, opts):
                try:
                    browserAttempt = webdriver.Remote(command_executor=link, desired_capabilities=dc, options=opts)
                    Settings.print("remote browser created - {}".format(browserType))
                    return browserAttempt
                except Exception as e:
                    Settings.warn_print("unable to connect remotely!")
                    Settings.dev_print(e)
                return None

            def chrome_options():
                try:
                    Settings.dev_print("attempting remote: chrome")
                    dC = DesiredCapabilities.CHROME
                    options = webdriver.ChromeOptions()
                    if Settings.is_show_window() == "False":
                        options.add_argument('--headless')
                    browserTypeFinal = "chrome"
                    return dC, options
                except Exception as e:
                    Settings.dev_print(e)
                return None, None

            def firefox_options():
                try:
                    Settings.dev_print("attempting remote: firefox")
                    dC = DesiredCapabilities.FIREFOX
                    options = webdriver.FirefoxOptions()
                    if Settings.is_show_window() == "False":
                        options.add_argument('--headless')
                    browserTypeFinal = "firefox"
                    return dC, options
                except Exception as e:
                    Settings.dev_print(e)
                return None, None

            if "chrome" in browserType: return attempt(*chrome_options())
            elif "firefox" in browserType: return attempt(*firefox_options())
            else: # auto
                # alphabetical
                try:
                    return attempt(*chrome_options())
                except Exception as e:
                    Settings.warn_print("unable to connect remotely via chrome!")
                    Settings.dev_print(e)
                try:
                    return attempt(*firefox_options())
                except Exception as e:
                    Settings.warn_print("unable to connect remotely via firefox!")
                    Settings.dev_print(e)
            return None

        ################################################################################################################################################
        ################################################################################################################################################
        ################################################################################################################################################

        if "auto" in browserType:
            browser = attempt_reconnect() or attempt_chrome() or attempt_firefox()
        elif "remote" in browserType:
            browser = attempt_remote()
        elif "chrome" in browserType:
            browser = attempt_chrome()
        elif "firefox" in browserType:
            browser = attempt_firefox()
        if "reconnect" in browserType:
            if not browser: browser = attempt_chrome() or attempt_firefox()
            browser = attempt_reconnect(browser)

        if browser and Settings.is_keep() == "True":
            Driver.write_session_data(browser.session_id, browser.command_executor._url, browserTypeFinal)
        if not browser:
            Settings.err_print("unable to spawn a web browser!")
            os._exit(1)
        browser.implicitly_wait(30) # seconds
        browser.set_page_load_timeout(1200)
        browser.file_detector = LocalFileDetector() # for uploading via remote sessions
        Driver.browser = browser
        Driver.browsers.append(browser)

    ## possibly move these functions elsewhere (again)
    def read_session_data():
        Settings.maybe_print("reading local session")
        path_ = os.path.join(Settings.get_base_directory(), "session.json")
        Settings.dev_print("local session path: "+str(path_))
        id_ = None
        url = None
        browserTypeFinal = None
        try:
            with open(str(path_)) as json_file:  
                data = json.load(json_file)
                id_ = data['id']
                url = data['url']
                browserTypeFinal = data['browserTypeFinal']
            Settings.maybe_print("loaded local users")
        except Exception as e:
            Settings.dev_print(e)
        return (id_, url, browserTypeFinal)

    def write_session_data(id_, url, browserTypeFinal):
        Settings.maybe_print("writing local session")
        Settings.dev_print("saving session id: {}".format(id_))        
        Settings.dev_print("saving session url: {}".format(url))
        path_ = os.path.join(Settings.get_base_directory(), "session.json")
        Settings.dev_print("local session path: "+str(path_))
        data = {}
        data['id'] = id_
        data['url'] = url
        data['browserTypeFinal'] = browserTypeFinal
        try:
            with open(str(path_), 'w') as outfile:  
                json.dump(data, outfile, indent=4, sort_keys=True)
        except FileNotFoundError:
            Settings.err_print("Missing Session File")
        except OSError:
            Settings.err_print("Missing Session Path")

    #####

    #####


    def tryDriverFunction(function, objecto):
        try:
            successes = 0
            failures = 0
            successful = Driver[function](objecto)
            if successful: successes+=1
            else: failures+=1
        except Exception as e:
            Settings.dev_print(e)
            failures+=1
        Settings.maybe_print("successful: {}".format(successes))
        Settings.maybe_print("failed: {}".format(failures))
        if successes > failures: return True


    ##################
    ##### Upload #####
    ##################

    def upload_files(files):
        """
        Upload the files to a post or message.

        Must be on a post or message.

        Parameters
        ----------
        files : list
            The list of files to upload

        Returns
        -------
        bool
            Whether or not the upload was successful

        """

        if Settings.is_skip_download() == "True": 
            Settings.print("skipping upload (download)")
            return True
        elif Settings.is_skip_upload() == "True": 
            Settings.print("skipping upload (upload)")
            return True
        if len(files) == 0:
            Settings.maybe_print("skipping upload (empty file list)")
            return True
        if Settings.is_skip_upload() == "True":
            Settings.print("skipping upload (disabled)")
            return True
        files = files[:int(Settings.get_upload_max())]
        Settings.print("uploading file(s): {}".format(len(files)))

        ####

        import threading
        import concurrent.futures

        files_ = []

        def prepare(file):
            uploadable = file.prepare() # downloads if Google_File
            if not uploadable: Settings.err_print("unable to upload - {}".format(file.get_title()))
            else: files_.append(file)    

        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.map(prepare, files)

        Settings.dev_print("files prepared: {}".format(len(files_)))
        if len(files_) == 0:
            Settings.err_print("skipping upload (unable to prepare files)")
            return False

        ####

        enter_file = Driver.browser.find_element_by_id("attach_file_photo")

        i = 1
        for file in files_:
            Settings.print('> {} - {}/{}'.format(file.get_title(), i, len(files)))
            i += 1
            Driver.drag_and_drop_file(enter_file , file.get_path())
            time.sleep(1)
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
        Settings.debug_delay_check()
        if Driver.error_window_upload(): Settings.dev_print("### Files Upload Successful ###")
        else: Settings.dev_print("### Files Upload Successful (probably) ###")
        return True

    #################
    ##### Users #####
    #################

    def get_username():
        """
        Gets the username of the logged in user.

        Returns
        -------
        str
            The username of the logged in user

        """

        username = None
        try:
            Driver.go_to_home()
            Driver.auth()
            eles = Driver.browser.find_elements_by_tag_name("a")
            eles = [ele for ele in eles 
                    if "@" in str(ele.get_attribute("innerHTML"))
                    and "onlyfans" not in str(ele.get_attribute("innerHTML"))
                    ]
            Settings.dev_print("successfully found users")
            # for ele in eles:
                # Settings.print("{} - {}".format(ele.get_attribute("innerHTML"), ele.get_attribute("href")))
            if len(eles) == 0:
                Settings.err_print("unable to find username")
                return None
            username = str(eles[0].get_attribute("href")).replace(ONLYFANS_HOME_URL2,"")
            Settings.dev_print("successfully got username: {}".format(username))
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to find username")
        return username

    def following_get():
        """
        Return lists of accounts followed by the logged in user.

        Returns
        -------
        list
            The list of users being followed

        """

        users = []
        try:
            Driver.go_to_page(ONLYFANS_USERS_FOLLOWING_URL)
            count = 0
            while True:
                elements = Driver.browser.find_elements_by_class_name("m-subscriptions")
                if len(elements) == count: break
                Settings.print_same_line("({}/{}) scrolling...".format(count, len(elements)))
                count = len(elements)
                Driver.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            Settings.print("")
            elements = Driver.browser.find_elements_by_class_name("m-subscriptions")
            Settings.dev_print("successfully found subscriptions")
            for ele in elements:
                username = ele.find_element_by_class_name("g-user-username").get_attribute("innerHTML").strip()
                name = ele.find_element_by_class_name("g-user-name").get_attribute("innerHTML")
                name = re.sub("<!-*>", "", name)
                name = re.sub("<.*\">", "", name)
                name = re.sub("</.*>", "", name).strip()
                # Settings.print("username: {}".format(username))
                # Settings.print("name: {}".format(name))
                users.append({"name":name, "username":username.replace("@","")}) 
            Settings.maybe_print("found: {}".format(len(users)))
            for user in users:
                Settings.dev_print(user)
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to find subscriptions")
        Settings.dev_print("successfully found following users")
        return users

    def users_get(page=ONLYFANS_USERS_ACTIVE_URL):
        """
        Return lists of accounts subscribed to the logged in user.

        Returns
        -------
        list
            The list of users subscribed

        """

        users = []
        try:
            Driver.go_to_page(page)
            # user_count = int(Driver.browser.find_element_by_class_name("l-sidebar__user-data__item__count").get_attribute("innerHTML").strip())
            user_count = Driver.browser.find_elements_by_tag_name("a")
            # for debugging new regexes:
            # for ele in user_count:
            #     Settings.print("{}  -  {}".format(ele.get_attribute("href"), ele.get_attribute("innerHTML")))
            user_count = [ele.get_attribute("innerHTML").strip() for ele in user_count
                            if "/my/subscribers/active" in str(ele.get_attribute("href"))][2] # get 3rd occurrence
            # should be:
            # <span class="l-sidebar__user-data__item__count">423</span> Fans
            user_count = re.search(r'>[0-9]*<', str(user_count))
            user_count = user_count.group()
            user_count = user_count.replace("<","").replace(">","")

            thirdTime = 0
            count = 0
            while True:
                elements = Driver.browser.find_elements_by_class_name("m-fans")
                if len(elements) == int(user_count): break
                if len(elements) == int(count) and thirdTime >= 3: break
                Settings.print_same_line("({}/{}) scrolling...".format(count, user_count))
                count = len(elements)
                Driver.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                if thirdTime >= 3 and len(elements) == 0: break
                thirdTime += 1
            Settings.print("")
            elements = Driver.browser.find_elements_by_class_name("m-fans")
            Settings.dev_print("successfully found fans")
            Settings.dev_print("finding users")
            for ele in elements:

                # add checks for lists here

                # /my/favorites
                # /my/lists/34324234

                # eles_ = ele.find_elements_by_tag_name("a")
                # isFavorite = False
                # eles = [ele for ele in eles_
                #     if "/my/favorites" in str(ele.get_attribute("href"))]
                # if len(eles) > 0: isFavorite = True

                # lists = []
                # eles = [ele.get_attribute("href") for ele in eles_
                #     if "/my/lists" in str(ele.get_attribute("href"))]
                # for list_ in eles:
                #     listNum = str(list_).replace("https://onlyfans.com/my/lists/", "")
                #     Settings.maybe_print("list #: {}".format(listNum))
                #     lists.append(listNum)

                    ##
                    # need to open tab and find name of list if not already known
                    ##
                    # check if list name is already known
                    # open tab to list page
                    # find html on page with list name
                    # save list
                # Settings.dev_print("successfully found lists")
                username = ele.find_element_by_class_name("g-user-username").get_attribute("innerHTML").strip()
                name = ele.find_element_by_class_name("g-user-name").get_attribute("innerHTML")
                name = re.sub("<!-*>", "", name)
                name = re.sub("<.*\">", "", name)
                name = re.sub("</.*>", "", name).strip()
                # Settings.print("username: {}".format(username))
                # Settings.print("name: {}".format(name))
                # start = datetime.strptime(str(datetime.now()), "%m-%d-%Y:%H:%M")
                # users.append({"name":name, "username":username.replace("@",""), "isFavorite":isFavorite, "lists":lists}) # ,"id":user_id, "started":start})
                users.append({"name":name, "username":username.replace("@","")}) # ,"id":user_id, "started":start})
            Settings.dev_print("found users")
            Settings.maybe_print("found: {}".format(len(users)))
            for user in users:
                Settings.dev_print(user)
            Settings.dev_print("successfully found users")
        except Exception as e:
            print(e)
            Driver.error_checker(e)
            Settings.err_print("failed to find users")
        return users

    def user_get_id(username):
        """
        Get the user id of the user by username.

        Parameters
        ----------
        username : str
            The username to find the id of

        Returns
        -------
        str
            The user id of the located user

        """

        user_id = None
        try:
            Driver.go_to_page(username)
            time.sleep(3) # this should realistically only fail if they're no longer subscribed but it fails often from loading
            elements = Driver.browser.find_elements_by_tag_name("a")
            ele = [ele.get_attribute("href") for ele in elements
                    if "/my/chats/chat/" in str(ele.get_attribute("href"))]
            if len(ele) == 0: 
                Settings.warn_print("unable to find user id")
                return None
            ele = ele[0]
            ele = ele.replace("https://onlyfans.com/my/chats/chat/", "")
            user_id = ele
            Settings.dev_print("successfully found user id: {}".format(user_id))
        except Exception as e:
            Settings.dev_print("failure to find id: {}".format(username))
            Driver.error_checker(e)
            Settings.err_print("failed to find user id")
        return user_id

    def search_for_list(name=None, number=None):
        """
        Search for list in Driver.lists cache by name or number.

        Parameters
        ----------
        name : str
            The name of the list to find
        number : int
            The number for the list to find

        Returns
        -------
        str
            The located list name
        str
            The located list number

        """

        Settings.dev_print("lists: {}".format(Driver.lists))
        try:
            for list_ in Driver.lists:
                if list_[0] == name or list_[1] == number:
                    return list_[0], list_[1]
            Settings.dev_print("failed to locate list: {} - {}".format(name, number))
        except Exception as e:
            if "Unable to locate window" not in str(e):
                Settings.dev_print(e)
        return name, number

    def get_list(name=None, number=None):
        """
        Search for list by name or number on OnlyFans.

        Parameters
        ----------
        name : str
            The name of the list to find
        number : int
            The number for the list to find

        Returns
        -------
        list
            The list of users on the found list
        str
            The located list name
        str
            The located list number

        """

        # gets members from list
        users = []
        Settings.maybe_print("getting list: {} - {}".format(name, number))
        name, number = Driver.search_for_list(name=name, number=number)
        try:
            if not name or not number:
                for list_ in Driver.get_lists():
                    if name and str(list_[1]).lower() == str(name).lower():
                        number = list_[0]
                    if number and str(list_[0]).lower() == str(number).lower():
                        name = list_[1]
            users = Driver.users_get(page="/my/lists/{}".format(number))
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to find list members")
        return users, name, number

    def get_lists():
        """
        Search and return all lists from OnlyFans.

        Returns
        -------
        list
            The list of lists that were found

        """

        lists = []
        try:
            Settings.maybe_print("getting lists")
            Driver.go_to_page("/my/lists")

            elements = Driver.browser.find_elements_by_class_name("b-users-lists__item")

            # find favorites
            # find bookmarks
            # find friends
            # find other lists and their names
            # each page has the same user boxes that are used in users_get

            # /my/favorites
            # /my/bookmarks
            # /my/friends
            # /my/lists
            # b-users-lists__item -> href -> /my/lists/#
            # b-users-lists__item__name -> innerHTML -> list name
            # b-users-lists__item__count -> innerHTML -> list amount

            for ele in elements:
                if "/my/favorites" in str(ele.get_attribute("href")):
                    # Settings.print("{} - {}".format(ele.get_attribute("innerHTML"), ele.get_attribute("href")))
                    count = ele.find_element_by_class_name("b-users-lists__item__count").get_attribute("innerHTML").replace("people", "").replace("person", "").strip()
                    if int(count) > 0: lists.append("favorites")
                elif "/my/bookmarks" in str(ele.get_attribute("href")):
                    # Settings.print("{} - {}".format(ele.get_attribute("innerHTML"), ele.get_attribute("href")))
                    count = ele.find_element_by_class_name("b-users-lists__item__count").get_attribute("innerHTML").replace("people", "").replace("person", "").strip()
                    if int(count) > 0: lists.append("bookmarks")
                elif "/my/friends" in str(ele.get_attribute("href")):
                    # Settings.print("{} - {}".format(ele.get_attribute("innerHTML"), ele.get_attribute("href")))
                    count = ele.find_element_by_class_name("b-users-lists__item__count").get_attribute("innerHTML").replace("people", "").replace("person", "").strip()
                    if int(count) > 0: lists.append("friends")
                elif "/my/lists" in str(ele.get_attribute("href")):
                    try:
                        # Settings.print("{} - {}".format(ele.get_attribute("innerHTML"), ele.get_attribute("href")))

                        # ele = ele.find_element_by_class_name("b-users-lists__item__text")
                        listNumber = ele.get_attribute("href").replace("https://onlyfans.com/my/lists/", "")
                        listName = ele.find_element_by_class_name("b-users-lists__item__name").get_attribute("innerHTML").strip()
                        count = ele.find_element_by_class_name("b-users-lists__item__count").get_attribute("innerHTML").replace("people", "").replace("person", "").strip()
                        Settings.dev_print("{} - {}: {}".format(listNumber, listName, count))
                        lists.append([listNumber, listName])
                    except Exception as e:
                        Settings.dev_print(e)
            Settings.dev_print("successfully found lists: {}".format(len(lists)))
        except Exception as e:
            Driver.error_checker(e)
            Settings.print(e)
            Settings.err_print("failed to find lists")
        return lists

    def get_list_members(list):
        """
        Get the members of a list.

        Parameters
        ----------
        list : list
            The list to get members of
        
        Returns
        -------
        list
            The list of members that were found

        """

        users = []
        try:
            users = Driver.users_get(page="/my/lists/{}".format(int(list_)))
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to find list members")
        return users

    def add_user_to_list(username=None, listNumber=None):
        """
        Add user by username to list by number.

        Parameters
        ----------
        username : str
            The username of the user to add to the list
        listNumber : int
            The number of the list to add the user to

        Returns
        -------
        bool
            Whether or not the user was added successfully

        """

        Settings.print("Adding user to list: {} - {}".format(username, listNumber))
        if not username:
            Settings.err_print("missing username for list")
            return False
        if not listNumber:
            Settings.err_print("missing list number")
            return False
        users = []
        try:
            Driver.go_to_page(ONLYFANS_USERS_ACTIVE_URL)
            end_ = True
            count = 0
            user_ = None
            while end_:
                elements = Driver.browser.find_elements_by_class_name("m-fans")
                for ele in elements:
                    username_ = ele.find_element_by_class_name("g-user-username").get_attribute("innerHTML").strip()
                    if str(username) == str(username_).replace("@",""):
                        Driver.browser.execute_script("arguments[0].scrollIntoView();", ele)
                        user_ = ele
                        end_ = False
                if not end_: continue
                if len(elements) == int(count): break
                Settings.print_same_line("({}/{}) scrolling...".format(count, len(elements)))
                count = len(elements)
                Driver.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            Settings.print("")
            Settings.dev_print("successfully found fans")
            if not user_:
                Settings.err_print("unable to find user - {}".format(username))
                return False
            Settings.maybe_print("found: {}".format(username))
            ActionChains(Driver.browser).move_to_element(user_).perform()
            Settings.dev_print("finding list add")
            listAdds = user_.find_elements_by_class_name("g-btn.m-add-to-lists")
            listAdd_ = None
            for listAdd in listAdds:
                if str("/my/lists/"+listNumber) in str(listAdd.get_attribute("href")):
                    Settings.print("skipping: User already on list - {}".format(listNumber))
                    return True
                if " lists " in str(listAdd.get_attribute("innerHTML")).lower():
                    Settings.dev_print("found list add")
                    listAdd_ = listAdd
            Settings.dev_print("clicking list add")
            listAdd_.click()
            links = Driver.browser.find_elements_by_class_name("b-users-lists__item")
            for link in links:
                # Settings.print("{} {}".format(link.get_attribute("href"), link.get_attribute("innerHTML")))
                if str("/my/lists/"+listNumber) in str(link.get_attribute("href")):
                    Settings.dev_print("clicking list")
                    Driver.move_to_then_click_element(link)
                    time.sleep(0.5)
                    Settings.dev_print("successfully clicked list")
            Settings.dev_print("searching for list save")
            close = Driver.find_element_to_click("listSingleSave")
            Settings.dev_print("clicking save list")
            close.click()
            Settings.dev_print("successfully added user to list - {}".format(listNumber))
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to add user to list")
        return False

    def add_users_to_list(users=[], number=None, name=None):
        """
        Add the users to the list by name or number.

        Parameters
        ----------
        users : list
            The list of users to add to the list
        number : int
            The number for the list to add to
        name : str
            The name of the list to add to

        Returns
        -------
        bool
            Whether or not the users were added successfully

        """

        try:
            users = users.copy()
            users_, name, number = Driver.get_list(number=number, name=name)
            # users = [user for user in users if user not in users_]
            for i, user in enumerate(users[:]):
                for user_ in users_:
                    for key, value in user_.items():
                        if str(key) == "username" and str(user.username) == str(value):
                            users.remove(user)
            Settings.maybe_print("adding users to list: {} - {} - {}".format(len(users), number, name))
            try:
                Settings.dev_print("opening toggle options")
                toggle = Driver.browser.find_element_by_class_name("b-users__list__add-btn")
                Settings.dev_print("clicking toggle options")
                toggle.click()
                Settings.dev_print("toggle options opened")
            except Exception as e:
                Settings.dev_print("no options to toggle - users already available")
                # Settings.print("weird fuckup")
                # return Driver.add_users_to_list(users=users, number=number, name=name)
            time.sleep(1)
            original_handle = Driver.browser.current_window_handle
            clicked = False
            Settings.maybe_print("searching for users")
            while len(users) > 0:
                # find user thing
                eles = Driver.browser.find_elements_by_class_name("b-chats__available-users__item.m-search")
                for ele in eles:
                    for user in users.copy():
                        # Settings.print("{} - {}".format(i, user.username))
                        if str(user.username) in str(ele.get_attribute("href")):
                            Settings.maybe_print("found user: {}".format(user.username))
                            # time.sleep(2)
                            Driver.move_to_then_click_element(ele)
                            users.remove(user)
                            clicked = True
                Settings.print_same_line("({}/{}) scrolling...".format(len(eles), len(users)))
                Driver.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                if len(eles) > 100:
                    Settings.maybe_print("adding users to list individually")
                    for user in users.copy():
                        successful = Driver.add_user_to_list(username=user.username, listNumber=number)
                        if successful: users.remove(user)
                # if current window has changed, switch back
                if Driver.browser.current_window_handle != original_handle:
                    Driver.browser.switch_to.window(original_handle)
            Settings.print("")
            if not clicked:
                Settings.print("skipping list add (none)")
                Settings.dev_print("skipping list save")
                Driver.browser.refresh()
                Settings.dev_print("### List Add Successfully Skipped ###")
                return True
            if Settings.is_debug() == "True":
                Settings.print("skipping list add (debug)")
                Settings.dev_print("skipping list save")
                Driver.browser.refresh()
                Settings.dev_print("### List Add Successfully Canceled ###")
                return True
            Settings.dev_print("saving list")
            save = Driver.find_element_by_name("listSave")
            Driver.move_to_then_click_element(save)
            Settings.dev_print("### successfully added users to list")
        except Exception as e:
            Settings.print(e)
            Driver.error_checker(e)
            Settings.err_print("failed to add users to list")
            return False
        return True

    ################
    ##### Exit #####
    ################

    def exit():
        """Save and exit"""

        if Driver.browser == None: return
        if Settings.is_save_users() == "True":
            Settings.print("Saving and Exiting OnlyFans")
            # from OnlySnarf.classes.user import User
            from ..classes.user import User
            User.write_users_local()
        if Settings.is_keep() == "True":
            Settings.maybe_print("keeping browser open")
            # Driver.go_to_home(force=True)
            Driver.go_to_home()
            Settings.dev_print("reset to home page")
            if not Driver.NOT_INFORMED_KEPT:
                Settings.print("Kept Browser Open")
            Driver.NOT_INFORMED_KEPT = True
            # todo: add delay for setting this back to false
            return
        else:
            Settings.print("Exiting OnlyFans")
        Driver.browser.quit()
        Settings.print("Browser Closed")
        Driver._initialized_ = False

##################################################################################

def parse_users(user_ids, starteds, users, usernames):
    # usernames.pop(0)
    # Settings.print("My User Id: {}".format(user_ids[0]))
    # user_ids.pop(0)
    Settings.dev_print("user_ids: "+str(len(user_ids)))
    Settings.dev_print("starteds: "+str(len(starteds)))
    useridsFailed = False
    startedsFailed = False
    if len(user_ids) == 0:
        Settings.maybe_Settings.warn_print("unable to find user ids")
        useridsFailed = True
    if len(starteds) == 0:
        Settings.maybe_Settings.warn_print("unable to find starting dates")
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
            Settings.maybe_Settings.warn_print("unable to find user ids")
            useridsFailed = True
        if len(starteds_) == 0:
            Settings.maybe_Settings.warn_print("unable to find starting dates")
            startedsFailed = True
        # Settings.maybe_print("ids vs starteds vs avatars: "+str(len(user_ids_))+" - "+str(len(starteds_))+" - "+str(len(avatars)))
        Settings.maybe_print("users vs ids vs starteds vs usernames:"+str(len(users))+" - "+str(len(user_ids_))+" - "+str(len(starteds_))+" - "+str(len(usernames)))
        # for user in usernames:
            # Settings.print(user.get_attribute("innerHTML"))
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
                # Settings.print("name: "+name)
                # if "<!" in str(name):
                name = re.sub("<!-*>", "", name)
                # Settings.print(name)
                # if "<" in str(name) and ">" in str(name):
                name = re.sub("<.*\">", "", name).strip()
                # Settings.print(name)
                name = re.sub("</.*>", "", name).strip()
                # Settings.print(name)
                # name = re.sub(name, "<.*>", "").strip()
                # Settings.print(name)
                # name = re.sub(name, "<!-*>", "")
                username = str(username.get_attribute("innerHTML"))
                # Settings.print("username: "+username)
                # if "<!" in str(username):
                username = re.sub("<!-*>", "", username)
                # Settings.print(username)
                # if "<" in str(username) and ">" in str(username):
                username = re.sub("<.*\">", "", username).strip()
                # Settings.print(username)
                username = re.sub("</.*>", "", username).strip()
                username = username.replace("@","")
                # Settings.print(username)
                # username = re.sub("<.*>", "", username).strip()
                # Settings.print(username)
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








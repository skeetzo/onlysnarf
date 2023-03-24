import re
import random
import os
import shutil
import json
import pathlib
import time
import wget
import pickle
from datetime import datetime, timedelta
from pathlib import Path
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
##
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as BraveService
# chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# chromium
from webdriver_manager.core.utils import ChromeType
# brave
# use ChromeService
# firefox
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
# ie
from selenium.webdriver.ie.service import Service as IEService
from webdriver_manager.microsoft import IEDriverManager
# edge
# from selenium.webdriver.edge.service import Service as EdgeService
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# from msedge.selenium_tools import Edge, EdgeOptions
# opera
from webdriver_manager.opera import OperaDriverManager
##
from ..classes.element import Element
from ..util.settings import Settings

###################
##### Globals #####
###################

# Urls
ONLYFANS_HOME_URL = "https://onlyfans.com"
ONLYFANS_HOME_URL2 = "https://onlyfans.com/"
ONLYFANS_NEW_MESSAGE_URL = "/my/chats/send"
ONLYFANS_CHAT_URL = "/my/chats/chat/"
ONLYFANS_SETTINGS_URL = "/my/settings/"
ONLYFANS_USERS_ACTIVE_URL = "/my/subscribers/active"
ONLYFANS_USERS_FOLLOWING_URL = "/my/subscriptions/active"
ONLYFANS_LISTS_URL = "/my/lists/"

class Driver:
    """Driver class for Selenium management"""

    BROWSER = None
    BROWSERS = []
    DRIVERS = []

    #
    DOWNLOADING = True
    DOWNLOADING_MAX = False
    DOWNLOAD_MAX_IMAGES = 1000
    DOWNLOAD_MAX_VIDEOS = 1000
    #
    MAX_TABS = 20
    NOT_INFORMED_KEPT = False # whether or not "Keep"ing the Driver.browser session has been printed once upon exit
    NOT_INFORMED_CLOSED = False # same dumb shit as above

    initialScrollDelay = 0.5
    scrollDelay = 0.5

    def __init__(self):

        # selenium web driver
        self.browser = None
        self.browsers = []

        # browser tabs cache
        self.tabs = []
        # OnlyFans discovered lists cache
        self.lists = []
        # save login state
        self.logged_in = False
        # web browser session id and url for reconnecting
        self.session_id = None
        self.session_url = None

        self._initialized_ = False

    def init(self):
        """
        Initiliaze the web driver aspect.


        """

        if self._initialized_: return
        self.browser = self.spawn_browser(Settings.get_browser_type())
        self.browsers.append(self.browser)
        # ## Cookies
        # if str(Settings.is_cookies()) == "True": self.cookies_load()
        if self.browser:
            self.tabs.append([self.browser.current_url, self.browser.current_window_handle, 0])
        self._initialized_ = True
        Driver.DRIVERS.append(self)

    def auth(self):
        """
        Authorization check

        Logs in with provided runtime creds if not logged in

        Returns
        -------
        bool
            Whether or not the login attempt was successful

        """

        self.init()
        if not self.login():
            if str(Settings.is_debug()) == "True":
                return False
            os._exit(1)
        return True

    ###################
    ##### Cookies #####
    ###################

    def cookies_load(self):
        """Loads existing web browser cookies from local source"""

        Settings.maybe_print("loading cookies...")
        try:
            if os.path.exists(Settings.get_cookies_path()):
                # must be at onlyfans.com to load cookies of onlyfans.com
                self.go_to_home()
                file = open(Settings.get_cookies_path(), "rb")
                cookies = pickle.load(file)
                file.close()
                Settings.dev_print("cookies: ")
                for cookie in cookies:
                    self.browser.add_cookie(cookie)
                Settings.maybe_print("successfully loaded cookies")
                self.refresh()
            else: 
                Settings.maybe_print("failed to load cookies, do not exist")
        except Exception as e:
            Settings.print("error loading cookies!")
            Settings.dev_print(e)

    def cookies_save(self):
        """Saves existing web browser cookies to local source"""

        Settings.maybe_print("saving cookies...")
        try:
            # must be at onlyfans.com to save cookies of onlyfans.com
            self.go_to_home()
            file = open(Settings.get_cookies_path(), "wb")
            pickle.dump(self.browser.get_cookies(), file) # "cookies.pkl"
            file.close()
            Settings.maybe_print("successfully saved cookies")
        except Exception as e:
            Settings.print("failed to save cookies!")
            Settings.dev_print(e)

    ####################
    ##### Discount #####
    ####################

    @staticmethod
    def discount_user(discount, reattempt=False):
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

        # BUG
        # doesn't want to work with local variables
        Driver.originalAmount = None
        Driver.originalMonths = None
        try:
            driver = Driver.get_driver()
            driver.auth()
            months = int(discount["months"])
            amount = int(discount["amount"])
            username = str(discount["username"])
            Settings.print("discounting: {} {} for {} month(s)".format(username, amount, months))
            driver.go_to_page(ONLYFANS_USERS_ACTIVE_URL)
            end_ = True
            count = 0
            user_ = None
            Settings.maybe_print("searching for fan...")
            # scroll through users on page until user is found
            attempts = 0
            while end_:
                elements = driver.browser.find_elements(By.CLASS_NAME, "m-fans")
                for ele in elements:
                    username_ = ele.find_element(By.CLASS_NAME, "g-user-username").get_attribute("innerHTML").strip()
                    # if str(username) == str(username_).replace("@",""):
                    if username in username_:
                        driver.browser.execute_script("arguments[0].scrollIntoView();", ele)
                        user_ = ele
                        end_ = False
                if not end_: continue

                if len(elements) == int(count):
                    Driver.scrollDelay += Driver.initialScrollDelay
                    attempts+=1
                    if attempts == 5:
                        break

                Settings.print_same_line("({}/{}) scrolling...".format(count, len(elements)))
                count = len(elements)
                driver.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(Driver.scrollDelay)

            Settings.print("")
            Settings.dev_print("successfully found fans")
            if not user_:
                Settings.err_print("unable to find fan - {}".format(username))
                if not reattempt:
                    Settings.maybe_print("reattempting fan search...")
                    return Driver.discount_user(discount, reattempt=True)
                return False

            Settings.maybe_print("found: {}".format(username))
            ActionChains(driver.browser).move_to_element(user_).perform()
            Settings.dev_print("successfully moved to fan")
            Settings.dev_print("finding discount btn")
            buttons = user_.find_elements(By.CLASS_NAME, Element.get_element_by_name("discountUser").getClass())
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
                discountEle = driver.browser.find_elements(By.CLASS_NAME, Element.get_element_by_name("discountUserAmount").getClass())[0]
                discountAmount = int(discountEle.get_attribute("innerHTML").replace("% discount", ""))
                if not Driver.originalAmount: Driver.originalAmount = discountAmount
                Settings.dev_print("amount: {}".format(discountAmount))
                Settings.dev_print("entering discount amount")
                if int(discountAmount) != int(amount):
                    up_ = int((discountAmount / 5) - 1)
                    down_ = int((int(amount) / 5) - 1)
                    Settings.dev_print("up: {}".format(up_))
                    Settings.dev_print("down: {}".format(down_))
                    action = ActionChains(driver.browser)
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
                monthsEle = driver.browser.find_elements(By.CLASS_NAME, Element.get_element_by_name("discountUserMonths").getClass())[1]
                monthsAmount = int(monthsEle.get_attribute("innerHTML").replace(" months", "").replace(" month", ""))
                if not Driver.originalMonths: Driver.originalMonths = monthsAmount
                Settings.dev_print("months: {}".format(monthsAmount))
                Settings.dev_print("entering discount months")
                if int(monthsAmount) != int(months):
                    up_ = int(monthsAmount - 1)
                    down_ = int(int(months) - 1)
                    Settings.dev_print("up: {}".format(up_))
                    Settings.dev_print("down: {}".format(down_))
                    action = ActionChains(driver.browser)
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
                discountEle = driver.browser.find_elements(By.CLASS_NAME, Element.get_element_by_name("discountUserAmount").getClass())[0]
                discountAmount = int(discountEle.get_attribute("innerHTML").replace("% discount", ""))
                monthsEle = driver.browser.find_elements(By.CLASS_NAME, Element.get_element_by_name("discountUserMonths").getClass())[1]
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
            buttons_ = driver.find_elements_by_name("discountUserButton")
            for button in buttons_:
                if not button.is_enabled() and not button.is_displayed(): continue
                if "Cancel" in button.get_attribute("innerHTML") and str(Settings.is_debug()) == "True":
                    Settings.print("skipping save discount (debug)")
                    button.click()
                    Settings.dev_print("successfully canceled discount")
                    Settings.dev_print("### Discount Successful ###")
                    return True
                elif "Cancel" in button.get_attribute("innerHTML") and int(discountAmount) == int(Driver.originalAmount) and int(monthsAmount) == int(Driver.originalMonths):
                    Settings.print("skipping existing discount")
                    button.click()
                    Settings.dev_print("successfully skipped existing discount")
                    Settings.dev_print("### Discount Successful ###")
                    # return True
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
            buttons_ = driver.find_elements_by_name("discountUserButton")
            for button in buttons_:
                if "Cancel" in button.get_attribute("innerHTML"):
                    button.click()
                    Settings.dev_print("### Discount Successful Failure ###")
                    return False
            Settings.dev_print("### Discount Failure ###")
            return False

    def download_content(self):
        """Downloads all content (images and video) from the user's profile page"""

        Settings.print("downloading content...")
        def scroll_to_bottom():
            try:
                # go to profile page and scroll to bottom
                self.go_to_profile()
                # count number of content elements to scroll to bottom
                num = self.browser.find_element(By.CLASS_NAME, "b-profile__sections__count").get_attribute("innerHTML")
                Settings.maybe_print("content count: {}".format(num))
                for n in range(int(int(int(num)/5)+1)):
                    Settings.print_same_line("({}/{}) scrolling...".format(n,int(int(int(num)/5)+1)))
                    self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(1)
                Settings.print("")
            except Exception as e:
                Settings.print(e)
                Settings.err_print("failed to find content to scroll")
        scroll_to_bottom()
        imagesDownloaded = self.download_images()
        videosDownloaded = self.download_videos()
        Settings.print("downloaded content")
        Settings.print("count: {}".format(len(imagesDownloaded)+len(videosDownloaded)))

    def download_images(self):
        """Downloads all images on the page"""

        imagesDownloaded = []
        try:
            images = self.browser.find_elements(By.TAG_NAME, "img")
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

    def download_messages(self, user="all"):
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
            self.message_user(user.username)
            contentCount = 0
            while True:
                self.browser.execute_script("document.querySelector('div[id=chatslist]').scrollTop=1e100")
                time.sleep(1)
                self.browser.execute_script("document.querySelector('div[id=chatslist]').scrollTop=1e100")
                time.sleep(1)
                self.browser.execute_script("document.querySelector('div[id=chatslist]').scrollTop=1e100")
                time.sleep(1)
                images = self.browser.find_elements(By.TAG_NAME, "img")
                videos = self.browser.find_elements(By.TAG_NAME, "video")
                # Settings.print((len(images)+len(videos)))
                if contentCount == len(images)+len(videos): break
                contentCount = len(images)+len(videos)
            # download all images and videos
            imagesDownloaded = self.download_images()
            videosDownloaded = self.download_videos()
            Settings.print("downloaded messages")
            Settings.print("count: {}".format(len(imagesDownloaded)+len(videosDownloaded)))
        except Exception as e:
            Settings.maybe_print(e)

    def download_videos(self):
        """Downloads all videos on the page"""

        videosDownloaded = []
        try:
            # find all video elements on page
            videos = self.browser.find_elements(By.TAG_NAME, "video")
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

    @staticmethod
    def drag_and_drop_file(drop_target, path):
        """
        Drag and drop the provided file path onto the provided element target.


        Parameters
        ----------
        drop_target : WebElement
            The web element to drop the file at path on

        path : str
            The file path to drag onto the web element

        Returns
        -------
        bool
            Whether or not dragging the file was successful

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
            return True
        except Exception as e:
            Settings.err_print(e) 
        return False

    def enter_text(self, text):
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
            Settings.dev_print("entering text: "+text)
            # extra redundancy in action chain for getting the text entry area
            # for clearing text field with action chain:
            # https://stackoverflow.com/questions/45690688/clear-selenium-action-chains
            textEntry = self.browser.find_element(By.ID, "new_post_text_input")
            action = ActionChains(self.browser)
            action.move_to_element(textEntry)
            action.click(on_element = textEntry)
            action.double_click()
            action.click_and_hold()
            action.send_keys(Keys.CLEAR)
            action.send_keys(str(text))
            action.perform()
            ## TODO
            ## check text was entered properly
            ## does not work
            # print(self.browser.find_element(By.ID, "new_post_text_input").get_attribute('innerHTML'))
            # Settings.debug_delay_check()
            # print(self.browser.find_element(By.ID, "new_post_text_input").get_attribute('innerHTML'))
            # if self.browser.find_element(By.ID, "new_post_text_input").get_attribute('innerHTML') != text:
                # Settings.dev_print("failed to enter text")
                # return False  
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

    def error_window_upload(self):
        """Closes error window that appears during uploads for 'duplicate' files"""

        try:
            element = Element.get_element_by_name("errorUpload")
            error_buttons = self.browser.find_elements(By.CLASS_NAME, element.getClass())
            Settings.dev_print("errors btns: {}".format(len(error_buttons)))
            if len(error_buttons) == 0: return True
            for butt in error_buttons:
                if butt.get_attribute("innerHTML").strip() == "Close" and butt.is_enabled():
                    Settings.maybe_print("upload error message, closing")
                    butt.click()
                    Settings.maybe_print("success: upload error message closed")
                    time.sleep(0.5)
                    return True
            return False
        except Exception as e:
            Driver.error_checker(e)
        return False

    ######################
    ##### Expiration #####
    ######################

    def expires(self, expiration):
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
            self.open_more_options()
            # open expires window
            Settings.dev_print("adding expiration")
            self.find_element_to_click("expiresAdd").click()
            # select duration
            Settings.dev_print("entering expiration")

            # leave in case needed again
            # nums = self.find_elements_by_name("expiresPeriods")
            # for num in nums:
            #     inner = num.get_attribute("innerHTML")
            #     if int(expiration) == 1  and ">1<" in str(inner): num.click()
            #     if int(expiration) == 3  and ">3<" in str(inner): num.click()
            #     if int(expiration) == 7  and ">7<" in str(inner): num.click()
            #     if int(expiration) == 30 and ">30<" in str(inner): num.click()
            #     if int(expiration) == 99 and ">o limit<" in str(inner): num.click()

            # expiration can now have any int, so update for entering any int less than 30
            self.find_element_by_name("periodValue").send_keys(expiration)

            Settings.dev_print("successfully selected expiration")
            Settings.debug_delay_check()
            # save
            if str(Settings.is_debug()) == "True":
                Settings.maybe_print("skipping expiration (debug)")
                Settings.dev_print("skipping expiration")
                self.find_element_to_click("expiresCancel").click()
                Settings.dev_print("successfully canceled expires")
                Settings.dev_print("### Expiration Successfully Canceled ###")
            else:
                Settings.dev_print("saving expiration")
                self.find_element_to_click("expiresSave").click()
                Settings.dev_print("successfully saved expires")
                Settings.dev_print("### Expiration Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to enter expiration")
            try:
                Settings.dev_print("canceling expiration")
                self.find_element_to_click("expiresCancel").click()
                Settings.dev_print("successfully canceled expiration")
                Settings.dev_print("### Expiration Successful Failure ###")
            except: 
                Settings.dev_print("### Expiration Failure Failure")
        return False

    ######################################################################

    def find_element_by_name(self, name):
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
            return None
        # prioritize id over class name
        eleID = None
        try: eleID = self.browser.find_element(By.ID, element.getId())
        except: eleID = None
        if eleID: return eleID
        for className in element.getClasses():
            ele = None
            eleCSS = None
            try: ele = self.browser.find_element(By.CLASS_NAME, className)
            except: ele = None
            # try: eleCSS = self.browser.find_element(By.CSS_SELECTOR, className)
            # except: eleCSS = None
            Settings.dev_print("class: {} - {}:css".format(ele, eleCSS))
            if ele: return ele
            # if eleCSS: return eleCSS
        raise Exception("unable to locate element")

    def find_elements_by_name(self, name):
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
            return []
        eles = []
        for className in element.getClasses():
            eles_ = []
            elesCSS_ = []
            try: eles_ = self.browser.find_elements(By.CLASS_NAME, className)
            except: eles_ = []
            # try: elesCSS_ = self.browser.find_elements(By.CSS_SELECTOR, className)
            # except: elesCSS_ = []
            Settings.dev_print("class: {} - {}:css".format(len(eles_), len(elesCSS_)))
            eles.extend(eles_)
            # eles.extend(elesCSS_)
        eles_ = []
        for i in range(len(eles)):
            # Settings.dev_print("ele: {} -> {}".format(eles[i].get_attribute("innerHTML").strip(), element.getText()))
            if eles[i].is_displayed():
                Settings.dev_print("found displayed ele: {}".format(eles[i].get_attribute("innerHTML").strip()))
                eles_.append(eles[i])
        if len(eles_) == 0:
            raise Exception("unable to locate elements: {}".format(name))
        return eles_

    def find_element_to_click(self, name, useId=False, offset=0):
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
            Settings.err_print("unable to find element reference - {}".format(name))
            return False
        elements = element.getClasses()
        if useId: elements = element.getIds()
        for className in elements:
            eles = []
            elesCSS = []
            try: eles = self.browser.find_elements(By.CLASS_NAME, className)
            except: eles = []
            # try: elesCSS = self.browser.find_elements(By.CSS_SELECTOR, className)
            # except: elesCSS = []
            Settings.dev_print("class: {} - {}:css".format(len(eles), len(elesCSS)))
            eles.extend(elesCSS)
            for i in range(len(eles)):
                i += offset
                if i > len(eles): i = len(eles)
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
            if len(eles) > 0: return eles[offset]
            Settings.dev_print("unable to find element - {}".format(name))
        raise Exception("unable to locate element - {}".format(name))

    ######################################################################

    @staticmethod
    def get_driver():
        """
        Return an existing driver, if not create one

        Returns
        -------
        classes.driver
            The default driver object.


        """

        if len(Driver.DRIVERS) > 0:
            return Driver.DRIVERS[0]
        return Driver()

    # waits for page load
    def get_page_load(self):
        """Attempt to generic page load"""

        time.sleep(2)
        try: WebDriverWait(self.browser, 60*3, poll_frequency=10).until(EC.visibility_of_element_located((By.CLASS_NAME, "main-wrapper")))
        except Exception as e: Settings.dev_print(e)

    def handle_alert(self):
        """Switch to alert pop up"""

        try:
            alert_obj = self.browser.switch_to.alert or None
            if alert_obj:
                alert_obj.accept()
        except: pass

    ##############
    ### Go Tos ###
    ##############

    def go_to_home(self, force=False):
        """
        Go to home page

        If already at home don't go unless forced

        Parameters
        ----------
        force : bool
            Force page goto even if already at url

        """

        def goto():
            Settings.maybe_print("goto -> onlyfans.com")
            try:
                self.browser.get(ONLYFANS_HOME_URL)
                # element_present = EC.presence_of_element_located((By.CLASS_NAME, Element.get_element_by_name("loginCheck").getClass()))
                # WebDriverWait(self.browser, 10).until(element_present)
            except TimeoutException:
                Settings.dev_print("timed out waiting for page to check login element")
            except WebDriverException as e:
                Settings.dev_print("error fetching home page")
                Settings.err_print(e)
            # self.open_tab(ONLYFANS_HOME_URL)
            self.handle_alert()
            self.get_page_load()
        if force: return goto()
        if self.search_for_tab(ONLYFANS_HOME_URL):
            Settings.maybe_print("found -> /")
            return
        Settings.dev_print("current url: {}".format(self.browser.current_url))
        if str(self.browser.current_url) == str(ONLYFANS_HOME_URL):
            Settings.maybe_print("at -> onlyfans.com")
            self.browser.execute_script("window.scrollTo(0, 0);")
        else: goto()        
        
    def go_to_page(self, page):
        """
        Go to page

        If already at page don't go

        Parameters
        ----------
        page : str
            The url of the OnlyFans 'page' to go to

        """

        self.auth()
        if self.search_for_tab(page):
            Settings.maybe_print("found -> {}".format(page))
            return
        if str(self.browser.current_url) == str(page) or str(page) in str(self.browser.current_url):
            Settings.maybe_print("at -> {}".format(page))
            self.browser.execute_script("window.scrollTo(0, 0);")
        else:
            Settings.maybe_print("goto -> {}".format(page))
            self.open_tab(page)
            self.handle_alert()
            self.get_page_load()

    def go_to_profile(self):
        """Go to OnlyFans profile page"""

        self.auth()
        username = Settings.get_username()
        if str(username) == "":
            username = self.get_username()
        page = "{}/{}".format(ONLYFANS_HOME_URL, username)
        if self.search_for_tab(page):
            Settings.maybe_print("found -> /{}".format(username))
            return
        if str(username) in str(self.browser.current_url):
            Settings.maybe_print("at -> {}".format(username))
            self.browser.execute_script("window.scrollTo(0, 0);")
        else:
            Settings.maybe_print("goto -> {}".format(username))
            # self.browser.get("{}{}".format(ONLYFANS_HOME_URL, username))
            self.open_tab(page)
            # self.handle_alert()
            # self.get_page_load()

    # onlyfans.com/my/settings
    def go_to_settings(self, settingsTab):
        """
        Go to settings tab on settings page

        If already at tab, stay

        Parameters
        ----------
        settingsTab : str
            The name of the Settings tab to go to

        """

        self.auth()
        if self.search_for_tab("{}{}".format(ONLYFANS_SETTINGS_URL, settingsTab)):  
            Settings.maybe_print("found -> settings/{}".format(settingsTab))
            return
        if str(ONLYFANS_SETTINGS_URL) in str(self.browser.current_url) and str(settingsTab) == "profile":
            Settings.maybe_print("at -> onlyfans.com/settings/{}".format(settingsTab))
            self.browser.execute_script("window.scrollTo(0, 0);")
        else:
            if str(settingsTab) == "profile": settingsTab = ""
            Settings.maybe_print("goto -> onlyfans.com/settings/{}".format(settingsTab))
            self.go_to_page("{}{}".format(ONLYFANS_SETTINGS_URL, settingsTab))

    def search_for_tab(self, page):
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

        original_handle = self.browser.current_window_handle
        Settings.dev_print("tabs: {}".format(self.tabs))
        Settings.dev_print("handles: {}".format(self.browser.window_handles))
        try:
            Settings.dev_print("checking tabs...")
            for page_, handle, value in self.tabs:
                Settings.dev_print("{} = {}".format(page_, page))
                if str(page_) in str(page):
                    self.browser.switch_to.window(handle)
                    value += 1
                    Settings.dev_print("successfully located tab in cache: {}".format(page))
                    return True
            Settings.dev_print("checking handles...")
            for handle in self.browser.window_handles:
                Settings.dev_print(handle)
                self.browser.switch_to.window(handle)
                if str(page) in str(self.browser.current_url):
                    Settings.dev_print("successfully located tab in handles: {}".format(page))
                    return True
            Settings.dev_print("failed to locate tab: {}".format(page))
            self.browser.switch_to.window(original_handle)
        except Exception as e:
            # print(e)
            # if "Unable to locate window" not in str(e):
            Settings.dev_print(e)
        return False

    def open_tab(self, url):
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
        # self.browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')
        # self.browser.get(url)
        # https://stackoverflow.com/questions/50844779/how-to-handle-multiple-windows-in-python-selenium-with-firefox-driver
        windows_before  = self.browser.current_window_handle
        Settings.dev_print("current window handle is : %s" %windows_before)
        windows = self.browser.window_handles
        self.browser.execute_script('''window.open("{}","_blank");'''.format(url))
        # self.browser.execute_script("window.open('{}')".format(url))
        self.handle_alert()
        self.get_page_load()
        # self.browser.execute_script("window.open('https://www.yahoo.com')")
        WebDriverWait(self.browser, 10).until(EC.number_of_windows_to_be(len(windows)+1))
        windows_after = self.browser.window_handles
        new_window = [x for x in windows_after if x not in windows][0]
        # self.browser.switch_to.window(new_window) <!---deprecated>
        self.browser.switch_to.window(new_window)
        Settings.dev_print("page title after tab switching is : %s" %self.browser.title)
        Settings.dev_print("new window handle is : %s" %new_window)
        # if len(self.tabs) >= Driver.MAX_TABS:
        #     least = self.tabs[0]
        #     for i, tab in enumerate(self.tabs):
        #         if int(tab[2]) < int(least[2]):
        #             least = tab
        #     self.tabs.remove(least)
        # self.tabs.append([url, new_window, 0]) # url, window_handle, use count
    
    ##################
    ###### Login #####
    ##################

    def login(self):
        """
        Logs into OnlyFans account provided via args and chosen method.

        Checks if already logged in first. Logs in via requested method or tries all available.

        Returns
        -------
        bool
            Whether or not the login was successful

        """

        if self.logged_in: return True
        Settings.print('logging into OnlyFans for {}...'.format(Settings.get_username()))

        def loggedin_check():
            """Check if already logged in before attempting to login again"""

            self.go_to_home(force=True)
            try:
                # ele = self.browser.find_element(By.CLASS_NAME, Element.get_element_by_name("loginCheck").getClass())
                WebDriverWait(self.browser, 10, poll_frequency=1).until(EC.visibility_of_element_located((By.CLASS_NAME, Element.get_element_by_name("loginCheck").getClass())))
                # if ele: 
                Settings.print("already logged into OnlyFans!")
                return True
            except TimeoutException as te:
                Settings.dev_print(str(te))
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
                Settings.dev_print("waiting for login check...")
                WebDriverWait(self.browser, 16, poll_frequency=2).until(EC.visibility_of_element_located((By.CLASS_NAME, Element.get_element_by_name("loginCheck").getClass())))
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
                if str(username) == "" or str(password) == "":
                    Settings.err_print("missing onlyfans login info")
                    return False
                self.go_to_home()
                WAIT = WebDriverWait(self.browser, 10, poll_frequency=2)
                Settings.dev_print("finding username & password")
                usernameField = WAIT.until(EC.presence_of_element_located((By.NAME, "email")))
                passwordField = WAIT.until(EC.presence_of_element_located((By.NAME, "password")))
                usernameField.click()
                usernameField.send_keys(username)
                Settings.dev_print("username entered")
                passwordField.click()
                passwordField.send_keys(password)
                Settings.dev_print("password entered")
                passwordField.send_keys(Keys.ENTER)
                def check_captcha():
                    try:
                        time.sleep(10) # wait extra long to make sure it doesn't verify obnoxiously
                        el = self.browser.find_element("name", "password")
                        if not el: return # likely logged in without captcha
                        Settings.print("waiting for captcha completion by user...")
                        # action = webdriver.common.action_chains.ActionChains(self.browser)
                        action = ActionChains(self.browser)
                        action.move_to_element_with_offset(el, 40, 100)
                        action.click()
                        action.perform()
                        time.sleep(10)
                        sub = None
                        submit = self.browser.find_element(By.CLASS_NAME, "g-btn.m-rounded.m-flex.m-lg")
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
                if str(username) == "" or str(password) == "":
                    Settings.err_print("missing google login info")
                    return False
                # self.go_to_home()
                elements = self.browser.find_elements(By.TAG_NAME, "a")
                [elem for elem in elements if '/auth/google' in str(elem.get_attribute('href'))][0].click()
                time.sleep(5)
                username_ = self.browser.switch_to.active_element
                # then click username spot
                username_.send_keys(username)
                username_.send_keys(Keys.ENTER)
                Settings.dev_print("username entered")
                time.sleep(2)
                password_ = self.browser.switch_to.active_element
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
                if str(username) == "" or str(password) == "":
                    Settings.err_print("missing twitter login info")
                    return False
                # self.go_to_home()
                # rememberMe checkbox doesn't actually cause login to be remembered
                # rememberMe = self.browser.find_element_by_xpath(Element.get_element_by_name("rememberMe").getXPath())
                # if not rememberMe.is_selected():
                    # rememberMe.click()
                # if str(Settings.MANUAL) == "True":
                    # Settings.print("Please Login")
                elements = self.browser.find_elements(By.TAG_NAME, "a")
                [elem for elem in elements if '/twitter/auth' in str(elem.get_attribute('href'))][0].click()
                self.browser.find_element("name", "session[username_or_email]").send_keys(username)
                Settings.dev_print("username entered")
                # fill in password and hit the login button 
                password_ = self.browser.find_element("name", "session[password]")
                password_.send_keys(password)
                Settings.dev_print("password entered")
                password_.send_keys(Keys.ENTER)
                return login_check("twitter")
            except Exception as e:
                Settings.dev_print("twitter login failure")
                Driver.error_checker(e)
            return False


        # this needs to go after them because they reconnect then need to login check
        # if Settings.get_browser_type() == "reconnect" or Settings.get_browser_type() == "remote" or 

        try:
            if loggedin_check():
                self.logged_in = True
                return True
        except Exception as e:
            Settings.err_print(e)
            return False

        if str(Settings.is_cookies()) == "True":
            self.cookies_load()
            if loggedin_check():
                self.logged_in = True
                return True
            elif str(Settings.is_cookies()) == "True" and str(Settings.is_debug("cookies")) == "True":
                Settings.err_print("failed to login from cookies!")
                Settings.set_cookies(False)
                return False
            elif str(Settings.is_cookies()) == "True":
                Settings.set_cookies(False)
                Settings.maybe_print("failed to login from cookies!")

        Settings.dev_print("attempting login...")
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
            if successful:
                self.logged_in = True
                return True
        except Exception as e:
            Driver.error_checker(e)
        Settings.err_print("OnlyFans login failed!")
        return False

    ####################
    ##### Messages #####
    ####################

    @staticmethod
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
            driver = Driver.get_driver()
            driver.auth()
            Settings.dev_print("attempting to start message for {}...".format(username))
            type__ = None # default
            # if the username is a key string it will behave differently
            if str(username).lower() == "all": type__ = "messageAll"
            elif str(username).lower() == "recent": type__ = "messageRecent"
            elif str(username).lower() == "favorite": type__ = "messageFavorite"
            elif str(username).lower() == "renew on": type__ = "messageRenewers"
            successful = False
            if type__ != None:
                driver.go_to_page(ONLYFANS_NEW_MESSAGE_URL)
                Settings.dev_print("clicking message type: {}".format(username))
                driver.find_element_to_click(type__).click()
                successful = True
            else:
                successful = driver.message_user(username, user_id=user_id)
            if successful: Settings.dev_print("started message for {}".format(username))
            else: Settings.warn_print("failed to start message for {}!".format(username))
            return successful
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failure to message - {}".format(username))
        return False
     
    def message_clear(self):
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
            Settings.dev_print("clearing message")
            clearButton = [ele for ele in self.browser.find_elements(By.TAG_NAME, "button") if "Clear" in ele.get_attribute("innerHTML")]
            if len(clearButton) > 0:
                Settings.dev_print("clicking clear button...")
                clearButton[0].click()
            else:
                Settings.dev_print("refreshing page and clearing text...")
                self.go_to_home(force=True)
                ActionChains(self.browser).move_to_element(self.browser.find_element(By.ID, "new_post_text_input")).double_click().click_and_hold().send_keys(Keys.CLEAR).perform()
            Settings.dev_print("successfully cleared message")
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failure to clear message")
        return False

    def message_confirm(self):
        """
        Wait for the message open on the page's Confirm button to be clickable and click it

        Returns
        -------
        bool
            Whether or not the message confirmation was successful

        """

        try:
            Settings.dev_print("waiting for message confirm to be clickable...")
            confirm = WebDriverWait(self.browser, int(Settings.get_upload_max_duration()), poll_frequency=3).until(EC.element_to_be_clickable((By.CLASS_NAME, Element.get_element_by_name("new_message").getClass())))
            Settings.dev_print("message confirm is clickable")
            if str(Settings.is_debug()) == "True":
                Settings.debug_delay_check()
                self.go_to_home()
                Settings.print('skipped message (debug)')
                return True
            Settings.dev_print("clicking confirm")
            confirm.click()
            Settings.print('OnlyFans message sent!')
            return True
        except TimeoutException:
            Settings.warn_print("timed out waiting for message confirm!")
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failure to confirm message!")
        self.message_clear()
        return False

    def message_price(self, price):
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
            try:
                Settings.dev_print("clearing any preexisting price...")
                self.browser.find_element(By.CLASS_NAME, "m-btn-remove").click()
            except Exception as e:
                Settings.dev_print(e)
            Settings.dev_print("entering price...")
            self.browser.find_element(By.CLASS_NAME, "b-make-post__actions__btns").find_elements(By.XPATH, "./child::*")[7].click()
            priceText = WebDriverWait(self.browser, 10, poll_frequency=2).until(EC.element_to_be_clickable(self.browser.find_element(By.ID, "priceInput_1")))
            priceText.click()
            priceText.send_keys(str(price))
            Settings.dev_print("entered price")
            Settings.debug_delay_check()
            Settings.dev_print("saving price...")
            self.find_element_to_click("priceSave").click()    
            Settings.dev_print("saved price")
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failure to enter price")
        return False

    def message_text(self, text):
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
            if not text or text == None or str(text) == "None" or str(text) == "":
                Settings.err_print("missing text for message!")
                return False
            Settings.dev_print("entering text")
            ActionChains(self.browser).move_to_element(self.browser.find_element(By.ID, "new_post_text_input")).double_click().click_and_hold().send_keys(Keys.CLEAR).send_keys(str(text)).perform()
            Settings.dev_print("successfully entered text")
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failure to enter message")
        return False

    def message_user_by_id(self, user_id=None):
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
            Settings.err_print("missing user id!")
            return False
        try:
            self.go_to_page("{}{}".format(ONLYFANS_CHAT_URL, user_id))
            Settings.dev_print("successfully messaging user id: {}".format(user_id))
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to message user by id!")
        return False

    def message_user(self, username, user_id=None):
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
        if user_id and str(user_id) != "None": return self.message_user_by_id(user_id=user_id)
        if not username:
            Settings.err_print("missing username to message!")
            return False
        try:
            self.go_to_page(username)
            time.sleep(5) # for whatever reason this constantly errors out from load times
            elements = self.browser.find_elements(By.TAG_NAME, "a")
            ele = [ele for ele in elements if ONLYFANS_CHAT_URL in str(ele.get_attribute("href"))]
            if len(ele) == 0:
                Settings.warn_print("user cannot be messaged - unable to locate id")
                return False
            ele = ele[0]
            ele = ele.get_attribute("href").replace("https://onlyfans.com", "")
            # clicking no longer works? just open href in self.browser
            # Settings.dev_print("clicking send message")
            # ele.click()
            # Settings.dev_print(ele.get_attribute("href"))
            Settings.maybe_print("user id found: {}".format(ele.replace(ONLYFANS_HOME_URL2, "")))
            self.go_to_page(ele)
            Settings.dev_print("successfully messaging username: {}".format(username))
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to message user")
        return False

    @staticmethod
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
        users = []
        try:
            driver = Driver.get_driver()
            driver.auth()
            driver.go_to_page("/my/chats")
            users_ = driver.browser.find_elements(By.CLASS_NAME, "g-user-username")
            Settings.dev_print("users: {}".format(len(users_)))
            user_ids = driver.browser.find_elements(By.CLASS_NAME, "b-chats__item__link")
            Settings.dev_print("ids: {}".format(len(user_ids)))
            for user in user_ids:
                if not user or not user.get_attribute("href") or str(user.get_attribute("href")) == "None": continue
                users.append(str(user.get_attribute("href")).replace("https://onlyfans.com/my/chats/chat/", ""))
            return users[:10]
        except Exception as e:
            Settings.print(e)
            Driver.error_checker(e)
            Settings.err_print("failed to scan messages")
        return users

    def move_to_then_click_element(self, element):
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
            ActionChains(self.browser).move_to_element(element).click().perform()
        except Exception as e:
            Settings.dev_print(e)
            if 'firefox' in self.browser.capabilities['browserName']:
                scroll_shim(self.browser, element)
            try:
                ActionChains(self.browser).move_to_element(element).click().perform()
            except Exception as e:
                Settings.dev_print(e)
            # self.browser.execute_script("arguments[0].scrollIntoView();", ele)
                self.browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
                ActionChains(self.browser).move_to_element(element).click().perform()


    ####################################################################################################
    ####################################################################################################
    ####################################################################################################

    # tries both and throws error for not found element internally
    def open_more_options(self):
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
            moreOptions = self.find_element_to_click("moreOptions")
            if not moreOptions: return False    
            moreOptions.click()
            Settings.dev_print("successfully opened more options (1)")
            return True
        def option_two():
            """Click in empty space"""

            Settings.dev_print("opening options (2)")
            moreOptions = self.browser.find_element(By.ID, Element.get_element_by_name("enterText").getId())
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

    def poll(self, poll):
        """
        Enter the Poll object into the current post

        Parameters
        ----------
        poll : dict
            The values of the poll in a dict

        Returns
        -------
        bool
            Whether or not entering the poll was successful

        """

        if str(poll) == "None" or not poll: return True
        try:
            Settings.print("Poll:")
            Settings.print("- Duration: {}".format(poll["duration"]))
            Settings.print("- Questions:")
            # make sure the extra options are shown
            # self.open_more_options()
            # add a poll
            Settings.dev_print("adding poll")
            self.browser.find_element(By.CLASS_NAME, "b-make-post__actions__btns").find_elements(By.XPATH, "./child::*")[5].click()
            # open the poll duration
            Settings.dev_print("adding duration")
            # self.find_element_to_click("pollDuration").click()
            self.browser.find_element(By.CLASS_NAME, "b-post-piece__value").click()
            # click on the correct duration number
            Settings.dev_print("setting duration")
            time.sleep(0.5)
            ActionChains(self.browser).move_to_element(self.browser.find_element(By.NAME, "periodValue")).double_click().click_and_hold().send_keys(Keys.CLEAR).send_keys(str(poll["duration"])).perform()
            # save the duration
            Settings.dev_print("saving duration")
            self.find_element_to_click("pollSave").click()
            Settings.dev_print("successfully saved duration")
            questions = self.browser.find_elements(By.CLASS_NAME, "v-text-field__slot")
            Settings.dev_print("configuring question paths...")
            # add extra question space
            OFFSET = 2 # number of preexisting questions
            if OFFSET + len(poll["questions"]) > len(questions):
                for i in range(OFFSET + len(poll["questions"])-len(questions)):
                    Settings.dev_print("adding question")
                    question_ = self.find_element_to_click("pollQuestionAdd").click()
                    Settings.dev_print("added question")
            # find the question inputs
            # questions_ = self.browser.find_elements(By.XPATH, Element.get_element_by_name("pollInput").getXPath())
            questions = self.browser.find_elements(By.CLASS_NAME, "v-text-field__slot")
            Settings.dev_print("question paths: {}".format(len(questions)))
            # enter the questions
            i = 0
            Settings.dev_print("questions: {}".format(poll["questions"]))
            for question in list(poll["questions"]):
                Settings.print("> {}".format(question))
                Settings.dev_print("entering question: {}".format(question))
                questions[i].find_elements(By.XPATH, "./child::*")[0].send_keys(str(question))
                Settings.dev_print("entered question")
                time.sleep(1)
                i+=1
            Settings.dev_print("successfully entered questions")
            Settings.debug_delay_check()
            if str(Settings.is_debug()) == "True":
                Settings.maybe_print("skipping poll (debug)")
                cancel = self.find_element_to_click("pollCancel")
                cancel.click()
            Settings.dev_print("### Poll Successful ###")
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to enter poll!")
        return False

    ################
    ##### Post #####
    ################

    @staticmethod
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
        message : dict
            The message values to be entered into the post 

        Returns
        -------
        bool
            Whether or not the post was successful

        """

        Settings.dev_print("posting...")
        driver = Driver.get_driver()
        driver.auth()


        ## TODO
        # add check for clearing any text or images already in post field
        driver.message_clear()

        # try:
        #     driver.find_element_to_click("postCancel").click()
        # except Exception as e:
        #     Settings.dev_print(e)

        #################### Formatted Text ####################
        Settings.print("====================")
        Settings.print("Posting:")
        Settings.print("- Files: {}".format(len(message["files"])))
        Settings.print("- Performers: {}".format(message["performers"]))
        Settings.print("- Tags: {}".format(message["tags"]))
        Settings.print("- Text: {}".format(message["text"]))
        Settings.print("- Tweeting: {}".format(Settings.is_tweeting()))
        ## Expires, Schedule, Poll ##
        if not driver.expires(message["expiration"]): return False
        if message["schedule"].validate() and not driver.schedule(message["schedule"].get()): return False
        if message["poll"].validate() and not driver.poll(message["poll"].get()): return False
        Settings.print("====================")
        ############################################################

        ## Tweeting ##
        ## TODO
        ## test this
        # if str(Settings.is_tweeting()) == "True":
            # Settings.dev_print("tweeting...")
            # twitter tweet button is 1st, post is 2nd
            # ActionChains(driver.browser).move_to_element(driver.browser.find_element(By.CLASS_NAME, "b-btns-group").find_elements(By.XPATH, "./child::*")[0]).click().perform()
            # WebDriverWait(driver.browser, 30, poll_frequency=3).until(EC.element_to_be_clickable((By.XPATH, Element.get_element_by_name("tweet").getXPath()))).click()
        # else: Settings.dev_print("not tweeting")

        ## Upload Files ##
        try:

            if not driver.enter_text(message["text"]):
                Settings.err_print("unable to post!")
                return False
            
            successful, skipped = driver.upload_files(message["files"])
            if successful and not skipped:
                # twitter tweet button is 1st, post is 2nd
                postButton = [ele for ele in driver.browser.find_elements(By.TAG_NAME, "button") if "Post" in ele.get_attribute("innerHTML")][0]
                WebDriverWait(driver.browser, Settings.get_upload_max_duration(), poll_frequency=3).until(EC.element_to_be_clickable(postButton))
                Settings.dev_print("upload complete")

            if str(Settings.is_debug()) == "True":
                driver.message_clear()
                Settings.print('skipped post (debug)')
                Settings.debug_delay_check()
                return True

            Settings.dev_print("uploading post...")
            postButton = [ele for ele in driver.browser.find_elements(By.TAG_NAME, "button") if "Post" in ele.get_attribute("innerHTML")][0]
            ActionChains(driver.browser).move_to_element(postButton).click().perform()
            Settings.print('posted to OnlyFans!')
            return True
        except TimeoutException:
            Settings.dev_print("timed out waiting for post upload!")
        except Exception as e:
            Settings.dev_print(e)
            Settings.err_print("unable to send post")
        driver.go_to_home(force=True)
        return False

    ######################
    ##### Promotions #####
    ######################

    def promotional_campaign(self, promotion=None):
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
            self.go_to_page("my/promotions")
            Settings.dev_print("checking existing promotion")
            copies = self.browser.find_elements(By.CLASS_NAME, "g-btn.m-rounded.m-uppercase")
            for copy in copies:
                if "copy link to profile" in str(copy.get_attribute("innerHTML")).lower():
                # Settings.print("{}".format(copy.get_attribute("innerHTML")))
                    copy.click()
                    Settings.dev_print("successfully clicked early copy")
                    Settings.warn_print("a promotion already exists")
                    Settings.print("Copied existing promotion")
                    return True
            Settings.dev_print("clicking promotion campaign")
            self.find_element_to_click("promotionalCampaign").click()
            Settings.dev_print("successfully clicked promotion campaign")
            # Settings.debug_delay_check()
            time.sleep(10)
            # limit dropdown
            Settings.dev_print("setting campaign count")
            limitDropwdown = self.find_element_by_name("promotionalTrialCount")
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
            expirationDropdown = self.find_element_by_name("promotionalTrialExpiration")
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
            durationDropdown = self.find_element_by_name("promotionalCampaignAmount")
            Settings.dev_print("entering discount amount")
            for n in range(11):
                durationDropdown.send_keys(str(Keys.UP))
            for n in range(round(int(amount)/5)-1):
                durationDropdown.send_keys(Keys.DOWN)
            Settings.dev_print("successfully entered discount amount")
            # todo: add message to users
            message = self.find_element_by_name("promotionalTrialMessage")
            Settings.dev_print("found message text")
            message.clear()
            Settings.dev_print("sending text")
            message.send_keys(str(text))
            # todo: [] apply to expired subscribers checkbox
            Settings.debug_delay_check()
            # find and click promotionalTrialConfirm
            if str(Settings.is_debug()) == "True":
                Settings.dev_print("finding campaign cancel")
                self.find_element_to_click("promotionalTrialCancel").click()
                Settings.maybe_print("skipping promotion (debug)")
                Settings.dev_print("successfully cancelled promotion campaign")
                return True
            Settings.dev_print("finding campaign save")
            # save_ = self.find_element_to_click("promotionalTrialConfirm")
            # save_ = self.find_element_to_click("promotionalCampaignConfirm")
            save_ = self.browser.find_elements(By.CLASS_NAME, "g-btn.m-rounded")
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
            copies = self.browser.find_elements(By.CLASS_NAME, "g-btn.m-rounded.m-uppercase")
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
    def promotional_trial_link(self, promotion=None):
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
            self.go_to_page("/my/promotions")
            Settings.dev_print("showing promotional trial link")
            self.find_element_to_click("promotionalTrialShow").click()
            Settings.dev_print("successfully showed promotional trial link")
            Settings.dev_print("creating promotional trial")
            self.find_element_to_click("promotionalTrial").click()
            Settings.dev_print("successfully clicked promotional trial")
            # limit dropdown
            Settings.dev_print("setting trial count")
            limitDropwdown = self.find_element_by_name("promotionalTrialCount")
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
            expirationDropdown = self.find_element_by_name("promotionalTrialExpiration")
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
            durationDropwdown = self.find_element_by_name("promotionalTrialDuration")
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
            #     self.find_element_to_click("promotionalTrialCancel").click()
            #     Settings.print("skipping: Promotion (debug)")
            #     Settings.dev_print("successfully cancelled promotion trial")
            #     return True
            Settings.dev_print("finding trial save")
            save_ = self.find_element_to_click("promotionalTrialConfirm")
            # "g-btn.m-rounded"

            save_ = self.browser.find_elements(By.CLASS_NAME, "g-btn.m-rounded")
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
            # self.find_element_by_name("promotionalTrialLink").click()
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

    def promotion_user_directly(self, promotion=None):
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
            self.go_to_page(user)
            # click discount button
            self.find_element_to_click("discountUserPromotion").click()
            # enter expiration
            expirations = self.find_element_by_name("promotionalTrialExpirationUser")
            # enter duration
            durations = self.find_element_by_name("promotionalTrialDurationUser")
            # enter message
            message = self.find_element_by_name("promotionalTrialMessageUser")
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
            save = self.find_element_by_name("promotionalTrialApply")
            if str(Settings.is_debug()) == "True":
                self.find_element_by_name("promotionalTrialCancel").click()
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
                self.find_element_by_name("promotionalTrialCancel").click()
                Settings.dev_print("### Discount Successful Failure ###")
                return False
            except Exception as e:
                Driver.error_checker(e)
            Settings.dev_print("### Discount Failure ###")
            return False

    ######################################################################

    @staticmethod
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
            driver = Driver.get_driver()
            # go to onlyfans.com/my/subscribers/active
            driver.message_user(username, user_id=user_id)
            messages_sent_ = []
            try:
                messages_sent_ = driver.find_elements_by_name("messagesFrom")
            except Exception as e:
                if "Unable to locate elements" in str(e):
                    pass
                else: Settings.dev_print(e)
            # Settings.print("first message: {}".format(messages_received_[0].get_attribute("innerHTML")))
            # messages_received_.pop(0) # drop self user at top of page
            messages_all_ = []
            try:
                messages_all_ = driver.find_elements_by_name("messagesAll")
            except Exception as e:
                if "Unable to locate elements" in str(e):
                    pass
                else: Settings.dev_print(e)
            messages_all = []
            messages_received = []
            messages_sent = []
            # timestamps_ = driver.browser.find_elements(By.CLASS_NAME, "b-chat__message__time")
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
                message = message.find_element(By.CLASS_NAME, Element.get_element_by_name("enterMessage").getClass()).get_attribute("innerHTML")
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

    def refresh(self):
        """Refresh the web browser"""

        Settings.dev_print("refreshing browser...")
        self.browser.refresh()

    #################
    ##### Reset #####
    #################

    def reset(self):
        """
        Reset the web browser to home page

        Returns
        -------
        bool
            Whether or not the browser was reset successfully

        """

        if not self.browser:
            Settings.print('OnlyFans not open, skipping reset')
            return True
        try:
            self.go_to_home()
            Settings.print('OnlyFans reset')
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failure resetting onlyfans")
            return False

    ####################
    ##### Schedule #####
    ####################

    def schedule_open(self):
        """Click schedule"""

        Settings.dev_print("opening schedule")
        self.find_element_to_click("scheduleAdd").click()
        Settings.dev_print("successfully opened schedule")

    def schedule_date(self, month, year):
        """Find and click month w/ correct date"""

        Settings.dev_print("setting date")
        while True:

            date = self.browser.find_element(By.CLASS_NAME, "vdatetime-calendar__current--month").get_attribute("innerHTML")

            # date = self.find_element_by_name("scheduleDate").get_attribute("innerHTML")
            Settings.dev_print("date: {} - {} {}".format(date, month, year))
            if str(month) in str(date) and str(year) in str(date):
                Settings.dev_print("set month and year")
                return True
            else:
                self.find_element_to_click("scheduleNextMonth").click()
        return False

    def schedule_day(self, day):
        """Set day in month"""

        Settings.dev_print("setting day")
        for ele in self.find_elements_by_name("scheduleDays"):
            if str(day) in ele.get_attribute("innerHTML").replace("<span><span>","").replace("</span></span>",""):
                ele.click()
                Settings.dev_print("set day")
                return True
        return False

    def schedule_save_date(self):
        """Save schedule date and move to next view in frame by hitting next"""
        
        self.find_element_to_click("scheduleNext").click()
        Settings.dev_print("successfully saved date")

    def schedule_hour(self, hour):
        """Set schedule hour"""

        Settings.dev_print("setting hours")
        eles = self.browser.find_element(By.CLASS_NAME, "vdatetime-time-picker__list--hours").find_elements(By.XPATH, "./child::*")
        for ele in eles:
            if str(hour) in ele.get_attribute("innerHTML").strip():
                # ActionChains(self.browser).move_to_element(ele).click().perform()
                ele.click()
                Settings.dev_print("set hour")
                return True
        return False

    def schedule_minutes(self, minutes):
        """Set schedule minutes"""

        Settings.dev_print("setting minutes")
        eles = self.browser.find_element(By.CLASS_NAME, "vdatetime-time-picker__list--minutes").find_elements(By.XPATH, "./child::*")
        for ele in eles:
            if str(minutes) in ele.get_attribute("innerHTML").strip():
                ele.click()
                Settings.dev_print("set minutes")
                return True
        return False

    def schedule_suffix(self, suffix):
        """Set am/pm suffix"""

        Settings.dev_print("setting suffix")
        eles = self.browser.find_element(By.CLASS_NAME, "vdatetime-time-picker__list--suffix").find_elements(By.XPATH, "./child::*")
        for ele in eles:
            if str(suffix).lower() in ele.get_attribute("innerHTML").strip().lower():
                ele.click()
                Settings.dev_print("set suffix")
                return True
        return False

    def schedule_cancel(self):
        """Cancel schedule by clicking cancel"""

        self.browser.find_element(By.CLASS_NAME, "vdatetime-popup__actions__button--cancel").find_elements(By.XPATH, "./child::*")[0].click()
        Settings.print("canceled schedule")
        return True

    def schedule_save(self):
        """Save schedule by clicking save"""

        # self.find_element_to_click("scheduleSave").click()
        self.browser.find_element(By.CLASS_NAME, "vdatetime-popup__actions__button--confirm").find_elements(By.XPATH, "./child::*")[0].click()
        Settings.print("saved schedule")
        return True

    def schedule(self, schedule):
        """
        Enter the provided schedule

        Parameters
        ----------
        schedule : dict
            The schedule object containing the values to enter

        Returns
        -------
        bool
            Whether or not the schedule was entered successfully

        """

        if str(schedule) == "None" or not schedule: return True
        try:
            Settings.print("Schedule:")
            Settings.print("- Date: {}".format(Settings.format_date(schedule["date"])))
            Settings.print("- Time: {}".format(Settings.format_time(schedule["time"])))
            # ensure schedule button can be accessed
            # self.open_more_options()

            # tries twice to solve various bugs
            try:
                self.schedule_open()
            except Exception as e:
                Settings.dev_print(e)
                self.go_to_home()
                self.schedule_open()

            # return self.schedule_cancel()

            # set month, year, and day
            if not self.schedule_date(schedule["month"], schedule["year"]):
                Settings.debug_delay_check()
                raise Exception("failed to enter date!")
            if not self.schedule_day(schedule["day"]):
                Settings.debug_delay_check()
                raise Exception("failed to enter day!")
            Settings.debug_delay_check()
            self.schedule_save_date()
            # set time
            if not self.schedule_hour(schedule["hour"]):
                Settings.debug_delay_check()
                raise Exception("failed to enter hour!")
            if not self.schedule_minutes(schedule["minute"]):
                Settings.debug_delay_check()
                raise Exception("failed to enter minutes!")
            if not self.schedule_suffix(schedule["suffix"]):
                Settings.debug_delay_check()
                raise Exception("failed to enter suffix!")
            # save time
            Settings.debug_delay_check()
            Settings.dev_print("saving schedule")
            if str(Settings.is_debug()) == "True":
                Settings.print("skipping schedule save (debug)")
                return self.schedule_cancel()
            else:
                return self.schedule_save()
        except Exception as e:
            Driver.error_checker(e)
        # attempt to cancel window
        return self.schedule_cancel()

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
    #             data = self.sync_from_settings_page(page)
    #             for key, value in data:
    #                 profile[key] = value
    #         Settings.dev_print("successfully got settings")
    #         Settings.print("Settings Retrieved")
    #     except Exception as e:
    #         Driver.error_checker(e)
    #     return profile

    def sync_from_settings_page(self, profile=None, page=None):
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
            self.go_to_settings(page)
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
                    element = self.find_element_by_name(name)
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
                    ele = self.find_element_by_name(name)
                    Select(self.browser.find_element(By.ID, ele.getId()))
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
    def sync_to_settings_page(self, profile=None, page=None):
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
            self.go_to_settings(page)
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
                    element = self.find_element_by_name(name)
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
                    ele = self.find_element_by_name(name)
                    Select(self.browser.find_element(By.ID, ele.getId()))
                    # go to top
                    # then go to matching value
                    pass
                elif str(type_) == "list":
                    element.send_keys(getattr(profile, str(name)))
                elif str(type_) == "file":
                    element.send_keys(getattr(profile, str(name)))
                elif str(type_) == "checkbox":
                    element.click()
            if str(Settings.is_debug()) == "True":
                Settings.dev_print("successfully cancelled settings page: {}".format(page))
            else:
                self.settings_save(page=page)
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
    #             self.sync_to_settings_page(Profile, page)
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
    def settings_save(self, page=None):
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
            element = self.find_element_by_name("profileSave")
            Settings.dev_print("derp")
            element = self.find_element_to_click("profileSave")
            Settings.dev_print("found page save")
            if str(Settings.is_debug()) == "True":
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

    def spawn_browser(self, browserType):
        """
        Spawns a browser according to args.

        Browser options can be: auto, chrome, firefox, remote

        Parameters
        ----------
        browserType : str
            The configured browser type to use

        Returns
        -------
        Selenium.WebDriver
            The created browser object

        """

        if str(Settings.is_debug("selenium")) == "False":
            import logging
            from selenium.webdriver.remote.remote_connection import LOGGER as SeleniumLogger
            SeleniumLogger.setLevel(logging.ERROR)
            logging.getLogger("urllib3").setLevel(logging.ERROR)
            logging.getLogger("requests").setLevel(logging.ERROR)
            logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.ERROR)

            if int(Settings.get_verbosity()) >= 2:
                SeleniumLogger.setLevel(logging.WARNING)
                logging.getLogger("urllib3").setLevel(logging.WARNING)
                logging.getLogger("requests").setLevel(logging.WARNING)
                logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)

        browser = None
        Settings.print("spawning web browser...")

        def add_options(options):
            if str(Settings.is_show_window()) == "False":
                options.add_argument('--headless')
            options.add_argument("--no-sandbox") # Bypass OS security model
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("user-data-dir=/tmp/selenium") # do not disable, required for cookies to work 
            # options.add_argument("--allow-insecure-localhost")            
            # possibly linux only
            # options.add_argument('disable-notifications')
            # https://stackoverflow.com/questions/50642308/webdriverexception-unknown-error-devtoolsactiveport-file-doesnt-exist-while-t
            # options.add_arguments("start-maximized"); // open Browser in maximized mode
            # options.add_argument("--window-size=1920,1080")
            # options.add_argument("--disable-crash-reporter")
            # options.add_argument("--disable-infobars")
            # options.add_argument("--disable-in-process-stack-traces")
            # options.add_argument("--disable-logging")
            # options.add_argument("--log-level=3")
            # options.add_argument("--output=/dev/null")
            # TODO: to be added to list of removed (if not truly needed by then)
            # options.add_argument('--disable-software-rasterizer')
            # options.add_argument('--ignore-certificate-errors')
            # options.add_argument("--remote-debugging-address=localhost")    
            # options.add_argument("--remote-debugging-port=9223")

        def browser_error(err, browserName):
            Settings.warn_print("unable to launch {}!".format(browserName))
            Settings.dev_print(err)

        def attempt_chrome(brave=False, chromium=False, edge=False):
            browserName = None
            browserAttempt = None
            try:
                options = webdriver.ChromeOptions()
                add_options(options)
                if brave:
                    browserName = "brave"
                    Settings.maybe_print("attempting {} web browser...".format(browserName))
                    browserAttempt = webdriver.Chrome(service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()), options=options)
                    Settings.print("browser created - {}".format(browserName))
                elif chromium:
                    browserName = "chromium"
                    Settings.maybe_print("attempting {} web browser...".format(browserName))
                    browserAttempt = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=options)
                    Settings.print("browser created - {}".format(browserName))
                elif edge:
                    # doesn't work
                    browserName = "edge"
                    Settings.maybe_print("attempting {} web browser...".format(browserName))
                    # options = EdgeOptions()
                    # options.use_chromium = True
                    # add_options(options)
                    # options.binary_location="/home/{user}/.wdm/drivers/edgedriver/linux64/111.0.1661/msedgedriver".format(user=os.getenv('USER'))
                    # fix any permissions issues
                    # os.chmod(options.binary_location, 0o755)
                    # shutil.chown(options.binary_location, user=os.getenv('USER'), group=None)
                    # browserAttempt = Edge(executable_path=options.binary_location, options=options)
                    # browserAttempt = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()))
                    Settings.print("browser created - {}".format(browserName))
                else:
                    browserName = "chrome"
                    # linux = x86_64
                    # rpi = aarch64
                    import platform
                    # raspberrypi arm processors don't work with webdriver manager
                    if platform.processor() == "aarch64":
                        browserAttempt = webdriver.Chrome('/usr/bin/chromedriver', options=options)
                    else:
                        browserAttempt = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
                return browserAttempt
            except Exception as e:
                browser_error(e, browserName)
            return None

        def attempt_firefox():
            Settings.maybe_print("attempting firefox web browser...")
            # firefox needs non root
            if os.geteuid() == 0:
                Settings.print("You must run `onlysnarf` as non-root for Firefox to work correctly!")
                return False
            try:
                options = FirefoxOptions()
                if str(Settings.is_debug("firefox")) == "True":
                    options.log.level = "trace"
                add_options(options)
                # options.add_argument("--enable-file-cookies")
                browserAttempt = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
                return browserAttempt
            except Exception as e:
                browser_error(e, "firefox")
            return None

        # doesn't work
        def attempt_ie():
            Settings.maybe_print("attempting ie web browser...")
            try:
                driver_path = IEDriverManager().install()
                os.chmod(driver_path, 0o755)
                # browserAttempt = webdriver.Ie(executable_path=IEService(driver_path))
                browserAttempt = webdriver.Ie(service=IEService(IEDriverManager().install()))
                return browserAttempt
            except Exception as e:
                browser_error(e, "ie")
            return None

        # doesn't work
        def attempt_opera():
            Settings.maybe_print("attempting opera web browser...")
            try:
                # options.add_argument('allow-elevated-browser')
                # options.binary_location = "C:\\Users\\USERNAME\\FOLDERLOCATION\\Opera\\VERSION\\opera.exe"
                browserAttempt = webdriver.Opera(executable_path=OperaDriverManager().install())
                return browserAttempt
            except Exception as e:
                browser_error(e, "opera")
            return None

        def attempt_reconnect():
            self.read_session_data()
            if not self.session_id and not self.session_url:
                Settings.warn_print("unable to read session data!")
                return None
            Settings.maybe_print("reconnecting to web browser...")
            Settings.dev_print("reconnect id: {}".format(self.session_id))
            Settings.dev_print("reconnect url: {}".format(self.session_url))
            try:
                browserAttempt = webdriver.Remote(command_executor=self.session_url, desired_capabilities={})
                browserAttempt.close()   # this closes the session's window - it is currently the only one, thus the session itself will be auto-killed, yet:
                # take the session that's already running
                browserAttempt.session_id = self.session_id
                browserAttempt.title # fails check with: 'NoneType' object has no attribute 'title'
                Settings.print("browser reconnected!")
                return browserAttempt
            except Exception as e:
                Settings.warn_print("unable to reconnect!")
                Settings.dev_print(e)
            return None

        def attempt_remote():
            link = 'http://{}:{}/wd/hub'.format(Settings.get_remote_browser_host(), Settings.get_remote_browser_port())
            Settings.dev_print("remote url: {}".format(link))
            def attempt(dc, opts):
                try:
                    if str(Settings.is_show_window()) == "False":
                        opts.add_argument('--headless')
                    Settings.dev_print("attempting remote: {}".format(browserType))
                    browserAttempt = webdriver.Remote(command_executor=link, desired_capabilities=dc, options=opts)
                    Settings.print("remote browser created - {}".format(browserType))
                    return browserAttempt
                except Exception as e:
                    Settings.warn_print("unable to connect remotely!")
                    Settings.dev_print(e)
                return None

            def brave_options():
                dC = DesiredCapabilities.BRAVE
                options = webdriver.BraveOptions()
                return dC, options

            def chrome_options():
                dC = DesiredCapabilities.CHROME
                options = webdriver.ChromeOptions()
                return dC, options

            def chromium_options():
                dC = DesiredCapabilities.CHROMIUM
                options = webdriver.ChromeOptions()
                return dC, options

            def edge_options():
                dC = DesiredCapabilities.EDGE
                options = webdriver.EdgeOptions()
                return dC, options

            def firefox_options():
                dC = DesiredCapabilities.FIREFOX
                options = webdriver.FirefoxOptions()
                return dC, options

            def ie_options():
                dC = DesiredCapabilities.IE
                options = webdriver.ChromeOptions()
                return dC, options

            def opera_options():
                dC = DesiredCapabilities.OPERA
                options = webdriver.OperaOptions()
                return dC, options

            if "brave" in browserType: return attempt(*brave_options())
            elif "chrome" in browserType: return attempt(*chrome_options())
            elif "chromium" in browserType: return attempt(*chromium_options())
            elif "edge" in browserType: return attempt(*edge_options())
            elif "firefox" in browserType: return attempt(*firefox_options())
            elif "ie" in browserType: return attempt(*ie_options())
            elif "opera" in browserType: return attempt(*opera_options())
            Settings.warn_print("unable to connect remotely via {}!".format(browserType))
            return None

        ################################################################################################################################################
        ################################################################################################################################################
        ################################################################################################################################################

        if "auto" in browserType:
            browser = attempt_reconnect()
            if not browser: browser = attempt_chrome(brave=True, chromium=False, edge=False)
            if not browser: browser = attempt_chrome(brave=False, chromium=False, edge=False)
            if not browser: browser = attempt_chrome(brave=False, chromium=True, edge=False)
            if not browser: browser = attempt_chrome(brave=False, chromium=False, edge=True)
            if not browser: browser = attempt_firefox()
            if not browser: browser = attempt_ie()
            if not browser: browser = attempt_opera()
        elif "remote" in browserType:
            browser = attempt_remote()
        elif "brave" in browserType:
            browser = attempt_chrome(brave=True, chromium=False, edge=False)
        elif "chrome" in browserType:
            browser = attempt_chrome(brave=False, chromium=False, edge=False)
        elif "chromium" in browserType:
            browser = attempt_chrome(brave=False, chromium=True, edge=False)
        elif "edge" in browserType:
            browser = attempt_chrome(brave=False, chromium=False, edge=True)
        elif "firefox" in browserType:
            browser = attempt_firefox()
        elif "ie" in browserType:
            browser = attempt_ie()
        elif "opera" in browserType:
            browser = attempt_opera()

        if browser and str(Settings.is_keep()) == "True":
            self.session_id = browser.session_id
            self.session_url = browser.command_executor._url
            self.write_session_data()

        if not browser:
            Settings.err_print("unable to spawn a web browser!")
            if os.environ.get("ENV") and str(os.environ.get("ENV")) == "test": return False
            os._exit(1)

        browser.implicitly_wait(30) # seconds
        browser.set_page_load_timeout(1200)
        browser.file_detector = LocalFileDetector() # for uploading via remote sessions
        if str(Settings.is_show_window()) == "False":
            Settings.print("browser created - {} (headless)".format(browserType))
        else:
            Settings.print("browser created - {}".format(browserType))
        return browser

    ## possibly move these functions elsewhere (again)
    def read_session_data(self):
        Settings.maybe_print("reading local session")
        path_ = os.path.join(Settings.get_base_directory(), "session.json")
        Settings.dev_print("local session path: "+str(path_))
        try:
            with open(str(path_)) as json_file:  
                data = json.load(json_file)
                self.session_id = data['id']
                self.session_url = data['url']
            Settings.maybe_print("loaded local users")
        except Exception as e:
            Settings.dev_print(e)

    def write_session_data(self):
        Settings.maybe_print("writing local session")
        Settings.dev_print("saving session id: {}".format(self.session_id))        
        Settings.dev_print("saving session url: {}".format(self.session_url))
        path_ = os.path.join(Settings.get_base_directory(), "session.json")
        Settings.dev_print("local session path: "+str(path_))
        data = {}
        data['id'] = self.session_id
        data['url'] = self.session_url
        try:
            with open(str(path_), 'w') as outfile:  
                json.dump(data, outfile, indent=4, sort_keys=True)
            Settings.maybe_print("saved session data")
        except FileNotFoundError:
            Settings.err_print("Missing Session File")
        except OSError:
            Settings.err_print("Missing Session Path")

    ##################
    ##### Upload #####
    ##################

    def upload_files(self, files):
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

        if str(Settings.is_skip_download()) == "True": 
            Settings.print("skipping upload (download)")
            return True, True
        elif str(Settings.is_skip_upload()) == "True": 
            Settings.print("skipping upload (upload)")
            return True, True
        if len(files) == 0:
            Settings.maybe_print("skipping upload (empty file list)")
            return True, True
        if str(Settings.is_skip_upload()) == "True":
            Settings.print("skipping upload (disabled)")
            return True, True
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
            return False, True

        ####

        enter_file = self.browser.find_element(By.ID, "attach_file_photo")
        successful = []

        i = 1
        for file in files_:
            Settings.print('> {} - {}/{}'.format(file.get_title(), i, len(files)))
            i += 1
            successful.append(self.drag_and_drop_file(enter_file , file.get_path()))
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
        if all(successful):
            if self.error_window_upload(): Settings.dev_print("files uploaded successfully")
            else: Settings.dev_print("files probably uploaded succesfully")
            time.sleep(1) # bug prevention
            return True, False
        Settings.warn_print("a file failed to upload!")
        return False, True

    #################
    ##### Users #####
    #################

    @staticmethod
    def get_username():
        """
        Gets the username of the logged in user.

        Returns
        -------
        str
            The username of the logged in user

        """

        try:
            driver = Driver.get_driver()
            driver.auth()
            eles = [ele for ele in driver.browser.find_elements(By.TAG_NAME, "a") if "@" in str(ele.get_attribute("innerHTML")) and "onlyfans" not in str(ele.get_attribute("innerHTML"))]
            Settings.dev_print("successfully found users...")
            if Settings.is_debug():
                for ele in eles:
                    Settings.dev_print("{} - {}".format(ele.get_attribute("innerHTML"), ele.get_attribute("href")))
            if len(eles) == 0:
                Settings.err_print("unable to find username!")
            else:
                username = str(eles[0].get_attribute("href")).replace(ONLYFANS_HOME_URL2, "")
                Settings.dev_print("successfully found active username: {}".format(username))
                return username
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to find username")
        return None

    @staticmethod
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
            driver = Driver.get_driver()
            driver.go_to_page(ONLYFANS_USERS_FOLLOWING_URL)
            count = 0
            while True:
                elements = driver.browser.find_elements(By.CLASS_NAME, "m-subscriptions")
                if len(elements) == count: break
                Settings.print_same_line("({}/{}) scrolling...".format(count, len(elements)))
                count = len(elements)
                driver.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            Settings.print("")
            elements = driver.browser.find_elements(By.CLASS_NAME, "m-subscriptions")
            Settings.dev_print("successfully found subscriptions")
            for ele in elements:
                username = ele.find_element(By.CLASS_NAME, "g-user-username").get_attribute("innerHTML").strip()
                name = ele.find_element(By.CLASS_NAME, "g-user-name").get_attribute("innerHTML")
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

    @staticmethod
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
            driver = Driver.get_driver()
            driver.go_to_page(page)
            user_count = driver.browser.find_elements(By.TAG_NAME, "a")
            # for debugging new regexes:
            for ele in user_count:
                Settings.dev_print("{}  -  {}".format(ele.get_attribute("href"), ele.get_attribute("innerHTML")))
            user_count = [ele.get_attribute("innerHTML").strip() for ele in user_count
                            if "/my/subscribers/active" in str(ele.get_attribute("href"))]
            user_count = user_count[2] # get 3rd occurrence
            # should be:
            # '<span data-v-601d81dd="" class="l-sidebar__user-data__item__count"> 190 </span><span data-v-601d81dd="" class="l-sidebar__user-data__item__text m-break-word"> Fans </span>', 
            user_count = re.search(r'>\s*[0-9]+\s*<', str(user_count))
            Settings.dev_print(user_count)
            user_count = user_count.group()
            user_count = user_count.replace("<","").replace(">","").strip()
            Settings.dev_print(user_count)
            if not user_count or not user_count.isnumeric():
                raise Exception("unable to find fan count!")
            Settings.maybe_print("num fans found: "+user_count)
            thirdTime = 0
            count = 0
            while True:
                elements = driver.browser.find_elements(By.CLASS_NAME, "m-fans")
                if len(elements) == int(user_count): break
                if len(elements) == int(count) and thirdTime >= 3: break
                Settings.print_same_line("({}/{}) scrolling...".format(count, user_count))
                count = len(elements)
                driver.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                if thirdTime >= 3 and len(elements) == 0: break
                thirdTime += 1
            Settings.print("")
            elements = driver.browser.find_elements(By.CLASS_NAME, "m-fans")
            Settings.dev_print("searching fan elements...")
            for ele in elements:

                # TODO ?
                # add checks for lists here

                # /my/favorites
                # /my/lists/34324234

                # eles_ = ele.find_elements(By.TAG_NAME, "a")
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
                username = ele.find_element(By.CLASS_NAME, "g-user-username").get_attribute("innerHTML").strip()
                name = ele.find_element(By.CLASS_NAME, "g-user-name").get_attribute("innerHTML")
                name = re.sub("<!-*>", "", name)
                name = re.sub("<.*\">", "", name)
                name = re.sub("</.*>", "", name).strip()
                # start = datetime.strptime(str(datetime.now()), "%m-%d-%Y:%H:%M")
                # users.append({"name":name, "username":username.replace("@",""), "isFavorite":isFavorite, "lists":lists}) # ,"id":user_id, "started":start})
                users.append({"name":name, "username":username.replace("@","")}) # ,"id":user_id, "started":start})
                Settings.dev_print(users[-1])
            Settings.maybe_print("found {} fans".format(len(users)))
            Settings.dev_print("successfully found fans")
        except Exception as e:
            Settings.print(e)
            Driver.error_checker(e)
            Settings.err_print("failed to find fans")
        return users

    @staticmethod
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
            driver = Driver.get_driver()
            driver.go_to_page(username)
            time.sleep(3) # this should realistically only fail if they're no longer subscribed but it fails often from loading
            elements = driver.browser.find_elements(By.TAG_NAME, "a")
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

    def search_for_list(self, name=None, number=None):
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

        Settings.dev_print("lists: {}".format(self.lists))
        try:
            for list_ in self.lists:
                if list_[0] == name or list_[1] == number:
                    return list_[0], list_[1]
            Settings.dev_print("failed to locate list: {} - {}".format(name, number))
        except Exception as e:
            if "Unable to locate window" not in str(e):
                Settings.dev_print(e)
        return name, number

    @staticmethod
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

        driver = Driver.get_driver()
        driver.auth()
        # gets members from list
        users = []
        Settings.maybe_print("getting list: {} - {}".format(name, number))
        name, number = driver.search_for_list(name=name, number=number)
        try:
            if not name or not number:
                for list_ in driver.get_lists():
                    if name and str(list_[1]).lower() == str(name).lower():
                        number = list_[0]
                    if number and str(list_[0]).lower() == str(number).lower():
                        name = list_[1]
            users = Driver.users_get(page="/my/lists/{}".format(number))
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to find list members")
        return users, name, number

    def get_lists(self):
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
            self.go_to_page("/my/lists")

            elements = self.browser.find_elements(By.CLASS_NAME, "b-users-lists__item")

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
                    count = ele.find_elements(By.CLASS_NAME, "b-users-lists__item__count").get_attribute("innerHTML").replace("people", "").replace("person", "").strip()
                    if int(count) > 0: lists.append("favorites")
                elif "/my/bookmarks" in str(ele.get_attribute("href")):
                    # Settings.print("{} - {}".format(ele.get_attribute("innerHTML"), ele.get_attribute("href")))
                    count = ele.find_elements(By.CLASS_NAME, "b-users-lists__item__count").get_attribute("innerHTML").replace("people", "").replace("person", "").strip()
                    if int(count) > 0: lists.append("bookmarks")
                elif "/my/friends" in str(ele.get_attribute("href")):
                    # Settings.print("{} - {}".format(ele.get_attribute("innerHTML"), ele.get_attribute("href")))
                    count = ele.find_elements(By.CLASS_NAME, "b-users-lists__item__count").get_attribute("innerHTML").replace("people", "").replace("person", "").strip()
                    if int(count) > 0: lists.append("friends")
                elif "/my/lists" in str(ele.get_attribute("href")):
                    try:
                        # Settings.print("{} - {}".format(ele.get_attribute("innerHTML"), ele.get_attribute("href")))

                        # ele = ele.find_elements(By.CLASS_NAME, "b-users-lists__item__text")
                        listNumber = ele.get_attribute("href").replace("https://onlyfans.com/my/lists/", "")
                        listName = ele.find_element(By.CLASS_NAME, "b-users-lists__item__name").get_attribute("innerHTML").strip()
                        count = ele.find_element(By.CLASS_NAME, "b-users-lists__item__count").get_attribute("innerHTML").replace("people", "").replace("person", "").strip()
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

    def get_list_members(self, list):
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

    def add_user_to_list(self, username=None, listNumber=None):
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
            self.go_to_page(ONLYFANS_USERS_ACTIVE_URL)
            end_ = True
            count = 0
            user_ = None
            while end_:
                elements = self.browser.find_elements(By.CLASS_NAME, "m-fans")
                for ele in elements:
                    username_ = ele.find_element(By.CLASS_NAME, "g-user-username").get_attribute("innerHTML").strip()
                    if str(username) == str(username_).replace("@",""):
                        self.browser.execute_script("arguments[0].scrollIntoView();", ele)
                        user_ = ele
                        end_ = False
                if not end_: continue
                if len(elements) == int(count): break
                Settings.print_same_line("({}/{}) scrolling...".format(count, len(elements)))
                count = len(elements)
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            Settings.print("")
            Settings.dev_print("successfully found fans")
            if not user_:
                Settings.err_print("unable to find user - {}".format(username))
                return False
            Settings.maybe_print("found: {}".format(username))
            ActionChains(self.browser).move_to_element(user_).perform()
            Settings.dev_print("finding list add")
            listAdds = user_.find_elements(By.CLASS_NAME, "g-btn.m-add-to-lists")
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
            links = self.browser.find_elements(By.CLASS_NAME, "b-users-lists__item")
            for link in links:
                # Settings.print("{} {}".format(link.get_attribute("href"), link.get_attribute("innerHTML")))
                if str("/my/lists/"+listNumber) in str(link.get_attribute("href")):
                    Settings.dev_print("clicking list")
                    self.move_to_then_click_element(link)
                    time.sleep(0.5)
                    Settings.dev_print("successfully clicked list")
            Settings.dev_print("searching for list save")
            close = self.find_element_to_click("listSingleSave")
            Settings.dev_print("clicking save list")
            close.click()
            Settings.dev_print("successfully added user to list - {}".format(listNumber))
            return True
        except Exception as e:
            Driver.error_checker(e)
            Settings.err_print("failed to add user to list")
        return False

    def add_users_to_list(self, users=[], number=None, name=None):
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
            users_, name, number = self.get_list(number=number, name=name)
            # users = [user for user in users if user not in users_]
            for i, user in enumerate(users[:]):
                for user_ in users_:
                    for key, value in user_.items():
                        if str(key) == "username" and str(user.username) == str(value):
                            users.remove(user)
            Settings.maybe_print("adding users to list: {} - {} - {}".format(len(users), number, name))
            try:
                Settings.dev_print("opening toggle options")
                toggle = self.browser.find_element(By.CLASS_NAME, "b-users__list__add-btn")
                Settings.dev_print("clicking toggle options")
                toggle.click()
                Settings.dev_print("toggle options opened")
            except Exception as e:
                Settings.dev_print("no options to toggle - users already available")
                # Settings.print("weird fuckup")
                # return self.add_users_to_list(users=users, number=number, name=name)
            time.sleep(1)
            original_handle = self.browser.current_window_handle
            clicked = False
            Settings.maybe_print("searching for users")
            while len(users) > 0:
                # find user thing
                eles = self.browser.find_elements(By.CLASS_NAME, "b-chats__available-users__item.m-search")
                for ele in eles:
                    for user in users.copy():
                        # Settings.print("{} - {}".format(i, user.username))
                        if str(user.username) in str(ele.get_attribute("href")):
                            Settings.maybe_print("found user: {}".format(user.username))
                            # time.sleep(2)
                            self.move_to_then_click_element(ele)
                            users.remove(user)
                            clicked = True
                Settings.print_same_line("({}/{}) scrolling...".format(len(eles), len(users)))
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                if len(eles) > 100:
                    Settings.maybe_print("adding users to list individually")
                    for user in users.copy():
                        successful = self.add_user_to_list(username=user.username, listNumber=number)
                        if successful: users.remove(user)
                # if current window has changed, switch back
                if self.browser.current_window_handle != original_handle:
                    self.browser.switch_to.window(original_handle)
            Settings.print("")
            if not clicked:
                Settings.print("skipping list add (none)")
                Settings.dev_print("skipping list save")
                self.browser.refresh()
                Settings.dev_print("### List Add Successfully Skipped ###")
                return True
            if str(Settings.is_debug()) == "True":
                Settings.print("skipping list add (debug)")
                Settings.dev_print("skipping list save")
                self.browser.refresh()
                Settings.dev_print("### List Add Successfully Canceled ###")
                return True
            Settings.dev_print("saving list")
            save = self.find_element_by_name("listSave")
            self.move_to_then_click_element(save)
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

    def exit(self):
        """Save and exit"""

        if not self.browser: return
        ## Cookies
        if str(Settings.is_cookies()) == "True":
            self.cookies_save()
        if str(Settings.is_save_users()) == "True":
            Settings.print("saving and exiting OnlyFans...")
            # from OnlySnarf.classes.user import User
            from ..classes.user import User
            User.write_users_local()
        if str(Settings.is_keep()) == "True":
            self.go_to_home()
            Settings.dev_print("reset to home page")
            if not Driver.NOT_INFORMED_KEPT:
                Settings.print("kept browser open")
            Driver.NOT_INFORMED_KEPT = True
            # todo: add delay for setting this back to false?
        else:
            Settings.print("exiting OnlyFans...")
            self.browser.quit()
            Settings.maybe_print("browser closed")
            self._initialized_ = False
            Driver.DRIVERS.remove(self)

    @staticmethod
    def exit_all():
        """Exit all known browsers."""

        for driver in Driver.DRIVERS:
            driver.exit()

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
            match = re.findall("Started.*([A-Za-z]{3}\\s[0-9]{1,2},\\s[0-9]{4})", text)
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








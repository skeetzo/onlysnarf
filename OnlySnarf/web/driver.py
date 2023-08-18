import os
import time
import pickle
#
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
#
from ..classes.element import Element
from ..util.settings import Settings

class Driver:
    """Driver class for Selenium management"""

    _initialized_ = False

    # MAX_TABS = 20
    initialScrollDelay = 0.5
    scrollDelay = 0.5

    # selenium web driver
    browser = None
    # browser tabs cache
    tabs = []
    logged_in = False

    # Urls
    ONLYFANS_HOME_URL = "https://onlyfans.com"
    ONLYFANS_HOME_URL2 = "https://onlyfans.com/"
    ONLYFANS_NEW_MESSAGE_URL = "/my/chats/send"
    ONLYFANS_CHAT_URL = "/my/chats/chat/"
    ONLYFANS_SETTINGS_URL = "/my/settings/"
    ONLYFANS_USERS_ACTIVE_URL = "/my/subscribers/active"
    ONLYFANS_USERS_FOLLOWING_URL = "/my/subscriptions/active"
    ONLYFANS_LISTS_URL = "/my/lists/"

    def __init__():
        pass
        
    def init():
        """
        Initiliaze the web driver aspect.


        """

        if Driver._initialized_: return

        enable_logging()

        Driver.browser = create_browser(Settings.get_browser_type())
        if not Driver.browser: return

        ## Cookies
        Driver.cookies_load()
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

        Driver.init()
        if not Driver.login():
            if Settings.is_debug():
                return False
            os._exit(1)
        Driver.cookies_save()
        return True

    ###################
    ##### Cookies #####
    ###################

    def cookies_load():
        """Loads existing web browser cookies from local source"""

        if not Settings.is_cookies():
            Settings.maybe_print("skipping cookies load")
            return
        Settings.maybe_print("loading cookies...")
        try:
            if os.path.exists(Settings.get_cookies_path()):
                # must be at onlyfans.com to load cookies of onlyfans.com
                Driver.go_to_home()
                file = open(Settings.get_cookies_path(), "rb")
                cookies = pickle.load(file)
                file.close()
                Settings.dev_print("cookies: ")
                for cookie in cookies:
                    Settings.dev_print(cookie)
                    Driver.browser.add_cookie(cookie)
                Settings.maybe_print("successfully loaded cookies")
                Driver.refresh()
            else: 
                Settings.maybe_print("failed to load cookies, do not exist")
        except Exception as e:
            Settings.print("error loading cookies!")
            Settings.dev_print(e)

    def cookies_save():
        """Saves existing web browser cookies to local source"""

        if not Settings.is_cookies():
            Settings.maybe_print("skipping cookies save")
            return
        Settings.maybe_print("saving cookies...")
        try:
            # must be at onlyfans.com to save cookies of onlyfans.com
            Driver.go_to_home()
            Settings.dev_print(Driver.browser.get_cookies())
            file = open(Settings.get_cookies_path(), "wb")
            pickle.dump(Driver.browser.get_cookies(), file) # "cookies.pkl"
            file.close()
            Settings.maybe_print("successfully saved cookies")
        except Exception as e:
            Settings.print("failed to save cookies!")
            Settings.dev_print(e)

    #####################
    ### Drag and Drop ###
    #####################

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

    ##############
    ### Errors ###
    ##############

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

                    "classes": ["g-btn.m-flat.m-btn-gaps.m-reset-width", "g-btn.m-transparent-bg", "g-btn.m-rounded.m-border", "button.g-btn.m-rounded.m-border"],


            error_buttons = Driver.browser.find_elements(By.CLASS_NAME, element.getClass())
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

    ################
    ### Elements ###
    ################

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
            return None
        # prioritize id over class name
        eleID = None
        try: eleID = Driver.browser.find_element(By.ID, element.getId())
        except: eleID = None
        if eleID: return eleID
        for className in element.getClasses():
            ele = None
            eleCSS = None
            try: ele = Driver.browser.find_element(By.CLASS_NAME, className)
            except: ele = None
            # try: eleCSS = Driver.browser.find_element(By.CSS_SELECTOR, className)
            # except: eleCSS = None
            Settings.dev_print("class: {} - {}:css".format(ele, eleCSS))
            if ele: return ele
            # if eleCSS: return eleCSS
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
            return []
        eles = []
        for className in element.getClasses():
            eles_ = []
            elesCSS_ = []
            try: eles_ = Driver.browser.find_elements(By.CLASS_NAME, className)
            except: eles_ = []
            # try: elesCSS_ = Driver.browser.find_elements(By.CSS_SELECTOR, className)
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

    def find_element_to_click(name, useId=False, offset=0):
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
            try: eles = Driver.browser.find_elements(By.CLASS_NAME, className)
            except: eles = []
            # try: elesCSS = Driver.browser.find_elements(By.CSS_SELECTOR, className)
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
            return True
        except Exception as e:
            # Settings.dev_print(e)
            # if 'firefox' in Driver.browser.capabilities['browserName']:
            try:
                scroll_shim(Driver.browser, element)
                ActionChains(Driver.browser).move_to_element(element).click().perform()
            except Exception as e:
                pass
                # Settings.dev_print(e)
                Driver.browser.execute_script("arguments[0].scrollIntoView();", element)
                # try:
                #     Driver.browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
                #     ActionChains(Driver.browser).move_to_element(element).click().perform()
                # except Exception as e:
                #     Settings.dev_print(e)
        return False

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

        def goto():
            Settings.maybe_print("goto -> onlyfans.com")
            try:
                Driver.browser.set_page_load_timeout(10)
                Driver.browser.get(ONLYFANS_HOME_URL)
            except TimeoutException:
                Settings.dev_print("timed out waiting for page to check login element")
            except WebDriverException as e:
                Settings.dev_print("error fetching home page")
                Settings.err_print(e)
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

    ############
    ### Tabs ###
    ############

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
        # Driver.browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + 't')
        # Driver.browser.get(url)
        # https://stackoverflow.com/questions/50844779/how-to-handle-multiple-windows-in-python-selenium-with-firefox-driver
        windows_before  = Driver.browser.current_window_handle
        Settings.dev_print("current window handle is : %s" %windows_before)
        windows = Driver.browser.window_handles
        Driver.browser.execute_script('''window.open("{}","_blank");'''.format(url))
        # Driver.browser.execute_script("window.open('{}')".format(url))
        Driver.handle_alert()
        Driver.get_page_load()
        try:
            WebDriverWait(Driver.browser, 10, poll_frequency=1).until(EC.number_of_windows_to_be(len(windows)+1))
        except TimeoutException as te:
            Settings.dev_print("Timeout Exception:")
            Settings.err_print(str(te))
            return
        except Exception as e:
            Settings.err_print(e)
            return
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
        Settings.dev_print("searching for page: {}".format(page))
        Settings.dev_print("tabs: {}".format(Driver.tabs))
        Settings.dev_print("handles: {}".format(Driver.browser.window_handles))
        try:
            Settings.dev_print("checking tabs...")
            for page_, handle, value in Driver.tabs:
                Settings.dev_print("{} = {}".format(page_, page))
                if str(page_) in str(page):
                    Driver.browser.switch_to.window(handle)
                    value += 1
                    Settings.dev_print("successfully located tab in cache: {}".format(page))
                    return True
            Settings.dev_print("checking handles...")
            for handle in Driver.browser.window_handles:
                Settings.dev_print(handle)
                Driver.browser.switch_to.window(handle)
                if str(page) in str(Driver.browser.current_url):
                    Settings.dev_print("successfully located tab in handles: {}".format(page))
                    return True
            Settings.dev_print("failed to locate tab: {}".format(page))
            Driver.browser.switch_to.window(original_handle)
        except Exception as e:
            # print(e)
            # if "Unable to locate window" not in str(e):
            Settings.dev_print(e)
        return False

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
            moreOptions = Driver.browser.find_element(By.ID, "new_post_text_input")
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

    ####################################################################################################
    ####################################################################################################
    ####################################################################################################

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

    ####################################################################################################
    ####################################################################################################
    ####################################################################################################

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
            Settings.dev_print("entering text: "+text)
            # extra redundancy in action chain for getting the text entry area
            # for clearing text field with action chain:
            # https://stackoverflow.com/questions/45690688/clear-selenium-action-chains
            textEntry = Driver.browser.find_element(By.ID, "new_post_text_input")
            action = ActionChains(Driver.browser)
            action.move_to_element(textEntry)
            action.click(on_element = textEntry)
            action.double_click()
            action.click_and_hold()
            action.send_keys(Keys.CLEAR)
            action.send_keys(str(text))
            action.perform()
            Settings.dev_print("successfully entered text!")
            return True
        except Exception as e:
            Settings.dev_print(e)
        return False

    #################
    ##### Reset #####
    #################

    def refresh():
        """Refresh the web browser"""

        Settings.dev_print("refreshing browser...")
        Driver.browser.refresh()

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

    ################
    ##### Exit #####
    ################

    def exit():
        """Save and exit"""

        if not Driver.browser: return
        if Settings.is_keep():
            write_session_data(Driver.browser.session_id, Driver.browser.command_executor._url)
        Driver.cookies_save()
        if Settings.is_keep():
            Driver.go_to_home()
            Settings.maybe_print("reset to home page")
        else:
            Driver._initialized_ = False
            Driver.browser.quit()
            Settings.print("closed browser!")

def exit_handler():
    """Exit cleanly"""

    try:
        Driver.exit()
        # import sys
        # sys.exit(0)
    except Exception as e:
        webdriver_logger.error(e)

import atexit
atexit.register(exit_handler)
import os
import time
#
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
#
from ..util.settings import Settings

BROWSER = None

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
        
    @staticmethod
    def init():
        """
        Initiliaze the web driver aspect.


        """

        if Driver._initialized_: return Driver._initialized_

        enable_logging()

        global BROWSER
        BROWSER = create_browser(Settings.get_browser_type())
        if not BROWSER:
            if Settings.is_debug():
                return False
            os._exit(1)

        ## Cookies
        cookies_load(BROWSER)
        Driver.tabs.append([BROWSER.current_url, BROWSER.current_window_handle, 0])
        Driver._initialized_ = True
        return Driver._initialized_

    def auth():
        """
        Authorization check

        Logs in with provided runtime creds if not logged in

        Returns
        -------
        bool
            Whether or not the login attempt was successful

        """

        if not Driver.init(): return
        if not Driver.login():
            if Settings.is_debug():
                return False
            os._exit(1)
        Driver.cookies_save()
        return True

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

    ####################################################################################################
    ####################################################################################################
    ####################################################################################################

    # no longer used?
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
    def get_browser():
        if Driver.browser: return Driver.browser
        Driver.init()
        Driver.auth()
        if not Driver.browser:
            Settings.err_print("unable to get browser!")
        return Driver.browser

    # @staticmethod
    # def get_driver():
    #     """
    #     Return an existing driver, if not create one

    #     Returns
    #     -------
    #     classes.driver
    #         The default driver object.


    #     """

    #     if len(Driver.DRIVERS) > 0:
    #         return Driver.DRIVERS[0]
    #     return Driver()

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
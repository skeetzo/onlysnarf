import os
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

from .browser import create_browser
from .chat import get_user_chat
from .cookies import cookies_load, cookies_save
from .goto import go_to_home
from .login import login
from .message import message
from .post import post
from .users import get_current_username, get_userid_by_username, get_users_by_type
from ..util.settings import Settings

BROWSER = None

class Driver:
    """Driver class for Selenium management"""

    TABS = []

    ###############
    ##### Get #####
    ###############

    def get_browser():
        global BROWSER
        if BROWSER: return BROWSER
        BROWSER = create_browser(Settings.get_browser_type())
        cookies_load(BROWSER)
        Driver.TABS.append([BROWSER.current_url, BROWSER.current_window_handle, 0])
        if login(BROWSER):
            cookies_save(BROWSER)
            return BROWSER
        raise Exception("Unable to create OnlyFans browser!")

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
            Settings.err_print("Unable to locate element; OnlySnarf may require an update!")
        elif "Message: " in str(e):
            Settings.dev_print(e)
        else:
            Settings.err_print(e)

    ################
    ##### Exit #####
    ################

    def exit(browser):
        """Save and exit"""

        if not browser: return
        if Settings.is_keep():
            write_session_data(browser.session_id, browser.command_executor._url)
        cookies_save(browser)
        if Settings.is_keep():
            go_to_home(browser)
            Settings.maybe_print("reset to home page")
        else:
            browser.quit()
            Settings.print("Web browser closed!")

    #########################
    ##### Functionality #####
    #########################

    Driver.post = post
    Driver.message = message
    Driver.get_current_username = get_current_username
    Driver.get_userid_by_username = get_userid_by_username
    # Driver.get_username_by_id = get_username_by_id # unfinished
    Driver.get_users = get_users_by_type
    Driver.get_user_chat = get_user_chat
    # Driver.get_recent_chats = get_recent_chats # unfinished

    # TODO: add remaining functionality like lists, promotion, profile, etc
    # lists (todo)
    #     get_list

import os
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

from ..util.settings import Settings

# Globals #
BROWSER = None
TABS = []

# TODO: move somewhere like DEFAULTS or a new file like URLS
ONLYFANS_HOME_URL = "https://onlyfans.com"
ONLYFANS_HOME_URL2 = "https://onlyfans.com/"
ONLYFANS_NEW_MESSAGE_URL = "/my/chats/send"
ONLYFANS_CHAT_URL = "/my/chats/chat/"
ONLYFANS_SETTINGS_URL = "/my/settings/"
ONLYFANS_USERS_ACTIVE_URL = "/my/subscribers/active"
ONLYFANS_USERS_FOLLOWING_URL = "/my/subscriptions/active"
ONLYFANS_LISTS_URL = "/my/lists/"
# MAX_TABS = 20

class Driver:
    """Driver class for Selenium management"""

    initialScrollDelay = 0.5
    scrollDelay = 0.5

    def auth(browser):
        """
        Authorization check

        Logs in with provided runtime creds if not logged in

        Returns
        -------
        bool
            Whether or not the login attempt was successful

        """

        if not login(browser):
            if Settings.is_debug():
                return False
            os._exit(1)
        cookies_save(browser)
        return True

    ####################################################################################################
    ####################################################################################################
    ####################################################################################################

    def get_browser():
        global BROWSER
        if BROWSER: return BROWSER
        BROWSER = create_browser(Settings.get_browser_type())
        cookies_load(BROWSER)
        global TABS
        TABS.append([BROWSER.current_url, BROWSER.current_window_handle, 0])
        if auth(BROWSER):
            cookies_save(BROWSER)
            return BROWSER
        raise Exception("Unable to create OnlyFans browser!")

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
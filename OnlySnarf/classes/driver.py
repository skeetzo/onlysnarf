import os
import time
import logging

from .webdriver import create_browser, get_user_chat, cookies_load, cookies_save, go_to_home, login, \
    message as WEBDRIVER_message, post as WEBDRIVER_post, \
    get_userid_by_username as WEBDRIVER_get_userid_by_username, get_users_by_type as WEBDRIVER_get_users_by_type, \
    get_recent_chat_users as WEBDRIVER_get_recent_chat_users

from ..util.config import CONFIG

BROWSER = None
TABS = []

class Webdriver:

    def __init__(self):
        pass

    ###############
    ##### Get #####
    ###############

    def get_browser():
        global BROWSER
        if BROWSER: return BROWSER
        BROWSER = create_browser(CONFIG["browser"])
        cookies_load(BROWSER)
        global TABS
        TABS.append([BROWSER.current_url, BROWSER.current_window_handle, 0])
        if login(BROWSER):
            cookies_save(BROWSER)
            return BROWSER
        raise Exception("Unable to create OnlyFans browser!")

    ################
    ##### Exit #####
    ################

    def exit(browser):
        """Save and exit"""

        if not browser: return
        if CONFIG["keep"]:
            write_session_data(browser.session_id, browser.command_executor._url)
        cookies_save(browser)
        if CONFIG["keep"]:
            go_to_home(browser)
            logging.debug("reset to home page")
        else:
            browser.quit()
            logging.info("Web browser closed!")

    #########

    @staticmethod
    def discount_user(discount_object):
        return WEBDRIVER_discount_user(Webdriver.get_browser(), discount_object)

    @staticmethod
    def message(message_object):
        return WEBDRIVER_message(Webdriver.get_browser(), message_object)

    @staticmethod
    def post(post_object):
        return WEBDRIVER_post(Webdriver.get_browser(), post_object)

    @staticmethod
    def get_recent_chat_users():
        return WEBDRIVER_get_recent_chat_users(Webdriver.get_browser())

    @staticmethod
    def get_userid_by_username():
        return WEBDRIVER_get_userid_by_username(Webdriver.get_browser())

    @staticmethod
    def get_users(isFan=False, isFollower=False):
        return WEBDRIVER_get_users_by_type(Webdriver.get_browser(), isFan=isFan, isFollower=isFollower)

    @staticmethod
    def get_user_chat():
        return WEBDRIVER_get_user_chat(Webdriver.get_browser())


# TODO: add remaining functionality like lists, promotion, profile, etc
# lists (todo)
#     get_list

discount_user = Webdriver.discount_user
message = Webdriver.message
post = Webdriver.post

get_recent_chat_users = Webdriver.get_recent_chat_users
get_userid_by_username = Webdriver.get_userid_by_username
get_users = Webdriver.get_users

# read_user_messages = Webdriver.read_user_messages

def exit_handler():
    """Exit cleanly"""

    try:
        global BROWSER
        Webdriver.exit(BROWSER)
    except Exception as e:
        print(e)

import atexit
atexit.register(exit_handler)

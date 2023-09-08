import os
import time
import logging

from .webdriver import create_browser, get_user_chat, cookies_load, cookies_save, go_to_home, login as WEBDRIVER_login, \
    discount_user as WEBDRIVER_discount_user, message as WEBDRIVER_message, post as WEBDRIVER_post, \
    get_userid_by_username as WEBDRIVER_get_userid_by_username, get_users_by_type as WEBDRIVER_get_users_by_type, \
    get_recent_chat_users as WEBDRIVER_get_recent_chat_users

from ..util.config import CONFIG

BROWSER = None

###############
##### Get #####
###############

def get_browser():
    global BROWSER
    if BROWSER: return BROWSER
    BROWSER = create_browser(CONFIG["browser"])
    cookies_load(BROWSER)
    # return BROWSER
    if WEBDRIVER_login(BROWSER):
        cookies_save(BROWSER)
        return BROWSER
    raise Exception("Unable to create OnlyFans browser!")

################
##### Exit #####
################

def close_browser(browser=BROWSER):
    """Save and exit"""

    logging.debug("closing web browser...")
    # global BROWSER
    if not BROWSER:
        logging.debug("no browser to close!")
        return
    cookies_save(BROWSER)
    if CONFIG["keep"]:
        go_to_home(BROWSER, force=True)
        logging.debug("reset to home page")
    else:
        BROWSER.quit()
        logging.info("web browser closed!")

#####################################
### Basic Functionality Shortcuts ###
#####################################

def discount_user(discount_object):
    return WEBDRIVER_discount_user(get_browser(), discount_object)

def message(message_object):
    return WEBDRIVER_message(get_browser(), message_object)

def post(post_object):
    return WEBDRIVER_post(get_browser(), post_object)

def get_recent_chat_users():
    return WEBDRIVER_get_recent_chat_users(get_browser())

def get_userid_by_username():
    return WEBDRIVER_get_userid_by_username(get_browser())

def get_users(isFan=False, isFollower=False):
    return WEBDRIVER_get_users_by_type(get_browser(), isFan=isFan, isFollower=isFollower)

def get_user_chat():
    return WEBDRIVER_get_user_chat(get_browser())


# TODO: add remaining functionality like lists, promotion, profile, etc
# lists (todo)
#     get_list


def exit_handler():
    """Exit cleanly"""

    try:
        close_browser()
    except Exception as e:
        print(e)

import atexit
atexit.register(exit_handler)
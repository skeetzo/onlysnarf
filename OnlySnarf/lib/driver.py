import os
import time
import logging
logger = logging.getLogger(__name__)

from .webdriver import create_browser, get_user_chat, cookies_save, go_to_home, login as WEBDRIVER_login, \
    discount_user as WEBDRIVER_discount_user, message as WEBDRIVER_message, post as WEBDRIVER_post, \
    get_userid_by_username as WEBDRIVER_get_userid_by_username, get_users_by_type as WEBDRIVER_get_users_by_type, \
    get_recent_chat_users as WEBDRIVER_get_recent_chat_users

from .webdriver import expiration as WEBDRIVER_expiration, poll as WEBDRIVER_poll, schedule as WEBDRIVER_schedule

from ..util.config import CONFIG

BROWSER = None
LOGGED_IN = False

#################
##### Close #####
#################

def close_browser():
    """Save and exit"""

    global BROWSER
    logger.debug("closing web browser...")
    if not BROWSER:
        logger.debug("no browser to close!")
        return
    cookies_save(BROWSER)
    if CONFIG["keep"]:
        go_to_home(BROWSER, force=True)
        logger.debug("reset to home page")
    else:
        BROWSER.quit()
        logger.info("web browser closed!")

###############
##### Get #####
###############

def get_browser():
    global BROWSER
    if BROWSER: return BROWSER
    try:
        BROWSER = create_browser(CONFIG["browser"])
    except Exception as e:
        logger.critical(e)
        os._exit(1)
    return BROWSER

#################
##### Login #####
#################

def login():
    global LOGGED_IN
    global BROWSER
    if LOGGED_IN: return BROWSER
    BROWSER = get_browser()
    try:
        WEBDRIVER_login(BROWSER, CONFIG["login"])
    except Exception as e:
        logger.critical(e)
        os._exit(1)
    LOGGED_IN = True
    return BROWSER

#####################################
### Basic Functionality Shortcuts ###
#####################################

def discount_user(discount_object):
    return WEBDRIVER_discount_user(login(), discount_object)

def expiration(expires_amount):
    return WEBDRIVER_expiration(login(), expires_amount)

def message(message_object):
    return WEBDRIVER_message(login(), message_object)

def poll(poll_object):
    return WEBDRIVER_poll(login(), poll_object)

def post(post_object):
    return WEBDRIVER_post(login(), post_object)

def schedule(schedule_object):
    return WEBDRIVER_schedule(login(), schedule_object)

def get_recent_chat_users():
    return WEBDRIVER_get_recent_chat_users(login())

def get_userid_by_username():
    return WEBDRIVER_get_userid_by_username(login())

def get_users(isFan=False, isFollower=False):
    return WEBDRIVER_get_users_by_type(login(), isFan=isFan, isFollower=isFollower)

def get_user_chat():
    return WEBDRIVER_get_user_chat(login())


# TODO: add remaining functionality like lists, promotion, profile, etc
# lists (todo)
#     get_list

####################
### Exit Handler ###
####################

def exit_handler():
    """Exit cleanly"""

    try:
        close_browser()
    except Exception as e:
        logger.error(e)

import atexit
atexit.register(exit_handler)
import os
import time
import logging
logger = logging.getLogger(__name__)

from .webdriver import create_browser, get_user_chat, cookies_save, go_to_home, login as WEBDRIVER_login, \
    discount as WEBDRIVER_discount, message as WEBDRIVER_message, post as WEBDRIVER_post, \
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
    if CONFIG.get("keep", False):
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
        BROWSER = create_browser(CONFIG.get("browser", "auto"))
    except Exception as e:
        logger.critical(e)
        os._exit(1)
    return BROWSER

#################
##### Login #####
#################

def login(method="auto", cookies=False):
    global LOGGED_IN
    global BROWSER
    if LOGGED_IN: return BROWSER
    BROWSER = get_browser()
    try:
        WEBDRIVER_login(BROWSER, method=method, cookies=cookies)
    except Exception as e:
        logger.critical(e)
        os._exit(1)
    LOGGED_IN = True
    return BROWSER

#####################################
### Basic Functionality Shortcuts ###
#####################################

def discount_user(discount_object):
    return WEBDRIVER_discount(login(cookies=CONFIG["cookies"]), discount_object)

def expiration(expires_amount):
    return WEBDRIVER_expiration(login(cookies=CONFIG["cookies"]), expires_amount)

def message(message_object):
    return WEBDRIVER_message(login(cookies=CONFIG["cookies"]), message_object)

def poll(poll_object):
    return WEBDRIVER_poll(login(cookies=CONFIG["cookies"]), poll_object)

def post(post_object):
    return WEBDRIVER_post(login(cookies=CONFIG["cookies"]), post_object)

def schedule(schedule_object):
    return WEBDRIVER_schedule(login(cookies=CONFIG["cookies"]), schedule_object)

def get_recent_chat_users():
    return WEBDRIVER_get_recent_chat_users(login(cookies=CONFIG["cookies"]))

def get_userid_by_username():
    return WEBDRIVER_get_userid_by_username(login(cookies=CONFIG["cookies"]))

def get_users(isFan=False, isFollower=False):
    return WEBDRIVER_get_users_by_type(login(cookies=CONFIG["cookies"]), isFan=isFan, isFollower=isFollower)

def get_user_chat():
    return WEBDRIVER_get_user_chat(login(cookies=CONFIG["cookies"]))


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
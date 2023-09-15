import os
import time
import logging

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
    logging.debug("closing web browser...")
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

###############
##### Get #####
###############

def get_browser():
    global BROWSER
    if BROWSER: return BROWSER
    try:
        BROWSER = create_browser(CONFIG["browser"])
    except Exception as e:
        logging.error(e)
        os._exit(1)
    return BROWSER

#################
##### Login #####
#################

def login():
    global LOGGED_IN
    if LOGGED_IN: return True
    browser = get_browser()
    try:
        WEBDRIVER_login(browser, CONFIG["login"])
    except Exception as e:
        logging.error(e)
        os._exit(1)
    LOGGED_IN = True
    return True

#####################################
### Basic Functionality Shortcuts ###
#####################################

def discount_user(discount_object):
    return WEBDRIVER_discount_user(get_browser(), discount_object)

def expiration(expires_amount):
    return WEBDRIVER_expiration(get_browser(), expires_amount)

def message(message_object):
    return WEBDRIVER_message(get_browser(), message_object)

def poll(poll_object):
    return WEBDRIVER_poll(get_browser(), poll_object)

def post(post_object):
    return WEBDRIVER_post(get_browser(), post_object)

def schedule(schedule_object):
    return WEBDRIVER_schedule(get_browser(), schedule_object)

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

####################
### Exit Handler ###
####################

def exit_handler():
    """Exit cleanly"""

    try:
        close_browser()
    except Exception as e:
        print(e)

import atexit
atexit.register(exit_handler)
import os
import pickle
import logging
logger = logging.getLogger(__name__)

from .. import DEFAULT
from .errors import error_checker
from .goto import go_to_home

###################
##### Cookies #####
###################

def cookies_load(browser):
    """Loads existing web browser cookies from local source"""

    logger.debug("loading cookies...")
    try:
        if os.path.exists(get_cookies_path()):
            # must be at onlyfans.com to load cookies of onlyfans.com
            go_to_home(browser)
            file = open(get_cookies_path(), "rb")
            cookies = pickle.load(file)
            file.close()
            # logger.debug("cookies: ")
            for cookie in cookies:
                # logger.debug(cookie)
                browser.add_cookie(cookie)
            browser.refresh()
            logger.debug("successfully loaded cookies!")
        else: 
            logger.warning("missing cookies file!")
    except Exception as e:
        error_checker(e)
        logger.warning("failed to load cookies!")

def cookies_save(browser):
    """Saves existing web browser cookies to local source"""

    logger.debug("saving cookies...")
    try:
        # must be at onlyfans.com to save cookies of onlyfans.com
        go_to_home(browser)
        # logger.debug(browser.get_cookies())
        file = open(get_cookies_path(), "wb")
        pickle.dump(browser.get_cookies(), file) # "cookies.pkl"
        file.close()
        logger.debug("successfully saved cookies!")
    except Exception as e:
        error_checker(e)
        logger.warning("failed to save cookies!")

def get_cookies_path():
    return os.path.join(DEFAULT.ROOT_PATH, "cookies.pkl")

def reset_cookies():
    logging.debug("resetting cookies...")
    try:
        os.remove(get_cookies_path())
    except Exception as e:
        pass
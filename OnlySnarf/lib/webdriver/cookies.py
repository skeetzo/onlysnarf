import os
import pickle
import logging

from .. import CONFIG, DEFAULT
from .errors import error_checker
from .goto import go_to_home

###################
##### Cookies #####
###################

def cookies_load(browser):
    """Loads existing web browser cookies from local source"""

    if not CONFIG["cookies"]:
        logging.debug("skipping cookies (load)")
        return
    logging.debug("loading cookies...")
    try:
        if os.path.exists(get_cookies_path()):
            # must be at onlyfans.com to load cookies of onlyfans.com
            go_to_home(browser)
            file = open(get_cookies_path(), "rb")
            cookies = pickle.load(file)
            file.close()
            # logging.debug("cookies: ")
            for cookie in cookies:
                # logging.debug(cookie)
                browser.add_cookie(cookie)
            browser.refresh()
            logging.debug("successfully loaded cookies!")
        else: 
            logging.warning("missing cookies file!")
    except Exception as e:
        error_checker(e)
        logging.warning("failed to load cookies!")

def cookies_save(browser):
    """Saves existing web browser cookies to local source"""

    if not CONFIG["cookies"]:
        logging.debug("skipping cookies (save)")
        return
    logging.debug("saving cookies...")
    try:
        # must be at onlyfans.com to save cookies of onlyfans.com
        go_to_home(browser)
        # logging.debug(browser.get_cookies())
        file = open(get_cookies_path(), "wb")
        pickle.dump(browser.get_cookies(), file) # "cookies.pkl"
        file.close()
        logging.debug("successfully saved cookies!")
    except Exception as e:
        error_checker(e)
        logging.warning("failed to save cookies!")

def get_cookies_path():
    return os.path.join(DEFAULT.ROOT_PATH, "cookies.pkl")
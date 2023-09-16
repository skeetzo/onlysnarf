import os
import logging
logger = logging.getLogger(__name__)

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .element import find_element_to_click
from .errors import error_checker
from .message import click_close_icons
from .. import CONFIG, DEFAULT, debug_delay_check

######################
##### Expiration #####
######################

def expiration(browser, expires):
    """
    Enters the provided expiration duration for a post

    Must be on home page

    Parameters
    ----------
    expires : str
        The duration (in days) until the post expires
    
    Returns
    -------
    bool
        Whether or not entering the expiration was successful

    """

    if str(expires) == str(DEFAULT.EXPIRATION_NONE):
        logger.debug("skipping empty expiration")
        return True
    try:
        logger.info(f"Expiration: {expires}")
        enter_expiration(browser, expires)
        # unnecessary due to clear_message
        if CONFIG["debug"]:
            logger.debug("skipping expiration save (debug)")
            click_close_icons(browser)
        return True
    except Exception as e:
        error_checker(e)
    click_close_icons(browser)
    return False

def enter_expiration(browser, expires):
    try:
        logger.debug("entering expiration...")
        element = find_element_to_click(browser, "b-make-post__expire-period-btn")
        action = ActionChains(browser)
        action.click(on_element=element)
        action.pause(int(1))
        action.send_keys(Keys.TAB)
        action.send_keys(str(expires))
        action.pause(int(1))
        action.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
        action.pause(int(1))
        action.send_keys(Keys.ENTER)
        action.perform()
        logger.debug("successfully entered expiration!")
        debug_delay_check()
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to enter expiration!")
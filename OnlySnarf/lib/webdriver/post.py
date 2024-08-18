import time
import logging
logger = logging.getLogger(__name__)

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from .clear import click_clear_button, clear_text
from .element import find_element_to_click
from .expiration import expiration as EXPIRES
from .errors import error_checker
from .poll import poll as POLL
from .schedule import schedule as SCHEDULE
from .upload import upload_files
from .. import CONFIG, debug_delay_check

################
##### Post #####
################

def post(browser, post_object):
    """
    Post the message to OnlyFans.

    Optionally tweet if enabled. A message must contain text and can contain:
    - files
    - keywords
    - performers
    - expiration
    - schedule
    - poll

    Parameters
    ----------
    post_object : dict
        The message values to be entered into the post 

    Returns
    -------
    bool
        Whether or not the post was successful

    """

    if not post_object:
        logger.debug("skipping empty post")
        return True
    click_clear_button(browser)
    #################### Formatted Text ####################
    logger.info("====================")
    logger.info("Posting:")
    logger.info(f"- Files: {len(post_object['files'])}")
    logger.info(f"- Performers: {post_object['performers']}")
    logger.info(f"- Keywords: {post_object['keywords']}")
    logger.info(f"- Text: {post_object['text']}")
    logger.info(f"- Tweeting: {CONFIG['tweeting']}")
    ## Expires, Schedule, Poll ##
    if not EXPIRES(browser, post_object["expiration"]): return False
    if post_object["schedule"] and not SCHEDULE(browser, post_object["schedule"]): return False
    if post_object["poll"] and not POLL(browser, post_object["poll"]): return False
    logger.info("====================")
    ############################################################
    try:
        if CONFIG["tweeting"]: enable_tweeting(browser)
        if not enter_text(browser, post_object["text"]):
            logger.error("failed to post!")
            return False
        successful, skipped = upload_files(browser, post_object["files"])
        if successful and not skipped:
            postButton = [ele for ele in browser.find_elements(By.TAG_NAME, "button") if "Post" in ele.get_attribute("innerHTML")][0]
            WebDriverWait(browser, CONFIG["upload_max_duration"], poll_frequency=3).until(EC.element_to_be_clickable(postButton))
            logger.info("upload complete!")
        send_post(browser)
    except TimeoutException:
        logger.error("timed out waiting for post upload!")
    except Exception as e:
        logger.debug(e)
        logger.error("failed to send post!")
    click_clear_button(browser)
    return True

def enter_text(browser, text):
        """
        Enter the provided text into the page's text area

        Must be ran on a page with an OnlyFans text area.


        Parameters
        ----------
        text : str
            The text to enter

        Returns
        -------
        bool
            Whether or not entering the text was successful

        """

        try:
            clear_text(browser)
            logger.debug("entering text: "+text)
            element = browser.find_element(By.ID, "new_post_text_input")
            action = ActionChains(browser)
            action.move_to_element(element)
            action.click(on_element=element)
            action.double_click()
            action.click_and_hold()
            action.send_keys(Keys.CLEAR)
            action.send_keys(str(text))
            action.perform()
            logger.debug("successfully entered text!")
            return True
        except Exception as e:
            error_checker(e)
        raise Exception("failed to enter text!")

# TODO: test this
def enable_tweeting(browser):
    logger.debug("enabling tweeting...")
    ActionChains(browser).move_to_element(browser.find_element(By.CLASS_NAME, "b-btns-group").find_elements(By.XPATH, "./child::*")[0]).click().perform()
    logger.debug("enabled tweeting")

def send_post(browser):
    logger.debug("sending post...")
    if CONFIG["debug"] and str(CONFIG["debug"]) == "True":
        logger.info('skipped post (debug)')
        debug_delay_check()
        return True
    find_element_to_click(browser, "button", by=By.TAG_NAME, text="Post").click()
    logger.info('posted to OnlyFans!')
    time.sleep(1)
    return True

# no longer used?
# tries both and throws error for not found element internally
def open_more_options(browser):
    """
    Click to open more options on a post.

    Returns
    -------
    bool
        Whether or not opening more options was successful

    """

    def option_one():
        """Click on '...' element"""

        logger.debug("opening options (1)")
        moreOptions = find_element_to_click(browser, "button.g-btn.m-flat.b-make-post__more-btn")
        if not moreOptions: return False    
        moreOptions.click()
        logger.debug("successfully opened more options (1)")
        return True
    def option_two():
        """Click in empty space"""

        logger.debug("opening options (2)")
        moreOptions = find_element_to_click(browser, "new_post_text_input", by=By.ID)
        if not moreOptions: return False    
        moreOptions.click()
        logger.debug("successfully opened more options (2)")
        return True

    try:
        return option_one()
    except Exception as e:
        error_checker(e)

    try:
        return option_two()
    except Exception as e:
        error_checker(e)
    
    raise Exception("unable to locate 'More Options' element")

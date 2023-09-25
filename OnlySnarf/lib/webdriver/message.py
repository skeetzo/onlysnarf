import time
import logging
logger = logging.getLogger(__name__)

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import WebDriverException

from .clear import clear_text, click_close_icons
from .collections import clear_collections, click_collections
from .element import find_element_to_click
from .errors import error_checker
from .goto import go_to_home, go_to_page
# from .post import enter_text
from .upload import upload_files
from .upload import error_window_upload
from .users import click_user_button, get_user_by_username
from .. import debug_delay_check
from .. import CONFIG
from .. import ONLYFANS_HOME_URL, ONLYFANS_CHAT_URL, ONLYFANS_NEW_MESSAGE_URL

####################
##### Messages #####
####################

def message(browser, message_object):

    """
    Complete the various components of sending a message to a user.
    
    Parameters
    ----------
    message : Object
        The message to send as a serialized Message object from get_message.

    Returns
    -------
    bool
        Whether or not the message was successful
    """

    try:
        logger.info(f"Entering message to {', '.join(message_object['recipients'])}: (${message_object['price']}) {message_object['text']}")
        if len(message_object['includes']) > 0:
            logger.info(f"Includes: {','.join(message_object['includes'])}")
        if len(message_object['excludes']) > 0:
            logger.info(f"Excludes: {','.join(message_object['excludes'])}")
        # prepare the message
        if len(message_object["recipients"]) > 1 or message_object["includes"] or message_object["excludes"]:
            go_to_page(browser, ONLYFANS_NEW_MESSAGE_URL)
            clear_collections(browser, includes=message_object["includes"], excludes=message_object["excludes"])
            # if not messaging a single user directly, all these can be stacked in a single message
            click_collections(browser, includes=message_object["includes"], excludes=message_object["excludes"])
            # use same page to add additional users to message 
            for username in message_object["recipients"]:
                add_user_to_message(browser, username)
        else:
            # if none of above or solo messaging, switch to normal user messaging (locates user_id on profile page and opens url link)
            # doesn't need to clear lists when opening a new tab to search for the username then send them a message
            message_user_by_username(browser, message_object["recipients"][0])

        message_text(browser, message_object['text'])
        message_price(browser, message_object['price'])
        upload_files(browser, message_object['files'])
        message_send(browser)
        if CONFIG["debug"]:
            clear_collections(browser, includes=message_object["includes"], excludes=message_object["excludes"])
            # message confirm function contains default clear text behavior
            # message_clear(browser)
            browser.refresh() # removes all users from input fields
        return True
    except Exception as e:
        error_checker(e)
    # try to clear message just in case
    try:
        clear_collections(browser, includes=message_object["includes"], excludes=message_object["excludes"])
        message_clear(browser)
        browser.refresh() # clears entered usernames
    except Exception as e:
        error_checker(e)
    logger.error("failed to send message!")
    return False

########################################################################
########################################################################
########################################################################

# add username to existing mass message being started
def add_user_to_message(browser, username):
    try:
        logger.debug(f"adding user to message: {username}")
        element = browser.find_element(By.CLASS_NAME, "b-search-users-form__input")
        ActionChains(browser).move_to_element(element).click(on_element=element).double_click().click_and_hold().send_keys(Keys.CLEAR).send_keys(str(username)).perform()
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "b-search-users-form__input")))
        elements = browser.find_elements(By.CLASS_NAME, "b-available-users__item")
        if len(elements) > 0:
            for element in elements:
                element.click()
            return True
    except Exception as e:
        error_checker(e)
    raise Exception(f"unable to add {username} to message!")

## TODO: add check for clearing any text or images already in post field?
def message_clear(browser):
    try:
        clear_text(browser)
        click_close_icons(browser)
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to clear message!")

def message_send(browser):
    """
    Wait for the send button to be clickable and click it

    Returns
    -------
    bool
        Whether or not the button click was successful

    """

    try:
        logger.debug("waiting for message send to be clickable...")
        confirm = WebDriverWait(browser, int(CONFIG["upload_max_duration"]), poll_frequency=3).until(EC.element_to_be_clickable((By.CLASS_NAME, "g-btn.m-rounded.b-chat__btn-submit")))
        logger.debug("message send is clickable")
        debug_delay_check()
        if CONFIG["debug"] and str(CONFIG["debug"]) == "True":
            logger.info('skipping message (debug)')
            message_clear(browser)
            return True
        else:
            logger.debug("clicking send...")
            confirm.click()
            time.sleep(0.5) # allow final modal to appear 
            return message_confirm(browser)
    except TimeoutException:
        logger.error("Timed out waiting for message confirm!")
    except Exception as e:
        error_checker(e)
    message_clear(browser)
    raise Exception("failed to confirm message!")

def message_confirm(browser):
    try:
        logger.debug("clicking confirm...")
        find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Yes").click()
        logger.info('OnlyFans message sent!')
        time.sleep(1)
        return True
    except Exception as e:
        error_checker(e)
    return False

def message_price(browser, price):
    """
    Enter the provided price into the message on the page

    Parameters
    ----------
    price : str
        The price to enter in dollars

    Returns
    -------
    bool
        Whether or not entering the price was successful

    """

    try:
        if not price or str(price) == "None":
            logger.debug("skipping empty price")
            return True
        message_price_clear(browser)
        message_price_open(browser)
        message_price_enter(browser, price)
        message_price_save(browser)
        logger.debug("successfully entered message price!")
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to enter message price!")

# clear any pre-existing message price
def message_price_clear(browser):
    try:
        logger.debug("clearing any preexisting price...")
        # this is not the same class as the x icons for close_icons
        element = browser.find_element(By.CLASS_NAME, "m-btn-remove")
        if element:
            element.click()
            logger.debug("sucessfully cleared preexisting price!")
    except Exception as e:
        if "unable to locate element" not in str(e).lower():
            error_checker(e)
            raise Exception("failed to clear message price!")
    return True

def message_price_open(browser, reattempt=False):
    try:
        logger.debug("clicking price button...")
        for element in browser.find_element(By.CLASS_NAME, "b-make-post__actions__btns").find_elements(By.XPATH, "./child::*"):
            if "icon-price" in str(element.get_attribute("innerHTML")):
                browser.execute_script("arguments[0].click()", element)
                logger.debug("sucessfully clicked price button!")
                return True
                # BUG: normal methods not working :/
                # ActionChains(browser).move_to_element(element).click().perform()
                # element.click()
                # element.send_keys("\n")
    except Exception as e:
        print(e)
        if "obscures it" in str(e) and not reattempt:
            error_window_upload(browser)
            return message_price_open(browser, reattempt=True)
        error_checker(e)
    raise Exception("failed to open price model!")

def message_price_enter(browser, price, reattempt=False):
    try:
        logger.debug("entering price...")
        element = WebDriverWait(browser, 10, poll_frequency=2).until(EC.element_to_be_clickable(browser.find_element(By.ID, "priceInput_1")))
        element.click()
        element.send_keys(str(price))
        logger.debug("entered price!")
        debug_delay_check()
        return True
    except Exception as e:
        if "obscures it" in str(e) and not reattempt:
            error_window_upload(browser)
            return message_price_enter(browser, price, reattempt=True)
        error_checker(e)
    raise Exception("failed to enter price amount!")

def message_price_save(browser):
    try:
        logger.debug("saving price...")
        find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Save").click()
        logger.debug("saved price!")
        debug_delay_check()
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to save price!")

def message_text(browser, text):
    """
    Enter the provided text into the message on the page

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
        logger.debug("entering text...")
        # clear any preexisting text first
        element = WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.ID, 'new_post_text_input')))
        ActionChains(browser).move_to_element(element).double_click().click_and_hold().send_keys(Keys.CLEAR).send_keys(str(text)).perform()
        logger.debug("successfully entered text!")
        time.sleep(0.5)
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to enter message text!")

######################################################################
######################################################################
######################################################################

# TODO: possibly remove
def message_user_by_id(browser, user_id):
    """
    Message the provided user id

    Parameters
    ----------
    user_id : str
        The user id of the user to message

    Returns
    -------
    bool
        Whether or not messaging the user was successful

    """

    user_id = str(user_id).replace("@u","").replace("@","")
    try:
        go_to_page(browser, "{}{}".format(ONLYFANS_CHAT_URL, user_id))
        logger.debug("successfully messaging user id: {}".format(user_id))
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to message user by id!")

def message_user_by_username(browser, username):
    """
    Message the matching username or user id

    Parameters
    ----------
    username : str
        The username of the user to message

    Returns
    -------
    bool
        Whether or not messaging the user was successful

    """

    logger.debug(f"messaging username: {username}")
    try:
        user = get_user_by_username(browser, username, collection="Active", reattempt=True) # a True value for reattempt has the function skip "All" as a search option
        # backup method aka original method that needs updates / debugging
        if not user: return message_user_by_user_page(browser, username)
        click_user_button(browser, user, text="Message")
        time.sleep(0.5)
        logger.debug(f"successfully messaging username: {username}")
        return True
    except Exception as e:
        error_checker(e)
    raise Exception(f"failed to message user: {username}")    

def message_user_by_user_page(browser, username):
    logger.debug(f"messaging username via page: {username}")
    try:
        logger.warning("TODO: DEBUG THIS")
        logger.debug("BACKUP USER SEARCH")
        logger.debug("BACKUP USER SEARCH")
        logger.debug("BACKUP USER SEARCH")

        go_to_page(browser, username)
        time.sleep(3) # for whatever reason this constantly errors out from load times
        WebDriverWait(browser, 10, poll_frequency=3).until(EC.visibility_of_element_located((By.TAG_NAME, "a")))
        elements = browser.find_elements(By.TAG_NAME, "a")
        ele = [ele for ele in elements if ONLYFANS_CHAT_URL in str(ele.get_attribute("href"))]
        if len(ele) == 0:
            raise Exception("user cannot be messaged - unable to locate id!")
        ele = ele[0]
        ele = ele.get_attribute("href").replace("https://onlyfans.com", "")
        # clicking no longer works? just open href in self.browser
        # logger.debug("clicking send message")
        # ele.click()
        logger.debug(f"user id found: {ele.replace(ONLYFANS_HOME_URL+'/', '')}")
        go_to_page(browser, ele)
        return True
    except Exception as e:
        error_checker(e)
    raise Exception(f"failed to message user by page: {username}")
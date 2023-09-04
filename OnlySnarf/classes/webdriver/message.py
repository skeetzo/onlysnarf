import time
import logging

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import WebDriverException

from .element import find_element_to_click
from .errors import error_checker
from .goto import go_to_home, go_to_page
from .upload import upload_files
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
        logging.info(f"Entering message to {message_object['recipients']}: (${message_object['price']}) {message_object['text']}")
        successful_message_steps = []

        if len(message_object["recipients"]) > 1 or message_object["includes"] or message_object["excludes"]:
            # prepare the message
            # TODO: add ability to select other custom lists of users
            if message_object["includes"]:
                # if not messaging a user directly, all these can be stacked in a single message
                for label in message_object['includes']:
                    if str(label).lower() == "all" or str(label).lower() == "fans": successful_message_steps.append(message_fans(browser))
                    if str(label).lower() == "recent": successful_message_steps.append(message_recent(browser))
                    if str(label).lower() == "favorite": successful_message_steps.append(message_favorites(browser))
                    if str(label).lower() == "renew on": successful_message_steps.append(message_renewers(browser))
                    if str(label).lower() == "renew off": successful_message_steps.append(message_renewers(browser, on=False))
                    if str(label).lower() == "bookmarks": successful_message_steps.append(message_bookmarks(browser))
                    # if str(label).lower() == "random": successful_message_steps.append(message_random(browser))
            if message_object["excludes"]:
                for label in message_object["excluded_recipients"]:
                    if str(label).lower() == "all" or str(label).lower() == "fans": successful_message_steps.append(message_fans(browser, exclude=True))
                    if str(label).lower() == "recent": successful_message_steps.append(message_recent(browser, exclude=True))
                    if str(label).lower() == "favorite": successful_message_steps.append(message_favorites(browser, exclude=True))
                    if str(label).lower() == "renew on": successful_message_steps.append(message_renewers(browser, exclude=True))
                    if str(label).lower() == "renew off": successful_message_steps.append(message_renewers(browser, exclude=True, on=False))
                    if str(label).lower() == "bookmarks": successful_message_steps.append(message_bookmarks(browser, exclude=True))
                    # if str(label).lower() == "random": successful_message_steps.append(message_random(browser, exclude=True))
            # use same page to add additional users to message 
            for username in message_object["recipients"]:
                successful_message_steps.append(add_user_to_message(browser, username))
        else:
            # if none of above or solo messaging, switch to normal user messaging (locates user_id on profile page and opens url link)
            successful_message_steps.append(message_user_by_username(browser, username))

        if not all(successful_message_steps): raise Exception(f"Failed to begin message for {message_object['recipients']}!")

        # actually send the message
        return all([message_text(browser, message_object['text']), message_price(browser, message_object['price']), upload_files(browser, message_object['files']), message_confirm(browser)])
    except Exception as e:
        logging.error(e)
    message_clear(browser)
    logging.error("Message failed to send!")
    return False

# TODO: test all these added behaviors
def message_fans(browser, exclude=False):
    try:
        go_to_page(ONLYFANS_NEW_MESSAGE_URL)
        logging.debug("clicking message recipients: fans")
        find_element_to_click(browser, "b-tabs__nav__text", text="Fans", fuzzyMatch=True, index=1 if exclude else 0).click()
        return True
    except Exception as e:
        logging.warning("unable to message all fans!")
    return False

def message_recent(browser, exclude=False):
    try:
        go_to_page(ONLYFANS_NEW_MESSAGE_URL)
        logging.debug("clicking message recipients: recent")
        find_element_to_click(browser, "b-tabs__nav__text", text="Recent", fuzzyMatch=True, index=1 if exclude else 0).click()

        # TODO: add method for interacting with popup calendar for selecting date for recent subscribers

        return True
    except Exception as e:
        logging.warning("unable to message all recent!")
    return False

def message_following(browser, exclude=False):
    try:
        go_to_page(ONLYFANS_NEW_MESSAGE_URL)
        logging.debug("clicking message recipients: following")
        find_element_to_click(browser, "b-tabs__nav__text", text="Following", fuzzyMatch=True, index=1 if exclude else 0).click()
        return True
    except Exception as e:
        logging.warning("unable to message all following!")
    return False

def message_favorites(browser, exclude=False):
    try:
        go_to_page(ONLYFANS_NEW_MESSAGE_URL)
        logging.debug("clicking message recipients: favorites")
        find_element_to_click(browser, "b-tabs__nav__text", text="Favorites", index=1 if exclude else 0).click()
        return True
    except Exception as e:
        logging.warning("unable to message all favorites!")
    return False

def message_friends(browser, exclude=False):
    try:
        go_to_page(ONLYFANS_NEW_MESSAGE_URL)
        logging.debug("clicking message recipients: friends")
        find_element_to_click(browser, "b-tabs__nav__text", text="Friends", index=1 if exclude else 0).click()
        return True
    except Exception as e:
        logging.warning("unable to message all friends!")
    return False

def message_renewers(browser, exclude=False, on=True):
    try:
        go_to_page(ONLYFANS_NEW_MESSAGE_URL)
        logging.debug(f"clicking message recipients: renew ({on})")
        find_element_to_click(browser, "b-tabs__nav__text", text="Renew On" if on else "Renew Off", index=1 if exclude else 0).click()
        return True
    except Exception as e:
        logging.warning("unable to message all renewals!")
    return False

def message_bookmarks(browser, exclude=False):
    try:
        go_to_page(ONLYFANS_NEW_MESSAGE_URL)
        logging.debug(f"clicking message recipients: bookmarks")
        find_element_to_click(browser, "b-tabs__nav__text", text="Bookmarks", index=1 if exclude else 0).click()
        return True
    except Exception as e:
        logging.warning("unable to message all bookmarks!")
    return False

# def message_random(browser):
#     return message_user_by_username(browser, get_random_user().username)

# TODO: finish and test this functionality of mass messaging
# add username to existing mass message being started
def add_user_to_message(browser, username):
    logging.error("TODO: finish me!")
    pass

######################################################################
######################################################################
######################################################################

def clear_button(browser, retry=False):
    try:
        find_element_to_click(browser, "button", by=By.TAG_NAME, text="Clear").click()
        logging.debug("successfully clicked clear button!")
        return True
    except Exception as e:
        if not retry:
            go_to_home(browser, force=True)
            action = ActionChains(browser)
            action.move_to_element(browser.find_element(By.ID, "new_post_text_input"))
            action.click(on_element=browser.find_element(By.ID, "new_post_text_input"))
            action.perform()
            time.sleep(0.5) # needs to load: TODO: possibly add wait
            return clear_button(browser, retry=True)
        logging.debug("unable to click clear button!")
    return False

def close_icons(browser):
    try:
        elements = browser.find_elements(By.CLASS_NAME, "b-dropzone__preview__delete")
        for element in elements:
            ActionChains(browser).move_to_element(element).click().perform()
            logging.debug("successfully clicked close button!")
    except Exception as e:
        logging.debug("unable to click close icons!")

def clear_text(browser):
    try:
        action = ActionChains(browser)
        action.move_to_element(browser.find_element(By.ID, "new_post_text_input"))
        action.click(on_element=browser.find_element(By.ID, "new_post_text_input"))
        action.double_click()
        action.click_and_hold()
        action.send_keys(Keys.CLEAR)
        action.perform()
        logging.debug("successfully cleared text!")
    except Exception as e:
        logging.error(e)
        logging.warning("unable to clear text!")

## TODO: add check for clearing any text or images already in post field
def message_clear(browser):
    logging.debug("clearing message...")
    successful = clear_button(browser)
    if not successful:
        close_icons(browser)
        clear_text(browser)
    if successful: return True
    logging.warning("failed to clear message!")
    return False

def message_confirm(browser):
    """
    Wait for the message open on the page's Confirm button to be clickable and click it

    Returns
    -------
    bool
        Whether or not the message confirmation was successful

    """

    try:
        logging.debug("waiting for message confirm to be clickable...")
        confirm = WebDriverWait(browser, int(CONFIG["upload_max_duration"]), poll_frequency=3).until(EC.element_to_be_clickable((By.CLASS_NAME, "g-btn.m-rounded.b-chat__btn-submit")))
        logging.debug("message confirm is clickable")
        debug_delay_check()
        # TODO: switch to regular type after extra debugging
        if CONFIG["debug"] and str(CONFIG["debug"]) == "True":
            logging.info('skipping message (debug)')
            message_clear(browser)
        else:
            logging.debug("clicking confirm...")
            confirm.click()
            logging.info('OnlyFans message sent!')
        return True
    except TimeoutException:
        logging.error("Timed out waiting for message confirm!")
    except Exception as e:
        error_checker(e)
        logging.error("Failure to confirm message!")
    message_clear(browser)
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
            logging.error("missing price!")
            return False
        message_price_clear(browser)
        if message_price_enter(browser, price) and message_price_save(browser):
            logging.debug("successfully entered message price!")
            return True
    except Exception as e:
        error_checker(e)
        logging.error("failed to enter message price!")
    return False

# clear any pre-existing message price
def message_price_clear(browser):
    try:
        logging.debug("clearing any preexisting price...")
        # browser.find_element(By.CLASS_NAME, "m-btn-remove").click()
        find_element_to_click(browser, "m-btn-remove").click()
    except Exception as e:
        logging.error(e)

def message_price_enter(browser, price):
    try:
        logging.debug("entering price...")
        browser.find_element(By.CLASS_NAME, "b-make-post__actions__btns").find_elements(By.XPATH, "./child::*")[7].click()
        element = WebDriverWait(browser, 10, poll_frequency=2).until(EC.element_to_be_clickable(browser.find_element(By.ID, "priceInput_1")))
        element.click()
        element.send_keys(str(price))
        logging.debug("entered price!")
        debug_delay_check()
        return True
    except Exception as e:
        logging.debug("failed to enter price!")
        logging.error(e)
    return False

def message_price_save(browser):
    try:
        logging.debug("saving price...")
        find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Save").click()
        logging.debug("saved price!")
        debug_delay_check()
        return True
    except Exception as e:
        logging.debug("failed to save price!")
        logging.error(e)
    return False

def message_text(browser, text=""):
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
        if not text:
            logging.error("missing text for message!")
            return False
        logging.debug("entering text...")
        # clear any preexisting text first
        ActionChains(browser).move_to_element(browser.find_element(By.ID, "new_post_text_input")).double_click().click_and_hold().send_keys(Keys.CLEAR).send_keys(str(text)).perform()
        logging.debug("successfully entered text")
        time.sleep(0.5)
        return True
    except Exception as e:
        error_checker(e)
        logging.error("failure to enter message!")
    return False

######################################################################
######################################################################
######################################################################

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

    if not user_id:
        logging.error("missing user id!")
        return False
    user_id = str(user_id).replace("@u","").replace("@","")
    try:
        go_to_page(browser, "{}{}".format(ONLYFANS_CHAT_URL, user_id))
        logging.debug("successfully messaging user id: {}".format(user_id))
        return True
    except Exception as e:
        error_checker(e)
        logging.error("failed to message user by id!")
    return False

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

    logging.debug(f"username: {username}")
    if not username:
        logging.error("missing username to message!")
        return False
    try:
        go_to_page(browser, username)
        # time.sleep(5) # for whatever reason this constantly errors out from load times
        WebDriverWait(browser, 10, poll_frequency=1).until(EC.visibility_of_element_located((By.TAG_NAME, "a")))
        elements = browser.find_elements(By.TAG_NAME, "a")
        ele = [ele for ele in elements if ONLYFANS_CHAT_URL in str(ele.get_attribute("href"))]
        if len(ele) == 0:
            logging.warning("user cannot be messaged - unable to locate id!")
            return False
        ele = ele[0]
        ele = ele.get_attribute("href").replace("https://onlyfans.com", "")
        # clicking no longer works? just open href in self.browser
        # logging.debug("clicking send message")
        # ele.click()
        logging.debug(f"user id found: {ele.replace(ONLYFANS_HOME_URL+'/', '')}")
        go_to_page(browser, ele)
        logging.debug(f"successfully messaging username: {username}")
        return True
    except Exception as e:
        error_checker(e)
        logging.error("failed to message user")
    return False

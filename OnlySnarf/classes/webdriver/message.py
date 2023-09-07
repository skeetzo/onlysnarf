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
        logging.info(f"Entering message to {','.join(message_object['recipients'])}: (${message_object['price']}) {message_object['text']}")
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
            successful_message_steps.append(message_user_by_username(browser, message_object["recipients"][0]))
        if not all(successful_message_steps): raise Exception(f"failed to begin message for {message_object['recipients']}!")

        # TODO: fix this circular import issue, probably move enter_text somewhere else
        from .post import enter_text
        time.sleep(1)

        # actually send the message
        return all([enter_text(browser, message_object['text']), message_price(browser, message_object['price']), upload_files(browser, message_object['files']), message_confirm(browser)])
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

def close_icons(browser):
    try:
        while len(browser.find_elements(By.CLASS_NAME, "b-dropzone__preview__delete")) > 0:
            for element in browser.find_elements(By.CLASS_NAME, "b-dropzone__preview__delete"):
                ActionChains(browser).move_to_element(element).click().perform()
                logging.debug("successfully clicked close button!")
    except Exception as e:
        logging.debug("unable to click close icons!")

def clear_text(browser):
    try:        
        # BUGS: only backspace is working
        element = WebDriverWait(browser, 60).until(EC.visibility_of_element_located((By.ID, 'new_post_text_input')))
        # TODO: fix this horribly inefficient loop
        for i in range(300):
            element.send_keys(Keys.BACK_SPACE)
        logging.debug("successfully cleared text!")
    # broken method one:
        # print(element.get_attribute("innerHTML"))
        # element.click()
        # element.clear()
    # broken method two:
        # action = ActionChains(browser)
        # action.move_to_element(element)
        # action.click(on_element=element)
        # action.double_click()
        # action.click_and_hold()
        # action.send_keys(Keys.CLEAR)
        # action.perform()
    # broken method 3:
        # # action.send_keys(Keys.CONTROL + "a")
        # action.send_keys(Keys.DELETE)
    except Exception as e:
        logging.error(e)
        logging.warning("unable to clear text!")

## TODO: add check for clearing any text or images already in post field?
def message_clear(browser):
    try:
        clear_text(browser)
        close_icons(browser)
        return True
    except Exception as e:
        logging.error(e)
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
            logging.debug("skipping empty price")
            return True
        message_price_clear(browser)
        message_price_open(browser)
        message_price_enter(browser, price)
        message_price_save(browser)
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
        # logging.error(e)
        pass

def message_price_open(browser, reattempt=False):
    try:
        logging.debug("opening price...")
        for element in browser.find_element(By.CLASS_NAME, "b-make-post__actions__btns").find_elements(By.XPATH, "./child::*"):
            if "icon-price" in str(element.get_attribute("innerHTML")):
                logging.debug("clicking price button...")
                browser.execute_script("arguments[0].click()", element)
                return True
                # BUG: normal methods not working :/
                # ActionChains(browser).move_to_element(element).click().perform()
                # element.click()
                # element.send_keys("\n")
    except Exception as e:
        logging.debug("failed to open price model!")
        if "obscures it" in str(e) and not reattempt:
            error_window_upload(browser)
            return message_price_open(browser, reattempt=True)
        logging.error(e)
    raise Exception("unable to open price model!")

def message_price_enter(browser, price, reattempt=False):
    try:
        logging.debug("entering price...")
        element = WebDriverWait(browser, 10, poll_frequency=2).until(EC.element_to_be_clickable(browser.find_element(By.ID, "priceInput_1")))
        element.click()
        element.send_keys(str(price))
        logging.debug("entered price!")
        debug_delay_check()
        return True
    except Exception as e:
        if "obscures it" in str(e) and not reattempt:
            error_window_upload(browser)
            return message_price_enter(browser, price, reattempt=True)
        logging.debug("failed to enter price!")
        logging.error(e)
    raise Exception("unable to enter price amount!")

def message_price_save(browser):
    try:
        logging.debug("saving price...")
        find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Save").click()
        logging.debug("saved price!")
        debug_delay_check()
        return True
    except Exception as e:
        logging.error(e)
    raise Exception("failed to save price!")

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
        clear_text(browser)
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

    logging.debug(f"messaging username: {username}")
    if not username:
        logging.error("missing username to message!")
        return False
    try:
        user = get_user_by_username(browser, username, collection="Active")
        if not user: 
            if message_user_by_user_page(browser, username): return True
            raise Exception("unable to message missing user!")
        click_user_button(browser, user, text="Message")
        logging.debug(f"successfully messaging username: {username}")
        return True

        # changed in favor of similar discount method 
        # open user page and click on message button there
            # go_to_page(browser, username)
            # time.sleep(5) # for whatever reason this constantly errors out from load times
            # WebDriverWait(browser, 10, poll_frequency=1).until(EC.visibility_of_element_located((By.TAG_NAME, "a")))
            # elements = browser.find_elements(By.TAG_NAME, "a")
            # ele = [ele for ele in elements if ONLYFANS_CHAT_URL in str(ele.get_attribute("href"))]
            # if len(ele) == 0:
            #     logging.warning("user cannot be messaged - unable to locate id!")
            #     return False
            # ele = ele[0]
            # ele = ele.get_attribute("href").replace("https://onlyfans.com", "")
            # # clicking no longer works? just open href in self.browser
            # # logging.debug("clicking send message")
            # # ele.click()
            # logging.debug(f"user id found: {ele.replace(ONLYFANS_HOME_URL+'/', '')}")
            # go_to_page(browser, ele)
    except Exception as e:
        error_checker(e)
        logging.error(f"failed to message user: {username}")
    return False

def message_user_by_user_page(browser, username):
    logging.debug(f"messaging username via page: {username}")
    if not username:
        logging.error("missing username to message!")
        return False
    try:
        logging.debug("BACKUP USER SEARCH")
        logging.debug("BACKUP USER SEARCH")
        logging.debug("BACKUP USER SEARCH")

        go_to_home(browser, force=True)
        go_to_page(browser, username)
        time.sleep(3) # for whatever reason this constantly errors out from load times
        WebDriverWait(browser, 10, poll_frequency=1).until(EC.visibility_of_element_located((By.TAG_NAME, "a")))
        elements = browser.find_elements(By.TAG_NAME, "a")
        ele = [ele for ele in elements if ONLYFANS_CHAT_URL in str(ele.get_attribute("href"))]


        logging.debug()



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
        return True
    except Exception as e:
        error_checker(e)
        logging.error(f"failed to message user by page: {username}")
    return False
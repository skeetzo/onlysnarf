# TODO: clean up this huge file and reorganize it properly to mesh with User class

import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import WebDriverException

from .element import find_element_to_click
from .driver import go_to_home
from ..util.settings import Settings
from ..util.urls import ONLYFANS_CHAT_URL

####################
##### Messages #####
####################


## TODO: I don't think i want to have the code here for user -> send message
# because it would make it difficult to run per user and save information directly back to each user
# maybe just take a break and come back and rework the user class into this new webdriver class more cleanly


def message(browser, message_object={}):

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

    Settings.print("Entering message: (${}) {}".format(message_object["price"], message_object["text"]))
    try:
        for recipient in message_object['recipients']:
        message_username(browser, recipient)
        if all([message_text(browser, message_object["text"]), message_price(browser, message_object["price"]), upload_files(browser, message_object["files"])]):
            return message_confirm(browser)
    except Exception as e:
        Settings.dev_print(e)
    Settings.err_print("Message failed to send!")
    return False

def message_username(browser, username, user_id=None):
    """
    Start a message to the username (or group of users) or user_id.

    Parameters
    ----------
    username : str
        The username of the user to message
    user_id : str
        The user id of the user to message

    Returns
    -------
    bool
        Whether or not the message was successful

    """

    if not username and not user_id:
        Settings.err_print("missing user to message!")
        return False
    try:
        go_to_home(browser, force=True)
        Settings.dev_print("attempting to message {}...".format(username))
        # if the username is a key string it will behave differently
        if str(username).lower() == "all": return message_all(browser)
        elif str(username).lower() == "recent": return message_recent(browser)
        elif str(username).lower() == "favorite": return message_favorite(browser)
        elif str(username).lower() == "renew on": return message_renewers(browser)
        elif str(username).lower() == "random": return message_random(browser)
        else: return message_user_by_username(browser, username, user_id=user_id)
        # if successful: Settings.dev_print("started message for {}".format(username))
        # else: Settings.warn_print("failed to start message for {}!".format(username))
        # return successful
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failure to message - {}".format(username))
    return False
 
# TODO: add these behaviors
def message_all(browser):
    pass

def message_recent(browser):
        
        # successful = False
        # if type__ != None:
        #     driver.go_to_page(ONLYFANS_NEW_MESSAGE_URL)
        #     Settings.dev_print("clicking message type: {}".format(username))
        #     driver.find_element_to_click(type__).click()
        #     successful = True
    pass

def message_favorite(browser):
    pass

def message_renewers(browser):
    pass

def message_random(browser):
    from ..classes.user import User
    username = User.get_random_user().username

######################################################################
######################################################################
######################################################################

def close_icons(browser):
    try:
        #icon-close
        elements = browser.find_elements(By.TAG_NAME, "use")
        for element in [elem for elem in elements if '#icon-close' in str(elem.get_attribute('href'))]:
            ActionChains(browser).move_to_element(element).click().perform()
    except Exception as e:
        Settings.err_print(e)
        Settings.dev_print("unable to click: #icon-close")

def clear_text(browser):
    try:
        ActionChains(browser).move_to_element(browser.find_element(By.ID, "new_post_text_input")).double_click().click_and_hold().send_keys(Keys.CLEAR).perform()
    except Exception as e:
        Settings.err_print(e)
        Settings.dev_print("unable to clear text!")

## TODO
# add check for clearing any text or images already in post field
def message_clear(browser):
    try:
        Settings.dev_print("clearing message...")
        clearButton = [ele for ele in browser.find_elements(By.TAG_NAME, "button") if "Clear" in ele.get_attribute("innerHTML") and ele.is_enabled()]
        if len(clearButton) > 0:
            Settings.dev_print("clicking clear button...")
            clearButton[0].click()
        else:
            Settings.dev_print("refreshing page and clearing text...")
            go_to_home(browser, force=True)
            clear_text(browser)
            close_icons(browser)
        Settings.dev_print("successfully cleared message!")
        return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.warn_print("failed to clear message!")
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
        Settings.dev_print("waiting for message confirm to be clickable...")
        confirm = WebDriverWait(browser, int(Settings.get_upload_max_duration()), poll_frequency=3).until(EC.element_to_be_clickable((By.CLASS_NAME, "g-btn.m-rounded.b-chat__btn-submit")))
        Settings.dev_print("message confirm is clickable")
        Settings.debug_delay_check()
        # TODO: switch to regular type after extra debugging
        if str(Settings.is_debug()) == "True":
            Settings.print('skipping message (debug)')
            message_clear(browser)
            return True
        Settings.dev_print("clicking confirm...")
        confirm.click()
        Settings.print('OnlyFans message sent!')
        return True
    except TimeoutException:
        Settings.warn_print("timed out waiting for message confirm!")
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failure to confirm message!")
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
            Settings.err_print("missing price!")
            return False
        # clear any pre-existing message
        message_price_clear(browser)
        successful = []
        successful.append(message_price_enter(browser, price))
        successful.append(message_price_save(browser))
        if all(successful):
            Settings.dev_print("successfully entered message price!")
            return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failed to enter message price!")
    return False

def message_price_clear(browser):
    try:
        Settings.dev_print("clearing any preexisting price...")
        browser.find_element(By.CLASS_NAME, "m-btn-remove").click()
    except Exception as e:
        Settings.dev_print(e)

def message_price_enter(browser, price):
    try:
        Settings.dev_print("entering price...")
        browser.find_element(By.CLASS_NAME, "b-make-post__actions__btns").find_elements(By.XPATH, "./child::*")[7].click()
        element = WebDriverWait(browser, 10, poll_frequency=2).until(EC.element_to_be_clickable(browser.find_element(By.ID, "priceInput_1")))
        element.click()
        element.send_keys(str(price))
        Settings.dev_print("entered price!")
        Settings.debug_delay_check()
        return True
    except Exception as e:
        Settings.dev_print("failed to enter price!")
        Settings.err_print(e)
    return False

def message_price_save(browser):
    try:
        Settings.dev_print("saving price...")
        find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Save").click()    
        Settings.dev_print("saved price!")
        Settings.debug_delay_check()
        return True
    except Exception as e:
        Settings.dev_print("failed to save price!")
        Settings.err_print(e)
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
            Settings.err_print("missing text for message!")
            return False
        Settings.dev_print("entering text...")
        # clear any preexisting text first
        ActionChains(browser).move_to_element(browser.find_element(By.ID, "new_post_text_input")).double_click().click_and_hold().send_keys(Keys.CLEAR).send_keys(str(text)).perform()
        Settings.dev_print("successfully entered text")
        time.sleep(0.5)
        return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failure to enter message")
    return False

######################################################################
######################################################################
######################################################################

def message_user_by_id(browser, user_id=""):
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
        Settings.err_print("missing user id!")
        return False
    user_id = str(user_id).replace("@u","").replace("@","")
    try:
        go_to_page(browser, "{}{}".format(ONLYFANS_CHAT_URL, user_id))
        Settings.dev_print("successfully messaging user id: {}".format(user_id))
        return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failed to message user by id!")
    return False

def message_user_by_username(browser, username, user_id=None):
    """
    Message the matching username or user id

    Parameters
    ----------
    username : str
        The username of the user to message
    user_id : str
        The user id of the user to message

    Returns
    -------
    bool
        Whether or not messaging the user was successful

    """

    Settings.dev_print("username: {} : {}: user_id".format(username, user_id))
    if user_id: return message_user_by_id(user_id=user_id)
    if not username:
        Settings.err_print("missing username to message!")
        return False
    try:
        go_to_page(browser, username)
        # time.sleep(5) # for whatever reason this constantly errors out from load times
        WebDriverWait(browser, 10, poll_frequency=1).until(EC.visibility_of_element_located((By.TAG_NAME, "a")))
        elements = browser.find_elements(By.TAG_NAME, "a")
        ele = [ele for ele in elements if ONLYFANS_CHAT_URL in str(ele.get_attribute("href"))]
        if len(ele) == 0:
            Settings.warn_print("user cannot be messaged - unable to locate id!")
            return False
        ele = ele[0]
        ele = ele.get_attribute("href").replace("https://onlyfans.com", "")
        # clicking no longer works? just open href in self.browser
        # Settings.dev_print("clicking send message")
        # ele.click()
        Settings.maybe_print("user id found: {}".format(ele.replace(ONLYFANS_HOME_URL2, "")))
        go_to_page(browser, ele)
        Settings.dev_print("successfully messaging username: {}".format(username))
        return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failed to message user")
    return False

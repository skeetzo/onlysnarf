# TODO: clean up this huge file and reorganize it properly to mesh with User class

import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import WebDriverException

from .element import find_element_to_click
from .driver import Driver
from .goto import go_to_home, go_to_page
from .upload import upload_files
from ..classes.user import User
from ..util.settings import Settings
from ..util.urls import ONLYFANS_CHAT_URL, ONLYFANS_NEW_MESSAGE_URL

####################
##### Messages #####
####################

def message(message_object={}):

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

    browser = Driver.get_browser()
    try:
        Settings.print(f"Entering message to {message_object["recipients"]}: (${message_object["price"]}) {message_object["text"]}")
        successful = []
        if message_object["includes"] or message_object["excludes"]:
            # if not messaging a user directly, all these can be stacked in a single message
            for label in message_object['includes']:
                if str(label).lower() == "all" or str(label).lower() == "fans": successful.append(message_fans(browser))
                if str(label).lower() == "recent": successful.append(message_recent(browser))
                if str(label).lower() == "favorite": successful.append(message_favorites(browser))
                if str(label).lower() == "renew on": successful.append(message_renewers(browser))
                if str(label).lower() == "renew off": successful.append(message_renewers(browser, on=False))
                if str(label).lower() == "bookmarks": successful.append(message_bookmarks(browser))
                if str(label).lower() == "random": successful.append(message_random(browser))
            for label in message_object["excluded_recipients"]:
                if str(label).lower() == "all" or str(label).lower() == "fans": successful.append(message_fans(browser, exclude=True))
                if str(label).lower() == "recent": successful.append(message_recent(browser, exclude=True))
                if str(label).lower() == "favorite": successful.append(message_favorites(browser, exclude=True))
                if str(label).lower() == "renew on": successful.append(message_renewers(browser, exclude=True))
                if str(label).lower() == "renew off": successful.append(message_renewers(browser, exclude=True, on=False))
                if str(label).lower() == "bookmarks": successful.append(message_bookmarks(browser, exclude=True))
                if str(label).lower() == "random": successful.append(message_random(browser, exclude=True))
            # use same page to add additional users to message 
            for username in message_object["recipients"]:
                successful.append(add_user_to_message(browser, username))
        else:
            # if none of the above have been run, switch to normal user messaging (locates user_id on profile page and opens url link)
            successful.append(message_user_by_username(browser, username))
        if not all(successful): raise Exception(f"Failed to message {message_object["recipients"]}!")
        successful.append(all([message_text(browser, message_object["text"]), message_price(browser, message_object["price"]), upload_files(browser, message_object["files"]), message_confirm(browser)]))
        return all(successful)
    except Exception as e:
        Settings.err_print(e)
    message_clear(browser)
    Settings.err_print("Message failed to send!")
    return False

# TODO: test all these added behaviors
def message_fans(browser, exclude=False):
    try:
        go_to_page(ONLYFANS_NEW_MESSAGE_URL)
        Settings.dev_print("clicking message recipients: fans")
        find_element_to_click(browser, "b-tabs__nav__text", text="Fans", fuzzyMatch=True, index=1 if exclude else 0).click()
        return True
    except Exception as e:
        Setings.dev_print("unable to message all fans!")
    return False

def message_recent(browser, exclude=False):
    try:
        go_to_page(ONLYFANS_NEW_MESSAGE_URL)
        Settings.dev_print("clicking message recipients: recent")
        find_element_to_click(browser, "b-tabs__nav__text", text="Recent", fuzzyMatch=True, index=1 if exclude else 0).click()

        # TODO: add method for interacting with popup calendar for selecting date for recent subscribers

        return True
    except Exception as e:
        Setings.dev_print("unable to message all recent!")
    return False

def message_following(browser, exclude=False):
    try:
        go_to_page(ONLYFANS_NEW_MESSAGE_URL)
        Settings.dev_print("clicking message recipients: following")
        find_element_to_click(browser, "b-tabs__nav__text", text="Following", fuzzyMatch=True, index=1 if exclude else 0).click()
        return True
    except Exception as e:
        Setings.dev_print("unable to message all following!")
    return False

def message_favorites(browser, exclude=False):
    try:
        go_to_page(ONLYFANS_NEW_MESSAGE_URL)
        Settings.dev_print("clicking message recipients: favorites")
        find_element_to_click(browser, "b-tabs__nav__text", text="Favorites", index=1 if exclude else 0).click()
        return True
    except Exception as e:
        Setings.dev_print("unable to message all favorites!")
    return False

def message_friends(browser, exclude=False):
    try:
        go_to_page(ONLYFANS_NEW_MESSAGE_URL)
        Settings.dev_print("clicking message recipients: friends")
        find_element_to_click(browser, "b-tabs__nav__text", text="Friends", index=1 if exclude else 0).click()
        return True
    except Exception as e:
        Setings.dev_print("unable to message all friends!")
    return False

def message_renewers(browser, exclude=False, on=True):
    try:
        go_to_page(ONLYFANS_NEW_MESSAGE_URL)
        Settings.dev_print(f"clicking message recipients: renew ({on})")
        find_element_to_click(browser, "b-tabs__nav__text", text="Renew On" if on else "Renew Off", index=1 if exclude else 0).click()
        return True
    except Exception as e:
        Setings.dev_print("unable to message all renewals!")
    return False

def message_bookmarks(browser, exclude=False):
    try:
        go_to_page(ONLYFANS_NEW_MESSAGE_URL)
        Settings.dev_print(f"clicking message recipients: bookmarks")
        find_element_to_click(browser, "b-tabs__nav__text", text="Bookmarks", index=1 if exclude else 0).click()
        return True
    except Exception as e:
        Setings.dev_print("unable to message all bookmarks!")
    return False

def message_random(browser):
    username = User.get_random_user().username
    return message_user_by_username(browser, username)

# TODO: finish and test this functionality of mass messaging
# add username to existing mass message being started
def add_user_to_message(browser, username):
    pass

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
            return message_clear(browser)
        Settings.dev_print("clicking confirm...")
        confirm.click()
        Settings.print('OnlyFans message sent!')
        return True
    except TimeoutException:
        Settings.err_print("Timed out waiting for message confirm!")
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("Failure to confirm message!")
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
        message_price_clear(browser)
        if message_price_enter(browser, price) and message_price_save(browser):
            Settings.dev_print("successfully entered message price!")
            return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failed to enter message price!")
    return False

# clear any pre-existing message price
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

    Settings.dev_print(f"username: {username}")
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
        Settings.maybe_print(f"user id found: {ele.replace(ONLYFANS_HOME_URL2, "")}")
        go_to_page(browser, ele)
        Settings.dev_print(f"successfully messaging username: {username}")
        return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failed to message user")
    return False

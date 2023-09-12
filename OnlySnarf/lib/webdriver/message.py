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
        logging.info(f"Entering message to {','.join(message_object['recipients'])}: (${message_object['price']}) {message_object['text']}\nIncludes: {','.join(message_object['includes'])}\nExcludes: {','.join(message_object['excludes'])}")


        # prepare the message
        if len(message_object["recipients"]) > 1 or message_object["includes"] or message_object["excludes"]:
            clear_lists(browser, includes=message_object["includes"], excludes=message_object["excludes"])

            # if not messaging a user directly, all these can be stacked in a single message
            message_list(browser, includes=message_object["includes"], excludes=message_object["excludes"])
            # use same page to add additional users to message 
            for username in message_object["recipients"]:
                add_user_to_message(browser, username)
        else:
            # if none of above or solo messaging, switch to normal user messaging (locates user_id on profile page and opens url link)
            # doesn't need to clear lists when opening a new tab to search for the username then send them a message
            message_user_by_username(browser, message_object["recipients"][0])

        # TODO: fix this circular import issue, probably move enter_text somewhere else
        from .post import enter_text
        time.sleep(1)

        enter_text(browser, message_object['text'])
        message_price(browser, message_object['price'])
        upload_files(browser, message_object['files'])
        message_confirm(browser)

        if CONFIG["debug"]:
            clear_lists(browser, includes=message_object["includes"], excludes=message_object["excludes"])
            message_clear(browser)
            browser.refresh()
        return True
    except Exception as e:
        error_checker(e)
    message_clear(browser)
    clear_lists(browser, includes=message_object["includes"], excludes=message_object["excludes"])
    browser.refresh() # clears entered usernames
    raise Exception("failed to send message!")

# TODO: when clearing lists, just open the list menu for both and deselect every option available
# TODO: when clicking lists, do multiple labels at the same time while having the list selection open

# searches for a single '#icon-done'
def check_clear_lists(browser, reattempt=False):
    try:
        for element in browser.find_elements(By.TAG_NAME, "use"):
            if '#icon-done' in str(element.get_attribute('href')) and element.is_displayed():
                return True
    except Exception as e:
        if "stale element" in str(e) and not reattempt:
            logging.debug('reattempting message_list...')
            if not reattempt: return check_clear_lists(browser, reattempt=True)
    logging.debug("no lists to clear!")
    return False

def clear_lists(browser, includes=[], excludes=[]):
    if not check_clear_lists(browser): return
    logging.debug("clearing lists...")
    try:
        message_list(browser, includes=includes, excludes=excludes, unclick=True)
        logging.debug("successfully cleared lists!")
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("unable to clear user lists!")

# click existing button
# def method_one(browser, collection, include=True, unclick=False, reattempt=False):
#     logging.debug("METHOD ONE")
#     try:
#         element = find_element_to_click(browser, "b-tabs__nav__text", text=collection, fuzzyMatch=True, index=0 if include else 1)
#         if unclick:
#             try:
#                 parent_element = element.find_element(By.XPATH, '..')
#                 icon_done = parent_element.find_element(By.TAG_NAME, "use")
#                 if not icon_done: return True
#             except Exception as e:
#                 print(e)
#                 if not reattempt: return method_one(browser, collection, include=include, unclick=unclick, reattempt=True)
#                 return True
#             logging.debug(f"unclicking message recipients: {collection}")
#         else:
#             logging.debug(f"clicking message recipients: {collection}")
#         ActionChains(browser).move_to_element(element).click().perform()
#         return True
#     except Exception as e:
#         error_checker(e)
#     return False

# click 1st or 2nd 'View All'
def click_view_all_lists(browser, include=True):
    try:
        elements = browser.find_elements(By.CLASS_NAME, "b-content-filter__group-btns")
        element = None
        if include:
            logging.debug("clicking view all 1...")
            element = elements[0]
        elif not include and len(elements) > 1:
            logging.debug("clicking view all 2...")
            element = elements[1] 
        ActionChains(browser).move_to_element(element).click().perform()
        time.sleep(1)
        logging.debug("clicked view all button")
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("unable to click view all lists!")

# click existing list available
def click_collection_button(browser, collection, unclick=False, reattempt=False):
    logging.debug("METHOD TWO")
    # elements = browser.find_elements(By.CLASS_NAME, "b-rows-lists__item__name")
    try:

        # b-rows-lists__item__label m-collection-item b-input-radio__container
        for element in browser.find_elements(By.CLASS_NAME, "b-rows-lists__item__label"):
            if str(collection).lower().strip() in str(element.get_attribute("innerHTML")).lower().strip():
                if unclick:
                    try:

                        checkbox = element.find_element(By.CLASS_NAME, "b-input-radio")
                        if not checkbox.is_selected():
                            logging.debug(f"not unclicking not clicked element: {collection}")
                            return True

                        # parent_element = element.find_element(By.XPATH, '..')
                        # icon_done = element.find_element(By.TAG_NAME, "use")
                        # if not icon_done: continue
                    except Exception as e:
                        print(e)
                        continue
                    logging.debug("unclicking on list element...")
                    ActionChains(browser).move_to_element(element).click(on_element=element).perform()
                    # find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Done").click()
                else:
                    logging.debug("clicking on list element...")
                    ActionChains(browser).move_to_element(element).click(on_element=element).perform()
                    # find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Done").click()
                return True
    except Exception as e:
        if "stale element" in str(e) and not reattempt:
            logging.debug("reattempting method two (stale element)...")
            return click_collection_button(browser, collection, unclick=unclick, reattempt=True)
        else:
            error_checker(e)
    return False

# search for list
def search_for_collection(browser, collection, unclick=False):
    logging.debug("METHOD THREE")
    elements = browser.find_elements(By.TAG_NAME, "use")
    element = [elem for elem in elements if '#icon-search' in str(elem.get_attribute('href'))][0]
    ActionChains(browser).move_to_element(element).click(on_element=element).click().send_keys(collection).perform()
    return click_collection_button(browser, collection, unclick=unclick)



# TODO: update the message process to match the following backup process of opening the lists up and scrolling for it or typing into the list's search function and then clicking it there
# if one of the below fails, click and open the list of "lists to send to" via the "view all" button
# same for exlude process
# scroll through lists until matching name of list is found and click on it there

# Fans is synonymous with All
# def message_list(browser, collection="Fans", include=True, unclick=False):
def message_list(browser, includes=[], excludes=[], unclick=False):
    go_to_page(browser, ONLYFANS_NEW_MESSAGE_URL)

    def attempt_list(collections, include=True):
        click_view_all_lists(browser, include=include)
        for collection in collections:
            if collection.lower() == "all":
                collection = "Fans"
            elif collection.lower() == "recent" and include:
                return message_recent(browser, exclude=False)

            successful = click_collection_button(browser, collection, unclick=unclick)
            if not successful:
                successful = search_for_collection(browser, collection, unclick=unclick)
            if successful: continue
            raise Exception(f"unable to click list: {collection}")

        find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Done").click()

    if len(includes) > 0:
        attempt_list(includes, include=True)

    if len(excludes) > 0:
        attempt_list(excludes, include=False)

# TODO: ADD SCHEDULE BEHAVIOR HERE
def message_recent(browser, exclude=False, unclick=False):
    try:
        go_to_page(browser, ONLYFANS_NEW_MESSAGE_URL)
        logging.debug("clicking message recipients: recent")
        element = find_element_to_click(browser, "b-tabs__nav__text", text="Recent", fuzzyMatch=True)

        if unclick:
            try:
                icon_done = element.find_element(By.TAG_NAME, "use")
                if not icon_done: return True
            except Exception as e:
                print(e)
                return False
            logging.debug("unclicking on list element...")
            ActionChains(browser).move_to_element(element).click(on_element=element).perform()

            # find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Done").click()
        else:
            # TODO: add method for interacting with popup calendar for selecting date for recent subscribers
            logging.error("TODO: FINISH ME")




        return True

    except Exception as e:
        error_checker(e)
    raise Exception("unable to message all recent!")

# add username to existing mass message being started
def add_user_to_message(browser, username):
    try:
        logging.debug(f"adding user to message: {username}")
        element = browser.find_element(By.CLASS_NAME, "b-search-users-form__input")
        ActionChains(browser).move_to_element(element).click(on_element=element).double_click().click_and_hold().send_keys(Keys.CLEAR).send_keys(str(username)).perform()
        # time.sleep(1)
        WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "b-search-users-form__input")))
        # elements = browser.find_elements(By.CLASS_NAME, "b-available-users__item")
        elements = browser.find_elements(By.CLASS_NAME, "b-available-users__item")
        if len(elements) == 0:
            raise Exception(f"unable to add {username} to message!")
        for element in elements:
            element.click()
        return True
    except Exception as e:
        error_checker(e)
    raise Exception(f"unable to add {username} to message!")


































































































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
        element = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, 'new_post_text_input')))
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
        user = get_user_by_username(browser, username, collection="Active", reattempt=True) # a True value for reattempt has the function skip "All" as a search option
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
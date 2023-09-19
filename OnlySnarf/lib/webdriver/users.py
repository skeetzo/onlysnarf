import os
import re
import time
import random
import logging
logger = logging.getLogger(__name__)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# from . import scroll_to_bottom
from .element import find_element_to_click
from .errors import error_checker
from .goto import go_to_home, go_to_page
from .. import CONFIG, debug_delay_check, print_same_line
from .. import ONLYFANS_HOME_URL, ONLYFANS_FANS_URL, ONLYFANS_FOLLOWING_URL, ONLYFANS_FRIENDS_URL, ONLYFANS_RENEW_ON_URL, ONLYFANS_RENEW_OFF_URL, \
    ONLYFANS_RECENT_URL, ONLYFANS_TAGGED_URL, ONLYFANS_MUTED_URL, ONLYFANS_RESTRICTED_URL, ONLYFANS_BLOCKED_URL

#################
##### Users #####
#################

def get_current_username(browser):
    """
    Gets the username of the logged in user.

    Returns
    -------
    str
        The username of the logged in user

    """

    try:
        logger.debug("searching for active username...")
        go_to_home(browser)
        eles = [ele for ele in browser.find_elements(By.TAG_NAME, "a") if "@" in str(ele.get_attribute("innerHTML")) and "onlyfans" not in str(ele.get_attribute("innerHTML"))]
        if CONFIG["debug"]:
            for ele in eles:
                logger.debug("{} - {}".format(ele.get_attribute("innerHTML"), ele.get_attribute("href")))
        if len(eles) == 0:
            logger.error("failed to find username!")
        else:
            username = str(eles[0].get_attribute("href")).replace(ONLYFANS_HOME_URL+"/", "")
            logger.debug("successfully found active username: {}".format(username))
            return username
    except Exception as e:
        error_checker(e)
    raise Exception("failed to find active username!")

def get_userid_by_username(browser, username):
    """
    Get the user id of the user by username.

    Parameters
    ----------
    username : str
        The username to find the id of

    Returns
    -------
    str
        The user id of the located user

    """

    try:
        go_to_page(browser, username, force=True)
        elements = browser.find_elements(By.TAG_NAME, "a")
        user_id = [ele.get_attribute("href") for ele in elements if "/my/chats/chat/" in str(ele.get_attribute("href"))]
        if len(user_id) == 0: 
            logger.warning(f"failed to find user id for {username}!")
            return None
        user_id = user_id[0]
        user_id = user_id.replace("https://onlyfans.com/my/chats/chat/", "")
        logger.debug(f"successfully found user id: {user_id}")
        return user_id
    except Exception as e:
        error_checker(e)
    raise Exception(f"failed to find user id for username: {username}")

def get_user_element_at_page(browser, username, page, reattempt=False):
    if page == ONLYFANS_FOLLOWING_URL:
        class_name = "subscriptions"
    elif page == ONLYFANS_FANS_URL:
        class_name = "fans"
    try:
        SLEEP_WAIT = 1
        BREAK_COUNT = 0
        count = 0
        while True:
            elements = browser.find_elements(By.CLASS_NAME, f"m-{class_name}")
            if len(elements) == int(count) and BREAK_COUNT > 3:
                break
            elif len(elements) == 0 and count <= 2 and BREAK_COUNT > 0:
                break
            elif len(elements) == int(count):
                SLEEP_WAIT += 1
                BREAK_COUNT += 1
            elements = browser.find_elements(By.CLASS_NAME, "g-user-username")
            for ele in elements:
                # logger.debug(f"{str(username).strip().replace('@','')} == {str(ele.get_attribute('innerHTML')).strip().replace('@','')}")
                if str(username).strip().replace("@","") == str(ele.get_attribute("innerHTML")).strip().replace("@",""):
                    browser.execute_script("arguments[0].scrollIntoView();", ele)
                    logger.info("")
                    logger.debug("successfully found user: {}".format(username))
                    # TODO: figure out how to combine xpath statements?
                    # return parent element housing user info
                    return ele.find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..')
            count = len(elements)
            print_same_line(f"({count}) scrolling...")
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SLEEP_WAIT)
    except Exception as e:
        if "stale element reference" in str(e).lower() and not reattempt:
            return get_user_element_at_page(browser, username, page, reattempt=True)
        error_checker(e)
    raise Exception(f"failed to find {username} at {page}!")

def get_users_at_page(browser, page, collection="Active"):
    if page == ONLYFANS_FOLLOWING_URL:
        class_name = "subscriptions"
    elif page == ONLYFANS_FANS_URL:
        class_name = "fans"
    try:
        go_to_page(browser, os.path.join(page, collection.lower()), force=True)
        find_element_to_click(browser, "b-tabs__nav__text", text=collection, fuzzyMatch=True).click()
        # scroll until elements stop spawning
        SLEEP_WAIT = 1
        BREAK_COUNT = 0
        count = 0

        # logger.StreamHandler.terminator = ""

        while True:
            elements = browser.find_elements(By.CLASS_NAME, f"m-{class_name}")
            if len(elements) == int(count) and BREAK_COUNT > 3:
                break
            elif len(elements) == 0 and count <= 2 and BREAK_COUNT > 0:
                break
            elif len(elements) == int(count):
                SLEEP_WAIT += 1
                BREAK_COUNT += 1
            count = len(elements)
            print_same_line(f"({count}) scrolling...")
            # logger.info(f"({count}) scrolling...")
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SLEEP_WAIT)
        logger.info("")

        # logger.StreamHandler.terminator = "\n"

        users = []
        logger.debug(f"searching {class_name}...")
        elements = browser.find_elements(By.CLASS_NAME, f"m-{class_name}")
        for ele in elements:
            username = ele.find_element(By.CLASS_NAME, "g-user-username").get_attribute("innerHTML").strip()
            name = ele.find_element(By.CLASS_NAME, "g-user-name").get_attribute("innerHTML")
            name = re.sub("<!-*>", "", name)
            name = re.sub("<.*\">", "", name)
            name = re.sub("</.*>", "", name).strip()
            users.append({"name":name, "username":username.replace("@",""), "isFan":True if class_name=="fans" else False, "isFollower":True if class_name=="subscriptions" else False})
            logger.debug(users[-1])
        logger.debug(f"found {len(users)} {class_name}")
        logger.debug(f"successfully found {class_name}!")
        return users
    except Exception as e:
        error_checker(e)
    raise Exception(f"failed to find {class_name}!")

# not accurate; only useful for tests
def get_random_fan_username(browser, page=ONLYFANS_FANS_URL, collection="Active"):
    if page == ONLYFANS_FOLLOWING_URL:
        class_name = "subscriptions"
    elif page == ONLYFANS_FANS_URL:
        class_name = "fans"
    try:
        go_to_page(browser, os.path.join(ONLYFANS_FANS_URL, collection.lower()), force=True)
        find_element_to_click(browser, "b-tabs__nav__text", text=collection, fuzzyMatch=True).click()
        # scroll until elements stop spawning
        SLEEP_WAIT = 1
        BREAK_COUNT = 0
        count = 0
        while True:
            elements = browser.find_elements(By.CLASS_NAME, f"m-{class_name}")
            if len(elements) == int(count) and BREAK_COUNT > 3:
                break
            elif len(elements) == 0 and count <= 2 and BREAK_COUNT > 0:
                break
            elif len(elements) == int(count):
                SLEEP_WAIT += 1
                BREAK_COUNT += 1
            elif len(elements) > 2:
                break
            count = len(elements)
            print_same_line(f"({count}) scrolling...")
            # logger.info(f"({count}) scrolling...")
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SLEEP_WAIT)
        logger.info("")
        users = []
        logger.debug(f"searching users...")
        elements = browser.find_elements(By.CLASS_NAME, f"m-{class_name}")
        for ele in elements:
            random_element = random.choice(elements)
            username = random_element.find_element(By.CLASS_NAME, "g-user-username").get_attribute("innerHTML").strip()
            name = random_element.find_element(By.CLASS_NAME, "g-user-name").get_attribute("innerHTML")
            name = re.sub("<!-*>", "", name)
            name = re.sub("<.*\">", "", name)
            name = re.sub("</.*>", "", name).strip()
            logger.debug(f"found: {username}")
            logger.debug(f"successfully found random user!")
            return username.replace("@","")
    except Exception as e:
        error_checker(e)
        print(e)
    raise Exception(f"failed to find random user!")


# TODO: update to interact with other fan/follower types ala recent, favorite, etc
def get_users_by_type(browser, isFan=True, isFollower=False):
    users = []
    if isFan:
        users.extend(get_users_at_page(browser, ONLYFANS_FANS_URL))
    if isFollower:
        users.extend(get_users_at_page(browser, ONLYFANS_FOLLOWING_URL))
    return users

# TODO: change collection into enum stuff
def get_user_by_username(browser, username, reattempt=False, collection="All"):
    logger.debug(f"searching for user by username: {username}")
    if not username: return None
    try:
        search_for_username(browser, username, collection=collection)
        user = get_user_element_at_page(browser, username, ONLYFANS_FANS_URL)
        if user: return user
    except Exception as e:
        if not reattempt:
            logger.warning(e)
            return get_user_by_username(browser, username, reattempt=True)
        error_checker(e)
    raise Exception("failed to get user by username!")

def search_for_username(browser, username, collection="All"):
    try:
        logger.debug(f"searching for {username} by opening url...")
        go_to_page(browser, os.path.join(ONLYFANS_FANS_URL, "" if collection == "All" else collection.lower(), f"?search={username}"))
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to search for username!")

def get_user_from_elements(browser, username, reattempt=False):
    try:
        # WebDriverWait(browser, 10, poll_frequency=1).until(EC.visibility_of_element_located((By.CLASS_NAME, "g-user-username")))
        elements = browser.find_elements(By.CLASS_NAME, "g-user-username")
        for ele in elements:
            # logger.debug(f"{str(username).strip().replace('@','')} == {str(ele.get_attribute('innerHTML')).strip().replace('@','')}")
            if str(username).strip().replace("@","") == str(ele.get_attribute("innerHTML")).strip().replace("@",""):
                browser.execute_script("arguments[0].scrollIntoView();", ele)
                logger.debug("successfully found user: {}".format(username))
                # TODO: figure out how to combine xpath statements?
                # return parent element housing user info
                return ele.find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..')
    except Exception as e:
        error_checker(e)
    if not reattempt:
        scroll_to_bottom(browser)
        return get_user_from_elements(browser, username, reattempt=True)
    raise Exception(f"failed to get user from elements: '{username}'")

def click_user_button(browser, user_element, text="Message", reattempt=False):
    if not user_element: raise Exception("missing user element!")
    button = None
    try:
        logger.debug(f"clicking {text} btn...")
        button = find_element_to_click(user_element, "b-tabs__nav__text", text=text)
        browser.execute_script("return arguments[0].scrollIntoView(0, document.documentElement.scrollHeight-10);", button)
        # scroll into view to prevent element from being obscured by menu at top of page
        # browser.execute_script("return arguments[0].scrollIntoView(true);", button)
        button.click()
        logger.debug(f"clicked {text} btn")
        time.sleep(0.5)
        debug_delay_check()
        return True
    except Exception as e:
        if "obscures it" in str(e) and not reattempt:
            x = button.location_once_scrolled_into_view["x"]
            y = button.location_once_scrolled_into_view["y"]
            browser.execute_script(f"window.scrollTo({x}, {y-50})")
            return click_user_button(browser, user_element, text=text, reattempt=True)
        error_checker(e)
    raise Exception(f"failed to click {text} btn for user!")


















# TODO: move these somewhere else?
def scroll_to_bottom(browser):
    logger.debug("scrolling to bottom...")
    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        logger.debug("scrolling...")
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

# TODO: probably delete, or leave for reference
def scroll_to_bottom_once(browser):
    logger.debug("scrolling to bottom once...")
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Wait to load page
    time.sleep(1)




















# def get_user_by_username_old(browser, username, reattempt=False):
#     if not username: return None
#     go_to_page(browser, ONLYFANS_FANS_URL)
#     count = 0
#     logger.debug("searching for user: {} ...".format(username))
#     # scroll through users on page until user is found
#     attempts = 0
#     attemptsLimit = 5
#     initialScrollDelay = 0.5
#     scrollDelay = 0.5
#     while True:
#         try:
#             elements = browser.find_elements(By.CLASS_NAME, "g-user-username")
#             for ele in elements:
#                 found_username = ele.get_attribute("innerHTML").strip()
#                 if str(username).strip().replace("@","") == str(found_username).strip().replace("@",""):
#                     browser.execute_script("arguments[0].scrollIntoView();", ele)
#                     logger.info("")
#                     logger.debug("successfully found user: {}".format(username))
#                     # TODO: figure out how to combine xpath statements?
#                     # return parent element housing user info
#                     return ele.find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..')
#             if len(elements) == int(count):
#                 scrollDelay += initialScrollDelay
#                 attempts+=1
#                 if attempts == attemptsLimit:
#                     break
#             print_same_line("({}/{}) scrolling...".format(count, len(elements)))
#             count = len(elements)
#             browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(scrollDelay)
#         except Exception as e:
#             if "is stale" in str(e):
#                 logger.debug("stale element found, resetting search!")
#     logger.warning(f"failed to find user by username: {username}")
#     if not reattempt:
#         browser.refresh()
#         return get_user_by_username(browser, username, reattempt=True)
#     logger.info(f"Snarf isn't sure that '{username}' really exists...")
#     return None



# not needed, unnecessary once realizing that its simpler to just go to the url with the username in the search?= format
def get_user_search_field(browser):
    try:
        logger.debug(f"getting user search field...")
        WebDriverWait(browser, 10, poll_frequency=1).until(EC.visibility_of_element_located((By.CLASS_NAME, "b-content-filter__group-btns")))
        search_elements = browser.find_elements(By.CLASS_NAME, "b-content-filter__group-btns")
        search_element = search_elements[1].find_element(By.CLASS_NAME, "b-content-filter__btn")
        return search_element
    except Exception as e:
        error_checker(e)
    raise Exception("failed to find search element!")


def search_username_in_search_element(browser, search_element, username):
    try:
        logger.debug(f"entering username '{username}' into search field...")
        ActionChains(browser).move_to_element(search_element).click(on_element=search_element).send_keys(str(username)).send_keys(Keys.ENTER).perform()
        time.sleep(1) # required wait
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to enter username into search field!")

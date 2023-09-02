import re
import time
import logging
from selenium.webdriver.common.by import By

from .errors import error_checker
from .goto import go_to_home, go_to_page
from .. import CONFIG, print_same_line
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
        logging.debug("searching for active username...")
        go_to_home(browser)
        eles = [ele for ele in browser.find_elements(By.TAG_NAME, "a") if "@" in str(ele.get_attribute("innerHTML")) and "onlyfans" not in str(ele.get_attribute("innerHTML"))]
        if CONFIG["debug"]:
            for ele in eles:
                logging.debug("{} - {}".format(ele.get_attribute("innerHTML"), ele.get_attribute("href")))
        if len(eles) == 0:
            logging.error("unable to find username!")
        else:
            username = str(eles[0].get_attribute("href")).replace(ONLYFANS_HOME_URL+"/", "")
            logging.debug("successfully found active username: {}".format(username))
            return username
    except Exception as e:
        error_checker(e)
        logging.error("failed to find active username!")
    return None

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

    user_id = None
    try:
        go_to_page(browser, username)
        elements = browser.find_elements(By.TAG_NAME, "a")
        user_id = [ele.get_attribute("href") for ele in elements if "/my/chats/chat/" in str(ele.get_attribute("href"))]
        if len(user_id) == 0: 
            logging.warning(f"unable to find user id for {username}!")
            return None
        user_id = user_id[0]
        user_id = user_id.replace("https://onlyfans.com/my/chats/chat/", "")
        logging.debug(f"successfully found user id: {user_id}")
    except Exception as e:
        error_checker(e)
        logging.error(f"failed to find user id for username: {username}")
    return user_id

def get_users_at_page(browser, page):
    if page == ONLYFANS_FOLLOWING_URL:
        class_name = "subscriptions"
    elif page == ONLYFANS_FANS_URL:
        class_name = "fans"
    users = []
    try:
        go_to_page(browser, page)
        # scroll until elements stop spawning
        thirdTime = 0
        count = 0
        while True:
            elements = browser.find_elements(By.CLASS_NAME, f"m-{class_name}")
            if len(elements) == int(count) and thirdTime >= 3: break
            print_same_line(f"({count}) scrolling...")
            count = len(elements)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            if thirdTime >= 3 and len(elements) == 0: break
            thirdTime += 1
        logging.info("")
        elements = browser.find_elements(By.CLASS_NAME, f"m-{class_name}")
        logging.debug(f"searching {class_name}...")
        for ele in elements:
            username = ele.find_element(By.CLASS_NAME, "g-user-username").get_attribute("innerHTML").strip()
            name = ele.find_element(By.CLASS_NAME, "g-user-name").get_attribute("innerHTML")
            name = re.sub("<!-*>", "", name)
            name = re.sub("<.*\">", "", name)
            name = re.sub("</.*>", "", name).strip()
            users.append({"name":name, "username":username.replace("@",""), "isFan":True if class_name=="fans" else False, "isFollower":True if class_name=="subscriptions" else False})
            logging.debug(users[-1])
        logging.debug(f"found {len(users)} {class_name}")
        logging.debug(f"successfully found {class_name}!")
    except Exception as e:
        logging.info(e)
        error_checker(e)
        logging.error(f"failed to find {class_name}!")
    return users

# TODO: update to interact with other fan/follower types ala recent, favorite, etc
def get_users_by_type(browser, isFan=True, isFollower=False):
    users = []
    if isFan:
        users.extend(get_users_at_page(browser, ONLYFANS_FANS_URL))
    if isFollower:
        users.extend(get_users_at_page(browser, ONLYFANS_FOLLOWING_URL))
    return users

def get_user_by_username(browser, username, reattempt=False):
    if not username: return None
    go_to_page(browser, ONLYFANS_FANS_URL)
    count = 0
    logging.debug("searching for user: {} ...".format(username))
    # scroll through users on page until user is found
    attempts = 0
    attemptsLimit = 5
    initialScrollDelay = 0.5
    scrollDelay = 0.5
    while True:
        elements = browser.find_elements(By.CLASS_NAME, "g-user-username")
        for ele in elements:
            found_username = ele.get_attribute("innerHTML").strip()
            if str(username).strip().replace("@","") == str(found_username).strip().replace("@",""):
                browser.execute_script("arguments[0].scrollIntoView();", ele)
                logging.info("")
                logging.debug("successfully found user: {}".format(username))
                # TODO: figure out how to combine xpath statements?
                # return parent element housing user info
                return ele.find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..').find_element(By.XPATH, '..')
        if len(elements) == int(count):
            scrollDelay += initialScrollDelay
            attempts+=1
            if attempts == attemptsLimit:
                break
        print_same_line("({}/{}) scrolling...".format(count, len(elements)))
        count = len(elements)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scrollDelay)
    logging.warning(f"Unable to find user by username: {username}")
    logging.info("Are you sure that user really exists? shnarf")
    if reattempt: return get_user_by_username(browser, username)
    return None

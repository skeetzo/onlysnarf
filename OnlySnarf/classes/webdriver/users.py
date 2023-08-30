
from .errors import error_checker
from .goto import go_to_home, go_to_page
from .. import Settings
from .. import ONLYFANS_HOME_URL2, ONLYFANS_USERS_ACTIVE_URL, ONLYFANS_USERS_FOLLOWING_URL

#################
##### Users #####
#################


# TODO: add and weave these through newly added list urls
# get_active_users()
# get_active_subscriptions()



def get_current_username(browser):
    """
    Gets the username of the logged in user.

    Returns
    -------
    str
        The username of the logged in user

    """

    try:
        Settings.dev_print("searching for active username...")
        go_to_home(browser)
        eles = [ele for ele in browser.find_elements(By.TAG_NAME, "a") if "@" in str(ele.get_attribute("innerHTML")) and "onlyfans" not in str(ele.get_attribute("innerHTML"))]
        if Settings.is_debug():
            for ele in eles:
                Settings.dev_print("{} - {}".format(ele.get_attribute("innerHTML"), ele.get_attribute("href")))
        if len(eles) == 0:
            Settings.err_print("unable to find username!")
        else:
            username = str(eles[0].get_attribute("href")).replace(ONLYFANS_HOME_URL2, "")
            Settings.dev_print("successfully found active username: {}".format(username))
            return username
    except Exception as e:
        error_checker(e)
        Settings.err_print("failed to find active username!")
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
            Settings.warn_print(f"unable to find user id for {username}!")
            return None
        user_id = user_id[0]
        user_id = user_id.replace("https://onlyfans.com/my/chats/chat/", "")
        Settings.dev_print(f"successfully found user id: {user_id}")
    except Exception as e:
        error_checker(e)
        Settings.err_print(f"failed to find user id for username: {username}")
    return user_id

def get_users_at_page(browser, page):
    if page == ONLYFANS_USERS_FOLLOWING_URL:
        class_name = "subscriptions"
    elif page == ONLYFANS_USERS_ACTIVE_URL:
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
            Settings.print_same_line(f"({count}) scrolling...")
            count = len(elements)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            if thirdTime >= 3 and len(elements) == 0: break
            thirdTime += 1
        Settings.print("")
        elements = browser.find_elements(By.CLASS_NAME, f"m-{class_name}")
        Settings.dev_print(f"searching {class_name}...")
        for ele in elements:
            username = ele.find_element(By.CLASS_NAME, "g-user-username").get_attribute("innerHTML").strip()
            name = ele.find_element(By.CLASS_NAME, "g-user-name").get_attribute("innerHTML")
            name = re.sub("<!-*>", "", name)
            name = re.sub("<.*\">", "", name)
            name = re.sub("</.*>", "", name).strip()
            users.append({"name":name, "username":username.replace("@","")})
            Settings.dev_print(users[-1])
        Settings.maybe_print(f"found {len(users)} {class_name}")
        Settings.dev_print(f"successfully found {class_name}!")
    except Exception as e:
        Settings.print(e)
        error_checker(e)
        Settings.err_print(f"failed to find {class_name}!")
    return users

def get_users_by_type(isFan=True, isFollower=False):
    browser = Driver.get_browser()
    users = []
    if isFan:
        users.extend(get_users_at_page(browser, ONLYFANS_USERS_ACTIVE_URL))
    if isFollower:
        users.extend(get_users_at_page(browser, ONLYFANS_USERS_FOLLOWING_URL))
    return users

def get_user_by_username(browser, username, reattempt=False):
    if not username: return None
    go_to_page(browser, ONLYFANS_USERS_ACTIVE_URL)
    count = 0
    Settings.maybe_print("searching for user: {} ...".format(username))
    # scroll through users on page until user is found
    attempts = 0
    attemptsLimit = 5
    initialScrollDelay = 0.5
    scrollDelay = 0.5
    while True:
        elements = browser.find_elements(By.CLASS_NAME, "g-user-username")
        for ele in elements:
            found_username = ele.get_attribute("innerHTML").strip()
            if str(username) == str(found_username):
                browser.execute_script("arguments[0].scrollIntoView();", ele)
                Settings.print("")
                Settings.dev_print("successfully found user: {}".format(username))
                return ele
        if len(elements) == int(count):
            scrollDelay += initialScrollDelay
            attempts+=1
            if attempts == attemptsLimit:
                break
        Settings.print_same_line("({}/{}) scrolling...".format(count, len(elements)))
        count = len(elements)
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scrollDelay)
    Settings.warn_print(f"Unable to find user by username: {username}")
    Settings.print("Are you sure that user really exists? shnarf")
    if reattempt: return get_user_by_username(browser, username)
    return None

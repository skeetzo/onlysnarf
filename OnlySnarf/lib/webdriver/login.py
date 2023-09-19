import time
import logging
logger = logging.getLogger(__name__)

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from .cookies import cookies_load, cookies_save
from .errors import error_checker
from .goto import go_to_home
from .. import CONFIG, DEFAULT
from .. import get_username_onlyfans, get_password, get_username_google, get_password_google, get_username_twitter, get_password_twitter

##################
###### Login #####
##################

def login(browser, method="auto", cookies=False):
    """
    Logs into OnlyFans account provided via args and chosen method.

    Checks if already logged in first. Logs in via requested method or tries all available.

    Returns
    -------
    bool
        Whether or not the login was successful

    """

    def logged_in():
        if cookies: cookies_save(browser)
        else: logger.debug("skipping cookies (save)")
        logger.info(f"login successful! ({method})")
        return True

    if cookies: cookies_load(browser)
    else: logger.debug("skipping cookies (load)")

    if check_if_already_logged_in(browser): return logged_in()
    
    logger.info(f"logging into OnlyFans for {CONFIG['username']}...")
    try:
        successful = False
        if method == "auto":
            successful = via_form(browser)
            if not successful:      successful = via_google(browser)
            if not successful:      successful = via_twitter(browser)
        elif method == "onlyfans":  successful = via_form(browser)
        elif method == "twitter":   successful = via_twitter(browser)
        elif method == "google":    successful = via_google(browser)
        if successful: return logged_in()
    except Exception as e:
        error_checker(e)
    raise Exception("failed to login to OnlyFans!")

################################################################################################
################################################################################################
################################################################################################

def check_if_already_logged_in(browser):
    """Check if already logged in before attempting to login again"""

    # go_to_home(browser)
    go_to_home(browser, force=True)
    try:
        WebDriverWait(browser, 10, poll_frequency=1).until(EC.visibility_of_element_located((By.CLASS_NAME, "b-make-post__streaming-link")))
        logger.debug("already logged into OnlyFans!")
        return True
    except TimeoutException as te:
        logger.debug(str(te))
    except Exception as e:
        error_checker(e)
    return False

def check_if_logged_in(browser):
    """
    Check after login attempt for successful home page

    Returns
    -------
    bool
        Whether or not the login check was successful

    """

    try:
        logger.debug("waiting for login check...")
        WebDriverWait(browser, 30, poll_frequency=2).until(EC.visibility_of_element_located((By.CLASS_NAME, "b-make-post__streaming-link")))
        logger.info("OnlyFans login successful!")
        return True
    except TimeoutException as te:
        logger.warning("timeout during login check!")
        logger.debug(str(te))
        bodyText = browser.find_element(By.TAG_NAME, "body").text
        # output page text for debugging
        logger.debug(bodyText)
        # check for phone number page
        if "Verify your identity by entering the phone number associated with your Twitter account." in str(bodyText):
            verify_phone()
            return check_if_logged_in(browser)
        # check for email notification
        elif "Check your email" in str(bodyText):
            verify_email()
            return check_if_logged_in(browser)
        else:
            logger.error("Login Failure: Timed Out! Please check your credentials.")
            logger.error("If the problem persists, OnlySnarf may require an update.")
    except Exception as e:
        error_checker(e)
        logger.error("Login Failure!")
        logger.error("If the problem persists, OnlySnarf may require an update.")
    return False

def via_form(browser):
    """
    Logs in via OnlyFans username & password form
    
    Returns
    -------
    bool
        Whether or not the login attempt was successful

    """

    try:
        logger.debug("logging in via form...")
        if not str(get_username_onlyfans()) or not str(get_password()):
            logger.warning("missing onlyfans login info!")
            return False
        go_to_home(browser)
        WAIT = WebDriverWait(browser, 10, poll_frequency=2)
        logger.debug("entering username & password...")
        usernameField = WAIT.until(EC.presence_of_element_located((By.NAME, "email")))
        usernameField.click()
        usernameField.send_keys(str(get_username_onlyfans()))
        logger.debug("username entered")
        # passwordField = WAIT.until(EC.presence_of_element_located((By.NAME, "password")))
        passwordField = browser.find_element(By.NAME, "password")
        passwordField.click()
        passwordField.send_keys(str(get_password()))
        passwordField.send_keys(Keys.ENTER)
        logger.debug("password entered")
        check_captcha(browser)
        return check_if_logged_in(browser)
    except Exception as e:
        logger.debug("form login failure!")
        error_checker(e)
    return False

# TODO: requires testing
def via_google(browser):
    """
    Logs in via linked Google account. (doesn't work)
    
    Returns
    -------
    bool
        Whether or not the login attempt was successful

    """

    try:
        logger.debug("logging in via google...")
        if not str(get_username_google()) or not str(get_password_google()):
            logger.error("missing google login info")
            return False
        # click google login
        elements = browser.find_elements(By.TAG_NAME, "a")
        [elem for elem in elements if '/auth/google' in str(elem.get_attribute('href'))][0].click()
        time.sleep(3)
        username = browser.switch_to.active_element
        username.send_keys(str(get_username_google()))
        username.send_keys(Keys.ENTER)
        logger.debug("username entered")
        time.sleep(2)
        password = browser.switch_to.active_element
        password.send_keys(str(get_password_google()))
        password.send_keys(Keys.ENTER)
        logger.debug("password entered")
        return check_if_logged_in(browser)
    except Exception as e:
        logger.debug("google login failure!")
        error_checker(e)
    return False

def via_twitter(browser):
    """
    Logs in via linked Twitter account
    
    Returns
    -------
    bool
        Whether or not the login attempt was successful

    """

    try:
        logger.debug("logging in via twitter...")
        if not str(get_username_twitter()) or not str(get_password_twitter()):
            logger.error("missing twitter login info!")
            return False
        # click twitter login
        elements = browser.find_elements(By.TAG_NAME, "a")
        [elem for elem in elements if '/twitter/auth' in str(elem.get_attribute('href'))][0].click()
        browser.find_element(By.NAME, "session[username_or_email]").send_keys(str(get_username_twitter()))
        logger.debug("username entered")
        password = browser.find_element(By.NAME, "session[password]")
        password.send_keys(str(get_password_twitter()))
        password.send_keys(Keys.ENTER)
        logger.debug("password entered")
        return check_if_logged_in(browser)
    except Exception as e:
        logger.debug("twitter login failure!")
        error_checker(e)
    return False

################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

def check_captcha(browser):
    return
    try:
        time.sleep(3) # wait extra long to make sure it doesn't verify obnoxiously
        el = browser.find_element(By.NAME, "password")
        print(el.get_attribute("innerHTML"))
        if not el: return # likely logged in without captcha
        logger.info("waiting for captcha completion by user...")
        action = ActionChains(browser)
        action.move_to_element_with_offset(el, 40, 100)
        action.click()
        action.perform()
        time.sleep(10)
        submit = browser.find_elements(By.CLASS_NAME, "g-btn.m-rounded.m-flex.m-lg")
        for ele in submit:
            if str(ele.get_attribute("innerHTML")) == "Login" and ele.is_enabled():
                ele.click()
                return
        logger.error("unable to login via form - captcha")
    except Exception as e:
        print(e)
        if "Unable to locate element: [name=\"password\"]" not in str(e):
            logger.debug(e)

# Twitter second chance verification
def verify_phone(browser):
    try:
        logger.debug("verifying phone number...")
        element = browser.switch_to.active_element
        element.send_keys(str(CONFIG["phone"]))
        element.send_keys(Keys.ENTER)
    except Exception as e:
        logger.error("Unable to verify phone number!")
        logger.debug(e)

# TODO: requires testing, not successfuly receiving email w/ code to test further
# Twitter second chance verification
def verify_email(browser):
    try:
        logger.info("email verification required - please enter the code sent to your email!")
        element = browser.switch_to.active_element
        element.send_keys(str(input("Enter code: ")))
        element.send_keys(Keys.SHIFT + Keys.TAB)
        element.send_keys(Keys.ENTER)
    except Exception as e:
        logger.error("Unable to verify email!")
        logger.debug(e)
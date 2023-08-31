import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from .. import CONFIG, DEFAULT
from .errors import error_checker
from .goto import go_to_home

# TODO: finish replacing Settings references with methods to fetch user data that need to be readded


##################
###### Login #####
##################

def login(browser):
    """
    Logs into OnlyFans account provided via args and chosen method.

    Checks if already logged in first. Logs in via requested method or tries all available.

    Returns
    -------
    bool
        Whether or not the login was successful

    """

    if check_if_already_logged_in(browser): return True
    logging.info('Logging into OnlyFans for {}...'.format(CONFIG["username"]))
    try:
        if CONFIG["login"] == "auto":
            if via_form(browser) or via_google(browser) or via_twitter(browser):
                logging.debug("auto login successful!")
                return True
        elif CONFIG["login"] == "onlyfans":
            return via_form(browser)
        elif CONFIG["login"] == "twitter":
            return via_twitter(browser)
        elif CONFIG["login"] == "google":
            return via_google(browser)
    except Exception as e:
        error_checker(e)
    return False

################################################################################################
################################################################################################
################################################################################################

def check_if_already_logged_in(browser):
    """Check if already logged in before attempting to login again"""

    go_to_home(browser, force=True)
    try:
        WebDriverWait(browser, 10, poll_frequency=1).until(EC.visibility_of_element_located((By.CLASS_NAME, "b-make-post__streaming-link")))
        logging.info("already logged into OnlyFans!")
        return True
    except TimeoutException as te:
        logging.debug(str(te))
    except Exception as e:
        logging.debug(e)
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
        logging.debug("waiting for login check...")
        WebDriverWait(browser, 30, poll_frequency=2).until(EC.visibility_of_element_located((By.CLASS_NAME, "b-make-post__streaming-link")))
        logging.info("OnlyFans login successful!")
        return True
    except TimeoutException as te:
        logging.warning("timeout during login check!")
        logging.debug(str(te))
        bodyText = browser.find_element(By.TAG_NAME, "body").text
        # output page text for debugging
        logging.debug(bodyText)
        # check for phone number page
        if "Verify your identity by entering the phone number associated with your Twitter account." in str(bodyText):
            verify_phone()
            check_if_logged_in(browser)
        # check for email notification
        elif "Check your email" in str(bodyText):
            verify_email()
            check_if_logged_in(browser)
        else:
            logging.error("Login Failure: Timed Out! Please check your credentials.")
            logging.error("If the problem persists, OnlySnarf may require an update.")
    except Exception as e:
        error_checker(e)
        logging.error("Login Failure!")
        logging.error("If the problem persists, OnlySnarf may require an update.")
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
        logging.debug("logging in via form...")
        if not str(Settings.get_username_onlyfans()) or not str(Settings.get_password()):
            logging.warning("missing onlyfans login info!")
            return False
        go_to_home(browser)
        WAIT = WebDriverWait(browser, 10, poll_frequency=2)
        logging.debug("entering username & password...")
        usernameField = WAIT.until(EC.presence_of_element_located((By.NAME, "email")))
        usernameField.click()
        usernameField.send_keys(str(Settings.get_username_onlyfans()))
        logging.debug("username entered")
        # passwordField = WAIT.until(EC.presence_of_element_located((By.NAME, "password")))
        passwordField = browser.find_element(By.NAME, "password")
        passwordField.click()
        passwordField.send_keys(str(Settings.get_password()))
        passwordField.send_keys(Keys.ENTER)
        logging.debug("password entered")
        check_captcha(browser)
        return check_if_logged_in(browser)
    except Exception as e:
        logging.debug("form login failure!")
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
        logging.debug("logging in via google...")
        if not str(Settings.get_username_google()) or not str(Settings.get_password_google()):
            logging.error("missing google login info")
            return False
        # click google login
        elements = browser.find_elements(By.TAG_NAME, "a")
        [elem for elem in elements if '/auth/google' in str(elem.get_attribute('href'))][0].click()
        time.sleep(3)
        username = browser.switch_to.active_element
        username.send_keys(str(Settings.get_username_google()))
        username.send_keys(Keys.ENTER)
        logging.debug("username entered")
        time.sleep(2)
        password = browser.switch_to.active_element
        password.send_keys(str(Settings.get_password_google()))
        password.send_keys(Keys.ENTER)
        logging.debug("password entered")
        return check_if_logged_in(browser)
    except Exception as e:
        logging.debug("google login failure!")
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
        logging.debug("logging in via twitter...")
        if not str(Settings.get_username_twitter()) or not str(Settings.get_password_twitter()):
            logging.error("missing twitter login info!")
            return False
        # click twitter login
        elements = browser.find_elements(By.TAG_NAME, "a")
        [elem for elem in elements if '/twitter/auth' in str(elem.get_attribute('href'))][0].click()
        browser.find_element(By.NAME, "session[username_or_email]").send_keys(str(Settings.get_username_twitter()))
        logging.debug("username entered")
        password = browser.find_element(By.NAME, "session[password]")
        password.send_keys(str(Settings.get_password_twitter()))
        password.send_keys(Keys.ENTER)
        logging.debug("password entered")
        return check_if_logged_in(browser)
    except Exception as e:
        logging.debug("twitter login failure!")
        error_checker(e)
    return False


def check_captcha(browser):
    try:
        time.sleep(3) # wait extra long to make sure it doesn't verify obnoxiously
        el = browser.find_element(By.NAME, "password")
        if not el: return # likely logged in without captcha
        logging.info("waiting for captcha completion by user...")
        action = ActionChains(browser)
        action.move_to_element_with_offset(el, 40, 100)
        action.click()
        action.perform()
        time.sleep(10)
        sub = None
        submit = browser.find_element(By.CLASS_NAME, "g-btn.m-rounded.m-flex.m-lg")
        for ele in submit:
            if str(ele.get_attribute("innerHTML")) == "Login":
                sub = ele
        if sub and sub.is_enabled():
            submit.click()
        elif sub and not sub.is_enabled():
            logging.error("unable to login via form - captcha")
    except Exception as e:
        if "Unable to locate element: [name=\"password\"]" not in str(e):
            logging.debug(e)

# Twitter second chance verification
def verify_phone(browser):
    try:
        logging.debug("verifying phone number...")
        element = browser.switch_to.active_element
        element.send_keys(str(Settings.get_phone_number()))
        element.send_keys(Keys.ENTER)
    except Exception as e:
        logging.error("Unable to verify phone number!")
        logging.debug(e)

# TODO: requires testing, not successfuly receiving email w/ code to test further
# Twitter second chance verification
def verify_email(browser):
    try:
        logging.info("email verification required - please enter the code sent to your email!")
        element = browser.switch_to.active_element
        element.send_keys(str(input("Enter code: ")))
        element.send_keys(Keys.SHIFT + Keys.TAB)
        element.send_keys(Keys.ENTER)
    except Exception as e:
        logging.error("Unable to verify email!")
        logging.debug(e)

from .goto import go_to_home
from ..util.settings import Settings

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
    Settings.print('Logging into OnlyFans for {}...'.format(Settings.get_username()))
    successful = False
    try:
        if Settings.get_login_method() == "auto":
            successful = via_form(browser)
            if not successful: successful = via_twitter(browser)
            if not successful: successful = via_google(browser)
        elif Settings.get_login_method() == "onlyfans":
            successful = via_form(browser)
        elif Settings.get_login_method() == "twitter":
            successful = via_twitter(browser)
        elif Settings.get_login_method() == "google":
            successful = via_google(browser)
    except Exception as e:
        Driver.error_checker(e)
    return successful

################################################################################################
################################################################################################
################################################################################################

def check_if_already_logged_in(browser):
    """Check if already logged in before attempting to login again"""

    go_to_home(browser, force=True)
    try:
        WebDriverWait(browser, 10, poll_frequency=1).until(EC.visibility_of_element_located((By.CLASS_NAME, "b-make-post__streaming-link")))
        Settings.print("already logged into OnlyFans!")
        return True
    except TimeoutException as te:
        Settings.dev_print(str(te))
    except Exception as e:
        Settings.dev_print(e)
    return False

def check_if_logged_in(browser):
    """
    Check after login attempt for successful home page

    Returns
    -------
    bool
        Whether or not the login check was successful

    """

    def try_phone():
        Settings.maybe_print("verifying phone number...")
        element = browser.switch_to.active_element
        element.send_keys(str(Settings.get_phone_number()))
        element.send_keys(Keys.ENTER)

    # TODO: requires testing, not successfuly receiving email w/ code to test further
    def try_email():
        Settings.print("email verification required - please enter the code sent to your email!")
        element = browser.switch_to.active_element
        element.send_keys(str(input("Enter code: ")))
        element.send_keys(Keys.SHIFT + Keys.TAB)
        element.send_keys(Keys.ENTER)

    try:
        Settings.dev_print("waiting for login check...")
        WebDriverWait(browser, 30, poll_frequency=2).until(EC.visibility_of_element_located((By.CLASS_NAME, "b-make-post__streaming-link")))
        Settings.print("OnlyFans login successful!")
        return True
    except TimeoutException as te:
        bodyText = browser.find_element(By.TAG_NAME, "body").text
        # output page text for debugging
        Settings.dev_print(bodyText)
        # check for phone number page
        if "Verify your identity by entering the phone number associated with your Twitter account." in str(bodyText):
            try_phone()
            check_if_logged_in(browser)
        # check for email notification
        elif "Check your email" in str(bodyText):
            try_email()
            check_if_logged_in(browser)
        else:
            # Settings.dev_print(str(te))
            Settings.print("Login Failure: Timed Out! Please check your credentials.")
            Settings.print("If the problem persists, OnlySnarf may require an update.")
        return False
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("Login Failure!")
        Settings.print("If the problem persists, OnlySnarf may require an update.")
        return False
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
        Settings.maybe_print("logging in via form...")
        if not str(Settings.get_username_onlyfans()) or not str(Settings.get_password()):
            Settings.warn_print("missing onlyfans login info!")
            return False
        go_to_home(browser)
        WAIT = WebDriverWait(browser, 10, poll_frequency=2)
        Settings.dev_print("entering username & password...")
        usernameField = WAIT.until(EC.presence_of_element_located((By.NAME, "email")))
        usernameField.click()
        usernameField.send_keys(str(Settings.get_username_onlyfans()))
        Settings.dev_print("username entered")
        # passwordField = WAIT.until(EC.presence_of_element_located((By.NAME, "password")))
        passwordField = browser.find_element(By.NAME, "password")
        passwordField.click()
        passwordField.send_keys(str(Settings.get_password()))
        passwordField.send_keys(Keys.ENTER)
        Settings.dev_print("password entered")
        check_captcha(browser)
        return check_if_logged_in(browser)
    except Exception as e:
        Settings.dev_print("form login failure!")
        Driver.error_checker(e)
    return False

# TODO: requires testing
def via_google():
    """
    Logs in via linked Google account. (doesn't work)
    
    Returns
    -------
    bool
        Whether or not the login attempt was successful

    """

    try:
        Settings.maybe_print("logging in via google...")
        if not str(Settings.get_username_google()) or not str(Settings.get_password_google()):
            Settings.err_print("missing google login info")
            return False
        # click google login
        elements = browser.find_elements(By.TAG_NAME, "a")
        [elem for elem in elements if '/auth/google' in str(elem.get_attribute('href'))][0].click()
        time.sleep(3)
        username = browser.switch_to.active_element
        username.send_keys(str(Settings.get_username_google()))
        username.send_keys(Keys.ENTER)
        Settings.dev_print("username entered")
        time.sleep(2)
        password = browser.switch_to.active_element
        password.send_keys(str(Settings.get_password_google()))
        password.send_keys(Keys.ENTER)
        Settings.dev_print("password entered")
        return check_if_logged_in(browser)
    except Exception as e:
        Settings.dev_print("google login failure!")
        Driver.error_checker(e)
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
        Settings.maybe_print("logging in via twitter...")
        if not str(Settings.get_username_twitter()) or not str(Settings.get_password_twitter()):
            Settings.err_print("missing twitter login info!")
            return False
        # click twitter login
        elements = browser.find_elements(By.TAG_NAME, "a")
        [elem for elem in elements if '/twitter/auth' in str(elem.get_attribute('href'))][0].click()
        browser.find_element(By.NAME, "session[username_or_email]").send_keys(str(Settings.get_username_twitter()))
        Settings.dev_print("username entered")
        password = browser.find_element(By.NAME, "session[password]")
        password.send_keys(str(Settings.get_password_twitter()))
        password.send_keys(Keys.ENTER)
        Settings.dev_print("password entered")
        return check_if_logged_in(browser)
    except Exception as e:
        Settings.dev_print("twitter login failure!")
        Driver.error_checker(e)
    return False


def check_captcha(browser):
    try:
        time.sleep(3) # wait extra long to make sure it doesn't verify obnoxiously
        el = browser.find_element(By.NAME, "password")
        if not el: return # likely logged in without captcha
        Settings.print("waiting for captcha completion by user...")
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
            Settings.err_print("unable to login via form - captcha")
    except Exception as e:
        if "Unable to locate element: [name=\"password\"]" not in str(e):
            Settings.dev_print(e)

####################
##### Messages #####
####################

@staticmethod
def message(username, user_id=None):
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
        driver = Driver.get_driver()
        driver.auth()
        driver.go_to_home(force=True)
        Settings.dev_print("attempting to message {}...".format(username))
        
        # if the username is a key string it will behave differently
        if str(username).lower() == "all": return message_all(driver)
        elif str(username).lower() == "recent": return message_recent(driver)
        elif str(username).lower() == "favorite": return message_favorite(driver)
        elif str(username).lower() == "renew on": return message_renewers(driver)
        elif str(username).lower() == "random": return message_random(driver)
        else: return driver.message_user(username, user_id=user_id)
        # if successful: Settings.dev_print("started message for {}".format(username))
        # else: Settings.warn_print("failed to start message for {}!".format(username))
        # return successful
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failure to message - {}".format(username))
    return False
 
# TODO: add these behaviors
def message_all():
    pass

def message_recent():
        
        # successful = False
        # if type__ != None:
        #     driver.go_to_page(ONLYFANS_NEW_MESSAGE_URL)
        #     Settings.dev_print("clicking message type: {}".format(username))
        #     driver.find_element_to_click(type__).click()
        #     successful = True
    pass

def message_favorite():
    pass

def message_renewers():
    pass

def message_random(driver):
    from ..classes.user import User
    username = User.get_random_user().username


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

def message_clear(self):
    try:
        Settings.dev_print("clearing message...")
        clearButton = [ele for ele in self.browser.find_elements(By.TAG_NAME, "button") if "Clear" in ele.get_attribute("innerHTML") and ele.is_enabled()]
        if len(clearButton) > 0:
            Settings.dev_print("clicking clear button...")
            clearButton[0].click()
        else:
            Settings.dev_print("refreshing page and clearing text...")
            self.go_to_home(force=True)
            clear_text(self.browser)
            close_icons(self.browser)
        Settings.dev_print("successfully cleared message!")
        return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.warn_print("failed to clear message!")
    return False

def message_confirm(self):
    """
    Wait for the message open on the page's Confirm button to be clickable and click it

    Returns
    -------
    bool
        Whether or not the message confirmation was successful

    """

    try:
        Settings.dev_print("waiting for message confirm to be clickable...")
        confirm = WebDriverWait(self.browser, int(Settings.get_upload_max_duration()), poll_frequency=3).until(EC.element_to_be_clickable((By.CLASS_NAME, "g-btn.m-rounded.b-chat__btn-submit")))
        Settings.dev_print("message confirm is clickable")
        Settings.debug_delay_check()
        if Settings.is_debug():
            Settings.print('skipping message (debug)')
            self.message_clear()
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
    self.message_clear()
    return False

def message_price(self, price):
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
        try:
            Settings.dev_print("clearing any preexisting price...")
            self.browser.find_element(By.CLASS_NAME, "m-btn-remove").click()
        except Exception as e:
            Settings.dev_print(e)
        Settings.dev_print("entering price...")
        self.browser.find_element(By.CLASS_NAME, "b-make-post__actions__btns").find_elements(By.XPATH, "./child::*")[7].click()
        priceText = WebDriverWait(self.browser, 10, poll_frequency=2).until(EC.element_to_be_clickable(self.browser.find_element(By.ID, "priceInput_1")))
        priceText.click()
        priceText.send_keys(str(price))
        Settings.dev_print("entered price")
        Settings.debug_delay_check()
        Settings.dev_print("saving price...")
        self.find_element_to_click("priceSave").click()    
        # {
        #     "name": "priceSave",
        #     "classes": ["g-btn.m-flat.m-btn-gaps.m-reset-width", "g-btn.m-transparent-bg", "g-btn.m-rounded"], # "b-chat__btn-set-price", "button.g-btn.m-rounded"
        #     "text": ["Save"],
        #     "id": []
        # },
        Settings.dev_print("saved price")
        return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failure to enter price")
    return False

def message_text(self, text):
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
        if not text or str(text) == "None":
            Settings.err_print("missing text for message!")
            return False
        Settings.dev_print("entering text...")
        # clear any preexisting text first
        ActionChains(self.browser).move_to_element(self.browser.find_element(By.ID, "new_post_text_input")).double_click().click_and_hold().send_keys(Keys.CLEAR).send_keys(str(text)).perform()
        Settings.dev_print("successfully entered text")
        time.sleep(0.5)
        return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failure to enter message")
    return False

def message_user_by_id(self, user_id=None):
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

    user_id = str(user_id).replace("@u","").replace("@","")
    if not user_id or str(user_id) == "None":
        Settings.err_print("missing user id!")
        return False
    try:
        self.go_to_page("{}{}".format(ONLYFANS_CHAT_URL, user_id))
        Settings.dev_print("successfully messaging user id: {}".format(user_id))
        return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failed to message user by id!")
    return False

def message_user(self, username, user_id=None):
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
    if user_id: return self.message_user_by_id(user_id=user_id)
    if not username:
        Settings.err_print("missing username to message!")
        return False
    try:
        self.go_to_page(username)

        # time.sleep(5) # for whatever reason this constantly errors out from load times
        WebDriverWait(self.browser, 10, poll_frequency=1).until(EC.visibility_of_element_located((By.TAG_NAME, "a")))

        elements = self.browser.find_elements(By.TAG_NAME, "a")
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
        self.go_to_page(ele)
        Settings.dev_print("successfully messaging username: {}".format(username))
        return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failed to message user")
    return False


# TODO: update, test, and probably rename
@staticmethod
def messages_scan(num=0):
    """
    Scan messages page for recent users

    Parameters
    ----------
    num : int
        The number of users to consider recent (doesn't work)

    Returns
    -------
    list
        The list of users found

    """

    # go to /messages page
    # get top n users
    Settings.dev_print("scanning messages")
    users = []
    try:
        driver = Driver.get_driver()
        driver.auth()
        driver.go_to_page("/my/chats")
        users_ = driver.browser.find_elements(By.CLASS_NAME, "g-user-username")
        Settings.dev_print("users: {}".format(len(users_)))
        user_ids = driver.browser.find_elements(By.CLASS_NAME, "b-chats__item__link")
        Settings.dev_print("ids: {}".format(len(user_ids)))
        for user in user_ids:
            if not user or not user.get_attribute("href") or str(user.get_attribute("href")) == "None": continue
            users.append(str(user.get_attribute("href")).replace("https://onlyfans.com/my/chats/chat/", ""))
        return users[:10]
    except Exception as e:
        Settings.print(e)
        Driver.error_checker(e)
        Settings.err_print("failed to scan messages")
    return users

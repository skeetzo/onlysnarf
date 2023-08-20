
def search_for_fan(driver, fan, reattempt=False):
    driver.go_to_page(ONLYFANS_USERS_ACTIVE_URL)
    count = 0
    Settings.maybe_print("searching for fan: {} ...".format(fan))
    # scroll through users on page until user is found
    attempts = 0
    attemptsLimit = 5
    while True:
        # elements = driver.browser.find_elements(By.CLASS_NAME, "m-fans")
        elements = driver.browser.find_elements(By.CLASS_NAME, "g-user-username")
        for ele in elements:
            username = ele.get_attribute("innerHTML").strip()
            print("username: {}".format(username))
            print("fan: {}".format(fan))
            if str(fan) == str(username):
                driver.browser.execute_script("arguments[0].scrollIntoView();", ele)
                Settings.print("")
                Settings.dev_print("successfully found fan: {}".format(fan))
                return ele
        if len(elements) == int(count):
            Driver.scrollDelay += Driver.initialScrollDelay
            attempts+=1
            if attempts == attemptsLimit:
                break
        Settings.print_same_line("({}/{}) scrolling...".format(count, len(elements)))
        count = len(elements)
        driver.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(Driver.scrollDelay)

    Settings.warn_print("unable to find fan!")

    if reattempt: return search_for_fan(driver, fan)
    return None





######################################################################

@staticmethod
def read_user_messages(username, user_id=None):
    """
    Read the messages of the target user by username or user id.

    Parameters
    ----------
    username : str
        The username of the user to read messages of
    user_id : str
        The user id of the user to read messages of

    Returns
    -------
    list
        A list containing the messages read

    """

    try:
        driver = Driver.get_driver()
        # go to onlyfans.com/my/subscribers/active
        driver.message_user(username, user_id=user_id)
        messages_sent_ = []

        try:
            messages_sent_ = driver.find_elements_by_name("messagesFrom")
        except Exception as e:
            if "Unable to locate elements" in str(e):
                pass
            else: Settings.dev_print(e)
        
        messages_all_ = []
        try:
            messages_all_ = driver.find_elements_by_name("messagesAll")
        except Exception as e:
            if "Unable to locate elements" in str(e):
                pass
            else: Settings.dev_print(e)
        messages_all = []
        messages_received = []
        messages_sent = []
        # timestamps_ = driver.browser.find_elements(By.CLASS_NAME, "b-chat__message__time")
        # timestamps = []
        # for timestamp in timestamps_:
            # Settings.maybe_print("timestamp1: {}".format(timestamp))
            # timestamp = timestamp["data-timestamp"]
            # timestamp = timestamp.get_attribute("innerHTML")
            # Settings.maybe_print("timestamp: {}".format(timestamp))
            # timestamps.append(timestamp)
        for message in messages_all_:
            message = message.get_attribute("innerHTML")
            message = re.sub(r'<[a-zA-Z0-9=\"\\/_\-!&;%@#$\(\)\.:\+\s]*>', "", message)
            Settings.maybe_print("all: {}".format(message))
            messages_all.append(message)
        messages_and_timestamps = []
        # messages_and_timestamps = [j for i in zip(timestamps,messages_all) for j in i]
        # Settings.maybe_print("chat log:")
        # for f in messages_and_timestamps:
            # Settings.maybe_print(": {}".format(f))
        for message in messages_sent_:
            # Settings.maybe_print("from1: {}".format(message.get_attribute("innerHTML")))
            message = message.find_element(By.CLASS_NAME, Element.get_element_by_name("enterMessage").getClass()).get_attribute("innerHTML")
            message = re.sub(r'<[a-zA-Z0-9=\"\\/_\-!&;%@#$\(\)\.:\+\s]*>', "", message)
            Settings.maybe_print("sent: {}".format(message))
            messages_sent.append(message)
        i = 0

        # messages_all = list(set(messages_all))
        # messages_sent = list(set(messages_sent))
        # i really only want to remove duplicates if they're over a certain str length

        def remove_dupes(list_):
            """Remove duplicates from the list"""

            for i in range(len(list_)):
                for j in range(len(list_)):
                    # if j >= len(list_): break
                    if i==j: continue
                    if str(list_[i]) == str(list_[j]) and len(str(list_[i])) > 10:
                        del list_[j]
                        remove_dupes(list_)
                        return
                        
        remove_dupes(messages_all)
        remove_dupes(messages_sent)

        for message in messages_all:
            if message not in messages_sent:
                messages_received.append(message)
            i += 1
        Settings.maybe_print("received: {}".format(messages_received))
        Settings.maybe_print("sent: {}".format(messages_sent))
        Settings.maybe_print("messages sent: {}".format(len(messages_sent)))
        Settings.maybe_print("messages received: {}".format(len(messages_received)))
        Settings.maybe_print("messages all: {}".format(len(messages_all)))
        return [messages_all, messages_and_timestamps, messages_received, messages_sent]
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failure to read chat - {}".format(username))
        return [[],[],[],[]]



#################
##### Users #####
#################

@staticmethod
def get_username():
    """
    Gets the username of the logged in user.

    Returns
    -------
    str
        The username of the logged in user

    """

    try:
        driver = Driver.get_driver()
        driver.auth()
        eles = [ele for ele in driver.browser.find_elements(By.TAG_NAME, "a") if "@" in str(ele.get_attribute("innerHTML")) and "onlyfans" not in str(ele.get_attribute("innerHTML"))]
        Settings.dev_print("successfully found users...")
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
        Driver.error_checker(e)
        Settings.err_print("failed to find username")
    return None

fansOrFollowers should be 'fans' or 'subscriptions/following'
def get_users(fansOrFollowers="fans"):

    if "follow" in str(fansOrFollowers):
        fansOrFollowers = "subscriptions"

    page = ONLYFANS_USERS_ACTIVE_URL
    # if fansOrFollowers == "fans":
        # page = ONLYFANS_USERS_ACTIVE_URL
    if fansOrFollowers == "subscriptions":
        page = ONLYFANS_USERS_FOLLOWING_URL

    users = []
    try:
        driver = Driver.get_driver()
        driver.go_to_page(page)
        # scroll until elements stop spawning
        thirdTime = 0
        count = 0
        while True:
            elements = driver.browser.find_elements(By.CLASS_NAME, f"m-{fansOrFollowers}")
            if len(elements) == int(count) and thirdTime >= 3: break
            Settings.print_same_line("({}) scrolling...".format(count))
            count = len(elements)
            driver.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            if thirdTime >= 3 and len(elements) == 0: break
            thirdTime += 1
        Settings.print("")
        elements = driver.browser.find_elements(By.CLASS_NAME, f"m-{fansOrFollowers}")
        Settings.dev_print(f"searching {fansOrFollowers}...")
        for ele in elements:
            username = ele.find_element(By.CLASS_NAME, "g-user-username").get_attribute("innerHTML").strip()
            name = ele.find_element(By.CLASS_NAME, "g-user-name").get_attribute("innerHTML")
            name = re.sub("<!-*>", "", name)
            name = re.sub("<.*\">", "", name)
            name = re.sub("</.*>", "", name).strip()
            users.append({"name":name, "username":username.replace("@","")})
            Settings.dev_print(users[-1])
        Settings.maybe_print(f"found {len(users)} {fansOrFollowers}")
        Settings.dev_print(f"successfully found {fansOrFollowers}!")
    except Exception as e:
        Settings.print(e)
        Driver.error_checker(e)
        Settings.err_print(f"failed to find {fansOrFollowers}!")
    return users

@staticmethod
def user_get_id(username):
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
        driver = Driver.get_driver()
        driver.go_to_page(username)
        elements = driver.browser.find_elements(By.TAG_NAME, "a")
        ele = [ele.get_attribute("href") for ele in elements
                if "/my/chats/chat/" in str(ele.get_attribute("href"))]
        if len(ele) == 0: 
            Settings.warn_print("unable to find user id")
            return None
        ele = ele[0]
        ele = ele.replace("https://onlyfans.com/my/chats/chat/", "")
        user_id = ele
        Settings.dev_print("successfully found user id: {}".format(user_id))
    except Exception as e:
        Settings.dev_print("failure to find id: {}".format(username))
        Driver.error_checker(e)
        Settings.err_print("failed to find user id")
    return user_id


    
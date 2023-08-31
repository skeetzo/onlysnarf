## TODO: update lists functionality

from .. import Settings

def search_for_list(self, name=None, number=None):
    """
    Search for list in Driver.lists cache by name or number.

    Parameters
    ----------
    name : str
        The name of the list to find
    number : int
        The number for the list to find

    Returns
    -------
    str
        The located list name
    str
        The located list number

    """

    Settings.dev_print("lists: {}".format(self.lists))
    try:
        for list_ in self.lists:
            if list_[0] == name or list_[1] == number:
                return list_[0], list_[1]
        Settings.dev_print("failed to locate list: {} - {}".format(name, number))
    except Exception as e:
        if "Unable to locate window" not in str(e):
            Settings.dev_print(e)
    return name, number

@staticmethod
def get_list(name=None, number=None):
    """
    Search for list by name or number on OnlyFans.

    Parameters
    ----------
    name : str
        The name of the list to find
    number : int
        The number for the list to find

    Returns
    -------
    list
        The list of users on the found list
    str
        The located list name
    str
        The located list number

    """

    driver = Driver.get_driver()
    driver.auth()
    # gets members from list
    users = []
    Settings.maybe_print("getting list: {} - {}".format(name, number))
    name, number = driver.search_for_list(name=name, number=number)
    try:
        if not name or not number:
            for list_ in driver.get_lists():
                if name and str(list_[1]).lower() == str(name).lower():
                    number = list_[0]
                if number and str(list_[0]).lower() == str(number).lower():
                    name = list_[1]
        users = Driver.users_get(page="/my/lists/{}".format(number))
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failed to find list members")
    return users, name, number

def get_lists(self):
    """
    Search and return all lists from OnlyFans.

    Returns
    -------
    list
        The list of lists that were found

    """

    lists = []
    try:
        Settings.maybe_print("getting lists")
        self.go_to_page("/my/lists")

        elements = self.browser.find_elements(By.CLASS_NAME, "b-users-lists__item")

        # find favorites
        # find bookmarks
        # find friends
        # find other lists and their names
        # each page has the same user boxes that are used in users_get

        # /my/favorites
        # /my/bookmarks
        # /my/friends
        # /my/lists
        # b-users-lists__item -> href -> /my/lists/#
        # b-users-lists__item__name -> innerHTML -> list name
        # b-users-lists__item__count -> innerHTML -> list amount

        for ele in elements:
            if "/my/favorites" in str(ele.get_attribute("href")):
                # Settings.print("{} - {}".format(ele.get_attribute("innerHTML"), ele.get_attribute("href")))
                count = ele.find_elements(By.CLASS_NAME, "b-users-lists__item__count").get_attribute("innerHTML").replace("people", "").replace("person", "").strip()
                if int(count) > 0: lists.append("favorites")
            elif "/my/bookmarks" in str(ele.get_attribute("href")):
                # Settings.print("{} - {}".format(ele.get_attribute("innerHTML"), ele.get_attribute("href")))
                count = ele.find_elements(By.CLASS_NAME, "b-users-lists__item__count").get_attribute("innerHTML").replace("people", "").replace("person", "").strip()
                if int(count) > 0: lists.append("bookmarks")
            elif "/my/friends" in str(ele.get_attribute("href")):
                # Settings.print("{} - {}".format(ele.get_attribute("innerHTML"), ele.get_attribute("href")))
                count = ele.find_elements(By.CLASS_NAME, "b-users-lists__item__count").get_attribute("innerHTML").replace("people", "").replace("person", "").strip()
                if int(count) > 0: lists.append("friends")
            elif "/my/lists" in str(ele.get_attribute("href")):
                try:
                    # Settings.print("{} - {}".format(ele.get_attribute("innerHTML"), ele.get_attribute("href")))

                    # ele = ele.find_elements(By.CLASS_NAME, "b-users-lists__item__text")
                    listNumber = ele.get_attribute("href").replace("https://onlyfans.com/my/lists/", "")
                    listName = ele.find_element(By.CLASS_NAME, "b-users-lists__item__name").get_attribute("innerHTML").strip()
                    count = ele.find_element(By.CLASS_NAME, "b-users-lists__item__count").get_attribute("innerHTML").replace("people", "").replace("person", "").strip()
                    Settings.dev_print("{} - {}: {}".format(listNumber, listName, count))
                    lists.append([listNumber, listName])
                except Exception as e:
                    Settings.dev_print(e)
        Settings.dev_print("successfully found lists: {}".format(len(lists)))
    except Exception as e:
        Driver.error_checker(e)
        Settings.print(e)
        Settings.err_print("failed to find lists")
    return lists

def get_list_members(self, list):
    """
    Get the members of a list.

    Parameters
    ----------
    list : list
        The list to get members of
    
    Returns
    -------
    list
        The list of members that were found

    """

    users = []
    try:
        users = Driver.users_get(page="/my/lists/{}".format(int(list_)))
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failed to find list members")
    return users

def add_user_to_list(self, username=None, listNumber=None):
    """
    Add user by username to list by number.

    Parameters
    ----------
    username : str
        The username of the user to add to the list
    listNumber : int
        The number of the list to add the user to

    Returns
    -------
    bool
        Whether or not the user was added successfully

    """

    Settings.print("Adding user to list: {} - {}".format(username, listNumber))
    if not username:
        Settings.err_print("missing username for list")
        return False
    if not listNumber:
        Settings.err_print("missing list number")
        return False
    users = []
    try:
        self.go_to_page(ONLYFANS_USERS_ACTIVE_URL)
        end_ = True
        count = 0
        user_ = None
        while end_:
            elements = self.browser.find_elements(By.CLASS_NAME, "m-fans")
            for ele in elements:
                username_ = ele.find_element(By.CLASS_NAME, "g-user-username").get_attribute("innerHTML").strip()
                if str(username) == str(username_).replace("@",""):
                    self.browser.execute_script("arguments[0].scrollIntoView();", ele)
                    user_ = ele
                    end_ = False
            if not end_: continue
            if len(elements) == int(count): break
            Settings.print_same_line("({}/{}) scrolling...".format(count, len(elements)))
            count = len(elements)
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        Settings.print("")
        Settings.dev_print("successfully found fans")
        if not user_:
            Settings.err_print("unable to find user - {}".format(username))
            return False
        Settings.maybe_print("found: {}".format(username))
        ActionChains(self.browser).move_to_element(user_).perform()
        Settings.dev_print("finding list add")
        listAdds = user_.find_elements(By.CLASS_NAME, "g-btn.m-add-to-lists")
        listAdd_ = None
        for listAdd in listAdds:
            if str("/my/lists/"+listNumber) in str(listAdd.get_attribute("href")):
                Settings.print("skipping: User already on list - {}".format(listNumber))
                return True
            if " lists " in str(listAdd.get_attribute("innerHTML")).lower():
                Settings.dev_print("found list add")
                listAdd_ = listAdd
        Settings.dev_print("clicking list add")
        listAdd_.click()
        links = self.browser.find_elements(By.CLASS_NAME, "b-users-lists__item")
        for link in links:
            # Settings.print("{} {}".format(link.get_attribute("href"), link.get_attribute("innerHTML")))
            if str("/my/lists/"+listNumber) in str(link.get_attribute("href")):
                Settings.dev_print("clicking list")
                self.move_to_then_click_element(link)
                time.sleep(0.5)
                Settings.dev_print("successfully clicked list")
        Settings.dev_print("searching for list save")
        close = self.find_element_to_click("listSingleSave")
        Settings.dev_print("clicking save list")
        close.click()
        Settings.dev_print("successfully added user to list - {}".format(listNumber))
        return True
    except Exception as e:
        Driver.error_checker(e)
        Settings.err_print("failed to add user to list")
    return False

def add_users_to_list(self, users=[], number=None, name=None):
    """
    Add the users to the list by name or number.

    Parameters
    ----------
    users : list
        The list of users to add to the list
    number : int
        The number for the list to add to
    name : str
        The name of the list to add to

    Returns
    -------
    bool
        Whether or not the users were added successfully

    """

    try:
        users = users.copy()
        users_, name, number = self.get_list(number=number, name=name)
        # users = [user for user in users if user not in users_]
        for i, user in enumerate(users[:]):
            for user_ in users_:
                for key, value in user_.items():
                    if str(key) == "username" and str(user.username) == str(value):
                        users.remove(user)
        Settings.maybe_print("adding users to list: {} - {} - {}".format(len(users), number, name))
        try:
            Settings.dev_print("opening toggle options")
            toggle = self.browser.find_element(By.CLASS_NAME, "b-users__list__add-btn")
            Settings.dev_print("clicking toggle options")
            toggle.click()
            Settings.dev_print("toggle options opened")
        except Exception as e:
            Settings.dev_print("no options to toggle - users already available")
            # Settings.print("weird fuckup")
            # return self.add_users_to_list(users=users, number=number, name=name)
        time.sleep(1)
        original_handle = self.browser.current_window_handle
        clicked = False
        Settings.maybe_print("searching for users")
        while len(users) > 0:
            # find user thing
            eles = self.browser.find_elements(By.CLASS_NAME, "b-chats__available-users__item.m-search")
            for ele in eles:
                for user in users.copy():
                    # Settings.print("{} - {}".format(i, user.username))
                    if str(user.username) in str(ele.get_attribute("href")):
                        Settings.maybe_print("found user: {}".format(user.username))
                        # time.sleep(2)
                        self.move_to_then_click_element(ele)
                        users.remove(user)
                        clicked = True
            Settings.print_same_line("({}/{}) scrolling...".format(len(eles), len(users)))
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if len(eles) > 100:
                Settings.maybe_print("adding users to list individually")
                for user in users.copy():
                    successful = self.add_user_to_list(username=user.username, listNumber=number)
                    if successful: users.remove(user)
            # if current window has changed, switch back
            if self.browser.current_window_handle != original_handle:
                self.browser.switch_to.window(original_handle)
        Settings.print("")
        if not clicked:
            Settings.print("skipping list add (none)")
            Settings.dev_print("skipping list save")
            self.browser.refresh()
            Settings.dev_print("### List Add Successfully Skipped ###")
            return True
        if str(CONFIG["debug"]) == "True":
            Settings.print("skipping list add (debug)")
            Settings.dev_print("skipping list save")
            self.browser.refresh()
            Settings.dev_print("### List Add Successfully Canceled ###")
            return True
        Settings.dev_print("saving list")
        save = self.find_element_by_name("listSave")
        self.move_to_then_click_element(save)
        Settings.dev_print("### successfully added users to list")
    except Exception as e:
        Settings.print(e)
        Driver.error_checker(e)
        Settings.err_print("failed to add users to list")
        return False
    return True
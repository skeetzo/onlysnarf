
from ..util.settings import Settings

def discount_user(discount, reattempt=False):
    """
    Enter and apply discount to user

    Discount object requires:
    - duration (in months)
    - amount
    - username

    Parameters
    ----------
    discount : classes.Discount
        Discount object that contains or prompts for proper values

    Returns
    -------
    bool
        Whether or not the discount was applied successfully

    """

    if not discount:
        Settings.err_print("missing discount")
        return False

    # BUG
    # doesn't want to work with local variables
    Driver.originalAmount = None
    Driver.originalMonths = None
    try:
        driver = Driver.get_driver()
        driver.auth()
        months = int(discount["months"])
        amount = int(discount["amount"])
        username = str(discount["username"])
        Settings.print("discounting: {} {} for {} month(s)".format(username, amount, months))

        user_ = None

        def search_for_fan(username):
            driver.go_to_page(ONLYFANS_USERS_ACTIVE_URL)
            end_ = True
            count = 0
            Settings.maybe_print("searching for fan...")
            # scroll through users on page until user is found
            attempts = 0
            while end_:
                elements = driver.browser.find_elements(By.CLASS_NAME, "m-fans")
                for ele in elements:
                    username_ = ele.find_element(By.CLASS_NAME, "g-user-username").get_attribute("innerHTML").strip()
                    # if str(username) == str(username_).replace("@",""):
                    if username in username_:
                        driver.browser.execute_script("arguments[0].scrollIntoView();", ele)
                        Settings.print("")
                        Settings.dev_print("successfully found fan: {}".format(username))
                        return ele
                if len(elements) == int(count):
                    Driver.scrollDelay += Driver.initialScrollDelay
                    attempts+=1
                    if attempts == 5:
                        break
                Settings.print_same_line("({}/{}) scrolling...".format(count, len(elements)))
                count = len(elements)
                driver.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(Driver.scrollDelay)
            return None

        user_ = search_for_fan(username)


        if not user_:
            Settings.err_print("unable to find fan - {}".format(username))
            if not reattempt:
                Settings.maybe_print("reattempting fan search...")
                return Driver.discount_user(discount, reattempt=True)
            return False

        Settings.maybe_print("found: {}".format(username))
        ActionChains(driver.browser).move_to_element(user_).perform()
        Settings.dev_print("successfully moved to fan")
        Settings.dev_print("finding discount btn")
        buttons = user_.find_elements(By.CLASS_NAME, Element.get_element_by_name("discountUser").getClass())
        clicked = False
        for button in buttons:
            # print(button.get_attribute("innerHTML"))
            if "Discount" in button.get_attribute("innerHTML") and button.is_enabled() and button.is_displayed():
                try:
                    Settings.dev_print("clicking discount btn")
                    button.click()
                    Settings.dev_print("clicked discount btn")
                    clicked = True
                    break
                except Exception as e:
                    Driver.error_checker(e)
                    Settings.warn_print("unable to click discount btn for: {}".format(username))
                    return False
        if not clicked:
            Settings.warn_print("unable to find discount btn for: {}".format(username))
            return False
        time.sleep(1)

        def apply_discount():
            Settings.maybe_print("attempting discount entry...")
            Settings.dev_print("finding months and discount amount btns")
            ## amount
            discountEle = driver.browser.find_elements(By.CLASS_NAME, Element.get_element_by_name("discountUserAmount").getClass())[0]
            discountAmount = int(discountEle.get_attribute("innerHTML").replace("% discount", ""))
            if not Driver.originalAmount: Driver.originalAmount = discountAmount
            Settings.dev_print("amount: {}".format(discountAmount))
            Settings.dev_print("entering discount amount")
            if int(discountAmount) != int(amount):
                up_ = int((discountAmount / 5) - 1)
                down_ = int((int(amount) / 5) - 1)
                Settings.dev_print("up: {}".format(up_))
                Settings.dev_print("down: {}".format(down_))
                action = ActionChains(driver.browser)
                action.click(on_element=discountEle)
                action.pause(1)
                for n in range(up_):
                    action.send_keys(Keys.UP)
                    action.pause(0.5)
                for n in range(down_):
                    action.send_keys(Keys.DOWN)
                    action.pause(0.5)                
                action.send_keys(Keys.TAB)
                action.perform()
            Settings.dev_print("successfully entered discount amount")
            ## months
            monthsEle = driver.browser.find_elements(By.CLASS_NAME, Element.get_element_by_name("discountUserMonths").getClass())[1]
            monthsAmount = int(monthsEle.get_attribute("innerHTML").replace(" months", "").replace(" month", ""))
            if not Driver.originalMonths: Driver.originalMonths = monthsAmount
            Settings.dev_print("months: {}".format(monthsAmount))
            Settings.dev_print("entering discount months")
            if int(monthsAmount) != int(months):
                up_ = int(monthsAmount - 1)
                down_ = int(int(months) - 1)
                Settings.dev_print("up: {}".format(up_))
                Settings.dev_print("down: {}".format(down_))
                action = ActionChains(driver.browser)
                action.click(on_element=monthsEle)
                action.pause(1)
                for n in range(up_):
                    action.send_keys(Keys.UP)
                    action.pause(0.5)
                for n in range(down_):
                    action.send_keys(Keys.DOWN)
                    action.pause(0.5)
                action.send_keys(Keys.TAB)
                action.perform()
            Settings.dev_print("successfully entered discount months")
            discountEle = driver.browser.find_elements(By.CLASS_NAME, Element.get_element_by_name("discountUserAmount").getClass())[0]
            discountAmount = int(discountEle.get_attribute("innerHTML").replace("% discount", ""))
            monthsEle = driver.browser.find_elements(By.CLASS_NAME, Element.get_element_by_name("discountUserMonths").getClass())[1]
            monthsAmount = int(monthsEle.get_attribute("innerHTML").replace(" months", "").replace(" month", ""))
            return discountAmount, monthsAmount

        # discount method is repeated until values are correct because somehow it occasionally messes up...
        discountAmount, monthsAmount = apply_discount()
        while int(discountAmount) != int(amount) and int(monthsAmount) != int(months):
            # Settings.print("{} = {}    {} = {}".format(discountAmount, amount, monthsAmount, months))
            discountAmount, monthsAmount = apply_discount()

        Settings.debug_delay_check()
        ## apply
        Settings.dev_print("applying discount")
        buttons_ = driver.find_elements_by_name("discountUserButton")
        for button in buttons_:
            if not button.is_enabled() and not button.is_displayed(): continue
            if "Cancel" in button.get_attribute("innerHTML") and str(Settings.is_debug()) == "True":
                Settings.print("skipping save discount (debug)")
                button.click()
                Settings.dev_print("successfully canceled discount")
                Settings.dev_print("### Discount Successful ###")
                return True
            elif "Cancel" in button.get_attribute("innerHTML") and int(discountAmount) == int(Driver.originalAmount) and int(monthsAmount) == int(Driver.originalMonths):
                Settings.print("skipping existing discount")
                button.click()
                Settings.dev_print("successfully skipped existing discount")
                Settings.dev_print("### Discount Successful ###")
                # return True
            elif "Apply" in button.get_attribute("innerHTML"):
                button.click()
                Settings.print("discounted: {}".format(username))
                Settings.dev_print("successfully applied discount")
                Settings.dev_print("### Discount Successful ###")
                return True
        Settings.dev_print("### Discount Failure ###")
        return False
    except Exception as e:
        Settings.print(e)
        Driver.error_checker(e)
        buttons_ = driver.find_elements_by_name("discountUserButton")
        for button in buttons_:
            if "Cancel" in button.get_attribute("innerHTML"):
                button.click()
                Settings.dev_print("### Discount Successful Failure ###")
                return False
        Settings.dev_print("### Discount Failure ###")
        return False
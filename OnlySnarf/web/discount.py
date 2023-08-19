
from ..util.settings import Settings

def discount_user(discount):
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

    if not discount or not discount.is_valid():
        Settings.err_print("missing or invalid discount!")
        return False

    driver = Driver.get_driver()
    driver.auth()
    
    Settings.print(f"Discounting {discount["username"]} {discount["amount"]}% for {discount["months"]} month(s)")

    try:
        user = search_for_fan(driver, username, reattempt=True)
        # ActionChains(driver.browser).move_to_element(user).perform()

        click_discount_button(user)
        
        # discount method is repeated until values are correct because somehow it occasionally messes up...
        discount_amount, discount_months = apply_discount_values(driver, discount["amount"], discount["months"])
        while int(discount_amount) != int(discount["amount"]) and int(discount_months) != int(discount["months"]):
            Settings.dev_print("repeating discount amount & months...")
            discount_amount, discount_months = apply_discount()

        Settings.debug_delay_check()

        Settings.dev_print("applying discount")

        if Settings.is_debug():
            return cancel_discount(driver)
        else:
            return apply_discount(driver)

    except Exception as e:
        Driver.error_checker(e)
    return cancel_discount(driver, onsuccess=False)

def apply_discount_values(driver, amount, months):
    apply_discount_amount(driver, int(amount))
    apply_discount_months(driver, int(months))
    amount_element, discount_amount = get_discount_amount(driver)
    months_element, discount_months = get_discount_months(driver)
    return discount_amount, discount_months

def apply_discount(driver):
    buttons = driver.find_elements_by_name("discountUserButton")
    for button in buttons:
        if not button.is_enabled() and not button.is_displayed(): continue
        if "Apply" in button.get_attribute("innerHTML"):
            button.click()
            Settings.dev_print("### Discount Successful ###")
            Settings.print("Discount successful!")
            return True
    Settings.err_print("### Discount Failure - Missing Apply Button ###")
    return False

def cancel_discount(driver, onsuccess=True):
    # {
    #     "name": "discountUserButton",
    #     "classes": ["g-btn.m-flat.m-btn-gaps.m-reset-width", "g-btn.m-rounded"],
    #     "text": ["Apply"],
    #     "id": []
    # }
    buttons = driver.find_elements_by_name("discountUserButton")
    for button in buttons:
        if "Cancel" in button.get_attribute("innerHTML"):
            button.click()
            if onsuccess:
                Settings.dev_print("### Discount Successfully Canceled ###")
                Settings.print("Discount canceled!")
                return True
            else:
                Settings.print("Discount failed!")
                Settings.dev_print("### Discount Failure ###")
                return False
    Settings.err_print("### Discount Failure - Missing Cancel Button ###")
    return False

def click_discount_button(element):
    buttons = element.find_elements(By.CLASS_NAME, "b-tabs__nav__text")
    Settings.dev_print("finding discount btn")
    for button in buttons:
        # print(button.get_attribute("innerHTML"))
        if "Discount" in button.get_attribute("innerHTML") and button.is_enabled() and button.is_displayed():
            try:
                Settings.dev_print("clicking discount btn")
                button.click()
                Settings.dev_print("clicked discount btn")
                time.sleep(0.5)
                return True
            except Exception as e:
                Driver.error_checker(e)
                Settings.warn_print("unable to click discount btn for: {}".format(element.get_attribute("innerHTML").strip()))
                return False
    Settings.warn_print("unable to find discount btn for: {}".format(element.get_attribute("innerHTML").strip()))
    return False

def get_discount_amount(driver):
    amount_element = driver.browser.find_elements(By.CLASS_NAME, "v-select__selection.v-select__selection--comma")[0]
    amount = int(amount_element.get_attribute("innerHTML").replace("% discount", ""))
    Settings.dev_print(f"discount amount: {amount}")
    return amount_element, amount

def get_discount_months(driver):
    months_element = driver.browser.find_elements(By.CLASS_NAME, "v-select__selection.v-select__selection--comma")[1]
    months = int(months_element.get_attribute("innerHTML").replace(" months", "").replace(" month", ""))
    Settings.dev_print(f"discount months: {months}")
    return months_element, months
    
def apply_discount_amount(driver, amount):
    Settings.maybe_print("attempting discount amount entry...")
    # amount_element = driver.browser.find_elements(By.CLASS_NAME, "v-select__selection.v-select__selection--comma")[0]
    # discount_amount = int(amount_element.get_attribute("innerHTML").replace("% discount", ""))
    amount_element, discount_amount = get_discount_amount(driver)
    Settings.dev_print("amount: {}".format(discount_amount))
    Settings.dev_print("entering discount amount")
    if int(discount_amount) != int(amount):
        up_ = int((discount_amount / 5) - 1)
        down_ = int((int(amount) / 5) - 1)
        Settings.dev_print("up: {}".format(up_))
        Settings.dev_print("down: {}".format(down_))
        action = ActionChains(driver.browser)
        action.click(on_element=amount_element)
        action.pause(1)
        for n in range(up_):
            action.send_keys(Keys.UP)
            action.pause(0.5)
        for n in range(down_):
            action.send_keys(Keys.DOWN)
            action.pause(0.5)                
        action.send_keys(Keys.TAB)
        action.perform()
    Settings.dev_print("successfully entered discount amount!")

def apply_discount_months(driver, months):
    Settings.maybe_print("attempting discount months entry...")
    # months_element = driver.browser.find_elements(By.CLASS_NAME, "v-select__selection.v-select__selection--comma")[1]
    # discount_months = int(months_element.get_attribute("innerHTML").replace(" months", "").replace(" month", ""))
    months_element, discount_months = get_discount_months(driver)
    Settings.dev_print("months: {}".format(discount_months))
    Settings.dev_print("entering discount months")
    if int(discount_months) != int(months):
        up_ = int(discount_months - 1)
        down_ = int(int(months) - 1)
        Settings.dev_print("up: {}".format(up_))
        Settings.dev_print("down: {}".format(down_))
        action = ActionChains(driver.browser)
        action.click(on_element=months_element)
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

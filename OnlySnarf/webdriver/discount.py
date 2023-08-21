
from .element import find_element_to_click
from .user import get_user_by_username
from ..classes.discount import Discount
from ..util.settings import Settings

def discount_user(discount_object=Discount()):
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

    if not discount_object or not discount_object.is_valid():
        Settings.err_print("missing or invalid discount!")
        return False

    browser = Driver.get_browser()    
    Settings.print(f"Discounting {discount_object["username"]} {discount_object["amount"]}% for {discount_object["months"]} month(s)")

    try:
        user = get_user_by_username(browser, username, reattempt=True)
        click_discount_button(user)
        
        # discount method is repeated until values are correct because somehow it occasionally messes up...
        discount_amount, discount_months = apply_discount_values(browser, discount_object["amount"], discount_object["months"])
        while int(discount_amount) != int(discount_object["amount"]) and int(discount_months) != int(discount_object["months"]):
            Settings.dev_print("repeating discount amount & months...")
            discount_amount, discount_months = apply_discount()

        if Settings.is_debug():
            return cancel_discount(browser)
        else:
            return apply_discount(browser)
    except Exception as e:
        Driver.error_checker(e)
    return cancel_discount(browser, onsuccess=False)

def apply_discount_values(browser, amount, months):
    apply_discount_amount(browser, int(amount))
    apply_discount_months(browser, int(months))
    amount_element, discount_amount = get_discount_amount(browser)
    months_element, discount_months = get_discount_months(browser)
    return discount_amount, discount_months

def apply_discount(browser):
    try:
        Settings.dev_print("applying discount...")
        find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Apply").click()
        Settings.dev_print("### Discount Successful ###")
        Settings.print("Discount successful!")
        Settings.debug_delay_check()
        return True
    except Exception as e:
        Settings.dev_print("### Discount Failure - Missing Apply Button ###")
        Settings.err_print(e)
    return False

def cancel_discount(browser, onsuccess=True):
    try:
        Settings.dev_print("canceling discount...")
        find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Cancel").click()
        if onsuccess:
            Settings.dev_print("### Discount Successfully Canceled ###")
            Settings.print("Discount canceled!")
            Settings.debug_delay_check()
            return True
        else:
            Settings.print("Discount failed!")
            Settings.dev_print("### Discount Failure ###")
    except Exception as e:
        Settings.dev_print("### Discount Failure - Missing Cancel Button ###")
        Settings.err_print(e)
    return False

def click_discount_button(user_element):
    try:
        Settings.dev_print("clicking discount btn...")
        find_element_to_click(user_element, "b-tabs__nav__text", text="Discount").click()
        Settings.dev_print("clicked discount btn")
        time.sleep(0.5)
        Settings.debug_delay_check()
        return True
    except Exception as e:
        Driver.error_checker(e)
    Settings.warn_print(f"unable to click discount btn for: {element.get_attribute("innerHTML").strip()}")
    return False

def get_discount_amount(browser):
    amount_element = browser.find_elements(By.CLASS_NAME, "v-select__selection.v-select__selection--comma")[0]
    amount = int(amount_element.get_attribute("innerHTML").replace("% discount", ""))
    Settings.dev_print(f"discount amount: {amount}")
    return amount_element, amount

def get_discount_months(browser):
    months_element = browser.find_elements(By.CLASS_NAME, "v-select__selection.v-select__selection--comma")[1]
    months = int(months_element.get_attribute("innerHTML").replace(" months", "").replace(" month", ""))
    Settings.dev_print(f"discount months: {months}")
    return months_element, months
    
def apply_discount_amount(browser, amount):
    Settings.maybe_print("attempting discount amount entry")
    # amount_element = driver.browser.find_elements(By.CLASS_NAME, "v-select__selection.v-select__selection--comma")[0]
    # discount_amount = int(amount_element.get_attribute("innerHTML").replace("% discount", ""))
    amount_element, discount_amount = get_discount_amount(browser)
    Settings.dev_print("amount: {}".format(discount_amount))
    Settings.maybe_print("entering discount amount...")
    if int(discount_amount) != int(amount):
        up_ = int((discount_amount / 5) - 1)
        down_ = int((int(amount) / 5) - 1)
        Settings.dev_print("up: {}".format(up_))
        Settings.dev_print("down: {}".format(down_))
        action = ActionChains(browser)
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
    Settings.debug_delay_check()

def apply_discount_months(browser, months):
    Settings.maybe_print("attempting discount months entry")
    # months_element = driver.browser.find_elements(By.CLASS_NAME, "v-select__selection.v-select__selection--comma")[1]
    # discount_months = int(months_element.get_attribute("innerHTML").replace(" months", "").replace(" month", ""))
    months_element, discount_months = get_discount_months(browser)
    Settings.dev_print("months: {}".format(discount_months))
    Settings.maybe_print("entering discount months...")
    if int(discount_months) != int(months):
        up_ = int(discount_months - 1)
        down_ = int(int(months) - 1)
        Settings.dev_print("up: {}".format(up_))
        Settings.dev_print("down: {}".format(down_))
        action = ActionChains(browser)
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
    Settings.dev_print("successfully entered discount months!")
    Settings.debug_delay_check()

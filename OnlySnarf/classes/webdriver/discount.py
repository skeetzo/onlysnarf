import time
import logging
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .element import find_element_to_click
from .errors import error_checker
from .users import get_user_by_username
from .. import CONFIG, debug_delay_check

def discount_user(browser, discount_object):
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

    if not discount_object:
        logging.error("missing discount!")
        return False
    logging.info(f"Discounting {discount_object['username']} {discount_object['amount']}% for {discount_object['months']} month(s)")
    try:
        user = get_user_by_username(browser, discount_object['username'], reattempt=True)
        if not user: raise Exception("unable to discount missing user!")
        click_discount_button(browser, user)
        # discount method is repeated until values are correct because somehow it occasionally messes up...
        discount_amount, discount_months = apply_discount_values(browser, discount_object['amount'], discount_object['months'])
        while int(discount_amount) != int(discount_object['amount']) and int(discount_months) != int(discount_object['months']):
            logging.debug("repeating discount amount & months...")
            discount_amount, discount_months = apply_discount()
        if CONFIG["debug"]:
            return cancel_discount(browser)
        else:
            return apply_discount(browser)
    except Exception as e:
        error_checker(e)
    return cancel_discount(browser, onsuccess=False)

def apply_discount_values(browser, amount, months):
    apply_discount_amount(browser, int(amount))
    apply_discount_months(browser, int(months))
    amount_element, discount_amount = get_discount_amount(browser)
    months_element, discount_months = get_discount_months(browser)
    return discount_amount, discount_months

def apply_discount(browser):
    try:
        logging.debug("applying discount...")
        find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Apply").click()
        logging.debug("### Discount Successful ###")
        logging.info("Discount successful!")
        debug_delay_check()
        return True
    except Exception as e:
        logging.debug("### Discount Failure - Missing Apply Button ###")
        logging.error(e)
    return False

def cancel_discount(browser, onsuccess=True):
    try:
        logging.debug("canceling discount...")
        find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Cancel").click()
        if onsuccess:
            logging.debug("### Discount Successfully Canceled ###")
            logging.info("Discount canceled!")
            debug_delay_check()
            return True
        else:
            logging.info("Discount failed!")
            logging.debug("### Discount Failure ###")
    except Exception as e:
        logging.debug("### Discount Failure - Missing Cancel Button ###")
        logging.error(e)
    return False

def click_discount_button(browser, user_element, retry=False):
    try:
        logging.debug("clicking discount btn...")
        button = find_element_to_click(user_element, "b-tabs__nav__text", text="Discount")
        # scroll into view to prevent element from being obscured by menu at top of page
        browser.execute_script("return arguments[0].scrollIntoView(true);", button)
        button.click()
        logging.debug("clicked discount btn")
        time.sleep(0.5)
        debug_delay_check()
        return True
    except Exception as e:
        if "obscures it" in str(e) and not retry:
            click_discount_button(browser, user_element, retry=True)
        error_checker(e)
    raise Exception(f"unable to click discount btn for: {user_element.get_attribute('innerHTML').strip()}")
    # return False

def get_discount_amount(browser):
    amount_element = browser.find_elements(By.CLASS_NAME, "v-select__selection.v-select__selection--comma")[0]
    amount = int(amount_element.get_attribute("innerHTML").replace("% discount", ""))
    logging.debug(f"discount amount: {amount}")
    return amount_element, amount

def get_discount_months(browser):
    months_element = browser.find_elements(By.CLASS_NAME, "v-select__selection.v-select__selection--comma")[1]
    months = int(months_element.get_attribute("innerHTML").replace(" months", "").replace(" month", ""))
    logging.debug(f"discount months: {months}")
    return months_element, months
    
def apply_discount_amount(browser, amount):
    logging.debug("attempting discount amount entry")
    # amount_element = driver.browser.find_elements(By.CLASS_NAME, "v-select__selection.v-select__selection--comma")[0]
    # discount_amount = int(amount_element.get_attribute("innerHTML").replace("% discount", ""))
    amount_element, discount_amount = get_discount_amount(browser)
    logging.debug(f"amount: {discount_amount}")
    logging.debug("entering discount amount...")
    if int(discount_amount) != int(amount):
        up_ = int((discount_amount / 5) - 1)
        down_ = int((int(amount) / 5) - 1)
        logging.debug(f"up: {up_}")
        logging.debug(f"down: {down_}")
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
    logging.debug("successfully entered discount amount!")
    debug_delay_check()

def apply_discount_months(browser, months):
    logging.debug("attempting discount months entry")
    # months_element = driver.browser.find_elements(By.CLASS_NAME, "v-select__selection.v-select__selection--comma")[1]
    # discount_months = int(months_element.get_attribute("innerHTML").replace(" months", "").replace(" month", ""))
    months_element, discount_months = get_discount_months(browser)
    logging.debug(f"months: {discount_months}")
    logging.debug("entering discount months...")
    if int(discount_months) != int(months):
        up_ = int(discount_months - 1)
        down_ = int(int(months) - 1)
        logging.debug(f"up: {up_}")
        logging.debug(f"down: {down_}")
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
    logging.debug("successfully entered discount months!")
    debug_delay_check()

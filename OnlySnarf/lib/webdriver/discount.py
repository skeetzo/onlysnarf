import time
import logging
logger = logging.getLogger(__name__)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .element import find_element_to_click
from .errors import error_checker
from .users import click_user_button, get_user_by_username
from .. import CONFIG, debug_delay_check

def discount(browser, discount_object):
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
        logger.error("missing discount!")
        return False
    logger.info(f"Discounting {discount_object['username']} {discount_object['amount']}% for {discount_object['months']} month(s)")
    try:
        user = get_user_by_username(browser, discount_object['username'], collection="Active")
        if not user: raise Exception("unable to discount missing user!")
        click_user_button(browser, user, text="Discount")
        # discount method is repeated until values are correct because somehow it occasionally messes up...
        discount_amount, discount_months = apply_discount_values(browser, discount_object['amount'], discount_object['months'])
        while int(discount_amount) != int(discount_object['amount']) and int(discount_months) != int(discount_object['months']):
            logger.debug("repeating discount amount & months...")
            discount_amount, discount_months = apply_discount_values(browser, discount_object['amount'], discount_object['months'])
        if CONFIG["debug"]:
            return cancel_discount(browser)
        else:
            return apply_discount(browser)
    except Exception as e:
        error_checker(e)
    logger.warning("discount failure!")
    return cancel_discount(browser)

def apply_discount(browser):
    try:
        logger.debug("applying discount...")
        find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Apply").click()
        logger.info("discount successfully applied!")
        debug_delay_check()
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("unable to apply discount!")

def cancel_discount(browser):
    try:
        logger.debug("canceling discount entry...")
        element = find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Cancel")
        if not element:
            logger.debug("skipping cancel click, missing button")
            return        
        element.click()
        logger.debug("discount successfully canceled!")
        debug_delay_check()
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("unable to cancel discount!")

def get_discount_amount(browser):
    amount_element = browser.find_elements(By.CLASS_NAME, "v-select__selection.v-select__selection--comma")[0]
    amount = int(amount_element.get_attribute("innerHTML").replace("% discount", ""))
    logger.debug(f"discount amount: {amount}")
    return amount_element, amount

def get_discount_months(browser):
    months_element = browser.find_elements(By.CLASS_NAME, "v-select__selection.v-select__selection--comma")[1]
    months = int(months_element.get_attribute("innerHTML").replace(" months", "").replace(" month", ""))
    logger.debug(f"discount months: {months}")
    return months_element, months
    
def apply_discount_amount(browser, amount):
    try:
        logger.debug("attempting discount amount entry...")
        # amount_element = driver.browser.find_elements(By.CLASS_NAME, "v-select__selection.v-select__selection--comma")[0]
        # discount_amount = int(amount_element.get_attribute("innerHTML").replace("% discount", ""))
        amount_element, discount_amount = get_discount_amount(browser)
        logger.debug(f"amount: {discount_amount}")
        logger.debug("entering discount amount...")
        if int(discount_amount) != int(amount):
            up_ = int((discount_amount / 5) - 1)
            down_ = int((int(amount) / 5) - 1)
            logger.debug(f"up: {up_}")
            logger.debug(f"down: {down_}")
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
        logger.debug("successfully entered discount amount!")
        debug_delay_check()
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("unable to apply discount amount!")

def apply_discount_months(browser, months):
    try:
        logger.debug("attempting discount months entry...")
        # months_element = driver.browser.find_elements(By.CLASS_NAME, "v-select__selection.v-select__selection--comma")[1]
        # discount_months = int(months_element.get_attribute("innerHTML").replace(" months", "").replace(" month", ""))
        months_element, discount_months = get_discount_months(browser)
        logger.debug(f"months: {discount_months}")
        logger.debug("entering discount months...")
        if int(discount_months) != int(months):
            up_ = int(discount_months - 1)
            down_ = int(int(months) - 1)
            logger.debug(f"up: {up_}")
            logger.debug(f"down: {down_}")
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
        logger.debug("successfully entered discount months!")
        debug_delay_check()
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("unable to apply discount months!")

def apply_discount_values(browser, amount, months):
    apply_discount_amount(browser, int(amount))
    apply_discount_months(browser, int(months))
    amount_element, discount_amount = get_discount_amount(browser)
    months_element, discount_months = get_discount_months(browser)
    return discount_amount, discount_months
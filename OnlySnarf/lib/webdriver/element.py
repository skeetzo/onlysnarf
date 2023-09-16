import logging
logger = logging.getLogger(__name__)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .errors import error_checker

################
### Elements ###
################

# text: the text that should be included in the element text
# isID: use id instead of class_name
# fuzzymatch: use "in" instead of "==" when matching text
# index: the index of the element to search for, used to ignore early matches
def find_element_to_click(browser, name, text="", by=By.CLASS_NAME, fuzzyMatch=False, index=-1):
    """
    Find element on page by name to click

    Does not auth check or otherwise change the focus. Checks that located element is properly 
    capable of being clicked.

    Parameters
    ----------
    name : str
        The name of the element to click as referenced from its /elements/element name

    Returns
    -------
    Selenium.WebDriver.WebElements
        The located web element that can be clicked

    """

    logger.debug(f"finding element: {name} - {text}")
    foundElement = None
    try:
        elements = browser.find_elements(by, name)
        logger.debug(f"elements found: {len(elements)}")
        i = 0
        for element in elements:
            # logger.debug(f"element: {element.get_attribute('innerHTML').strip()}")
            if element.is_displayed() and element.is_enabled() and ( (index >= 0 and i == index) or (index==-1) ):
                if text and str(text).lower().strip() == element.get_attribute("innerHTML").lower().strip():
                    logger.debug("found matching element!")
                    return element
                elif text and fuzzyMatch and str(text).lower().strip() in element.get_attribute("innerHTML").lower().strip():
                    logger.debug("found matching fuzzy element!")
                    return element
                elif not text:
                    logger.debug("found matching element!")
                    return element
            i += 1
    except Exception as e:
        error_checker(e)
    raise Exception(f"unable to find element: {name}")

def move_to_then_click_element(browser, element):
    """
    Move to then click element.
    
    From: https://stackoverflow.com/questions/44777053/selenium-movetargetoutofboundsexception-with-firefox

    Parameters
    ----------
    element : Selenium.WebDriver.WebElement
        The element to move to then click

    """

    def scroll_shim(passed_in_driver, object):
        x = object.location['x']
        y = object.location['y']
        scroll_by_coord = 'window.scrollTo(%s,%s);' % (
            x,
            y
        )
        scroll_nav_out_of_way = 'window.scrollBy(0, -120);'
        passed_in_driver.execute_script(scroll_by_coord)
        passed_in_driver.execute_script(scroll_nav_out_of_way)
    #
    try:
        ActionChains(browser).move_to_element(element).click().perform()
        return True
    except Exception as e:
        # logger.debug(e)
        # if 'firefox' in browser.capabilities['browserName']:
        try:
            scroll_shim(browser, element)
            ActionChains(browser).move_to_element(element).click().perform()
        except Exception as e:
            pass
            # logger.debug(e)
            browser.execute_script("arguments[0].scrollIntoView();", element)
            # try:
            #     browser.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)
            #     ActionChains(browser).move_to_element(element).click().perform()
            # except Exception as e:
            #     logger.debug(e)
    return False

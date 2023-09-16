import time
import logging
logger = logging.getLogger(__name__)

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import WebDriverException
# from selenium.common.exceptions import NoSuchElementException

from .element import find_element_to_click
from .errors import error_checker
from .goto import go_to_home

def clear_text(browser):
    try:
        # BUGS: only backspace method is working
        # TODO: fix this horribly inefficient loop; maybe add a way that checks for text in field and deltes until gone?
        #       reimplement methods in a way that allows for continuous debugging
        element = WebDriverWait(browser, 3).until(EC.visibility_of_element_located((By.ID, 'new_post_text_input')))
        for i in range(300):
            element.send_keys(Keys.BACK_SPACE)
        logger.debug("successfully cleared text!")
    # broken method one:
        # print(element.get_attribute("innerHTML"))
        # element.click()
        # element.clear()
    # broken method two:
        # action = ActionChains(browser)
        # action.move_to_element(element)
        # action.click(on_element=element)
        # action.double_click()
        # action.click_and_hold()
        # action.send_keys(Keys.CLEAR)
        # action.perform()
    # broken method 3:
        # # action.send_keys(Keys.CONTROL + "a")
        # action.send_keys(Keys.DELETE)
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to clear text!")

def click_clear_button(browser, reattempt=False):
    try:
        logger.debug("clicking clear button...")
        find_element_to_click(browser, "button", by=By.TAG_NAME, text="Clear").click()
        logger.debug("successfully clicked clear button!")
        return True
    except Exception as e:
        # if "obscures element" in str(e).lower() and not reattempt:
        if not reattempt:
            go_to_home(browser, force=True)
            element = browser.find_element(By.ID, "new_post_text_input")
            action = ActionChains(browser)
            action.move_to_element(element)
            action.click(on_element=element)
            action.perform()
            time.sleep(0.5) # needs to load: TODO: possibly add wait
            return click_clear_button(browser, reattempt=True)
        # error_checker(e)
    logger.debug("unable to click clear button!")
    # raise Exception("failed to click clear button!")

def click_close_icons(browser):
    try:
        logger.debug("clicking close icons...")
        while len(browser.find_elements(By.CLASS_NAME, "b-dropzone__preview__delete")) > 0:
            for element in browser.find_elements(By.CLASS_NAME, "b-dropzone__preview__delete"):
                ActionChains(browser).move_to_element(element).click().perform()
                logger.debug("successfully clicked close icon!")
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to click close icons!")

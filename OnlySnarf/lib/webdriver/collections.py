import time
import logging
logger = logging.getLogger(__name__)

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import TimeoutException
# from selenium.common.exceptions import WebDriverException

from .element import find_element_to_click
from .errors import error_checker
from .. import debug_delay_check
# from .. import CONFIG

# searches for a single '#icon-done'
def check_clear_collections(browser, reattempt=False):
    try:
        for element in browser.find_elements(By.TAG_NAME, "use"):
            if '#icon-done' in str(element.get_attribute('href')) and element.is_displayed():
                return True
    except Exception as e:
        if "stale element" in str(e) and not reattempt:
            logger.debug('reattempting message_list...')
            if not reattempt: return check_clear_collections(browser, reattempt=True)
    logger.debug("no collections to clear!")
    return False

# when clearing lists, just open the list menu for both and deselect every option available
def clear_collections(browser, includes=[], excludes=[]):
    if not check_clear_collections(browser): return True
    logger.debug("clearing collections...")
    try:
        click_collections(browser, includes=includes, excludes=excludes, unclick=True)
        logger.debug("successfully cleared collections!")
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to clear user collections!")

# click 1st or 2nd 'View All'
def click_view_all(browser, include=True):
    try:
        elements = browser.find_elements(By.CLASS_NAME, "b-content-filter__group-btns")
        element = None
        if include:
            logger.debug("clicking view all 1...")
            element = elements[0]
        elif not include and len(elements) > 1:
            logger.debug("clicking view all 2...")
            element = elements[1] 
        ActionChains(browser).move_to_element(element).click().perform()
        time.sleep(1)
        logger.debug("clicked view all button")
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to click view all collections!")

# click existing list available
def click_collection_button(browser, collection, unclick=False, reattempt=False):
    logger.debug(f"{'unclicking' if unclick else 'clicking'} collection button: {collection}")
    try:
        for element in browser.find_elements(By.CLASS_NAME, "b-rows-lists__item__label"):
            if str(collection).lower().strip() in str(element.get_attribute("innerHTML")).lower().strip():
                if unclick:
                    try:
                        checkbox = element.find_element(By.CLASS_NAME, "b-input-radio")
                        if not checkbox.is_selected():
                            logger.debug(f"not unclicking not clicked element: {collection}")
                            return True
                        # parent_element = element.find_element(By.XPATH, '..')
                        # icon_done = element.find_element(By.TAG_NAME, "use")
                        # if not icon_done: continue
                    except Exception as e:
                        error_checker(e)
                        continue
                logger.debug(f"{'unclicking' if unclick else 'clicking'} on collection element...")
                ActionChains(browser).move_to_element(element).click(on_element=element).perform()
                return True
    except Exception as e:
        # if "stale element" in str(e) and not reattempt:
        if not reattempt:
            logger.debug("reattempting clicking collection button (stale element)...")
            return click_collection_button(browser, collection, unclick=unclick, reattempt=True)
        error_checker(e)
    raise Exception(f"failed to {'unclick' if unclick else 'click'} on collection: {collection}")

# search for list
def search_for_collection(browser, collection):
    try:
        logger.debug(f"searching for collection: {collection}")
        elements = browser.find_elements(By.TAG_NAME, "use")
        element = [elem for elem in elements if '#icon-search' in str(elem.get_attribute('href'))][0]
        ActionChains(browser).move_to_element(element).click(on_element=element).click().send_keys(collection).perform()
        time.sleep(1)
        return True
    except Exception as e:
        error_checker(e)
    raise Exception(f"failed to search for collection: {collection}")

# when clicking lists, do multiple labels at the same time while having the list selection open
# Fans is synonymous with All
def click_collections(browser, includes=[], excludes=[], unclick=False):

    def attempt_collections_by_filter(collections, include=True):
        click_view_all(browser, include=include)
        for collection in collections:
            if collection.lower() == "all":
                collection = "Fans"
            elif collection.lower() == "recent" and include:
                message_recent(browser)
                continue
            logger.debug(f"attempting to {'unclick' if unclick else 'click'}: {collection}")
            try:
                click_collection_button(browser, collection, unclick=unclick)
            except Exception as e:
                search_for_collection(browser, collection)
                click_collection_button(browser, collection, unclick=unclick)
            # if successful: continue
            # raise Exception(f"failed to click list: {collection}")
        find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Done").click()

    try:
        if len(includes) > 0:
            attempt_collections_by_filter(includes, include=True)
        if len(excludes) > 0:
            attempt_collections_by_filter(excludes, include=False)
        return True
    except Exception as e:
        error_checker(e)
    raise Exception("failed to click collections!")

# TODO: ADD SCHEDULE BEHAVIOR HERE
def message_recent(browser, exclude=False, unclick=False):
    try:
        logger.debug("clicking message recipients: recent")
        element = find_element_to_click(browser, "b-tabs__nav__text", text="Recent", fuzzyMatch=True)

        if unclick:
            try:
                icon_done = element.find_element(By.TAG_NAME, "use")
                if not icon_done: return True
            except Exception as e:
                print(e)
                return False
            logger.debug("unclicking on collection element...")
            ActionChains(browser).move_to_element(element).click(on_element=element).perform()

            # find_element_to_click(browser, "g-btn.m-flat.m-btn-gaps.m-reset-width", text="Done").click()
        else:
            # TODO: add method for interacting with popup calendar for selecting date for recent subscribers
            logger.error("TODO: FINISH ME")

        return True

    except Exception as e:
        error_checker(e)
    raise Exception("failed to message all recent!")
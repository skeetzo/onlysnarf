import time
import logging
logger = logging.getLogger(__name__)

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

from .. import ONLYFANS_HOME_URL, ONLYFANS_SETTINGS_URL
from .. import CONFIG, DEFAULT

##############
### Go Tos ###
##############

# TODO: finally combine with go_to_page?
def go_to_home(browser, force=False):
    """
    Go to home page

    If already at home don't go unless forced

    Parameters
    ----------
    force : bool
        Force page goto even if already at url

    """

    def goto():
        logger.debug("goto -> onlyfans.com")
        try:
            browser.set_page_load_timeout(10)
            browser.get(ONLYFANS_HOME_URL)
        except TimeoutException:
            logger.warning("timed out waiting for page load!")
        except WebDriverException as e:
            logger.debug("error fetching home page!")
            logger.error(e)
        handle_alert(browser)
        get_page_load(browser)
    if force: return goto()
    if search_for_tab(browser, ONLYFANS_HOME_URL, force=force):
        logger.debug("found -> /")
        return
    logger.debug(f"current url: {browser.current_url}")
    if str(browser.current_url) == str(ONLYFANS_HOME_URL):
        logger.debug("already at -> onlyfans.com")
        browser.execute_script("window.scrollTo(0, 0);")
    else: goto()        
    
def go_to_page(browser, page, force=False):
    """
    Go to page

    If already at page don't go

    Parameters
    ----------
    page : str
        The url of the OnlyFans 'page' to go to

    """

    if search_for_tab(browser, page, force=force):
        logger.debug(f"found -> {page}")
        browser.execute_script("window.scrollTo(0, 0);")
    elif str(browser.current_url) == str(page) or (str(page) in str(browser.current_url) and not force):
        logger.debug(f"already at -> {page}")
        browser.execute_script("window.scrollTo(0, 0);")
    else:
        logger.debug(f"goto -> {page}")
        open_tab(browser, page)
        handle_alert(browser)
        get_page_load(browser)

def go_to_profile(browser):
    """Go to OnlyFans profile page"""

    username = CONFIG["username"]
    page = f"{ONLYFANS_HOME_URL}/{username}"
    if search_for_tab(browser, page):
        logger.debug(f"found -> /{username}")
        return
    if str(username) in str(browser.current_url):
        logger.debug(f"already at -> {username}")
        browser.execute_script("window.scrollTo(0, 0);")
    else:
        logger.debug(f"goto -> {username}")
        open_tab(browser, page)
        get_page_load(browser)

# onlyfans.com/my/settings
def go_to_settings(browser, settingsTab):
    """
    Go to settings tab on settings page

    If already at tab, stay

    Parameters
    ----------
    settingsTab : str
        The name of the Settings tab to go to

    """

    if search_for_tab(browser, f"{ONLYFANS_SETTINGS_URL}{settingsTab}"):  
        logger.debug(f"found -> settings/{settingsTab}")
        return
    if str(ONLYFANS_SETTINGS_URL) in str(browser.current_url) and str(settingsTab) == "profile":
        logger.debug(f"at -> onlyfans.com/settings/{settingsTab}")
        browser.execute_script("window.scrollTo(0, 0);")
    else:
        if str(settingsTab) == "profile": settingsTab = ""
        logger.debug(f"goto -> onlyfans.com/settings/{settingsTab}")
        go_to_page(f"{ONLYFANS_SETTINGS_URL}{settingsTab}")

############
### Tabs ###
############

# https://stackoverflow.com/questions/50844779/how-to-handle-multiple-windows-in-python-selenium-with-firefox-driver
def open_tab(browser, url):
    """
    Open new tab of url

    Parameters
    ----------
    url : str
        The url to open in a new tab

    Returns
    -------
    bool
        Whether or not the tab was opened successfully

    """

    logger.debug(f"opening tab -> {url}")
    windows_before  = browser.current_window_handle
    logger.debug(f"current window handle is : {windows_before}")
    windows = browser.window_handles
    browser.execute_script('''window.open("{}","_blank");'''.format(url))
    # handle_alert(browser)
    # get_page_load(browser)
    WebDriverWait(browser, 10, poll_frequency=1).until(EC.number_of_windows_to_be(len(windows)+1))
    windows_after = browser.window_handles
    new_window = [x for x in windows_after if x not in windows][0]
    browser.switch_to.window(new_window)
    logger.debug(f"page title after tab switching is : {browser.title}")
    logger.debug(f"new window handle is : {new_window}")
    # global TABS
    # if len(TABS) >= DEFAULT.MAX_TABS:
    #     least = TABS[0]
    #     for i, tab in enumerate(TABS):
    #         if int(tab[2]) < int(least[2]):
    #             least = tab
    #     TABS.remove(least)
    # TABS.append([url, new_window, 0]) # url, window_handle, use count

def search_for_tab(browser, page, force=False):
    """
    Search for (and goto if exists) tab in tabs cache

    Parameters
    ----------
    page : str
        The url of the OnlyFans 'page' to go to

    Returns
    -------
    bool
        Whether or not the tab exists


    """

    original_handle = browser.current_window_handle
    logger.debug(f"searching for page: {page}")
    logger.debug(f"handles: {browser.window_handles}")
    try:
        logger.debug("checking handles...")
        for handle in browser.window_handles:
            logger.debug(handle)
            browser.switch_to.window(handle)
            if force:
                print(f"{page} == {browser.current_url}")
                if str(page) == str(browser.current_url).replace(ONLYFANS_HOME_URL, ""):
                    logger.debug(f"successfully located exact tab in handles: {page}")
                    return True
            else:
                if str(page) in str(browser.current_url):
                    logger.debug(f"successfully located tab in handles: {page}")
                    return True
        logger.debug(f"failed to locate tab: {page}")
        browser.switch_to.window(original_handle)
    except Exception as e:
        # if "Unable to locate window" not in str(e):
        logger.debug(e)
    return False

# waits for page load
def get_page_load(browser):
    """Attempt to generic page load"""

    try:
        WebDriverWait(browser, 60*2, poll_frequency=1).until(EC.visibility_of_element_located((By.CLASS_NAME, "main-wrapper")))
    except Exception as e:
        logger.error(e)

def handle_alert(browser):
    """Switch to alert pop up"""

    try:
        alert_obj = browser.switch_to.alert or None
        if alert_obj:
            alert_obj.accept()
    except: pass

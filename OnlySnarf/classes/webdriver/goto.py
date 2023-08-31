import time
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

from .. import ONLYFANS_HOME_URL, ONLYFANS_SETTINGS_URL
from .. import CONFIG, DEFAULT

TABS = []

##############
### Go Tos ###
##############

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
        logging.debug("goto -> onlyfans.com")
        try:
            browser.set_page_load_timeout(10)
            browser.get(ONLYFANS_HOME_URL)
        except TimeoutException:
            logging.warning("timed out waiting for page load!")
        except WebDriverException as e:
            logging.debug("error fetching home page!")
            logging.error(e)
        handle_alert(browser)
        get_page_load(browser)
    if force: return goto()
    if search_for_tab(browser, ONLYFANS_HOME_URL):
        logging.debug("found -> /")
        return
    logging.debug(f"current url: {browser.current_url}")
    if str(browser.current_url) == str(ONLYFANS_HOME_URL):
        logging.debug("already at -> onlyfans.com")
        browser.execute_script("window.scrollTo(0, 0);")
    else: goto()        
    
def go_to_page(browser, page):
    """
    Go to page

    If already at page don't go

    Parameters
    ----------
    page : str
        The url of the OnlyFans 'page' to go to

    """

    if search_for_tab(browser, page):
        logging.debug(f"found -> {page}")
        return
    if str(browser.current_url) == str(page) or str(page) in str(browser.current_url):
        logging.debug(f"already at -> {page}")
        browser.execute_script("window.scrollTo(0, 0);")
    else:
        logging.debug(f"goto -> {page}")
        open_tab(browser, page)
        handle_alert(browser)
        get_page_load(browser)

def go_to_profile(browser):
    """Go to OnlyFans profile page"""

    username = CONFIG["username"]
    page = f"{ONLYFANS_HOME_URL}/{username}"
    if search_for_tab(browser, page):
        logging.debug(f"found -> /{username}")
        return
    if str(username) in str(browser.current_url):
        logging.debug(f"already at -> {username}")
        browser.execute_script("window.scrollTo(0, 0);")
    else:
        logging.debug(f"goto -> {username}")
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
        logging.debug(f"found -> settings/{settingsTab}")
        return
    if str(ONLYFANS_SETTINGS_URL) in str(browser.current_url) and str(settingsTab) == "profile":
        logging.debug(f"at -> onlyfans.com/settings/{settingsTab}")
        browser.execute_script("window.scrollTo(0, 0);")
    else:
        if str(settingsTab) == "profile": settingsTab = ""
        logging.debug(f"goto -> onlyfans.com/settings/{settingsTab}")
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

    logging.debug(f"opening tab -> {url}")
    windows_before  = browser.current_window_handle
    logging.debug(f"current window handle is : {windows_before}")
    windows = browser.window_handles
    browser.execute_script('''window.open("{}","_blank");'''.format(url))
    handle_alert(browser)
    get_page_load(browser)
    try:
        WebDriverWait(browser, 10, poll_frequency=1).until(EC.number_of_windows_to_be(len(windows)+1))
    except TimeoutException as te:
        logging.debug("timed out waiting for new tab!")
        logging.error(str(te))
        return
    except Exception as e:
        logging.error(e)
        return
    windows_after = browser.window_handles
    new_window = [x for x in windows_after if x not in windows][0]
    browser.switch_to.window(new_window)
    logging.debug(f"page title after tab switching is : {browser.title}")
    logging.debug(f"new window handle is : {new_window}")
    global TABS
    if len(TABS) >= DEFAULT.MAX_TABS:
        least = TABS[0]
        for i, tab in enumerate(TABS):
            if int(tab[2]) < int(least[2]):
                least = tab
        TABS.remove(least)
    TABS.append([url, new_window, 0]) # url, window_handle, use count

def search_for_tab(browser, page):
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

    global TABS
    original_handle = browser.current_window_handle
    logging.debug(f"searching for page: {page}")
    logging.debug(f"tabs: {TABS}")
    logging.debug(f"handles: {browser.window_handles}")
    try:
        logging.debug("checking tabs...")
        for page_, handle, value in TABS:
            logging.debug(f"{page_} = {page}")
            if str(page_) in str(page):
                browser.switch_to.window(handle)
                value += 1
                logging.debug(f"successfully located tab in cache: {page}")
                return True
        logging.debug("checking handles...")
        for handle in browser.window_handles:
            logging.debug(handle)
            browser.switch_to.window(handle)
            if str(page) in str(browser.current_url):
                logging.debug(f"successfully located tab in handles: {page}")
                return True
        logging.debug(f"failed to locate tab: {page}")
        browser.switch_to.window(original_handle)
    except Exception as e:
        # print(e)
        # if "Unable to locate window" not in str(e):
        logging.debug(e)
    return False

# waits for page load
def get_page_load(browser):
    """Attempt to generic page load"""

    time.sleep(2)
    try:
        WebDriverWait(browser, 60*3, poll_frequency=10).until(EC.visibility_of_element_located((By.CLASS_NAME, "main-wrapper")))
    except Exception as e:
        logging.error(e)

def handle_alert(browser):
    """Switch to alert pop up"""

    try:
        alert_obj = browser.switch_to.alert or None
        if alert_obj:
            alert_obj.accept()
    except: pass

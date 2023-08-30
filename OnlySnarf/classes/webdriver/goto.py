import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

from .. import Settings
from .. import ONLYFANS_HOME_URL, ONLYFANS_SETTINGS_URL

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
        Settings.maybe_print("goto -> onlyfans.com")
        try:
            browser.set_page_load_timeout(10)
            browser.get(ONLYFANS_HOME_URL)
        except TimeoutException:
            Settings.warn_print("timed out waiting for page load!")
        except WebDriverException as e:
            Settings.dev_print("error fetching home page!")
            Settings.err_print(e)
        handle_alert(browser)
        get_page_load(browser)
    if force: return goto()
    if search_for_tab(browser, ONLYFANS_HOME_URL):
        Settings.maybe_print("found -> /")
        return
    Settings.dev_print("current url: {}".format(browser.current_url))
    if str(browser.current_url) == str(ONLYFANS_HOME_URL):
        Settings.maybe_print("already at -> onlyfans.com")
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
        Settings.maybe_print("found -> {}".format(page))
        return
    if str(browser.current_url) == str(page) or str(page) in str(browser.current_url):
        Settings.maybe_print("already at -> {}".format(page))
        browser.execute_script("window.scrollTo(0, 0);")
    else:
        Settings.maybe_print("goto -> {}".format(page))
        open_tab(browser, page)
        handle_alert(browser)
        get_page_load(browser)

def go_to_profile(browser):
    """Go to OnlyFans profile page"""

    username = Settings.get_username()
    page = "{}/{}".format(ONLYFANS_HOME_URL, username)
    if search_for_tab(browser, page):
        Settings.maybe_print("found -> /{}".format(username))
        return
    if str(username) in str(browser.current_url):
        Settings.maybe_print("already at -> {}".format(username))
        browser.execute_script("window.scrollTo(0, 0);")
    else:
        Settings.maybe_print("goto -> {}".format(username))
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

    if search_for_tab(browser, "{}{}".format(ONLYFANS_SETTINGS_URL, settingsTab)):  
        Settings.maybe_print("found -> settings/{}".format(settingsTab))
        return
    if str(ONLYFANS_SETTINGS_URL) in str(browser.current_url) and str(settingsTab) == "profile":
        Settings.maybe_print("at -> onlyfans.com/settings/{}".format(settingsTab))
        browser.execute_script("window.scrollTo(0, 0);")
    else:
        if str(settingsTab) == "profile": settingsTab = ""
        Settings.maybe_print("goto -> onlyfans.com/settings/{}".format(settingsTab))
        go_to_page("{}{}".format(ONLYFANS_SETTINGS_URL, settingsTab))

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

    Settings.maybe_print("opening tab -> {}".format(url))
    windows_before  = browser.current_window_handle
    Settings.dev_print("current window handle is : %s" %windows_before)
    windows = browser.window_handles
    browser.execute_script('''window.open("{}","_blank");'''.format(url))
    handle_alert(browser)
    get_page_load(browser)
    try:
        WebDriverWait(browser, 10, poll_frequency=1).until(EC.number_of_windows_to_be(len(windows)+1))
    except TimeoutException as te:
        Settings.dev_print("timed out waiting for new tab!")
        Settings.err_print(str(te))
        return
    except Exception as e:
        Settings.err_print(e)
        return
    windows_after = browser.window_handles
    new_window = [x for x in windows_after if x not in windows][0]
    browser.switch_to.window(new_window)
    Settings.dev_print(f"page title after tab switching is : {browser.title}")
    Settings.dev_print(f"new window handle is : {new_window}")
    if len(tabs) >= DEFAULT.MAX_TABS:
        least = tabs[0]
        for i, tab in enumerate(tabs):
            if int(tab[2]) < int(least[2]):
                least = tab
        tabs.remove(least)
    tabs.append([url, new_window, 0]) # url, window_handle, use count

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

    original_handle = browser.current_window_handle
    Settings.dev_print("searching for page: {}".format(page))
    Settings.dev_print("tabs: {}".format(tabs))
    Settings.dev_print("handles: {}".format(browser.window_handles))
    try:
        Settings.dev_print("checking tabs...")
        for page_, handle, value in tabs:
            Settings.dev_print("{} = {}".format(page_, page))
            if str(page_) in str(page):
                browser.switch_to.window(handle)
                value += 1
                Settings.dev_print("successfully located tab in cache: {}".format(page))
                return True
        Settings.dev_print("checking handles...")
        for handle in browser.window_handles:
            Settings.dev_print(handle)
            browser.switch_to.window(handle)
            if str(page) in str(browser.current_url):
                Settings.dev_print("successfully located tab in handles: {}".format(page))
                return True
        Settings.dev_print("failed to locate tab: {}".format(page))
        browser.switch_to.window(original_handle)
    except Exception as e:
        # print(e)
        # if "Unable to locate window" not in str(e):
        Settings.dev_print(e)
    return False

# waits for page load
def get_page_load(browser):
    """Attempt to generic page load"""

    time.sleep(2)
    try:
        WebDriverWait(browser, 60*3, poll_frequency=10).until(EC.visibility_of_element_located((By.CLASS_NAME, "main-wrapper")))
    except Exception as e:
        Settings.err_print(e)

def handle_alert(browser):
    """Switch to alert pop up"""

    try:
        alert_obj = browser.switch_to.alert or None
        if alert_obj:
            alert_obj.accept()
    except: pass

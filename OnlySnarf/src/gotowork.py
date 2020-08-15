# waits for page load
def get_page_load(browser=None):
    if not browser: browser = Driver.BROWSER
    time.sleep(2)
    try: WebDriverWait(browser, 60*3, poll_frequency=10).until(EC.visibility_of_element_located((By.CLASS_NAME, "main-wrapper")))
    except Exception as e: Settings.dev_print(e)

def handle_alert(browser=None):
    if not browser: browser = Driver.BROWSER
    try:
        alert_obj = browser.switch_to.alert or None
        if alert_obj:
            alert_obj.accept()
    except: pass
    # alert = WebDriverWait(s.mydriver, 3).until(EC.alert_is_present(),"Enter Party Name")
    # alert.send_keys() – used to enter a value in the Alert text box.
    # alert.accept()
    # Settings.dev_print("alert accepted")

@staticmethod
def go_to_home(browser=None, force=False):
    if not browser: browser = Driver.BROWSER
    def goto():
        Settings.maybe_print("goto -> onlyfans.com")
        browser.get(ONLYFANS_HOME_URL)
        Driver.handle_alert(browser=browser)
        Driver.get_page_load(browser=browser)
    if force: return goto()
    Driver.search_for_tab(browser=browser, ONLYFANS_HOME_URL)
    Settings.dev_print("current url: {}".format(browser.current_url))
    if str(browser.current_url) == str(ONLYFANS_HOME_URL):
        Settings.maybe_print("at -> onlyfans.com")
        browser.execute_script("window.scrollTo(0, 0);")
    else: goto()
    
@staticmethod
def go_to_page(browser=None, page):
    if not browser: browser = Driver.BROWSER
    auth_ = Driver.auth()
    if not auth_: return False
    Driver.search_for_tab(browser=browser, page)
    if str(browser.current_url) == str(page) or str(page) in str(browser.current_url):
        Settings.maybe_print("at -> {}".format(page))
        browser.execute_script("window.scrollTo(0, 0);")
    else:
        Settings.maybe_print("goto -> {}".format(page))
        browser.get("{}{}".format(ONLYFANS_HOME_URL, page))
        Driver.handle_alert(browser=browser)
        Driver.get_page_load(browser=browser)

@staticmethod
def go_to_profile(browser=None):
    if not browser: browser = Driver.BROWSER
    auth_ = Driver.auth()
    if not auth_: return False
    username = Settings.get_username()
    if str(username) == "":
        username = Driver.get_username()
    Driver.search_for_tab(browser=browser, username)
    if str(username) in str(browser.current_url):
        Settings.maybe_print("at -> {}".format(username))
        browser.execute_script("window.scrollTo(0, 0);")
    else:
        Settings.maybe_print("goto -> {}".format(username))
        browser.get("{}{}".format(ONLYFANS_HOME_URL, username))
        Driver.handle_alert(browser=browser)
        Driver.get_page_load(browser=browser)

# onlyfans.com/my/settings
@staticmethod
def go_to_settings(browser=None, settingsTab):
    if not browser: browser = Driver.BROWSER
    auth_ = Driver.auth()
    if not auth_: return False
    Driver.search_for_tab(browser=browser, "settings/{}".format(settingsTab))
    if str(browser.current_url) == str(ONLYFANS_SETTINGS_URL) and str(settingsTab) == "profile":
        Settings.maybe_print("at -> onlyfans.com/settings/{}".format(settingsTab))
        browser.execute_script("window.scrollTo(0, 0);")
    else:
        if str(settingsTab) == "profile": settingsTab = ""
        Settings.maybe_print("goto -> onlyfans.com/settings/{}".format(settingsTab))
        Driver.go_to_page(browser=browser, "{}{}".format(ONLYFANS_SETTINGS_URL, settingsTab))

def search_for_tab(browser=None, page):
    if not browser: browser = Driver.BROWSER
    original_handle = browser.current_window_handle
    for page, handle in TABS:
        if str(page_) == str(page):
            browser.switch_to_window(handle)
            Settings.dev_print("successfully located tab in cache: {}".format(page))
            return True
    for handle in browser.window_handles[0]:
        browser.switch_to_window(handle)
        if str(browser.current_url) == str(page):
            Settings.dev_print("successfully located tab: {}".format(page))
            return True
    for handle in browser.window_handles:
        browser.switch_to_window(handle)
        if str(browser.current_url) == str(page):
            Settings.dev_print("successfully located tab in windows: {}".format(page))
            return True
    Settings.dev_print("failed to locate tab: {}".format(page))
    browser.switch_to_window(original_handle)
    return False

def open_tab(browser=None, page):
    if not browser: browser = Driver.BROWSER
    browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
    browser.get(page)
    found = False
    for page_, handle in Driver.TABS:
        if str(page_) == str(page):
            handle = browser.current_window_handle
            found = True
            break
    if not found:
        Driver.TABS.append([page, browser.current_window_handle])



import selenium.webdriver as webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from time import sleep

browser = webdriver.Firefox()
browser.get('https://www.google.com?q=python#q=python')
first_result = ui.WebDriverWait(browser, 15).until(lambda browser: browser.find_element_by_class_name('rc'))
first_link = first_result.find_element_by_tag_name('a')

main_window = browser.current_window_handle
first_link.send_keys(Keys.CONTROL + Keys.RETURN)

browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)
browser.switch_to_window(main_window)

sleep(2)

browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
browser.switch_to_window(main_window)
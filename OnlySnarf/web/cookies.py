import pickle

from .goto import go_to_home
from ..util.settings import Settings

###################
##### Cookies #####
###################

def cookies_load(browser):
    """Loads existing web browser cookies from local source"""

    if not Settings.is_cookies():
        Settings.maybe_print("skipping cookies load")
        return
    Settings.maybe_print("loading cookies...")
    try:
        if os.path.exists(Settings.get_cookies_path()):
            # must be at onlyfans.com to load cookies of onlyfans.com
            go_to_home(browser)
            file = open(Settings.get_cookies_path(), "rb")
            cookies = pickle.load(file)
            file.close()
            Settings.dev_print("cookies: ")
            for cookie in cookies:
                Settings.dev_print(cookie)
                browser.add_cookie(cookie)
            Settings.dev_print("successfully loaded cookies")
            browser.refresh()
        else: 
            Settings.warn_print("missing cookies file")
    except Exception as e:
        Settings.dev_print("error loading cookies!")
        Settings.err_print(e)

def cookies_save(browser):
    """Saves existing web browser cookies to local source"""

    if not Settings.is_cookies():
        Settings.maybe_print("skipping cookies save")
        return
    Settings.maybe_print("saving cookies...")
    try:
        # must be at onlyfans.com to save cookies of onlyfans.com
        go_to_home(browser)
        Settings.dev_print(browser.get_cookies())
        file = open(Settings.get_cookies_path(), "wb")
        pickle.dump(browser.get_cookies(), file) # "cookies.pkl"
        file.close()
        Settings.dev_print("successfully saved cookies!")
    except Exception as e:
        Settings.dev_print("failed to save cookies!")
        Settings.err_print(e)
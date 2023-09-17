import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.lib.webdriver.browser import create_browser as WEBDRIVER_create_browser
from OnlySnarf.lib.webdriver.login import login as WEBDRIVER_login, check_if_already_logged_in as WEBDRIVER_check_if_already_logged_in

configure_logs_for_module_tests("OnlySnarf.lib.webdriver.login")

class TestAuth(unittest.TestCase):

    def setUp(self):
        CONFIG["login"] = "auto"
        
    def tearDown(self):
        self.browser.quit()

    def test_login(self):
        CONFIG["cookies"] = False
        self.browser = WEBDRIVER_create_browser(CONFIG["browser"])
        assert WEBDRIVER_login(self.browser, CONFIG["login"]), "unable to login"

    def test_login_via_cookies(self):
        CONFIG["cookies"] = True
        CONFIG["debug_cookies"] = True
        self.browser = WEBDRIVER_create_browser(CONFIG["browser"])
        assert WEBDRIVER_check_if_already_logged_in(self.browser), "unable to login from cookies"

############################################################################################

if __name__ == '__main__':
    unittest.main()
import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({"debug_selenium":True,"keep":False,"show":False})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.lib.webdriver.browser import create_browser

class TestSelenium_Remote(unittest.TestCase):

    def setUp(self):
        self.browser = None
        CONFIG["remote_username"] = "skeetzo"

    def tearDown(self):
        if self.browser:
            self.browser.quit()

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.lib.driver")
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.browser")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests(flush=True)

    def test_remote_chrome(self):
        self.browser = create_browser(browserType="remote:chrome")
        assert self.browser, "unable to launch via chrome"

    def test_remote_firefox(self):
        self.browser = create_browser(browserType="remote:firefox")
        assert self.browser, "unable to launch via remote"

############################################################################################

if __name__ == '__main__':
    unittest.main()
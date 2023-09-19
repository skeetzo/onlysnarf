import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({"debug_selenium":True,"keep":True})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.lib.driver import close_browser
from OnlySnarf.lib.webdriver.browser import create_browser

class TestSnarf(unittest.TestCase):

    def setUp(self):
        self.browser = create_browser(browserType="chrome")

    def tearDown(self):
        self.browser.quit()

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.browser")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests("###FLUSH###")

    def test_chrome(self):
        assert self.browser, "unable to launch chrome"

    @unittest.skip("todo")
    def test_chrome_reconnect(self):
        close_browser()
        self.browser = create_browser(browserType="reconnect:chrome")
        assert self.browser, "unable to launch via reconnect"

############################################################################################

if __name__ == '__main__':
    unittest.main()
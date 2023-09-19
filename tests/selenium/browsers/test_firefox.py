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
        self.browser = create_browser(browserType="firefox")

    def tearDown(self):
        self.browser.quit()

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.lib.driver")
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.browser")
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.util")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests("###FLUSH###")

    def test_firefox(self):
        assert self.browser, "unable to launch firefox"

    @unittest.skip("todo")
    def test_firefox_reconnect(self):
        close_browser()
        self.browser = create_browser(browserType="reconnect:firefox")
        assert self.browser, "unable to launch via reconnect"

############################################################################################

if __name__ == '__main__':
    unittest.main()
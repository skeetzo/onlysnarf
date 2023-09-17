import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.lib.webdriver.browser import create_browser

configure_logs_for_module_tests("OnlySnarf.lib.webdriver.browser")

class TestSnarf(unittest.TestCase):

    def setUp(self):
        CONFIG["browser"] = "remote:firefox"
        CONFIG["debug_selenium"] = True
        CONFIG["keep"] = True
        self.browser = create_browser(CONFIG["browser"])

    def tearDown(self):
        self.browser.quit()

    def test_remote(self):
        config["browser"] = "remote"
        assert self.browser, "unable to launch via remote"
    
    # @unittest.skip("todo")
    # def test_remote_chrome(self):
    #     config["browser"] = "remote-chrome"
    #     self.driver.init()
    #     assert self.browser, "unable to launch via remote chrome"

    # @unittest.skip("todo")
    # def test_remote_firefox(self):
    #     config["browser"] = "remote-firefox"
    #     self.driver.init()
    #     assert self.browser, "unable to launch via remote firefox"

############################################################################################

if __name__ == '__main__':
    unittest.main()
import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({"debug_selenium":True,"keep":True})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.lib.driver import close_browser
from OnlySnarf.lib.webdriver.browser import create_browser

class TestSelenium_Remote(unittest.TestCase):

    def setUp(self):
        self.browser = create_browser(method="remote:firefox")

    def tearDown(self):
        close_browser()

    def test_remote(self):
        assert self.browser, "unable to launch via remote"

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.browser")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests("###FLUSH###")

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
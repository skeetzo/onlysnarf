import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({"debug_selenium":True,"keep":True})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.lib.driver import close_browser
from OnlySnarf.lib.webdriver.browser import create_browser

class TestSelenium_Browsers(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        close_browser()

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.lib.driver")
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.browser")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests(flush=True)

    def test_browser(self):
        assert create_browser(), "unable to create browser"

############################################################################################

if __name__ == '__main__':
    unittest.main()
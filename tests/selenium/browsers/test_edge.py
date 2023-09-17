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
        CONFIG["browser"] = "edge"
        CONFIG["debug_selenium"] = True
        CONFIG["keep"] = False
        self.browser = create_browser(CONFIG["browser"])

    def tearDown(self):
        self.browser.quit()

    def test_edge(self):
        assert self.browser, "unable to launch edge"

    # def test_edge_reconnect(self):
    #     CONFIG["keep"] = True
    #     self.browser = create_browser(CONFIG["browser"])
    #     self.browser.quit()
    #     self.browser = create_browser(CONFIG["browser"])        
    #     assert self.browser, "unable to reconnect to edge"

############################################################################################

if __name__ == '__main__':
    unittest.main()
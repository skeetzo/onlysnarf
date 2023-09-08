import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})

from OnlySnarf.lib.webdriver.browser import create_browser

class TestSeleniumBrave(unittest.TestCase):

    def setUp(self):
        CONFIG["browser"] = "brave"
        CONFIG["debug_selenium"] = True
        CONFIG["keep"] = False
        self.browser = create_browser(CONFIG["browser"])

    def tearDown(self):
        self.browser.quit()

    def test_brave(self):
        assert self.browser, "unable to launch brave"

    # def test_brave_reconnect(self):
    #     CONFIG["keep"] = True
    #     self.browser = create_browser(CONFIG["browser"])
    #     self.browser.quit()
    #     assert get_browser()
    #     self.browser = create_browser(CONFIG["browser"])        
    #     assert self.browser, "unable to reconnect to brave"

############################################################################################

if __name__ == '__main__':
    unittest.main()
import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})

from OnlySnarf.lib.webdriver.browser import create_browser

class TestSeleniumBrave(unittest.TestCase):

    def setUp(self):
        CONFIG["browser"] = "ie"
        CONFIG["debug_selenium"] = True
        CONFIG["keep"] = False
        self.browser = create_browser(CONFIG["browser"])

    def tearDown(self):
        self.browser.quit()

    def test_ie(self):
        assert self.browser, "unable to launch ie"

    # def test_ie_reconnect(self):
    #     CONFIG["keep"] = True
    #     self.browser = create_browser(CONFIG["browser"])
    #     self.browser.quit()
    #     self.browser = create_browser(CONFIG["browser"])        
    #     assert self.browser, "unable to reconnect to ie"

############################################################################################

if __name__ == '__main__':
    unittest.main()
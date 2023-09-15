import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})

# from OnlySnarf.lib.driver import close_browser
from OnlySnarf.lib.webdriver.browser import create_browser

class TestSeleniumBrave(unittest.TestCase):

    def setUp(self):
        CONFIG["browser"] = "firefox"
        CONFIG["debug_selenium"] = True
        # CONFIG["keep"] = False
        self.browser = create_browser(CONFIG["browser"])

    def tearDown(self):
        self.browser.quit()

    def test_firefox(self):
        assert self.browser, "unable to launch firefox"

    # def test_firefox_reconnect(self):
    #     CONFIG["keep"] = True
    #     self.browser = create_browser(CONFIG["browser"])
    #     close_browser()

    #     assert self.browser, "unable to keep browser open for reconnect test"

    #     self.browser = create_browser("reconnect:firefox")        
    #     assert self.browser, "unable to reconnect to firefox"

############################################################################################

if __name__ == '__main__':
    unittest.main()
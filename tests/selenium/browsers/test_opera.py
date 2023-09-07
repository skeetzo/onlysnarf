import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})

from OnlySnarf.classes.driver import create_browser

class TestSeleniumBrave(unittest.TestCase):

    def setUp(self):
        CONFIG["browser"] = "opera"
        CONFIG["debug_selenium"] = True
        CONFIG["keep"] = False
        self.browser = create_browser(CONFIG["browser"])

    def tearDown(self):
        self.browser.quit()

    def test_brave(self):
        assert self.browser, "unable to launch opera"

############################################################################################

if __name__ == '__main__':
    unittest.main()
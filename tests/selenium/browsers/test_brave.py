import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings

class TestSeleniumBrave(unittest.TestCase):

    def setUp(self):
        config["debug_selenium"] = True
        config["keep"] = False
        # config["show"] = True
        Settings.set_debug("tests")
        self.driver = Driver()

    def tearDown(self):
        # config["debug_brave"] = False
        config["show"] = False
        self.driver.exit()

    def test_brave(self):
        config["browser"] = "brave"
        # config["debug_brave"] = True
        self.driver.init()
        assert self.driver.browser, "unable to launch brave"

############################################################################################

if __name__ == '__main__':
    unittest.main()
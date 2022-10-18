import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings

class TestSeleniumChromium(unittest.TestCase):

    def setUp(self):
        config["debug_selenium"] = True
        config["keep"] = False
        # config["show"] = True
        Settings.set_debug("tests")
        self.driver = Driver()

    def tearDown(self):
        # config["debug_chromium"] = False
        config["show"] = False
        self.driver.exit()

    def test_chromium(self):
        config["browser"] = "chromium"
        # config["debug_chromium"] = True
        self.driver.init()
        assert self.driver.browser, "unable to launch chromium"

############################################################################################

if __name__ == '__main__':
    unittest.main()
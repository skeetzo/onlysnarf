import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings

class TestSeleniumReconnectChromium(unittest.TestCase):

    def setUp(self):
        config["debug_selenium"] = True
        config["keep"] = True
        # config["show"] = True
        Settings.set_debug("tests")
        self.driver = Driver()

    def tearDown(self):
        config["debug_selenium"] = False
        config["keep"] = False
        config["show"] = False
        self.driver.exit()

    def test_reconnect_chromium(self):
        config["browser"] = "chromium"
        self.driver.init()
        self.driver.exit()
        config["browser"] = "auto"
        self.driver.init()
        assert self.driver.browser, "unable to launch via reconnect chromium"

############################################################################################

if __name__ == '__main__':
    unittest.main()
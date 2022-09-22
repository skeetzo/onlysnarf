import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings
# from OnlySnarf.snarf import Snarf
# from OnlySnarf.classes.user import User

class TestSeleniumReconnect(unittest.TestCase):

    def setUp(self):
        # config["cookies"] = True
        config["debug_selenium"] = True
        config["keep"] = True
        # config["show"] = True
        Settings.set_debug("tests")
        self.driver = Driver()

    def tearDown(self):
        # config["cookies"] = False
        config["debug_selenium"] = False
        config["keep"] = False
        # config["show"] = False
        self.driver.exit()
    
    def test_reconnect(self):
        config["browser"] = "auto"
        self.driver.init()
        self.driver.exit()
        config["browser"] = "reconnect"
        self.driver.init()
        assert self.driver.browser, "unable to launch via reconnect"

    def test_reconnect_chrome(self):
        config["browser"] = "chrome"
        self.driver.init()
        self.driver.exit()
        config["browser"] = "reconnect-chrome"
        self.driver.init()
        assert self.driver.browser, "unable to launch via reconnect chrome"

    def test_reconnect_firefox(self):
        config["browser"] = "firefox"
        self.driver.init()
        self.driver.exit()
        config["browser"] = "reconnect-firefox"
        self.driver.init()
        assert self.driver.browser, "unable to launch via reconnect firefox"

############################################################################################

if __name__ == '__main__':
    unittest.main()
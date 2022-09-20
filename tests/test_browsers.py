import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf
# from OnlySnarf.classes.user import User

class TestSeleniumBrowsers(unittest.TestCase):

    def setUp(self):
        config["debug_selenium"] = True
        config["keep"] = False
        config["show"] = True
        Settings.set_debug("tests")

    def tearDown(self):
        config["debug_selenium"] = False
        config["show"] = False
        Driver.exit()

    def test_auto(self):
        config["browser"] = "auto"
        Driver.init()
        assert Driver.browser, "unable to launch via auto"

    def test_chrome(self):
        config["browser"] = "chrome"
        Driver.init()
        assert Driver.browser, "unable to launch chrome"

    def test_firefox(self):
        config["browser"] = "firefox"
        Driver.init()
        assert Driver.browser, "unable to launch firefox"

############################################################################################

if __name__ == '__main__':
    unittest.main()
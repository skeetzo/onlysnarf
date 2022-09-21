import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf
# from OnlySnarf.classes.user import User

class TestSeleniumReconnect(unittest.TestCase):

    def setUp(self):
        config["cookies"] = True
        config["debug_selenium"] = True
        config["keep"] = True
        config["show"] = True
        Settings.set_debug("tests")

    def tearDown(self):
        config["cookies"] = False
        config["debug_selenium"] = False
        config["keep"] = False
        config["show"] = False
        Driver.exit_all()
    
    def test_reconnect(self):
        config["browser"] = "auto"
        Driver.init()
        Driver.exit_all()
        config["browser"] = "reconnect"
        Driver.init()
        assert Driver.browser, "unable to launch via reconnect"

    def test_reconnect_chrome(self):
        config["browser"] = "chrome"
        Driver.init()
        Driver.exit_all()
        config["browser"] = "reconnect-chrome"
        Driver.init()
        assert Driver.browser, "unable to launch via reconnect chrome"

    def test_reconnect_firefox(self):
        config["browser"] = "firefox"
        Driver.init()
        Driver.exit_all()
        config["browser"] = "reconnect-firefox"
        Driver.init()
        assert Driver.browser, "unable to launch via reconnect firefox"

############################################################################################

if __name__ == '__main__':
    unittest.main()
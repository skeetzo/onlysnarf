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
        config["keep"] = False
        Settings.set_debug("tests")

    def tearDown(self):
        Driver.exit()
    
    # @unittest.skip("todo")
    def test_reconnect(self):
        config["browser"] = "reconnect"
        Driver.init()
        assert Driver.browser, "unable to launch via reconnect"

    @unittest.skip("todo")
    def test_reconnect_chrome(self):
        config["browser"] = "reconnect-chrome"
        Driver.init()
        assert Driver.browser, "unable to launch via reconnect chrome"

    @unittest.skip("todo")
    def test_reconnect_firefox(self):
        config["browser"] = "reconnect-firefox"
        Driver.init()
        assert Driver.browser, "unable to launch via reconnect firefox"

############################################################################################

if __name__ == '__main__':
    unittest.main()
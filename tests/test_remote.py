import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf
# from OnlySnarf.classes.user import User

class TestSeleniumRemote(unittest.TestCase):

    def setUp(self):
        config["debug_selenium"] = True
        config["keep"] = False
        Settings.set_debug("tests")

    def tearDown(self):
        Driver.exit_all()

    @unittest.skip("todo")
    def test_remote(self):
        config["browser"] = "remote"
        Driver.init()
        assert Driver.browser, "unable to launch via remote"
    
    @unittest.skip("todo")
    def test_remote_chrome(self):
        config["browser"] = "remote-chrome"
        Driver.init()
        assert Driver.browser, "unable to launch via remote chrome"

    @unittest.skip("todo")
    def test_remote_firefox(self):
        config["browser"] = "remote-firefox"
        Driver.init()
        assert Driver.browser, "unable to launch via remote firefox"

############################################################################################

if __name__ == '__main__':
    unittest.main()
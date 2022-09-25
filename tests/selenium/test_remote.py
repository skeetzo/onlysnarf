import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
# from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings
# from OnlySnarf.snarf import Snarf
# from OnlySnarf.classes.user import User

class TestSeleniumRemote(unittest.TestCase):

    def setUp(self):
        config["debug_selenium"] = True
        config["keep"] = False
        Settings.set_debug("tests")
        self.driver = self.driver()

    def tearDown(self):
        self.driver.exit()

    @unittest.skip("todo")
    def test_remote(self):
        config["browser"] = "remote"
        self.driver.init()
        assert self.driver.browser, "unable to launch via remote"
    
    @unittest.skip("todo")
    def test_remote_chrome(self):
        config["browser"] = "remote-chrome"
        self.driver.init()
        assert self.driver.browser, "unable to launch via remote chrome"

    @unittest.skip("todo")
    def test_remote_firefox(self):
        config["browser"] = "remote-firefox"
        self.driver.init()
        assert self.driver.browser, "unable to launch via remote firefox"

############################################################################################

if __name__ == '__main__':
    unittest.main()
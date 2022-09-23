import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
# from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings
# from OnlySnarf.snarf import Snarf
# from OnlySnarf.classes.user import User

class TestAuth(unittest.TestCase):

    def setUp(self):
        config["cookies"] = False
        config["debug_cookies"] = False
        config["keep"] = False
        Settings.set_debug("tests")
        self.driver = Driver()

    def tearDown(self):
        self.driver.exit()

    def test_login(self):
        assert self.driver.auth(), "unable to login"
        config["cookies"] = True # saves cookies for next test

    def test_login_via_cookies(self):
        config["cookies"] = True
        config["debug_cookies"] = True
        assert self.driver.auth(), "unable to save login from cookies"
        config["cookies"] = False
        config["debug_cookies"] = False

############################################################################################

if __name__ == '__main__':
    unittest.main()
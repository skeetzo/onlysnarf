import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings

class TestAuth(unittest.TestCase):

    def setUp(self):
        config["login"] = "auto"
        Settings.set_debug("tests")
        self.driver = Driver()

    def tearDown(self):
        self.driver.exit()

    def test_login(self):
        config["cookies"] = False
        assert self.driver.auth(), "unable to login"
        config["cookies"] = True # saves cookies for next test

    def test_login_via_cookies(self):
        config["cookies"] = True
        config["debug_cookies"] = True
        assert self.driver.auth(), "unable to login from cookies"

############################################################################################

if __name__ == '__main__':
    unittest.main()
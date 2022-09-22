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
        config["keep"] = False
        Settings.set_debug("tests")
        self.driver = Driver()

    def tearDown(self):
        self.driver.exit()

    def test_login(self):
        config["cookies"] = False
        assert self.driver.auth(), "unable to login"
        config["cookies"] = True

    def test_login_via_cookies(self):
        config["cookies"] = True
        assert self.driver.auth(), "unable to save login from cookies"
        config["cookies"] = False

############################################################################################

if __name__ == '__main__':
    unittest.main()
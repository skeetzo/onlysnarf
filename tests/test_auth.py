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
        config["cookies"] = True
        # config["show"] = True
        Settings.set_debug("tests")
        self.driver = Driver()

    def tearDown(self):
        config["cookies"] = False
        config["show"] = False
        self.driver.exit()

    def test_login(self):
        assert self.driver.auth(), "unable to login"

    @unittest.skip("todo")
    def test_login_via_cookies(self):
        assert self.driver.auth(), "unable to save login from cookies"

############################################################################################

if __name__ == '__main__':
    unittest.main()
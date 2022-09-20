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
        config["debug_selenium"] = True
        config["show"] = True
        Settings.set_debug("tests")

    def tearDown(self):
        config["cookies"] = False
        config["keep"] = False
        Driver.exit()

    def test_login(self):
        assert Driver.auth(), "unable to login"
        config["keep"] = True

    def test_login_via_cookies(self):
        assert Driver.auth(), "unable to save login from cookies"

############################################################################################

if __name__ == '__main__':
    unittest.main()
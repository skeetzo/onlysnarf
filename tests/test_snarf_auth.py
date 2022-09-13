import os
os.environ['ENV'] = "test"
import unittest

# from OnlySnarf.util.config import config
# from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings
# from OnlySnarf.snarf import Snarf
# from OnlySnarf.classes.user import User

class TestSnarfAuth(unittest.TestCase):

    def setUp(self):
        Settings.set_debug("tests")

    def tearDown(self):
        Driver.exit()

    def test_login(self):
        assert Driver.auth(), "unable to login"

############################################################################################

if __name__ == '__main__':
    unittest.main()
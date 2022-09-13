import os
os.environ['ENV'] = "test"
import unittest

# from OnlySnarf.util.config import config
# from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings
# from OnlySnarf.snarf import Snarf
from OnlySnarf.classes.user import User

class TestSnarfUsers(unittest.TestCase):

    def setUp(self):
        Settings.set_debug("tests")
        Settings.set_prefer_local(False)
        
    def tearDown(self):
        Driver.exit()

    def test_users(self):
        assert User.get_all_users(), "unable to read users"

############################################################################################

if __name__ == '__main__':
    unittest.main()
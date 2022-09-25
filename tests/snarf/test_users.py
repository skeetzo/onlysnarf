import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
# from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf
from OnlySnarf.classes.user import User

class TestUsers(unittest.TestCase):

    def setUp(self):
        config["cookies"] = True
        config["keep"] = True
        config["prefer_local"] = False
        Settings.set_debug("tests")
        self.test_snarf = Snarf()
        
    def tearDown(self):
        self.test_snarf.close()
        config["keep"] = False
        config["cookies"] = False

    def test_get_users(self):
        assert User.get_all_users(), "unable to read users"

    @unittest.skip("todo")
    def test_read_users_locally(self):
        assert User.read_users_local(), "unable to read in users locally"

    @unittest.skip("todo")
    def test_write_users_locally(self):
        assert User.write_users_local(), "unable to write out users locally"

    @unittest.skip("todo")
    def test_get_following(self):
        assert User.get_following(), "unable to read followers"

    @unittest.skip("todo")
    def test_read_following_local(self):
        assert User.read_following_local(), "unable to read in followers locally"

    @unittest.skip("todo")
    def test_write_following_local(self):
        assert User.write_following_local(), "unable to write out followers locally"

############################################################################################

if __name__ == '__main__':
    unittest.main()
import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({"debug_selenium":False,"debug_delay":False,"keep":False})
from OnlySnarf.util.logger import configure_logging
configure_logging(True, True)
from OnlySnarf.classes.user import User

class TestUsers(unittest.TestCase):

    def setUp(self):
        CONFIG["prefer_local"] = False

        
    def tearDown(self):
        CONFIG["prefer_local"] = True

    def test_get_users(self):
        assert User.get_all_users(), "unable to read users"

    # @unittest.skip("todo")
    # def test_read_users_locally(self):
    #     assert User.read_users_local(), "unable to read in users locally"

    # @unittest.skip("todo")
    # def test_write_users_locally(self):
    #     assert User.write_users_local(), "unable to write out users locally"

    # @unittest.skip("todo")
    # def test_get_following(self):
    #     assert User.get_following(), "unable to read followers"

    # @unittest.skip("todo")
    # def test_read_following_local(self):
    #     assert User.read_following_local(), "unable to read in followers locally"

    # @unittest.skip("todo")
    # def test_write_following_local(self):
    #     assert User.write_following_local(), "unable to write out followers locally"

############################################################################################

if __name__ == '__main__':
    unittest.main()
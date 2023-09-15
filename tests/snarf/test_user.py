import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging
configure_logging(True, True)

from OnlySnarf.classes.user import User

class TestUsers(unittest.TestCase):

    def setUp(self):
        pass
        # CONFIG["prefer_local"] = False

        
    def tearDown(self):
        pass
        # CONFIG["prefer_local"] = True

    # def test_get_users(self):
    #     assert User.get_all_users(), "unable to get users"

    def test_get_random_user(self):
        assert User.get_random_user(), "unable to get random user"


############################################################################################

if __name__ == '__main__':
    unittest.main()
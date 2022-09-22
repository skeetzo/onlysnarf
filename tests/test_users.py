import os
os.environ['ENV'] = "test"
import unittest

# from OnlySnarf.util.config import config
# from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf
from OnlySnarf.classes.user import User

class TestUsers(unittest.TestCase):

    def setUp(self):
        Settings.set_debug("tests")
        Settings.set_prefer_local(False)
        self.test_snarf = Snarf()
        
    def tearDown(self):
        self.test_snarf.close()

    def test_users(self):
        assert User.get_all_users(), "unable to read users"

############################################################################################

if __name__ == '__main__':
    unittest.main()
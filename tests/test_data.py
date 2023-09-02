import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})

from OnlySnarf.classes.user import User
from OnlySnarf.util.data import add_to_randomized_users, get_already_randomized_users, read_users_local, write_users_local

users = [User.create_user({'username':'yourmom'})]
randomized_users = [User.create_user({'username':'yourmom'})]

class TestData(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def test_write(self):
        write_users_local(users)

    def test_read(self):
        self.assertTrue(read_users_local())

############################################################################################

if __name__ == '__main__':
    unittest.main()
import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})

from OnlySnarf.classes.user import User
from OnlySnarf.util.data import add_to_randomized_users, read_users_local, write_users_local, reset_userlist

# TODO: restructure tests better, otherwise this line needs to be toggled on and off
# and the read_tests should run after the write tests and not beforehand alphabetically
# reset_userlist()

class TestData(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    # def test_write(self):
    #     write_users_local([User.create_user({'username':'yourmom'}), User.create_user({'username':'yourmom2222'})])

    # def test_write_random(self):
    #     add_to_randomized_users(User.create_user({'username':'randomyourmom'}))

    # def test_write_random_duplicate(self):
    #     try:
    #         add_to_randomized_users(User.create_user({'username':'randomyourmom'}))
    #     except Exception as e:
    #         self.assertTrue(True)

    def test_read(self):
        users, random_users = read_users_local()
        self.assertTrue(users)

    def test_read_random(self):
        users, random_users = read_users_local()
        self.assertTrue(random_users)


############################################################################################

if __name__ == '__main__':
    unittest.main()
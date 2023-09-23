import os
os.environ['ENV'] = "test"
import unittest

USERS_PATH = os.getcwd()+"/tests/test-users.json"

from OnlySnarf.util.config import set_config
CONFIG = set_config({"path_users":USERS_PATH})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.classes.user import User
from OnlySnarf.util.data import add_to_randomized_users, read_users_local, write_users_local, reset_userlist
from OnlySnarf.util import defaults as DEFAULT

class TestData(unittest.TestCase):

    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.util.data")
        reset_userlist()

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests(flush=True)
        # reset_userlist()

    def test_a_read(self):
        users, random_users = read_users_local()
        # empty lists are false
        self.assertFalse(users)
        self.assertFalse(random_users)

    def test_b_write(self):
        # simply runs function and that it does not fail inherently
        write_users_local([User.create_user({'username':'yourmom'})])
        self.assertTrue(True)

    def test_c_read(self):
        users, random_users = read_users_local()
        self.assertTrue(users)
        self.assertEqual(len(users), 1)
        self.assertFalse(users[0]["isFollower"])
        self.assertFalse(random_users)

    def test_d_write_update(self):
        write_users_local([User.create_user({'username':'yourmom','isFollower':True})])
        users, random_users = read_users_local()
        self.assertEqual(len(users), 1)
        self.assertTrue(users[0]["isFollower"])

    def test_e_write_add(self):
        write_users_local([User.create_user({'username':'yourdad'})])
        users, random_users = read_users_local()
        self.assertEqual(len(users), 2)

    def test_f_write_random(self):
        # runs and fails on its own
        add_to_randomized_users(User.create_user({'username':'randomyourmom'}))
        self.assertTrue(True)

    def test_g_read_random(self):
        users, random_users = read_users_local()
        self.assertTrue(random_users)
        self.assertEqual(len(random_users), 1)

    def test_h_write_random_duplicate(self):
        try:
            add_to_randomized_users(User.create_user({'username':'randomyourmom'}))
            self.assertTrue(False)
        except Exception as e:
            self.assertTrue(True)

    def test_i_write_random_nonduplicate(self):
        add_to_randomized_users(User.create_user({'username':'randomyourdad'}))
        self.assertTrue(True)

############################################################################################

if __name__ == '__main__':
    unittest.main()
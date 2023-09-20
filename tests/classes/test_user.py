# TODO: move other webdriver based tests to a new WEBDRIVER specific folder and create other tests for other classes

import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({"prefer_local":True})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.classes.user import User

class TestClasses_Users(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.classes.user")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests(flush=True)

    def test_get_all_users(self):
        assert User.get_all_users(), "unable to get all users"

    def test_get_all_fans(self):
        assert User.get_users_by_type(), "unable to get all fans"

    def test_get_all_followers(self):
        assert User.get_users_by_type(typeOf="follower"), "unable to get all followers"

    # TODO: add methods for configuring these or update fetching functions in webdriver
    @unittest.skip("todo")
    def test_get_all_friends(self):
        assert User.get_users_by_type(typeOf="friend"), "unable to get all friends"
    @unittest.skip("todo")
    def test_get_all_renew_on(self):
        assert User.get_users_by_type(typeOf="renew_on"), "unable to get all renew on"
    @unittest.skip("todo")
    def test_get_all_renew_off(self):
        assert User.get_users_by_type(typeOf="renew_off"), "unable to get all renew off" # not accurate until renew values are actually implemented and fetched
    @unittest.skip("todo")
    def test_get_all_recent(self):
        assert User.get_users_by_type(typeOf="recent"), "unable to get all recent"
    @unittest.skip("todo")
    def test_get_all_tagged(self):
        assert User.get_users_by_type(typeOf="tagged"), "unable to get all tagged"
    @unittest.skip("todo")
    def test_get_all_muted(self):
        assert User.get_users_by_type(typeOf="muted"), "unable to get all muted"
    @unittest.skip("todo")
    def test_get_all_restricted(self):
        assert User.get_users_by_type(typeOf="restricted"), "unable to get all restricted"
    @unittest.skip("todo")
    def test_get_all_blocked(self):
        assert User.get_users_by_type(typeOf="blocked"), "unable to get all blocked"

    def test_get_random_user(self):
        assert User.get_random_user(), "unable to get random user"

############################################################################################

if __name__ == '__main__':
    unittest.main()
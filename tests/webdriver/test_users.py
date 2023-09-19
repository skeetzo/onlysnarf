import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.lib.driver import close_browser, login as get_browser_and_login
from OnlySnarf.lib.webdriver.users import get_users_by_type as WEBDRIVER_get_users_by_type

class TestWebdriver_Users(unittest.TestCase):

    def setUp(self):
        self.browser = get_browser_and_login(cookies=CONFIG["cookies"])
        
    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.users")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests("###FLUSH###")
        close_browser()

    # def test_get_user_element(self):
        # pass

    # TODO: add tests for this and the rest in the webdriver class
    # get_current_username
    # get_userid_by_username
    # get_user_element_at_page
    # get_users_at_page
    # get_user_by_username
    # search_for_username
    # get_user_from_elements
    # click_user_button

    def test_get_users_by_type_fans(self):
        assert WEBDRIVER_get_users_by_type(self.browser, isFan=True), "unable to get users by type: fans"

    def test_get_users_by_type_followers(self):
        assert WEBDRIVER_get_users_by_type(self.browser, isFollower=True), "unable to get users by type: followers"


############################################################################################

if __name__ == '__main__':
    unittest.main()
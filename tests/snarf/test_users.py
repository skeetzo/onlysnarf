import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging
configure_logging(True, True)

from OnlySnarf.lib.driver import create_browser, login
from OnlySnarf.lib.webdriver.users import get_users_by_type as WEBDRIVER_get_users_by_type

class TestUsers(unittest.TestCase):

    def setUp(self):
        self.browser = create_browser(CONFIG["browser"])
        login()
        
    def tearDown(self):
        pass

    def test_get_user_element(self):
        pass

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
        assert User.get_users_by_type(self.browser), "unable to get users by type: fans"
        # which is by extension: get_users_at_page

    def test_get_users_by_type_followers(self):
        assert User.get_users_by_type(self.browser, isFan=False, isFollower=True), "unable to get users by type: followers"


############################################################################################

if __name__ == '__main__':
    unittest.main()
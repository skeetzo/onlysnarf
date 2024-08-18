import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.lib.driver import login as get_browser_and_login
from OnlySnarf.lib.webdriver.message import message as WEBDRIVER_message
from OnlySnarf.lib.webdriver.users import get_random_fan_username as WEBDRIVER_get_random_fan_username
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.util.data import reset_random_users

random_username_one = None
random_username_two = None

class TestWebdriver_Message(unittest.TestCase):

    def setUp(self):
        self.browser = get_browser_and_login(cookies=CONFIG["cookies"])
        global random_username_one
        if not random_username_one:
            random_username_one = WEBDRIVER_get_random_fan_username(self.browser)
        global random_username_two
        if not random_username_two:
            random_username_two = WEBDRIVER_get_random_fan_username(self.browser)
            while random_username_two == random_username_one:
                random_username_two = WEBDRIVER_get_random_fan_username(self.browser)
        self.random_username_one = random_username_one
        self.random_username_two = random_username_two
        self.message_object = {
            "schedule" : {},
            "text" : "test balls",
            "recipients" : [random_username_one],
            "files" : [],
            "price": 0,
            "includes": [],
            "excludes": []
        }

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.message")
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.users")
        reset_random_users()

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests(flush=True)
        reset_random_users()

    def test_message(self):
        assert WEBDRIVER_message(self.browser, self.message_object), "unable to send basic message"

    def test_message_all_include(self):
        self.message_object["files"] = ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg"]
        self.message_object["price"] = DEFAULT.PRICE_MINIMUM
        self.message_object["recipients"] = [random_username_one, random_username_two]
        self.message_object["includes"] = ["all","favorites","friends","renew on","renew off"]
        assert WEBDRIVER_message(self.browser, self.message_object), "unable to send message to included lists"

    def test_message_all_exclude(self):
        self.message_object["recipients"] = [random_username_one, random_username_two]
        # self.message_object["price"] = DEFAULT.PRICE_MINIMUM
        self.message_object["excludes"] = ["all","favorites","friends","renew on","renew off"]
        assert WEBDRIVER_message(self.browser, self.message_object), "unable to send message to excluded lists"

    def test_message_files_local(self):
        self.message_object["files"] = ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg", "/home/skeetzo/Projects/onlysnarf/public/images/snarf.jpg"]
        assert WEBDRIVER_message(self.browser, self.message_object), "unable to upload message files - local"

    def test_message_files_remote(self):
        self.message_object["files"] = ["https://github.com/skeetzo/onlysnarf/blob/master/public/images/shnarf.jpg?raw=true", "https://github.com/skeetzo/onlysnarf/blob/master/public/images/snarf.jpg?raw=true"]
        assert WEBDRIVER_message(self.browser, self.message_object), "unable to upload message files - remote"

    def test_message_price(self):
        self.message_object["files"] = ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg"]
        self.message_object["price"] = DEFAULT.PRICE_MINIMUM
        assert WEBDRIVER_message(self.browser, self.message_object), "unable to set message price"

    def test_message_failure(self):
        self.message_object["recipients"] = ["onlyfans"]
        assert not WEBDRIVER_message(self.browser, self.message_object), "unable to fail message properly"

    def test_message_inactive_user(self):
        import string
        import random
        self.message_object["recipients"] = [''.join(random.choices(string.ascii_uppercase + string.digits, k=8))]
        assert not WEBDRIVER_message(self.browser, self.message_object), "unable to properly fail messaging an inactive user"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
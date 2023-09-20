import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.lib.driver import close_browser, login as get_browser_and_login
from OnlySnarf.lib.webdriver.discount import discount as WEBDRIVER_discount
from OnlySnarf.lib.webdriver.users import get_random_fan_username as WEBDRIVER_get_random_fan_username
from OnlySnarf.util import defaults as DEFAULT

random_username = None

class TestWebdriver_Discount(unittest.TestCase):

    def setUp(self):
        self.browser = get_browser_and_login(cookies=CONFIG["cookies"])
        global random_username
        if not random_username:
            random_username = WEBDRIVER_get_random_fan_username(self.browser)
        self.username = random_username

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.discount")
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.users")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests(flush=True)
        close_browser()

    def test_discount(self):
        assert WEBDRIVER_discount(self.browser, {
            "amount" : DEFAULT.DISCOUNT_MAX_AMOUNT/2, # 55 / 2 = 27 or 28 -> 25
            "months" : DEFAULT.DISCOUNT_MAX_MONTHS/2, # 12 / 2 = 6
            "username" : self.username
        }), "unable to apply discount"

    def test_discount_max(self):
        assert WEBDRIVER_discount(self.browser, {
            "amount" : DEFAULT.DISCOUNT_MAX_AMOUNT, # 55 / 2 = 27 or 28 -> 25
            "months" : DEFAULT.DISCOUNT_MAX_MONTHS, # 12 / 2 = 6
            "username" : self.username
        }), "unable to apply discount maximum"


    def test_discount_min(self):
        assert WEBDRIVER_discount(self.browser, {
            "amount" : DEFAULT.DISCOUNT_MIN_AMOUNT, # 55 / 2 = 27 or 28 -> 25
            "months" : DEFAULT.DISCOUNT_MIN_MONTHS, # 12 / 2 = 6
            "username" : self.username
        }), "unable to apply discount minimum"

    def test_discount_inactive_user(self):
        assert WEBDRIVER_discount(self.browser, {
            "amount" : DEFAULT.DISCOUNT_MIN_AMOUNT, # 55 / 2 = 27 or 28 -> 25
            "months" : DEFAULT.DISCOUNT_MIN_MONTHS, # 12 / 2 = 6
            "username" : "yeahzers"
        }), "unable to apply discount to inactive user"

    # TODO: add a test for applying the same discount to an existing discount
    # def test_discount_repeat(self):
    #     CONFIG["user"] = "yeahzers"
    #     CONFIG["amount"] = DEFAULT.DISCOUNT_MIN_AMOUNT # 1
    #     CONFIG["months"] = DEFAULT.DISCOUNT_MIN_MONTHS # 1
    #     CONFIG["debug"] = False
    #     self.discount_object = Discount.create_discount({**CONFIG, 'username':CONFIG["user"]})
    #     assert WEBDRIVER_discount(self.browser, self.discount_object), "unable to skip equal discount"
        
############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.classes.discount import Discount

configure_logs_for_module_tests("OnlySnarf.lib.webdriver.discount")

class TestSnarf(unittest.TestCase):

    def setUp(self):
        CONFIG["amount"] = DEFAULT.DISCOUNT_MAX_AMOUNT/2 # 55 / 2 = 27 or 28 -> 25
        CONFIG["months"] = DEFAULT.DISCOUNT_MAX_MONTHS/2 # 12 / 2 = 6
        CONFIG["user"] = "random"
        CONFIG["prefer_local"] = True

    def tearDown(self):
        pass

    def test_discount(self):
        assert Discount.create_discount({**CONFIG, 'username':CONFIG["user"]}).apply(), "unable to apply discount"

    def test_discount_max(self):
        CONFIG["amount"] = DEFAULT.DISCOUNT_MAX_AMOUNT # 55
        CONFIG["months"] = DEFAULT.DISCOUNT_MAX_MONTHS # 12
        assert Discount.create_discount({**CONFIG, 'username':CONFIG["user"]}).apply(), "unable to apply discount maximum"

    def test_discount_min(self):
        CONFIG["amount"] = DEFAULT.DISCOUNT_MIN_AMOUNT # 1
        CONFIG["months"] = DEFAULT.DISCOUNT_MIN_MONTHS # 1
        assert Discount.create_discount({**CONFIG, 'username':CONFIG["user"]}).apply(), "unable to apply discount minimum"

    def test_discount_inactive_user(self):
        CONFIG["user"] = "yeahzers"
        CONFIG["amount"] = DEFAULT.DISCOUNT_MIN_AMOUNT # 1
        CONFIG["months"] = DEFAULT.DISCOUNT_MIN_MONTHS # 1
        assert Discount.create_discount({**CONFIG, 'username':CONFIG["user"]}).apply(), "unable to apply discount to inactive user"

    # TODO: add a test for applying the same discount to an existing discount
    def test_discount_repeat(self):
        CONFIG["user"] = "yeahzers"
        CONFIG["amount"] = DEFAULT.DISCOUNT_MIN_AMOUNT # 1
        CONFIG["months"] = DEFAULT.DISCOUNT_MIN_MONTHS # 1
        CONFIG["debug"] = False
        self.discount = Discount.create_discount({**CONFIG, 'username':CONFIG["user"]})
        self.discount.apply() # must actually apply discount or know existing discount values, if not applied already; easier than constantly fetching individual values i'll never need
        assert self.discount.apply(), "unable to skip equal discount"
        
############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
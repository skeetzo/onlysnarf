import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({"prefer_local":True})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.classes.discount import Discount

class TestClasses_Discount(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.classes.discount")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests(flush=True)

    def test_create_discount(self):
        assert Discount.create_discount({
            "amount" : DEFAULT.DISCOUNT_MAX_AMOUNT,
            "months" : DEFAULT.DISCOUNT_MAX_MONTHS,
            "username" : "random",
        }), "unable to create discount"

    def test_format_amount(self):
        assert Discount.format_amount(DEFAULT.DISCOUNT_MAX_AMOUNT/2), "unable to format discount amount"
        self.assertEqual(Discount.format_amount(DEFAULT.DISCOUNT_MAX_AMOUNT+1), DEFAULT.DISCOUNT_MAX_AMOUNT), "unable to format discount amount greater than maximum"
        self.assertEqual(Discount.format_amount(DEFAULT.DISCOUNT_MIN_AMOUNT-1), DEFAULT.DISCOUNT_MIN_AMOUNT), "unable to format discount amount less than minimum"

    def test_format_months(self):
        assert Discount.format_months(DEFAULT.DISCOUNT_MAX_MONTHS/2), "unable to format discount months"
        self.assertEqual(Discount.format_months(DEFAULT.DISCOUNT_MAX_MONTHS+1), DEFAULT.DISCOUNT_MAX_MONTHS), "unable to format discount months greater than maximum"
        self.assertEqual(Discount.format_months(DEFAULT.DISCOUNT_MIN_MONTHS-1), DEFAULT.DISCOUNT_MIN_MONTHS), "unable to format discount months less than minimum"

    def test_format_username(self):
        # if user is random, return a user not "random"
        self.assertEqual(Discount.format_username("@onlyfans"), "onlyfans", "unable to format discount username")
        formatted_username = Discount.format_username("random")
        self.assertNotEqual(formatted_username, "random", "unable to format random discount username")

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
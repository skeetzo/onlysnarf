import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({"debug_selenium":False})
from OnlySnarf.util.logger import configure_logging
configure_logging(True, True)

from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.classes.discount import Discount

class TestSnarf(unittest.TestCase):

    def setUp(self):
        CONFIG["amount"] = DEFAULT.DISCOUNT_MAX_AMOUNT/2 # 55 / 2 = 27 or 28 -> 25
        CONFIG["months"] = DEFAULT.DISCOUNT_MAX_MONTHS/2 # 12 / 2 = 6
        CONFIG["user"] = "random"
        CONFIG["prefer_local"] = True
        self.discount = Discount.create_discount({**CONFIG, 'username':CONFIG["user"]})

    def tearDown(self):
        CONFIG["amount"] = 0
        CONFIG["months"] = 0
        CONFIG["user"] = None

    def test_discount(self):
        # CONFIG["prefer_local"] = False
        assert self.discount.apply(), "unable to apply discount"

    # def test_discount_max(self):
    #     CONFIG["amount"] = DEFAULT.DISCOUNT_MAX_AMOUNT # 55
    #     CONFIG["months"] = DEFAULT.DISCOUNT_MAX_MONTHS # 12
    #     assert self.discount.apply(), "unable to apply discount maximum"

    # def test_discount_min(self):
    #     CONFIG["amount"] = DEFAULT.DISCOUNT_MIN_AMOUNT # 1
    #     CONFIG["months"] = DEFAULT.DISCOUNT_MIN_MONTHS # 1
    #     assert self.discount.apply(), "unable to apply discount minimum"

    # add a test for applying the same discount to an existing discount
        
############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
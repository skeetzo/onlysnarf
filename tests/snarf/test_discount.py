import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf

class TestSnarf(unittest.TestCase):

    def setUp(self):
        config["amount"] = DEFAULT.DISCOUNT_MAX_AMOUNT/2 # 55 / 2 = 27 or 28 -> 25
        config["months"] = DEFAULT.DISCOUNT_MAX_MONTHS/2 # 12 / 2 = 6
        config["user"] = "random"
        Settings.set_debug("tests")

    def tearDown(self):
        config["amount"] = 0
        config["months"] = 0
        config["user"] = None
        Snarf.close()

    def test_discount(self):
        assert Snarf.discount(), "unable to apply discount"

    def test_discount_max(self):
        config["amount"] = DEFAULT.DISCOUNT_MAX_AMOUNT # 55
        config["months"] = DEFAULT.DISCOUNT_MAX_MONTHS # 12
        assert Snarf.discount(), "unable to apply discount maximum"

    def test_discount_min(self):
        config["amount"] = DEFAULT.DISCOUNT_MIN_AMOUNT # 1
        config["months"] = DEFAULT.DISCOUNT_MIN_MONTHS # 1
        assert Snarf.discount(), "unable to apply discount minimum"

    # add a test for applying the same discount to an existing discount
        
############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
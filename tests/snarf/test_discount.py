import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf

class TestSnarf(unittest.TestCase):

    def setUp(self):
        config["amount"] = DEFAULT.DISCOUNT_MAX_AMOUNT
        config["months"] = DEFAULT.DISCOUNT_MAX_MONTHS
        config["user"] = "random"
        Settings.set_debug("tests")

    def tearDown(self):
        config["amount"] = 0
        config["months"] = 0
        config["user"] = None
        Snarf.close()

    def test_discount(self):
        assert Snarf.discount(), "unable to apply discount"
        
############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
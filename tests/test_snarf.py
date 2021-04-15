import unittest
import os
from decimal import Decimal

os.environ['ENV'] = "test"

# from lib.config import config
from lib.snarf import Snarf

# import warnings


class TestSnarf(unittest.TestCase):

    def setUp(self):
        self.test_snarf = Snarf()
        
    # @classmethod
    # def setUpClass(cls):
    #     ...

        # @classmethod
        # def tearDownClass(cls):
        #     ...
        
    def tearDown(self):
        pass

    def test_discount(self):
        pass

    def test_message(self):
        pass

    def test_post(self):
        pass

    def test_profile(self):
        pass

    def test_promotion(self):
        pass


############################################################################################

if __name__ == '__main__':
    unittest.main()
import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
# from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf
# from OnlySnarf.classes.user import User

class TestPromotion(unittest.TestCase):

    def setUp(self):
        Settings.set_debug("tests")
        config["prefer_local"] = False
        self.test_snarf = Snarf()

    def tearDown(self):
        self.test_snarf.close()

    @unittest.skip("todo")
    def test_promotion_campaign(self):
        config["promotion_method"] = "campaign"
        assert self.test_snarf.promotion(), "unable to apply promotion: campaign"

    @unittest.skip("todo")
    def test_promotion_trial(self):
        config["promotion_method"] = "trial"
        assert self.test_snarf.promotion(), "unable to apply promotion: trial"

    @unittest.skip("todo")
    def test_promotion_user(self):
        config["promotion_method"] = "user"
        assert self.test_snarf.promotion(), "unable to apply promotion: user"

    @unittest.skip("todo")
    def test_promotion_grandfather(self):
        config["promotion_method"] = "grandfather"
        assert self.test_snarf.promotion(), "unable to apply promotion: grandfather"

############################################################################################

if __name__ == '__main__':
    unittest.main()
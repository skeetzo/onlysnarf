import unittest
import datetime
from decimal import Decimal

import Snarf
import Discount
import config

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
        from .driver import Driver
        Driver.exit_all()

    def test_discount(self):
        assert self.test_snarf.discount(), "unable to apply discount"

    def test_message(self):
        assert self.test_snarf.Message(), "unable to send message"

    def test_post(self):
        assert self.test_snarf.Post(), "unable to post message"

    def test_poll(self):
        config["duration"] = 99
        config["expiration"] = 99
        config["questions"] = ["suck","my","dick"]
        assert self.test_snarf.Post(), "unable to post poll"

    def test_schedule(self):
        today = datetime.datetime()
        today = today + datetime.timedelta(1) # +1 day
        config["schedule"] = today.strftime("%m-%d-%Y:%H:%M") # "MM-DD-YYYY:HH:MM"
        assert self.test_snarf.Post(), "unable to post schedule"

    def test_profile_backup(self):
        config["profile_method"] = "backup"
        assert self.test_snarf.Profile(), "unable to backup profile"

    def test_profile_syncfrom(self):
        config["profile_method"] = "syncfrom"
        assert self.test_snarf.Profile(), "unable to sync from profile"

    def test_profile_syncto(self):
        config["profile_method"] = "syncto"
        assert self.test_snarf.Profile(), "unable to sync to profile"

    def test_promotion_campaign(self):
        config["promotion_method"] = "campaign"
        assert self.test_snarf.Promotion(), "unable to apply promotion: campaign"

    def test_promotion_trial(self):
        config["promotion_method"] = "trial"
        assert self.test_snarf.Promotion(), "unable to apply promotion: trial"

    def test_promotion_user(self):
        config["promotion_method"] = "user"
        assert self.test_snarf.Promotion(), "unable to apply promotion: user"

    @unittest.skip("unnecessary")
    def test_promotion_grandfather(self):
        config["promotion_method"] = "grandfather"
        assert self.test_snarf.Promotion(), "unable to apply promotion: grandfather"

############################################################################################

if __name__ == '__main__':
    unittest.main()
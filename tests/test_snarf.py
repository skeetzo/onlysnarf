import os
os.environ['ENV'] = "test"

import unittest
import datetime
from decimal import Decimal

from OnlySnarf.snarf import Snarf
from OnlySnarf.classes.discount import Discount
from OnlySnarf.util.config import config
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings
from OnlySnarf.util import defaults as DEFAULT

Settings.set_prompt(False)
config["confirm"] = False

# import warnings

class TestSnarf(unittest.TestCase):

    def setUp(self):
        self.test_snarf = Snarf()
        self.driver = Driver()
        
    # @classmethod
    # def setUpClass(cls):
    #     ...

        # @classmethod
        # def tearDownClass(cls):
        #     ...
        
    def tearDown(self):
        Driver.exit_all()

    # def test_login(self):
        # assert self.driver.auth(), "unable to login"

    # def test_users(self):
        # config["prefer_local"] = False
    #     from OnlySnarf.classes.user import User
    #     assert User.get_all_users(), "unable to read users"

    # def test_discount(self):
    #     config["prefer_local"] = True
    #     config["amount"] = DEFAULT.DISCOUNT_MIN_AMOUNT
    #     config["months"] = DEFAULT.DISCOUNT_MIN_MONTHS
    #     config["user"] = "ddezeht"
    #     assert self.test_snarf.discount(), "unable to apply discount"

    # def test_message(self):
    #     config["prefer_local"] = True
    #     config["input"] = "/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg"
    #     config["price"] = DEFAULT.PRICE_MINIMUM
    #     config["text"] = "test balls"
    #     config["user"] = "ddezeht"
    #     assert self.test_snarf.message(), "unable to send message"

    def test_post(self):
        config["input"] = "/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg"
        config["price"] = DEFAULT.PRICE_MINIMUM
        config["text"] = "test balls"
        assert self.test_snarf.post(), "unable to post message"

    # def test_poll(self):
    #     config["duration"] = DEFAULT.DURATION_ALLOWED[0]
    #     config["expiration"] = DEFAULT.EXPIRATION_ALLOWED[0]
    #     config["questions"] = ["suck","my","dick","please?"]
    #     assert self.test_snarf.post(), "unable to post poll"

    # def test_schedule(self):
    #     today = datetime.date.today()
    #     tomorrow = today + datetime.timedelta(1) # +1 day
    #     config["schedule"] = today.strftime("%m-%d-%Y:%H:%M") # "MM-DD-YYYY:HH:MM"
    #     assert self.test_snarf.post(), "unable to post schedule"

    ## TODO ##
    ## less important features, test these later

    # def test_profile_backup(self):
    #     config["profile_method"] = "backup"
    #     assert self.test_snarf.profile(), "unable to backup profile"

    # def test_profile_syncfrom(self):
    #     config["profile_method"] = "syncfrom"
    #     assert self.test_snarf.profile(), "unable to sync from profile"

    # def test_profile_syncto(self):
    #     config["profile_method"] = "syncto"
    #     assert self.test_snarf.profile(), "unable to sync to profile"

    # def test_promotion_campaign(self):
    #     config["promotion_method"] = "campaign"
    #     assert self.test_snarf.promotion(), "unable to apply promotion: campaign"

    # def test_promotion_trial(self):
    #     config["promotion_method"] = "trial"
    #     assert self.test_snarf.promotion(), "unable to apply promotion: trial"

    # def test_promotion_user(self):
    #     config["promotion_method"] = "user"
    #     assert self.test_snarf.promotion(), "unable to apply promotion: user"

    # @unittest.skip("unnecessary")
    # def test_promotion_grandfather(self):
    #     config["promotion_method"] = "grandfather"
    #     assert self.test_snarf.promotion(), "unable to apply promotion: grandfather"

    # def test_backup_to_ipfs(self):
    #     config["input"] = "/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg"
    #     config["text"] = "shnarf!"
    #     config["backup"] = True
    #     # config["force_backup"] = True
    #     config["destination"] = "IPFS"
    #     assert self.test_snarf.post(), "unable to backup content to ipfs"

    # def test_post_from_ipfs(self):
    #     config["input"] = "CID" # recognize CID format and automatically attempt to use IPFS
    #     config["price"] = DEFAULT.PRICE_MINIMUM
    #     config["text"] = "test balls"
    #     assert self.test_snarf.post(), "unable to post content from ipfs"


############################################################################################

if __name__ == '__main__':
    unittest.main()
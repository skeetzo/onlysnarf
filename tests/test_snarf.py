import os
os.environ['ENV'] = "test"
import unittest
import datetime

from OnlySnarf.util.config import config
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf
# from OnlySnarf.classes.user import User

class TestSnarf(unittest.TestCase):

    def setUp(self):
        config["text"] = "test balls"
        Settings.set_debug("tests")
        self.test_snarf = Snarf()

    def tearDown(self):
        config["price"] = 0
        Driver.exit()

    @unittest.skip("works")
    def test_discount(self):
        config["amount"] = DEFAULT.DISCOUNT_MAX_AMOUNT
        config["months"] = DEFAULT.DISCOUNT_MAX_MONTHS
        config["user"] = "randomficus"
        assert self.test_snarf.discount(), "unable to apply discount"
        config["amount"] = 0
        config["months"] = 0
        
    @unittest.skip("works")
    def test_message(self):
        config["input"] = ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg", "/home/skeetzo/Projects/onlysnarf/public/images/snarf.jpg"]
        config["price"] = DEFAULT.PRICE_MINIMUM
        config["user"] = "randomficus"
        assert self.test_snarf.message(), "unable to send message"
        config["input"] = []

    @unittest.skip("works")
    def test_post(self):
        config["input"] = ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg", "/home/skeetzo/Projects/onlysnarf/public/images/snarf.jpg"]
        config["price"] = DEFAULT.PRICE_MINIMUM
        assert self.test_snarf.post(), "unable to post message"
        config["input"] = []
        
    @unittest.skip("works")
    def test_poll(self):
        config["duration"] = DEFAULT.DURATION_ALLOWED[-1]
        config["expiration"] = 999
        config["questions"] = ["suck","my","dick","please?"]
        assert self.test_snarf.post(), "unable to post poll"
        config["duration"] = None
        config["expiration"] = 0
        config["questions"] = []

    def test_schedule(self):
        config["text"] = "test balls"
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(1) # +1 day
        config["schedule"] = today.strftime("%m-%d-%Y:%H:%M") # "MM-DD-YYYY:HH:MM"
        assert self.test_snarf.post(), "unable to post schedule"
        config["schedule"] = None

############################################################################################

if __name__ == '__main__':
    unittest.main()
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
        Settings.set_debug("tests")
        self.test_snarf = Snarf()

    def tearDown(self):
        Driver.exit()

    @unittest.skip("todo")
    def test_discount(self):
        config["amount"] = DEFAULT.DISCOUNT_MIN_AMOUNT
        config["months"] = DEFAULT.DISCOUNT_MIN_MONTHS
        config["user"] = "randomficus"
        assert self.test_snarf.discount(), "unable to apply discount"

    def test_message(self):
        config["input"] = "/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg"
        config["price"] = DEFAULT.PRICE_MINIMUM
        config["text"] = "test balls"
        config["user"] = "randomficus"
        assert self.test_snarf.message(), "unable to send message"

    @unittest.skip("works")
    def test_post(self):
        config["input"] = "/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg"
        config["price"] = DEFAULT.PRICE_MINIMUM
        config["text"] = "test balls"
        assert self.test_snarf.post(), "unable to post message"

    @unittest.skip("todo")
    def test_poll(self):
        config["duration"] = DEFAULT.DURATION_ALLOWED[0]
        config["expiration"] = DEFAULT.EXPIRATION_ALLOWED[0]
        config["questions"] = ["suck","my","dick","please?"]
        assert self.test_snarf.post(), "unable to post poll"

    @unittest.skip("todo")
    def test_schedule(self):
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(1) # +1 day
        config["schedule"] = today.strftime("%m-%d-%Y:%H:%M") # "MM-DD-YYYY:HH:MM"
        assert self.test_snarf.post(), "unable to post schedule"

############################################################################################

if __name__ == '__main__':
    unittest.main()
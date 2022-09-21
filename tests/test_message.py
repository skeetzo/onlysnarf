import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf
# from OnlySnarf.classes.user import User

class TestSnarf(unittest.TestCase):

    def setUp(self):
        config["cookies"] = True
        config["input"] = ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg", "/home/skeetzo/Projects/onlysnarf/public/images/snarf.jpg"]
        config["price"] = DEFAULT.PRICE_MINIMUM
        config["text"] = "test balls"
        config["user"] = "random"
        Settings.set_debug("tests")
        self.test_snarf = Snarf()

    def tearDown(self):
        config["cookies"] = False
        config["input"] = []
        config["price"] = 0
        config["user"] = None
        Driver.exit()

    def test_message(self):
        assert self.test_snarf.message(), "unable to send message"

    @unittest.skip("todo")
    def test_message_files(self):
        assert self.test_snarf.message(), "unable to upload message files"

    @unittest.skip("todo")
    def test_message_price(self):
        assert self.test_snarf.message(), "unable to set message price"

    @unittest.skip("todo")
    def test_message_text(self):
        assert self.test_snarf.message(), "unable to set message text"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
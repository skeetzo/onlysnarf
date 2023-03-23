import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf

class TestSnarf(unittest.TestCase):

    def setUp(self):
        config["input"] = ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg", "/home/skeetzo/Projects/onlysnarf/public/images/snarf.jpg"]
        config["price"] = DEFAULT.PRICE_MINIMUM
        config["text"] = "test balls"
        config["user"] = "random"
        # config["keep"] = True
        Settings.set_debug("tests")

    def tearDown(self):
        config["input"] = []
        config["price"] = 0
        config["user"] = None
        # config["keep"] = False
        Snarf.close()

    def test_message(self):
        assert Snarf.message(), "unable to send message"

    # @unittest.skip("pointless")
    # def test_message_files(self):
    #     successful, results = Snarf.message()
    #     assert Snarf.message(), "unable to upload message files"

    # @unittest.skip("pointless")
    # def test_message_price(self):
    #     assert Snarf.message(), "unable to set message price"

    # @unittest.skip("pointless")
    # def test_message_text(self):
    #     assert Snarf.message(), "unable to set message text"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
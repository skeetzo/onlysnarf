import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import get_config
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf

config = {}

class TestSnarf(unittest.TestCase):

    def setUp(self):
        config = get_config()
        config["text"] = "test balls"
        config["user"] = "random"
        Settings.set_debug("tests")
        # config["skip_download"] = False
        # config["skip_upload"] = True

    def tearDown(self):
        config["input"] = []
        config["price"] = 0

    def test_message(self):
        assert Snarf.message(config), "unable to send basic message"

    def test_message_files_local(self):
        config["input"] = ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg", "/home/skeetzo/Projects/onlysnarf/public/images/snarf.jpg"]
        assert Snarf.message(config), "unable to upload message files - local"

    def test_message_files_remote(self):
        config["input"] = ["https://github.com/skeetzo/onlysnarf/blob/master/public/images/shnarf.jpg?raw=true", "https://github.com/skeetzo/onlysnarf/blob/master/public/images/snarf.jpg?raw=true"]
        assert Snarf.message(config), "unable to upload message files - remote"

    def test_message_price(self):
        config["input"] = ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg"]
        config["price"] = DEFAULT.PRICE_MINIMUM
        assert Snarf.message(config), "unable to set message price"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
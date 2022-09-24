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
        Settings.set_debug("tests")
        self.test_snarf = Snarf()

    def tearDown(self):
        config["input"] = []
        config["price"] = 0
        self.test_snarf.close()

    def test_post(self):
        assert self.test_snarf.post(), "unable to post post"

    @unittest.skip("todo")
    def test_post_files(self):
        assert self.test_snarf.post(), "unable to upload post files"

    @unittest.skip("todo")
    def test_post_price(self):
        assert self.test_snarf.post(), "unable to set post price"

    @unittest.skip("todo")
    def test_post_text(self):
        assert self.test_snarf.post(), "unable to set post text"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
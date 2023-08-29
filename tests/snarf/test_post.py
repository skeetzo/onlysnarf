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
        config["input"] = ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg", "/home/skeetzo/Projects/onlysnarf/public/images/snarf.jpg"]
        config["price"] = DEFAULT.PRICE_MINIMUM
        config["text"] = "test balls"
        config["keywords"] = ["test","ticles"]
        config["performers"] = ["yourmom","yourdad"]
        Settings.set_debug("tests")

    def tearDown(self):
        config["input"] = []
        config["performers"] = []
        config["price"] = 0
        config["keywords"] = []

    def test_post(self):
        assert Snarf.post(config), "unable to post"

    @unittest.skip("todo")
    def test_post_files(self):
        assert Snarf.post(config), "unable to upload post files"

    @unittest.skip("todo")
    def test_post_price(self):
        assert Snarf.post(config), "unable to set post price"

    @unittest.skip("todo")
    def test_post_text(self):
        assert Snarf.post(config), "unable to set post text"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.lib.driver import close_browser
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.classes.message import Post

configure_logs_for_module_tests("OnlySnarf.lib.webdriver.post")
close_browser()

class TestSnarf(unittest.TestCase):

    def setUp(self):
        CONFIG["input"] = ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg", "/home/skeetzo/Projects/onlysnarf/public/images/snarf.jpg"]
        CONFIG["price"] = DEFAULT.PRICE_MINIMUM
        CONFIG["text"] = "test balls"
        CONFIG["keywords"] = ["test","ticles"]
        CONFIG["performers"] = ["yourmom","yourdad"]
        CONFIG["schedule"] = {}

    def tearDown(self):
        pass

    def test_post(self):
        assert Post.create_post({**CONFIG}).send(), "unable to post"

    # @unittest.skip("todo")
    # def test_post_files(self):
    #     assert Snarf.post(CONFIG), "unable to upload post files"

    # @unittest.skip("todo")
    # def test_post_price(self):
    #     assert Snarf.post(CONFIG), "unable to set post price"

    # @unittest.skip("todo")
    # def test_post_text(self):
    #     assert Snarf.post(CONFIG), "unable to set post text"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
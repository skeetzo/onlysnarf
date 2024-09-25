import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.lib.driver import login as get_browser_and_login, close_browser
from OnlySnarf.lib.webdriver.post import post as WEBDRIVER_post
from OnlySnarf.util import defaults as DEFAULT


class TestWebdriver_Post(unittest.TestCase):

    def setUp(self):
        self.browser = get_browser_and_login(cookies=CONFIG["cookies"])
        self.post_object = {
            "files" : ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg", "/home/skeetzo/Projects/onlysnarf/public/images/snarf.jpg"],
            "price" : DEFAULT.PRICE_MINIMUM,
            "text" : "test balls",
            "keywords" : ["test","ticles"],
            "performers" : ["yourmom","yourdad"],
            "expiration": 0,
            "poll": {},
            "schedule" : {}
        }

    def tearDown(self):
        # close_browser(self.browser)
        pass

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.post")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests(flush=True)

    def test_post(self):
        assert WEBDRIVER_post(self.browser, self.post_object), "unable to post"

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
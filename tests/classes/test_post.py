import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.classes.message import Post

class TestClasses_Post(unittest.TestCase):

    def setUp(self):
        self.post_object = {
            "input" : ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg", "/home/skeetzo/Projects/onlysnarf/public/images/snarf.jpg"],
            "price" : DEFAULT.PRICE_MINIMUM,
            "text" : "test balls",
            "keywords" : ["test","ticles"],
            "performers" : ["yourmom","yourdad"],
            "schedule" : {}
        }
        self.post = Post.create_post(self.post_object)

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.post")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests(flush=True)

    def test_post(self):
        assert self.post, "unable to create post object"

    # def test_post_format_poll(self):
        # pointless
        # pass

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
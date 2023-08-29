import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util.settings import Settings
from OnlySnarf.util.webdriver import Driver

class TestSeleniumChromium(unittest.TestCase):

    def setUp(self):
        config["debug_selenium"] = True
        config["keep"] = False
        # config["show"] = True
        Settings.set_debug("tests")

    def tearDown(self):
        # config["debug_chromium"] = False
        config["show"] = False

    @unittest.skip("todo")
    def test_chromium(self):
        config["browser"] = "chromium"
        # config["debug_chromium"] = True
        assert Driver.get_browser(), "unable to launch chromium"

############################################################################################

if __name__ == '__main__':
    unittest.main()
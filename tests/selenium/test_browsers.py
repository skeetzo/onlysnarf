import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util.settings import Settings
from OnlySnarf.util.webdriver import Driver

class TestSeleniumBrowsers(unittest.TestCase):

    def setUp(self):
        config["debug_selenium"] = True
        config["keep"] = False
        # config["show"] = True
        Settings.set_debug("tests")

    def tearDown(self):
        config["debug_selenium"] = False
        config["show"] = False

    def test_auto(self):
        config["browser"] = "auto"
        assert Driver.get_browser(), "unable to launch via auto"

############################################################################################

if __name__ == '__main__':
    unittest.main()
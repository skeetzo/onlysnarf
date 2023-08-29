import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util.settings import Settings
from OnlySnarf.util.webdriver import Driver

class TestSeleniumBrave(unittest.TestCase):

    def setUp(self):
        config["debug_selenium"] = True
        config["keep"] = False
        # config["show"] = True
        Settings.set_debug("tests")

    def tearDown(self):
        # config["debug_brave"] = False
        config["show"] = False

    def test_brave(self):
        config["browser"] = "brave"
        # config["debug_brave"] = True
        assert Driver.get_browser(), "unable to launch brave"

############################################################################################

if __name__ == '__main__':
    unittest.main()
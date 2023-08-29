import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util.settings import Settings
from OnlySnarf.util.webdriver import Driver

class TestSeleniumFirefox(unittest.TestCase):

    def setUp(self):
        config["debug_selenium"] = True
        config["keep"] = False
        # config["show"] = True
        Settings.set_debug("tests")

    def tearDown(self):
        config["debug_firefox"] = False
        config["show"] = False

    def test_firefox(self):
        config["browser"] = "firefox"
        config["debug_firefox"] = True
        assert Driver.get_browser(), "unable to launch firefox"

############################################################################################

if __name__ == '__main__':
    unittest.main()
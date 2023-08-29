import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util.settings import Settings
from OnlySnarf.util.webdriver import Driver

class TestSeleniumReconnect(unittest.TestCase):

    def setUp(self):
        config["debug_selenium"] = True
        config["keep"] = True
        # config["show"] = True
        Settings.set_debug("tests")

    def tearDown(self):
        config["debug_selenium"] = False
        config["keep"] = False
        config["show"] = False
    
    def test_reconnect(self):
        config["browser"] = "auto"
        Driver.get_browser()
        Driver.exit()
        config["browser"] = "auto"
        assert Driver.get_browser(), "unable to launch via reconnect auto"

############################################################################################

if __name__ == '__main__':
    unittest.main()
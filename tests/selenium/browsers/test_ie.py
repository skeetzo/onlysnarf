import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util.settings import Settings
from OnlySnarf.util.webdriver import Driver

class TestSeleniumIE(unittest.TestCase):

    def setUp(self):
        config["debug_selenium"] = True
        config["keep"] = False
        # config["show"] = True
        Settings.set_debug("tests")

    def tearDown(self):
        # config["debug_ie"] = False
        config["show"] = False

    # @unittest.skip("todo")
    def xtest_ie(self):
        config["browser"] = "ie"
        # config["debug_ie"] = True
        assert Driver.get_browser(), "unable to launch ie"

############################################################################################

if __name__ == '__main__':
    unittest.main()
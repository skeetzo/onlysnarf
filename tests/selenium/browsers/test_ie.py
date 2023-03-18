import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings

class TestSeleniumIE(unittest.TestCase):

    def setUp(self):
        config["debug_selenium"] = True
        config["keep"] = False
        # config["show"] = True
        Settings.set_debug("tests")
        self.driver = Driver()

    def tearDown(self):
        # config["debug_ie"] = False
        config["show"] = False
        self.driver.exit()

    # @unittest.skip("todo")
    def xtest_ie(self):
        config["browser"] = "ie"
        # config["debug_ie"] = True
        self.driver.init()
        assert self.driver.browser, "unable to launch ie"

############################################################################################

if __name__ == '__main__':
    unittest.main()
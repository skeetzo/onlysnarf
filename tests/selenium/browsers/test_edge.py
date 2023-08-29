import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util.settings import Settings
from OnlySnarf.util.webdriver import Driver

class TestSeleniumEdge(unittest.TestCase):

    def setUp(self):
        config["debug_selenium"] = True
        config["keep"] = False
        # config["show"] = True
        Settings.set_debug("tests")

    def tearDown(self):
        # config["debug_edge"] = False
        config["show"] = False

    # @unittest.skip("todo")
    def xtest_edge(self):
        config["browser"] = "edge"
        # config["debug_edge"] = True
        assert Driver.get_browser(), "unable to launch edge"

############################################################################################

if __name__ == '__main__':
    unittest.main()
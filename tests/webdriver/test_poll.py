import os
os.environ['ENV'] = "test"
import unittest
import datetime

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.lib.driver import close_browser, login as get_browser_and_login
from OnlySnarf.lib.webdriver.poll import poll as WEBDRIVER_poll
from OnlySnarf.util import defaults as DEFAULT

class TestWebdriver_Poll(unittest.TestCase):

    def setUp(self):
        self.browser = get_browser_and_login(cookies=CONFIG["cookies"])
        self.poll_object = {
            "duration": DEFAULT.DURATION_ALLOWED[0],
            "questions": ["suck","my","dick","please?"]
        }

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.poll")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests(flush=True)
        # close_browser()

    def test_poll(self):
        assert WEBDRIVER_poll(self.browser, self.poll_object), "unable to post poll"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
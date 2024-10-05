import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import login as get_browser_and_login, close_browser
from OnlySnarf.lib.webdriver.expiration import expiration as WEBDRIVER_expiration

class TestWebdriver_Expiration(unittest.TestCase):

    def setUp(self):
        self.browser = get_browser_and_login(cookies=CONFIG["cookies"])

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.expiration")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests(flush=True)

    def test_expiration(self):
        assert WEBDRIVER_expiration(self.browser, DEFAULT.EXPIRATION_MAX / 2), "unable to post with expiration"

    def test_expiration_min(self):
        assert WEBDRIVER_expiration(self.browser, DEFAULT.EXPIRATION_MIN), "unable to post with expiration: min"

    def test_expiration_max(self):
        assert WEBDRIVER_expiration(self.browser, DEFAULT.EXPIRATION_MAX), "unable to post with expiration: max"

    def test_expiration_none(self):
        assert WEBDRIVER_expiration(self.browser, DEFAULT.EXPIRATION_NONE), "unable to skip missing expiration"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
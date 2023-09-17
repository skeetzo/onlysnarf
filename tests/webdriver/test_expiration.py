import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import expiration

configure_logs_for_module_tests("OnlySnarf.lib.webdriver.expiration")

class TestSnarf(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_expiration(self):
        assert expiration(DEFAULT.EXPIRATION_MAX / 2), "unable to post with expiration"

    def test_expiration_min(self):
        assert expiration(DEFAULT.EXPIRATION_MIN), "unable to post with expiration: min"

    def test_expiration_max(self):
        assert expiration(DEFAULT.EXPIRATION_MAX), "unable to post with expiration: max"

    def test_expiration_none(self):
        assert expiration(DEFAULT.EXPIRATION_NONE), "unable to skip missing expiration"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
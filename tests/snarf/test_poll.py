import os
os.environ['ENV'] = "test"
import unittest
import datetime

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import poll
from OnlySnarf.classes.poll import Poll

configure_logs_for_module_tests("OnlySnarf.lib.webdriver.poll")

class TestSnarf(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_poll(self):
        poll_object = {
            "duration": DEFAULT.DURATION_ALLOWED[0],
            "questions": ["suck","my","dick","please?"]
        }
        poll_object = Poll.create_poll(poll_object).dump()
        assert poll(poll_object), "unable to post poll"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
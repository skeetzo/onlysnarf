import os
os.environ['ENV'] = "test"
import unittest
import datetime

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.classes.poll import Poll

class TestClasses_Poll(unittest.TestCase):

    def setUp(self):
        self.poll_object = {
            "duration": DEFAULT.DURATION_ALLOWED[0],
            "questions": ["suck","my","dick","please?"]
        }
        self.poll = Poll.create_poll(self.poll_object)

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.poll")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests(flush=True)

    def test_poll(self):
        assert self.poll, "unable to create poll object"

    def test_poll_validate(self):
        assert self.poll.validate(), "unable to validate poll object"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
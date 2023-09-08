import os
os.environ['ENV'] = "test"
import unittest
import datetime

from OnlySnarf.util.config import set_config
CONFIG = set_config({"debug_selenium":False,"debug_delay":False,"keep":False})
from OnlySnarf.util.logger import configure_logging
configure_logging(True, True)

from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.lib.driver import poll

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
        assert poll(poll_object), "unable to post poll"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
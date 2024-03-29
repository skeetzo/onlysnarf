import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf

class TestSnarf(unittest.TestCase):

    def setUp(self):
        config["duration"] = DEFAULT.DURATION_ALLOWED[0]
        config["questions"] = ["suck","my","dick","please?"]
        config["text"] = "test balls"
        Settings.set_debug("tests")

    def tearDown(self):
        config["duration"] = None
        config["questions"] = []
        Snarf.close()

    def test_poll(self):
        assert Snarf.post(), "unable to post poll"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
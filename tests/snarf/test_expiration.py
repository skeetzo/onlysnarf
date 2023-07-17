import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import config
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf

class TestSnarf(unittest.TestCase):

    def setUp(self):
        config["expiration"] = DEFAULT.EXPIRATION_MAX
        config["text"] = "test balls"
        Settings.set_debug("tests")

    def tearDown(self):
        Snarf.close()

    def test_poll(self):
        assert Snarf.post(), "unable to post with expiration"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
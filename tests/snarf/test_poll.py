import os
os.environ['ENV'] = "test"
import unittest
import datetime

from OnlySnarf.util.config import set_config
CONFIG = set_config({"debug_selenium":False,"debug_delay":False,"keep":False})
from OnlySnarf.util.logger import configure_logging
configure_logging(True, True)

from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.classes.message import Post

class TestSnarf(unittest.TestCase):

    def setUp(self):
        CONFIG["schedule"] = {}
        CONFIG["expiration"] = DEFAULT.DURATION_ALLOWED[0]
        CONFIG["questions"] = ["suck","my","dick","please?"]
        CONFIG["text"] = "test balls"
        self.post = Post.create_post({**CONFIG})

    def tearDown(self):
        pass

    def test_poll(self):
        assert self.post.send(), "unable to post poll"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
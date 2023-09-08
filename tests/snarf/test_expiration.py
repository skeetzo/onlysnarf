import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({"debug_selenium":False,"debug_delay":False,"keep":False})
from OnlySnarf.util.logger import configure_logging
configure_logging(True, True)

from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.classes.message import Post

class TestSnarf(unittest.TestCase):

    def setUp(self):
        CONFIG["poll"] = {}
        CONFIG["schedule"] = {
            "date" : DEFAULT.DATE,
            "time" : DEFAULT.TIME
        }
        CONFIG["expiration"] = DEFAULT.EXPIRATION_MAX
        CONFIG["text"] = "test balls"

    def tearDown(self):
        pass

    def test_poll(self):
        self.post = Post.create_post({**CONFIG, 'keywords':[]})
        assert self.post.send(), "unable to post with expiration"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
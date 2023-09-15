import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({'prefer_local':True})
from OnlySnarf.util.logger import configure_logging
configure_logging(True, True)

# from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.classes.message import Message

class TestSnarf(unittest.TestCase):

    def setUp(self):
        CONFIG["schedule"] = {}
        CONFIG["text"] = "test balls"
        CONFIG["recipients"] = ["random"]
        CONFIG["input"] = []

    def tearDown(self):
        # remove_from_randomized_users()
        pass

    def test_user_on_success(self):
        message = Message.create_message({**CONFIG})
        message.on_success()

        # TODO: add asserts for checking text & files variables in user object and saved user data have been updated

############################################################################################

if __name__ == '__main__':
    unittest.main()
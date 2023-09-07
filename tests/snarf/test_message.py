import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({"skip_upload":False,"skip_download":False,"debug_selenium":False,"debug_delay":False,"keep":False})
from OnlySnarf.util.logger import configure_logging
configure_logging(True, True)

from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.classes.message import Message

class TestSnarf(unittest.TestCase):

    def setUp(self):
        CONFIG["schedule"] = {}
        CONFIG["text"] = "test balls"
        CONFIG["recipients"] = ["random"]
        self.message = Message.create_message({**CONFIG})

    def tearDown(self):
        pass

    def test_message(self):
        assert self.message.send(), "unable to send basic message"

    def test_message_files_local(self):
        CONFIG["input"] = ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg", "/home/skeetzo/Projects/onlysnarf/public/images/snarf.jpg"]
        self.message = Message.create_message({**CONFIG})
        assert self.message.send(), "unable to upload message files - local"

    def test_message_files_remote(self):
        CONFIG["input"] = ["https://github.com/skeetzo/onlysnarf/blob/master/public/images/shnarf.jpg?raw=true", "https://github.com/skeetzo/onlysnarf/blob/master/public/images/snarf.jpg?raw=true"]
        self.message = Message.create_message({**CONFIG})
        assert self.message.send(), "unable to upload message files - remote"

    def test_message_price(self):
        CONFIG["input"] = ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg"]
        CONFIG["price"] = DEFAULT.PRICE_MINIMUM
        self.message = Message.create_message({**CONFIG})
        assert self.message.send(), "unable to set message price"

    # def test_message_failure(self):
    #     CONFIG["recipients"] = ["onlyfans"]
    #     self.message = Message.create_message({**CONFIG})
    #     assert not self.message.send(), "unable to fail message properly"

    def test_message_inactive_user(self):
        CONFIG["recipients"] = ["yeahzers"]
        self.message = Message.create_message({**CONFIG})
        assert not self.message.send(), "unable to properly fail messaging an inactive user"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
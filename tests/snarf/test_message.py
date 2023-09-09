import os
os.environ['ENV'] = "test"
import unittest

from OnlySnarf.util.config import set_config
CONFIG = set_config({"show":True})
from OnlySnarf.util.logger import configure_logging
configure_logging(True, True)

from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.classes.message import Message

class TestSnarf(unittest.TestCase):

    def setUp(self):
        CONFIG["schedule"] = {}
        CONFIG["text"] = "test balls"
        CONFIG["recipients"] = ["random"]
        CONFIG["input"] = []

    def tearDown(self):
        pass

    # def test_message(self):
        # assert Message.create_message({**CONFIG}).send(), "unable to send basic message"

    def test_message_all(self):
        assert Message.create_message({**CONFIG,"includes":["all","following","favorites","friends","renew on","renew off"]}).send(), "unable to send message to: all"

    # def test_message_recent(self):
    #     assert Message.create_message({**CONFIG,"includes":["recent"]}).send(), "unable to send message to: recent"

    # def test_message_favorite(self):
    #     assert Message.create_message({**CONFIG,"includes":["favorite"]}).send(), "unable to send message to: favorite"

    # def test_message_renew_on(self):
    #     assert Message.create_message({**CONFIG,"includes":["renew on"]}).send(), "unable to send message to: renew on"

    # def test_message_renew_off(self):
    #     assert Message.create_message({**CONFIG,"includes":["renew off"]}).send(), "unable to send message to: renew off"

    # def test_message_bookmarks(self):
    #     assert Message.create_message({**CONFIG,"includes":["bookmarks"]}).send(), "unable to send message to: bookmarks"

    # def test_message_exclude_recent(self):
    #     assert Message.create_message({**CONFIG,"includes":["all"],"excludes":["recent"]}).send(), "unable to exclude message from: recent"

    # def test_message_exclude_favorite(self):
    #     assert Message.create_message({**CONFIG,"includes":["all"],"excludes":["favorite"]}).send(), "unable to exclude message from: favorite"

    # def test_message_exclude_renew_on(self):
    #     assert Message.create_message({**CONFIG,"includes":["all"],"excludes":["renew on"]}).send(), "unable to exclude message from: renew on"

    # def test_message_exclude_renew_off(self):
    #     assert Message.create_message({**CONFIG,"includes":["all"],"excludes":["renew off"]}).send(), "unable to exclude message from: renew off"

    # def test_message_exclude_bookmarks(self):
    #     assert Message.create_message({**CONFIG,"includes":["all"],"excludes":["bookmarks"]}).send(), "unable to exclude message from: bookmarks"







    # def test_message_files_local(self):
    #     CONFIG["input"] = ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg", "/home/skeetzo/Projects/onlysnarf/public/images/snarf.jpg"]
    #     assert Message.create_message({**CONFIG}).send(), "unable to upload message files - local"

    # def test_message_files_remote(self):
    #     CONFIG["input"] = ["https://github.com/skeetzo/onlysnarf/blob/master/public/images/shnarf.jpg?raw=true", "https://github.com/skeetzo/onlysnarf/blob/master/public/images/snarf.jpg?raw=true"]
    #     assert Message.create_message({**CONFIG}).send(), "unable to upload message files - remote"

    # def test_message_price(self):
    #     CONFIG["input"] = ["/home/skeetzo/Projects/onlysnarf/public/images/shnarf.jpg"]
    #     CONFIG["price"] = DEFAULT.PRICE_MINIMUM
    #     assert Message.create_message({**CONFIG}).send(), "unable to set message price"

    # def test_message_failure(self):
    #     CONFIG["recipients"] = ["onlyfans"]
    #     assert not Message.create_message({**CONFIG}).send(), "unable to fail message properly"

    # def test_message_inactive_user(self):
    #     import string
    #     import random
    #     CONFIG["recipients"] = [''.join(random.choices(string.ascii_uppercase + string.digits, k=8))]
    #     assert not Message.create_message({**CONFIG}).send(), "unable to properly fail messaging an inactive user"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
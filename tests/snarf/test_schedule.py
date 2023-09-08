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

today = datetime.datetime.now()
tomorrow = today + datetime.timedelta(days=1, hours=13, minutes=10)

class TestSnarf(unittest.TestCase):

    def setUp(self):
        CONFIG["text"] = "test balls"
        CONFIG["schedule"] = {
            "date" : DEFAULT.DATE,
            "time" : DEFAULT.TIME
        }

    def tearDown(self):
        pass

    def test_schedule(self):
        CONFIG["schedule"] = {
            "date" : tomorrow.strftime(DEFAULT.DATE_FORMAT),
            "time" : (today + datetime.timedelta(hours=1, minutes=30)).strftime(DEFAULT.TIME_FORMAT)
        }
        self.post = Post.create_post({**CONFIG})
        assert self.post.send(), "unable to post schedule"

    # TODO: are these even necessary?
    @unittest.skip("todo")
    def test_schedule_calendar_day(self):
        pass

    @unittest.skip("todo")
    def test_schedule_calendar_hour(self):
        pass

    @unittest.skip("todo")
    def test_schedule_calendar_minute(self):
        pass

    @unittest.skip("todo")
    def test_schedule_calendar_suffix(self):
        pass

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
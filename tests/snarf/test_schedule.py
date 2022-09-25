import os
os.environ['ENV'] = "test"
import unittest
import datetime

from OnlySnarf.util.config import config
from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.util.settings import Settings
from OnlySnarf.snarf import Snarf

today = datetime.datetime.now()
tomorrow = today + datetime.timedelta(days=1, hours=13, minutes=10)

class TestSnarf(unittest.TestCase):

    def setUp(self):
        config["keep"] = True
        config["text"] = "test balls"
        Settings.set_debug("tests")
        self.test_snarf = Snarf()

    def tearDown(self):
        config["schedule"] = DEFAULT.SCHEDULE
        config["date"] = DEFAULT.DATE
        config["time"] = DEFAULT.TIME
        self.test_snarf.close()
        config["keep"] = False

    # @unittest.skip("works")
    def test_schedule(self):
        config["schedule"] = tomorrow.strftime(DEFAULT.SCHEDULE_FORMAT)
        assert self.test_snarf.post(), "unable to post schedule"
        
    @unittest.skip("todo")
    def test_schedule_date(self):
        config["date"] = tomorrow.strftime(DEFAULT.DATE_FORMAT)
        assert self.test_snarf.post(), "unable to post schedule via date"

    @unittest.skip("todo")
    def test_schedule_time(self):
        config["time"] = tomorrow.strftime(DEFAULT.TIME_FORMAT)
        assert self.test_snarf.post(), "unable to post schedule via time"

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
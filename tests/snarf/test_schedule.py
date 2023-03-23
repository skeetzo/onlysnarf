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
        config["schedule"] = DEFAULT.SCHEDULE
        config["date"] = DEFAULT.DATE
        config["time"] = DEFAULT.TIME
        Settings.set_debug("tests")

    def tearDown(self):
        Snarf.close()

    def test_schedule(self):
        config["schedule"] = tomorrow.strftime(DEFAULT.SCHEDULE_FORMAT)
        assert Snarf.post(), "unable to post schedule"
        
    def test_schedule_date(self):
        config["date"] = tomorrow.strftime(DEFAULT.DATE_FORMAT)
        assert Snarf.post(), "unable to post schedule via date"

    def test_schedule_time(self):
        config["time"] = (today + datetime.timedelta(hours=1, minutes=30)).strftime(DEFAULT.TIME_FORMAT)
        assert Snarf.post(), "unable to post schedule via time"

    ## TODO:
    # verify correct values by getting values of selected components:
        # vdatetime-calendar__current--month
    #     day, month, year: class="vdatetime-calendar__month__day vdatetime-calendar__month__day--selected"
    #     vdatetime-time-picker__item vdatetime-time-picker__item--selected

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
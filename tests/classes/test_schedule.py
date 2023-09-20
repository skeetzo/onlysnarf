import os
os.environ['ENV'] = "test"
import unittest
import datetime

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.util import defaults as DEFAULT
from OnlySnarf.classes.schedule import Schedule

today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1, hours=13, minutes=10)
tomorrow = today + datetime.timedelta(days=1, hours=13, minutes=10)

class TestClasses_Schedule(unittest.TestCase):

    def setUp(self):
        self.schedule_object = {
            "date" : tomorrow.strftime(DEFAULT.DATE_FORMAT),
            "time" : (today + datetime.timedelta(hours=1, minutes=30)).strftime(DEFAULT.TIME_FORMAT)
        }
        self.schedule = Schedule.create_schedule(self.schedule_object)

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.classes.schedule")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests(flush=True)

    def test_schedule(self):
        assert self.schedule, "unable to create schedule object"

    # TODO: possibly update these values
    def test_schedule_format_date(self):
        self.assertEqual(Schedule.format_date(DEFAULT.DATE), DEFAULT.DATE,"unable to format schedule date")

    def test_schedule_format_time(self):
        self.assertEqual(Schedule.format_time(DEFAULT.TIME), DEFAULT.TIME,"unable to format schedule date")

    def test_schedule_format_schedule(self):
        self.assertEqual(Schedule.format_schedule(DEFAULT.DATE, DEFAULT.TIME), DEFAULT.SCHEDULE,"unable to format schedule")

    def test_schedule_validate(self):
        assert self.schedule.validate(), "unable to validate schedule object"

    def test_schedule_invalidate_date(self):
        self.schedule_object = {
            "date" : yesterday.strftime(DEFAULT.DATE_FORMAT),
            "time" : (today + datetime.timedelta(hours=1, minutes=30)).strftime(DEFAULT.TIME_FORMAT)
        }
        self.schedule = Schedule.create_schedule(self.schedule_object)
        assert not self.schedule.validate(), "unable to invalidate late schedule object via date"

    def test_schedule_invalidate_time(self):
        self.schedule_object = {
            "date" : today.strftime(DEFAULT.DATE_FORMAT),
            "time" : (yesterday - datetime.timedelta(hours=1, minutes=30)).strftime(DEFAULT.TIME_FORMAT)
        }
        self.schedule = Schedule.create_schedule(self.schedule_object)
        assert not self.schedule.validate(), "unable to invalidate late schedule object via time"

############################################################################################

if __name__ == '__main__':
    unittest.main(warnings='ignore')
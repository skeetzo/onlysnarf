import os
os.environ['ENV'] = "test"
import unittest
import datetime

from OnlySnarf.util.config import set_config
CONFIG = set_config({})
from OnlySnarf.util.logger import configure_logging, configure_logs_for_module_tests
configure_logging(True, True)

from OnlySnarf.classes.schedule import Schedule
from OnlySnarf.lib.driver import login as get_browser_and_login, close_browser
from OnlySnarf.lib.webdriver.schedule import schedule as WEBDRIVER_schedule
from OnlySnarf.util import defaults as DEFAULT

today = datetime.datetime.now()
tomorrow = today + datetime.timedelta(days=1, hours=13, minutes=10)

class TestWebdriver_Schedule(unittest.TestCase):

    def setUp(self):
        self.browser = get_browser_and_login(cookies=CONFIG["cookies"])
        self.schedule_object = {
            "date" : tomorrow.strftime(DEFAULT.DATE_FORMAT),
            "time" : (today + datetime.timedelta(hours=1, minutes=30)).strftime(DEFAULT.TIME_FORMAT)
        }
        # creating a schedule object is annoying without the class helpers
        self.schedule_object = Schedule.create_schedule(self.schedule_object).dump()

    def tearDown(self):
        pass

    @classmethod
    def setUpClass(cls):
        configure_logs_for_module_tests("OnlySnarf.lib.webdriver.schedule")

    @classmethod
    def tearDownClass(cls):
        configure_logs_for_module_tests(flush=True)

    def test_schedule(self):
        assert WEBDRIVER_schedule(self.browser, self.schedule_object), "unable to post schedule"

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
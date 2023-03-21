from datetime import datetime

from ..util import defaults as DEFAULT
from ..util.settings import Settings

class Schedule:

    def __init__(self):
        self._initialized_ = False
        self.date = None
        self.time = None
        ##
        self.hour = "00"
        self.minute = "00"
        self.year = "0"
        self.month = "0"
        self.day = "0"
        self.suffix = "am"
        ##
        self.init()

    def init(self):
        """Initialize the schedule's settings"""

        if self._initialized_: return
        Settings.dev_print("initiliazing schedule...")
        schedule = Settings.get_schedule()
        date = datetime.strptime(str(schedule), DEFAULT.SCHEDULE_FORMAT)
        self.year = date.year
        self.month = date.strftime("%B")
        self.day = date.day
        self.hour = date.hour
        self.minute = date.minute
        self.suffix = "am"
        if int(self.hour) > 12:
            self.suffix = "pm"
            self.hour = int(self.hour) - 12
        Settings.dev_print("year: {}".format(self.year))
        Settings.dev_print("month: {}".format(self.month))
        Settings.dev_print("day: {}".format(self.day))
        Settings.dev_print("hour: {}".format(self.hour))
        Settings.dev_print("minutes: {}".format(self.minute))
        Settings.dev_print("suffix: {}".format(self.suffix))
        Settings.dev_print("initiliazed schedule")
        self._initialized_ = True

    def get(self):
        """
        Get the schedule's values in a dict.

        Returns
        -------
        dict
            A dict containing the values of the schedule

        """

        return dict({
            "date": self.get_date(),
            "time": self.get_time(),
            "hour" : self.hour,
            "minute" : self.minute,
            "year" : self.year,
            "month" : self.month,
            "day" : self.day,
            "suffix" : self.suffix
        })

    def get_date(self):
        """
        Gets the date value if not none else sets it from args or prompts.

        Returns
        -------
        str
            The date as a valid date string

        """

        if self.date: return self.date
        self.date = Settings.get_date()
        return self.date

        # prompt skip
        # confirm date
        if not Settings.confirm(date): return self.get_date()
        self.date = date
        return self.date

    def get_time(self):
        """
        Gets the time value if not none else sets it from args or prompts.

        Returns
        -------
        str
            The time as a valid time string

        """

        if self.time: return self.time
        # retrieve from args and return if exists
        self.time = Settings.get_time()
        return self.time



        # # if time: 
        # time = datetime.strptime(str(time), DEFAULT.SCHEDULE_FORMAT)
        # # Settings.dev_print(time)
        # time = time.strftime("%I:%M %p")
        # # Settings.dev_print(time)
        # self.time = time
        # return self.time

        # retrieve time from schedule args and return if exists
        schedule = Settings.get_schedule() or None
        if schedule:
            time = datetime.strptime(str(schedule), DEFAULT.SCHEDULE_FORMAT)
            # Settings.dev_print(time)
            time = time.strftime("%I:%M %p")
            # Settings.dev_print(time)
            self.time = time
            return self.time
        # prompt skip
        # confirm time
        if not Settings.confirm(time): return self.get_time()
        self.time = time
        return self.time

    def validate(self):
        """
        Determines whether or not the schedule settings are valid.

        Returns
        -------
        bool
            Whether or not the schedule is valid

        """

        Settings.dev_print("validating schedule...")
        today = datetime.strptime(str(datetime.now().strftime(DEFAULT.SCHEDULE_FORMAT)), DEFAULT.SCHEDULE_FORMAT)
        # schedule = datetime.strptime(str(Settings.get_schedule().now().strftime(DEFAULT.SCHEDULE_FORMAT)), DEFAULT.SCHEDULE_FORMAT)
        schedule = Settings.get_schedule()
        if isinstance(schedule, str):
            schedule = datetime.strptime(schedule, DEFAULT.SCHEDULE_FORMAT)
        # should invalidate if all default settings
        if str(self.get_date()) == DEFAULT.DATE and (str(self.get_time()) == DEFAULT.TIME or str(self.get_time()) == DEFAULT.TIME_NONE):
            Settings.dev_print("invalid schedule! (default date and time)")
            return False
        # cannot post in the past
        # TODO: possibly add margin of error if necessary
        elif schedule <= today:
            Settings.dev_print("invalid schedule! (must be in future)")
            return False
        Settings.dev_print("valid schedule!")
        return True

# round to 5
def myround(x, base=5):
    return base * round(x/base)
from datetime import datetime
from PyInquirer import prompt

from ..util import defaults as DEFAULT
from ..util.settings import Settings
from ..util.validators import TimeValidator, DateValidator

class Schedule:

    def __init__(self):
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
        Settings.dev_print("initiliazing schedule...")

        date = self.get_date()
        time = self.get_time()
        
        if "am" in str(time).lower(): self.suffix = "am"
        elif "pm" in str(time).lower(): self.suffix = "pm"

        self.year = date.year
        self.month = date.strftime("%B")
        self.day = date.day
        self.hour = date.hour
        self.minute = date.minute
        Settings.dev_print("initiliazed schedule")

    def get(self):
        Settings.maybe_print("Schedule:")
        Settings.maybe_print("year: {}".format(self.year))
        Settings.maybe_print("month: {}".format(self.month))
        Settings.maybe_print("day: {}".format(self.day))
        Settings.maybe_print("hour: {}".format(self.hour))
        Settings.maybe_print("minutes: {}".format(self.minute))
        if not self.validate(): return None
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
        if not Settings.prompt("date"): return None
        question = {
            'type': 'input',
            'name': 'date',
            'message': 'Enter a date (MM-DD-YYYY):',
            'validate': DateValidator
        }
        date = prompt(question)["date"]
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
        if not Settings.prompt("time"): return None
        question = {
            'type': 'input',
            'name': 'time',
            'message': 'Enter a time (HH:MM:SS):',
            'validate': TimeValidator
        }
        time = prompt(question)["time"]
        # confirm time
        if not Settings.confirm(time): return self.get_time()
        self.time = time
        return self.time

    def validate(self):
        Settings.dev_print("validating schedule...")

        today = datetime.now()
        todayF = today.strftime("%B")
        year = today.year
        yearF = today.strftime("%Y")
        time = today.time()
        timeF = time.strftime(DEFAULT.TIME_FORMAT)

        Settings.dev_print("today: {}".format(todayF))
        Settings.dev_print("year: {}".format(year))
        Settings.dev_print("yearF: {}".format(yearF))
        Settings.dev_print("time: {}".format(time))
        Settings.dev_print("timeF: {}".format(timeF))
        Settings.dev_print("vs")
        Settings.dev_print("date: {}".format(self.get_date()))
        Settings.dev_print("time: {}".format(self.get_time()))

        return True

        if str(self.get_date()) == str(today):
            Settings.dev_print("valid!")
        if str(self.get_time()) == str(time):
            Settings.dev_print("valid!")
        else:
            Settings.dev_print("invalid!")

        # if not date__:
        #     Settings.err_print("unable to parse date")
        #     return False
        # if date__ < today:
        #     Settings.err_print("unable to schedule earlier date")
        #     return False


# round to 5
def myround(x, base=5):
    return base * round(x/base)
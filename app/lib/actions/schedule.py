import re
from datetime import datetime
from .driver import Driver
from .settings import Settings
from .user import User
from PyInquirer import prompt
from PyInquirer import Validator, ValidationError
##
from .validators import AmountValidator, MonthValidator, LimitValidator, PriceValidator, NumberValidator, TimeValidator, DateValidator, DurationValidator, PromoDurationValidator, ExpirationValidator, ListValidator
from . import remote as Remote
from .file import File, Folder, Google_File, Google_Folder

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
        self.gotten = False

    def apply(self):
        self.get()
        if not self.gotten: return
        if not Settings.prompt("Schedule"): return

    def check(self):
        if self.get_date() and self.get_time(): return True
        return False

    def get(self):
        if self.gotten: return
        if self.get_date():
            date = self.get_date()
            maybe_print(0)
            maybe_print(date)
            if self.get_time():
                maybe_print(11)
                maybe_print(self.get_time())
                if "00:00:00" in str(date):
                    date = str(date).replace("00:00:00", self.get_time())
                else:
                    date = "{} {}".format(date, self.get_time())
            if "am" in self.get_time().lower(): self.suffix = "am"
            elif "pm" in self.get_time().lower(): self.suffix = "pm"
            maybe_print(1)
            maybe_print(date)
            date = datetime.strptime(str(date), "%Y-%m-%d %H:%M %p")
            maybe_print(2)
            maybe_print(date)
            self.year = date.year
            self.month = date.strftime("%B")
            self.day = date.day
            self.hour = date.hour
            self.minute = date.minute
            maybe_print("year: {}".format(self.year))
            maybe_print("month: {}".format(self.month))
            maybe_print("day: {}".format(self.day))
            maybe_print("hour: {}".format(self.hour))
            maybe_print("minutes: {}".format(self.minute))
        self.gotten = True

    def get_date(self):
        """
        Gets the date value if not none else sets it from args or prompts.

        Returns
        -------
        str
            The date as a valid date string

        """

        if self.date: return self.date
        date = Settings.get_date() or None
        if date: 
            self.date = date
            return date
        # retrieve from args and return if exists
        schedule = Settings.get_schedule() or None
        if schedule:
            date = datetime.strptime(str(schedule), "%Y-%m-%d %H:%M:%S")
            self.date = date.date()
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
        time = Settings.get_time() or None
        if time: 
            time = datetime.strptime(str(time), "%Y-%m-%d %H:%M:%S")
            # Settings.dev_print(time)
            time = time.strftime("%I:%M %p")
            # Settings.dev_print(time)
            self.time = time
            return self.time
        # retrieve time from schedule args and return if exists
        schedule = Settings.get_schedule() or None
        if schedule:
            time = datetime.strptime(str(schedule), "%Y-%m-%d %H:%M:%S")
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
            'message': 'Enter a time (HH:MM):',
            'validate': TimeValidator
        }
        time = prompt(question)["time"]
        # confirm time
        if not Settings.confirm(time): return self.get_time()
        self.time = time
        return self.time

# round to 5
def myround(x, base=5):
    return base * round(x/base)
from datetime import datetime

from ..util.defaults import DATE, SCHEDULE_FORMAT, TIME, TIME_NONE
from ..util.settings import Settings

class ScheduleSchema(Schema):
    schedule = fields.Str()
    date = fields.Str()
    time = fields.Str()
    hour = fields.Str(default="00")
    minute = fields.Str(default="00")
    year = fields.Int(default=0)
    month = fields.Int(default=0)
    day = fields.Int(default=0)
    suffix = fields.Str(default="am")

    @post_load
    def make_schedule(self, data, **kwargs):
        return Schedule(**data)

class Schedule:

    def __init__(self, schedule, date, time, hour, minute, year, month, day, suffix):
        self._initialized_ = False
        self.schedule = schedule
        self.date = date
        self.time = time
        self.hour = hour
        self.minute = minute
        self.year = year
        self.month = month
        self.day = day
        self.suffix = suffix
        # self.init()

    @staticmethod
    def create_schedule(schedule_data):
        schema = ScheduleSchema()
        return schema.load(schedule_data)

    def dump(self):
        schema = ScheduleSchema()
        result = schema.dump(self)
        # pprint(result, indent=2)
        return result

    def init(self):
        """Initialize the schedule's settings"""

        if self._initialized_: return
        Settings.dev_print("initiliazing schedule...")
        self.schedule = Settings.get_schedule()
        date = datetime.strptime(str(self.schedule), SCHEDULE_FORMAT)
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

    def get_schedule(self):
        if self.schedule: return self.schedule
        self.schedule = Settings.get_schedule()
        return self.schedule

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
        # time = datetime.strptime(str(time), SCHEDULE_FORMAT)
        # # Settings.dev_print(time)
        # time = time.strftime("%I:%M %p")
        # # Settings.dev_print(time)
        # self.time = time
        # return self.time

        # retrieve time from schedule args and return if exists
        schedule = Settings.get_schedule() or None
        if schedule:
            time = datetime.strptime(str(schedule), SCHEDULE_FORMAT)
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
        today = datetime.strptime(str(datetime.now().strftime(SCHEDULE_FORMAT)), SCHEDULE_FORMAT)
        # schedule = datetime.strptime(str(Settings.get_schedule().now().strftime(SCHEDULE_FORMAT)), SCHEDULE_FORMAT)
        schedule = Settings.get_schedule()
        if not schedule: return False
        if isinstance(schedule, str):
            schedule = datetime.strptime(schedule, SCHEDULE_FORMAT)
        # should invalidate if all default settings
        if str(self.get_date()) == DATE and (str(self.get_time()) == TIME or str(self.get_time()) == TIME_NONE):
            Settings.dev_print("invalid schedule! (default date and time)")
            return False
        # cannot post in the past
        # TODO: possibly add margin of error if necessary
        elif schedule <= today:
            Settings.dev_print("invalid schedule! (must be in future)")
            return False
        Settings.dev_print("valid schedule!")
        return True














    def format_date(date):
        try:
            date = Settings.format_date(date)
            if str(date) == DATE and str(config["schedule"]) != SCHEDULE and str(config["schedule"] != "None"):
                if isinstance(config["schedule"], str):
                    date = datetime.strptime(config["schedule"], SCHEDULE_FORMAT).date().strftime(DATE_FORMAT)
                else:
                    date = config["schedule"].date().strftime(DATE_FORMAT)
                date = datetime.strptime(str(date), DATE_FORMAT)
            else:
                date = datetime.strptime(str(date), DATE_FORMAT)
            date = date.strftime(DATE_FORMAT)    
        except Exception as e:
            date = datetime.strptime(DATE, DATE_FORMAT)
        Settings.maybe_print("date (settings): {}".format(str(date)[:10]))
        return str(date)[:10]

    def format_time(time):
        try:
            time = Settings.format_time(time)        
            if (str(time) == TIME or str(time) == TIME_NONE) and str(config["schedule"]) != SCHEDULE and str(config["schedule"]) != "None":
                Settings.dev_print("time from schedule")
                date = datetime.strptime(str(config["schedule"]), SCHEDULE_FORMAT)
                time = datetime.strptime(str(date.time().strftime(TIME_FORMAT)), TIME_FORMAT)
            else:
                Settings.dev_print("time from config")
                time = datetime.strptime(str(time), TIME_FORMAT)
            time = time.strftime(TIME_FORMAT)
        except Exception as e:
            time = datetime.strptime(TIME, TIME_FORMAT).strftime(TIME_FORMAT)
        Settings.maybe_print("time (settings): {}".format(str(time)[:9]))
        return str(time)[:9]

    def format_schedule(schedule=""):
        try:
            if str(schedule) == "None": schedule = SCHEDULE
            if str(schedule) == SCHEDULE:
                schedule = datetime.strptime(schedule, SCHEDULE_FORMAT).strftime(SCHEDULE_FORMAT)
            elif not isinstance(schedule, str):
                schedule = schedule.strftime(SCHEDULE_FORMAT)
        except Exception as e:
            schedule = datetime.strptime("{} {}".format(Settings.get_date(), Settings.get_time()), SCHEDULE_FORMAT).strftime(SCHEDULE_FORMAT)
        Settings.maybe_print("schedule (settings): {}".format(schedule))
        return str(schedule)[:20] # must be less than 19 characters

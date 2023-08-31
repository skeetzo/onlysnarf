import logging
from datetime import datetime
from marshmallow import Schema, fields, validate, post_load

from ..util.defaults import DATE, DATE_FORMAT, SCHEDULE, SCHEDULE_FORMAT, TIME, TIME_FORMAT, TIME_NONE

class ScheduleSchema(Schema):
    schedule = fields.Str()
    date = fields.Str()
    time = fields.Str()
    hour = fields.Str(default="00")
    minute = fields.Str(default="00")
    year = fields.Str(default="0")
    month = fields.Str(default="0")
    day = fields.Str(default="0")
    suffix = fields.Str(default="am")

    @post_load
    def make_schedule(self, data, **kwargs):
        return Schedule(**data)

class Schedule:

    def __init__(self, date, time):
        self.date = Schedule.format_date(date)
        self.time = Schedule.format_time(time)
        self.schedule = datetime.strptime(Schedule.format_schedule(date, time), SCHEDULE_FORMAT) # saved as a datetime
        self.year = schedule.year
        self.month = schedule.strftime("%B")
        self.day = schedule.day
        self.hour = schedule.hour
        self.minute = schedule.minute
        self.suffix = "am"
        if int(self.hour) > 12:
            self.suffix = "pm"
            self.hour = int(self.hour) - 12

    @staticmethod
    def create_schedule(schedule_data):
        schema = ScheduleSchema()
        return schema.load(schedule_data)

    def dump(self):
        if not self.validate(): return {}
        schema = ScheduleSchema()
        result = schema.dump(self)
        # pprint(result, indent=2)
        return result

    @staticmethod
    def format_date(date_string):
        date = ""
        try:
            date = datetime.strptime(str(date_string), DATE_FORMAT)    
        except Exception as e:
            logging.debug(f"unable to format date: {date_string}")
            logging.error(e)
            date = datetime.strptime(DATE, DATE_FORMAT)
        date = date.strftime(DATE_FORMAT)[:10]
        logging.debug(f"formatted date: {date}")
        return str(date)

    @staticmethod
    def format_time(time_string):
        time = ""
        try:
            time = datetime.strptime(str(time_string), TIME_FORMAT)
        except Exception as e:
            logging.debug(f"unable to format time: {time_string}")
            logging.error(e)
            time = datetime.strptime(TIME, TIME_FORMAT)
        time = time.strftime(TIME_FORMAT)[:9]
        logging.debug(f"formatted time: {time}")
        return str(time)

    @staticmethod
    def format_schedule(date_string, time_string):
        schedule = ""
        try:
            schedule_string = f"{Schedule.format_date(date_string)} {Schedule.format_time(time_string)}"
            schedule = datetime.strptime(schedule_string, SCHEDULE_FORMAT)
        except Exception as e:
            logging.debug(f"unable to format schedule: {date_string} {time_string}")
            logging.error(e)
            schedule = datetime.strptime(SCHEDULE, SCHEDULE_FORMAT)
        schedule = schedule.strftime(SCHEDULE_FORMAT)
        logging.debug(f"formatted schedule: {schedule}")
        return str(schedule)

    def validate(self):
        """
        Determines whether or not the schedule settings are valid.

        Returns
        -------
        bool
            Whether or not the schedule is valid

        """

        logging.debug("validating schedule...")
        today = datetime.strptime(str(datetime.now().strftime(SCHEDULE_FORMAT)), SCHEDULE_FORMAT)
        if not self.schedule: return False
        # should invalidate if all default settings
        if self.date == DATE and (self.time == TIME or self.time == TIME_NONE):
            logging.debug("invalid schedule! (default date and time)")
            return False
        elif self.schedule <= today:
            logging.debug("invalid schedule! (must be in future)")
            return False
        logging.debug("valid schedule!")
        return True

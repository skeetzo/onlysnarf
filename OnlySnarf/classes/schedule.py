import logging
logger = logging.getLogger(__name__)
from datetime import datetime
from marshmallow import Schema, fields, validate, post_load, EXCLUDE

from ..util.defaults import DATE, DATE_FORMAT, SCHEDULE, SCHEDULE_FORMAT, TIME, TIME_FORMAT, TIME_NONE

class ScheduleSchema(Schema):
    # schedule = fields.Str()
    date = fields.Str(dump_default=DATE)
    time = fields.Str(dump_default=TIME)
    hour = fields.Str(dump_default="00")
    minute = fields.Str(dump_default="00")
    year = fields.Str(dump_default="0")
    month = fields.Str(dump_default="0")
    day = fields.Str(dump_default="0")
    suffix = fields.Str(dump_default="am")

    @post_load
    def make_schedule(self, data, **kwargs):
        return Schedule(**data)

class Schedule:

    def __init__(self, date=DATE, time=TIME, hour="", day="", month="", minute="", suffix="am", year=""):
        self.date = Schedule.format_date(date)
        self.time = Schedule.format_time(time)
        self.schedule = datetime.strptime(Schedule.format_schedule(date, time), SCHEDULE_FORMAT) # saved as a datetime
        self.year = self.schedule.year
        self.month = self.schedule.strftime("%B")
        self.day = self.schedule.day
        self.hour = self.schedule.hour
        self.minute = self.schedule.minute
        self.suffix = "am"
        if int(self.hour) > 12:
            self.suffix = "pm"
            self.hour = int(self.hour) - 12

    @staticmethod
    def create_schedule(schedule_data):
        schema = ScheduleSchema(unknown=EXCLUDE)
        return schema.load(schedule_data)

    def dump(self):
        if not self.validate(): return {}
        schema = ScheduleSchema()
        return schema.dump(self)

    @staticmethod
    def format_date(date_string):
        if not date_string: return ""
        date = ""
        try:
            date = datetime.strptime(str(date_string), DATE_FORMAT)    
        except Exception as e:
            logger.debug(f"unable to format date: {date_string}")
            logger.error(e)
            date = datetime.strptime(DATE, DATE_FORMAT)
        date = date.strftime(DATE_FORMAT)[:10]
        logger.debug(f"formatted date: {date}")
        return str(date)

    @staticmethod
    def format_time(time_string):
        if not time_string: return ""
        time = ""
        try:
            time = datetime.strptime(str(time_string), TIME_FORMAT)
        except Exception as e:
            logger.debug(f"unable to format time: {time_string}")
            logger.error(e)
            time = datetime.strptime(TIME, TIME_FORMAT)
        time = time.strftime(TIME_FORMAT)[:9]
        logger.debug(f"formatted time: {time}")
        return str(time)

    @staticmethod
    def format_schedule(date_string, time_string):
        if not date_string or not time_string: return ""
        schedule = ""
        try:
            schedule_string = f"{Schedule.format_date(date_string)} {Schedule.format_time(time_string)}"
            schedule = datetime.strptime(schedule_string, SCHEDULE_FORMAT)
        except Exception as e:
            logger.debug(f"unable to format schedule: {date_string} {time_string}")
            logger.error(e)
            schedule = datetime.strptime(SCHEDULE, SCHEDULE_FORMAT)
        schedule = schedule.strftime(SCHEDULE_FORMAT)
        logger.debug(f"formatted schedule: {schedule}")
        return str(schedule)

    def validate(self):
        """
        Determines whether or not the schedule settings are valid.

        Returns
        -------
        bool
            Whether or not the schedule is valid

        """

        logger.debug("validating schedule...")
        if not self.schedule: return False
        # should invalidate if all default settings
        if self.date == DATE and (self.time == TIME or self.time == TIME_NONE):
            logger.debug("invalid schedule! (default date and time)")
            return False
        elif self.schedule < datetime.strptime(str(datetime.now().strftime(SCHEDULE_FORMAT)), SCHEDULE_FORMAT): # right now
            logger.debug("invalid schedule! (must be in future)")
            return False
        logger.debug("valid schedule!")
        return True

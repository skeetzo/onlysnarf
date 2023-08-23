import re
from datetime import datetime
from ..lib.driver import Driver
from ..util.settings import Settings
from .user import User
##
from .file import File, Folder

class PollSchema(Schema):
    duration = fields.Int(validate=validate.Range(min=1))
    questions = fields.List(fields.Str())

    @post_load
    def make_poll(self, data, **kwargs):
        return Poll(**data)

class Poll:
    """OnlyFans Poll class"""

    def __init__(self, duration=1, questions=[]):
        """OnlyFans Poll object"""

        # duration of poll
        self.duration = Poll.format_duration(duration)
        # list of strings
        self.questions = questions

    @staticmethod
    def create_poll(poll_data):
        schema = PollSchema()
        return schema.load(poll_data)

    def dump(self):
        schema = PollSchema()
        result = schema.dump(self)
        # pprint(result, indent=2)
        return result

    @staticmethod
    def format_duration(duration):
        """
        Gets the duration value if not none else sets it from args or prompts.

        Returns
        -------
        int
            The duration as an int

        """

        if int(duration) > 30: return "No limit"
        return duration

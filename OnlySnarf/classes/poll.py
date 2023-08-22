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

    def __init__(self, duration, questions):
        """OnlyFans Poll object"""

        # duration of poll
        self.duration = duration
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

    def get(self):
        """
        Get the poll's values in a dict.

        Returns
        -------
        dict
            A dict containing the values of the poll

        """

        return dict({
            "duration": self.get_duration(),
            "questions": self.get_questions()
        })

    def get_duration(self):
        """
        Gets the duration value if not none else sets it from args or prompts.

        Returns
        -------
        int
            The duration as an int

        """

        if self.duration: return self.duration
        self.duration = Settings.get_duration()
        if int(self.duration) > 30: self.duration = "No limit"
        return self.duration

    def get_questions(self):
        """
        Gets the questions value if not none else sets it from args or prompts.

        Returns
        -------
        list
            The questions as strings in a list

        """

        if len(self.questions) > 0: return self.questions
        self.questions = Settings.get_questions()
        return self.questions

    def validate(self):
        """
        Determines whether or not the poll settings are valid.

        Returns
        -------
        bool
            Whether or not the poll is valid

        """

        Settings.dev_print("validating poll...")
        if len(self.get_questions()) > 0 and str(self.get_duration()) != "0":
            Settings.dev_print("valid poll!")
            return True
        Settings.dev_print("invalid poll!")
        return False
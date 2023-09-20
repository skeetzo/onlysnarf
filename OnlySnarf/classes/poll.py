import logging
logger = logging.getLogger(__name__)
from marshmallow import Schema, fields, validate, ValidationError, post_load, EXCLUDE

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
        schema = PollSchema(unknown=EXCLUDE)
        return schema.load(poll_data)

    def dump(self):
        if not self.validate(): return {}
        schema = PollSchema()
        return schema.dump(self)

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

    def validate(self):
        logger.debug("validating poll...")
        if len(self.questions) > 0:
            logger.debug("valid poll!")
            return True
        logger.debug("invalid poll!")
        return False
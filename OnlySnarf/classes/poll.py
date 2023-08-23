
from marshmallow import Schema, fields, validate, ValidationError, post_load

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
        if not self.validate(): return {}
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

    def validate(self):
        if len(self.questions) > 0: return True
        return False
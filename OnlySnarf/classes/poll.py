import re
from datetime import datetime
from ..lib.driver import Driver
from ..util.settings import Settings
from .user import User
from PyInquirer import prompt
from PyInquirer import Validator, ValidationError
##
from ..util.validators import AmountValidator, MonthValidator, LimitValidator, PriceValidator, NumberValidator, TimeValidator, DateValidator, DurationValidator, PromoDurationValidator, ListValidator
from .file import File, Folder

class Poll:
    """OnlyFans Poll class"""

    def __init__(self):
        """OnlyFans Poll object"""

        # duration of poll
        self.duration = None
        # list of strings
        self.questions = []
        # prevents double prompts
        self.gotten = False

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

        # # prompt skip
        # if not Settings.prompt("duration"): return None
        # question = {
        #     'type': 'input',
        #     'name': 'duration',
        #     'message': 'Duration [1, 3, 7, 99 (\'No Limit\')]',
        #     'validate': DurationValidator
        # }
        # duration = prompt(question)["duration"]
        # # confirm duration
        # if not Settings.confirm(duration): return self.get_duration()
        # self.duration = duration
        # return self.duration

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

        # # prompt skip
        # if not Settings.prompt("questions"): return []
        # print("Enter Questions")
        # while True:
        #     question = {
        #         'type': 'input',
        #         'name': 'question',
        #         'message': 'Question:',
        #     }
        #     answers = prompt(question)["question"]
        #     if str(question) == "": break
        #     questions.append(question)
        # # confirm questions
        # if not Settings.confirm(questions): return self.get_questions()
        # self.questions = questions
        # return self.questions

    def validate(self):
        """
        Determines whether or not the poll settings are valid.

        Returns
        -------
        bool
            Whether or not the poll is valid

        """

        Settings.dev_print("validating poll...")
        if len(self.get_questions()) > 0 and self.get_duration():
            Settings.dev_print("valid poll!")
            return True
        Settings.dev_print("invalid poll!")
        return False
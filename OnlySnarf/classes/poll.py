import re
from datetime import datetime
from ..lib.driver import Driver
from ..util.settings import Settings
from .user import User
from PyInquirer import prompt
from PyInquirer import Validator, ValidationError
##
from ..util.validators import AmountValidator, MonthValidator, LimitValidator, PriceValidator, NumberValidator, TimeValidator, DateValidator, DurationValidator, PromoDurationValidator, ExpirationValidator, ListValidator
from ..lib import remote as Remote
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

    def check(self):
        """Check if poll is ready with valid values

        Returns
        -------
        bool
            Whether the poll is ready to be posted or not

        """

        if len(self.get_questions()) > 0: return True
        if self.get_duration(): return True
        return False

    def get(self):
        if self.gotten: return
        gotten = self.get_duration()
        # return early if skipped
        if not gotten: return
        gotten = self.get_questions()
        # return early if skipped
        if not gotten: return
        self.gotten = True

    def get_duration(self):
        """
        Gets the duration value if not none else sets it from args or prompts.

        Returns
        -------
        int
            The duration as an int

        """

        if self.duration: return self.duration
        # retrieve from args and return if exists
        duration = Settings.get_duration()
        if duration: 
            self.duration = duration
            return duration
        # prompt skip
        if not Settings.prompt("duration"): return None
        question = {
            'type': 'input',
            'name': 'duration',
            'message': 'Duration [1, 3, 7, 99 (\'No Limit\')]',
            'validate': DurationValidator
        }
        duration = prompt(question)["duration"]
        # confirm duration
        if not Settings.confirm(duration): return self.get_duration()
        self.duration = duration
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
        # retrieve from args and return if exists
        questions = Settings.get_questions()
        if len(questions) > 0: 
            self.questions = questions
            return questions
        # prompt skip
        if not Settings.prompt("questions"): return []
        print("Enter Questions")
        while True:
            question = {
                'type': 'input',
                'name': 'question',
                'message': 'Question:',
            }
            answers = prompt(question)["question"]
            if str(question) == "": break
            questions.append(question)
        # confirm questions
        if not Settings.confirm(questions): return self.get_questions()
        self.questions = questions
        return self.questions
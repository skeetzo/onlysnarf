from ..lib.driver import Driver
from ..util.settings import Settings
from .user import User
from PyInquirer import prompt
##
from ..util.validators import AmountValidator, MonthValidator
from ..util.defaults import DISCOUNT_MAX_AMOUNT, DISCOUNT_MIN_AMOUNT, DISCOUNT_MAX_MONTHS, DISCOUNT_MIN_MONTHS

class Discount:

    """OnlyFans discount class"""

    def __init__(self, username, amount=None, months=None):

        """OnlyFans discount action."""

        self.amount = amount or DISCOUNT_MIN_AMOUNT # amount in percent
        self.months = months or DISCOUNT_MIN_MONTHS # number of months (1-12)
        self.username = username # the recipient username

    def apply(self):

        """
        Applies the discounted amount to the recipient username via Driver.discount_user

        If the targeted username is one of the matching keywords then all of the 
        matching recipients will be discounted. Values are determined by runtime args or prompted
        for.

        """

        # skip prompt if disabled
        if Settings.is_prompt():
            if not Settings.prompt("Discount"): return
        Settings.maybe_print("discounting: {}".format(self.username))
        return Driver.discount_user(self.get())

    def get(self):
        """
        Get the discount's values in a dict.

        Returns
        -------
        dict
            A dict containing the values of the discount

        """

        return dict({
            "username": self.get_username(),
            "amount": self.get_amount(),
            "months": self.get_months()
        })

    def get_amount(self):

        """
        Populate and get the amount value

        If not found in args and prompt is enabled, ask for value.

        Returns
        -------
        int
            the discounted amount to apply

        """

        return self.amount or Settings.get_amount()

    def get_months(self):

        """
        Populate and get the months value

        If not found in args and prompt is enabled, ask for value.

        Returns
        -------
        int
            the number of months to discount for

        """

        return self.months or Settings.get_months()
        

    def get_username(self):

        """
        Populate and get the username value

        If not found in args and prompt is enabled, ask for value.

        Returns
        -------
        str
            the username to discount

        """

        # if self.username: return self.username
        # self.username = Settings.get_user().username
        return self.username

    def grandfatherer(self, users=[]):

        """
        Executes the 'Grandfather' discount model

        If users is empty it is populated with users from the 'Grandfather' OnlyFans list in 
        the account. All 'Grandfather'ed users are provided with the max discount for the max months.

        Parameters
        ----------
        users : list
            list of users to 'Grandfather'

        """

        if len(users) == 0:
            users = User.get_users_by_list(name="grandfathered")
        print("Discount - Grandfathering: {} users".format(len(users)))
        self.months = DISCOUNT_MAX_MONTHS
        self.amount = DISCOUNT_MAX_AMOUNT
        # apply discount to all users
        for user in users:
            self.username = user.username
            print("Grandfathering: {}".format(self.username))
            try:
                Driver.get_driver().discount_user(discount=self)
            except Exception as e:
                print(e)
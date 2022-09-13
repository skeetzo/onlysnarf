from ..lib.driver import Driver
from ..util.settings import Settings
from .user import User
from PyInquirer import prompt
##
from ..util.validators import AmountValidator, MonthValidator

class Discount:

    """OnlyFans discount class"""

    def __init__(self):

        """OnlyFans discount action."""

        # amount in percent
        self.amount = None
        # number of months (1-12)
        self.months = None
        # the recipient username
        self.username = None
        # prevents double prompts
        self.gotten = False

    def apply(self):

        """
        Applies the discounted amount to the recipient username via Driver.discount_user

        If the targeted username is one of the matching keywords then all of the 
        matching recipients will be discounted. Values are determined by runtime args or prompted
        for.

        """

        # ensure the discount has non default values
        self.get()
        if not self.gotten:
            Settings.err_print("Unable to apply discount")
            return
        # skip prompt if disabled
        if Settings.is_prompt():
            if not Settings.prompt("Discount"): return
        Settings.maybe_print("discounting: {}".format(self.username))
        # create new or find default browser
        if self.username.lower() == "all":
            users = User.get_all_users()
        elif self.username.lower() == "recent":
            users = User.get_recent_users()
        elif self.username.lower() == "favorite":
            users = User.get_favorite_users()
        elif self.username.lower() == "new":
            users = User.get_new_users()
        else: users = [self]
        successes = 0
        failures = 0
        for user in users:
            try:
                self.username = user.username
                successful = Driver.discount_user(discount=self)
                if successful: successes+=1
                else: failures+=1
            except Exception as e:
                Settings.dev_print(e)
                failures+=1
        if failures >= successes:
            Settings.print("Successful: {} | Failed: {}".format(successes, failures))
            return False
        return True

    @staticmethod
    def create():

        """Create and apply a discount from args or prompts"""

        discount = Discount()
        discount.apply()

    def get(self):
        """Update the discount object's default values"""

        if self.gotten: return
        gotten = self.get_username()
        gotten = self.get_amount()
        gotten = self.get_months()
        self.gotten = True

    def get_amount(self):

        """
        Populate and get the amount value

        If not found in args and prompt is enabled, ask for value.

        Returns
        -------
        int
            the discounted amount to apply

        """

        if self.amount: return self.amount
        # retrieve from args and return if exists
        amount = Settings.get_amount() or None
        if amount: 
            self.amount = amount
            return amount
        # prompt skip
        if not Settings.prompt("amount"): return None
        question = {
            'type': 'input',
            'name': 'amount',
            'message': 'Amount:',
            'validate': AmountValidator,
            'filter': lambda val: int(myround(int(val)))
        }
        amount = prompt(question)["amount"]
        if not Settings.confirm(amount): return self.get_amount()
        self.amount = amount
        return self.amount

    def get_months(self):

        """
        Populate and get the months value

        If not found in args and prompt is enabled, ask for value.

        Returns
        -------
        int
            the number of months to discount for

        """

        if self.months: return self.months
        # retrieve from args and return if exists
        months = Settings.get_months() or None
        if months: 
            self.months = months
            return months
        # prompt skip
        if not Settings.prompt("months"): return None
        question = {
            'type': 'input',
            'name': 'months',
            'message': 'Months:',
            'validate': MonthValidator,
            'filter': lambda val: int(val)
        }
        months = prompt(question)["months"]
        if not Settings.confirm(months): return self.get_months()
        self.months = months
        return self.months

    def get_username(self):

        """
        Populate and get the username value

        If not found in args and prompt is enabled, ask for value.

        Returns
        -------
        str
            the username to discount

        """

        if self.username: return self.username
        self.username = User.select_user().username
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
        from .validators import DISCOUNT_MAX_MONTHS, DISCOUNT_MAX_AMOUNT
        self.months = DISCOUNT_MAX_MONTHS
        self.amount = DISCOUNT_MAX_AMOUNT
        # apply discount to all users
        for user in users:
            self.username = user.username
            print("Grandfathering: {}".format(self.username))
            try:
                Driver.discount_user(discount=self)
            except Exception as e:
                print(e)

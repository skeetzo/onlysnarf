
from .user import User
from ..util.defaults import DISCOUNT_MAX_AMOUNT, DISCOUNT_MIN_AMOUNT, DISCOUNT_MAX_MONTHS, DISCOUNT_MIN_MONTHS
from ..util.settings import Settings
from ..webdriver import discount_user as WEBDRIVER_discount_user

from marshmallow import Schema, fields, validate, post_load

# https://marshmallow.readthedocs.io/en/stable/
class DiscountSchema(Schema):
    amount = fields.Int(required=True, error_messages={"required": "Amount is required."}, validate=validate.Range(min=DISCOUNT_MIN_AMOUNT, max=DISCOUNT_MAX_AMOUNT))
    months = fields.Int(required=True, error_messages={"required": "Months is required."}, validate=validate.Range(min=DISCOUNT_MIN_MONTHS, max=DISCOUNT_MAX_MONTHS))
    username = fields.Str(required=True, error_messages={"required": "Username is required."}, validate=validate.Length(min=4))

    @post_load
    def make_discount(self, data, **kwargs):
        return Discount(**data)

class Discount:

    """OnlyFans discount class"""

    def __init__(self, amount, months, username):

        """OnlyFans discount action."""

        self.amount = amount
        self.months = months
        self.username = username # the recipient username

    @staticmethod
    def create_discount(discount_data):
        schema = DiscountSchema()
        return schema.load(discount_data)

    def dump(self):
        schema = DiscountSchema()
        result = schema.dump(self)
        # pprint(result, indent=2)
        return result

    def apply(self):

        """
        Applies the discounted amount to the recipient username via Driver.discount_user

        If the targeted username is one of the matching keywords then all of the 
        matching recipients will be discounted. Values are determined by runtime args or prompted
        for.

        """

        Settings.maybe_print("discounting: {}".format(self.username))
        return WEBDRIVER_discount_user(self.get())

    def is_valid(self):
        if self.amount and self.months and self.username:
            return True
        return False

    def get(self):
        """
        Get the discount's values in a dict.

        Returns
        -------
        dict
            A dict containing the values of the discount

        """

        return dict({
            "amount": self.get_amount(),
            "months": self.get_months(),
            "username": self.get_username()
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

        amount = self.amount or Settings.get_amount()
        if int(amount) > int(Settings.get_discount_max_amount()):
            Settings.warn_print("discount amount too high, max -> {}%".format(Settings.get_discount_max_months()))
            amount = int(Settings.get_discount_max_amount())
        elif int(amount) < int(Settings.get_discount_min_amount()):
            Settings.warn_print("discount amount too low, min -> {}%".format(Settings.get_discount_min_months()))
            amount = int(Settings.get_discount_min_amount())
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

        months = self.months or Settings.get_months()
        # check variable constraints
        if int(months) > int(Settings.get_discount_max_months()):
            Settings.warn_print("discount months too high, max -> {} months".format(Settings.get_discount_max_months()))
            months = int(Settings.get_discount_max_months())
        elif int(months) < int(Settings.get_discount_min_months()):
            Settings.warn_print("discount months too low, min -> {} months".format(Settings.get_discount_min_months()))
            months = int(Settings.get_discount_min_months())
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
                discount_user(discount=self)
            except Exception as e:
                print(e)
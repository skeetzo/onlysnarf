import logging
logger = logging.getLogger(__name__)

from .user import User
from ..lib.driver import discount_user as WEBDRIVER_discount_user
from ..util.defaults import DISCOUNT_MAX_AMOUNT, DISCOUNT_MIN_AMOUNT, DISCOUNT_MAX_MONTHS, DISCOUNT_MIN_MONTHS

from marshmallow import Schema, fields, validate, post_load, EXCLUDE

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

        self.amount = Discount.format_amount(amount)
        self.months = Discount.format_months(months)
        self.username = Discount.format_username(username) # the recipient username

    @staticmethod
    def create_discount(discount_data):
        schema = DiscountSchema(unknown=EXCLUDE)
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

        logger.debug(f"applying discount to: {self.username}")
        try:
            return WEBDRIVER_discount_user(self.dump())
        except Exception as e:
            logger.error(e)
        return False

    @staticmethod
    def format_amount(amount):
        if int(amount) > int(DISCOUNT_MAX_AMOUNT):
            logger.warning(f"discount amount too high, max -> {DISCOUNT_MAX_AMOUNT}%")
            return int(DISCOUNT_MAX_AMOUNT)
        elif int(amount) < int(DISCOUNT_MIN_AMOUNT):
            logger.warning(f"discount amount too low, min -> {DISCOUNT_MIN_AMOUNT}%")
            return int(DISCOUNT_MIN_AMOUNT)
        return amount

    @staticmethod
    def format_months(months):
        if int(months) > int(DISCOUNT_MAX_MONTHS):
            logger.warning(f"discount months too high, max -> {DISCOUNT_MAX_MONTHS} months")
            return int(DISCOUNT_MAX_MONTHS)
        elif int(months) < int(DISCOUNT_MIN_MONTHS):
            logger.warning(f"discount months too low, min -> {DISCOUNT_MIN_MONTHS} months")
            return int(DISCOUNT_MIN_MONTHS)
        return months

    @staticmethod
    def format_username(username):
        if username == "random":
            username = User.get_random_user().username
        return str(username).replace("@","")

    # TODO: update or move
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
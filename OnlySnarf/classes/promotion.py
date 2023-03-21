import re
from datetime import datetime
##

from ..lib.driver import Driver
from ..util import defaults as DEFAULT
from ..util.settings import Settings
from .file import File, Folder
from .user import User

class Promotion:
    """Promotion class"""

    def __init__(self):
        """Promotion object"""

        # the amount to discount
        self.amount = None
        # the number of trials to allow
        self.limit = None
        # the expiration of the trial
        self.expiration = None
        # the duration of the discount
        self.duration = None
        # the user to apply the promotion to
        self.user = None
        # the message to provide with the promotion
        self.message = None
        # prevents double prompts
        self.gotten = False

    @staticmethod
    def apply_to_user():
        """Applies promotion directly to user via their profile page
        
           Applying a discount to a user requires:
           - amount
           - duration
           - expiration
           - message
           - user

        """

        print("Promotion - Apply To User")
        p = Promotion()
        # ensure the promotion has non default values, return early if missing
        # p.get()
        gotten = p.get_amount()
        if not gotten: return False
        gotten = p.get_duration()
        if not gotten: return False
        gotten = p.get_expiration()
        if not gotten: return False
        gotten = p.get_message()
        if not gotten: return False
        gotten = p.get_user()
        if not gotten: return False
        # prompt skip
        from .driver import Driver
        # get default driver and apply the promotion directly
        Driver.promotion_user_directly(promotion=p)
        return True

    @staticmethod
    def create_campaign():
        """Creates a Promotional Campaign

           A campaign consists of:
           - amount
           - duration
           - expiration
           - limit
           - user
           - text

        """

        print("Promotion - Creating Campaign")
        p = Promotion()
        # ensure the promotion has non default values, return early if missing
        # p.get()
        gotten = p.get_amount()
        if not gotten: return False
        gotten = p.get_user()
        if not gotten: return False
        gotten = p.get_expiration()
        if not gotten: return False
        gotten = p.get_limit()
        if not gotten: return False
        gotten = p.get_duration()
        if not gotten: return False
        gotten = p.get_message()
        if not gotten: return False
        # prompt skip
        from .driver import Driver
        # get the default driver and enter the promotion campaign
        Driver.promotional_campaign(promotion=p)
        return True

    # requires the copy/paste and email steps
    @staticmethod
    def create_trial_link():
        """Creates a Promotional Trial Link

           A trial link consists of:
           - duration
           - expiration
           - limit
           - message
           - user
            
           Note: this creates a free trial link but does NOT send it to the user
           because it is incomplete. The copy/paste step to message to a user is nonfunctioning.           

        """

        print("Promotion - Creating Trial Link")
        p = Promotion()
        # ensure the promotion has non default values, return early if missing
        # p.get()
        gotten = p.get_duration()
        if not gotten: return False
        gotten = p.get_expiration()
        if not gotten: return False
        gotten = p.get_limit()
        if not gotten: return False
        gotten = p.get_message()
        if not gotten: return False
        gotten = p.get_user()
        if not gotten: return False
        # if not self.gotten: return
        # limit, expiration, months, user
        from .driver import Driver
        link = Driver.promotional_trial_link(promotion=p)
        # text = "Here's your free trial link!\n"+link
        # Settings.dev_print("Link: "+str(text))
        # Settings.send_email(email, text)
        return True

    def get(self):
        """Update the promotion object's default values"""

        return dict({
            "user": self.get_user(),
            "amount": self.get_amount(),
            "expiration": self.get_expiration(),
            "limit": self.get_limit(),
            "duraction": self.get_duration(),
            "message": self.get_message()
        })

    def get_amount(self):
        """
        Gets the amount value if not none else sets it from args or prompts.

        Returns
        -------
        int
            The amount as an int

        """

        if self.amount: return self.amount
        # retrieve from args and return if exists
        amount = Settings.get_amount() or None
        if amount: 
            self.amount = amount
            return amount
        # prompt skip
        if not Settings.confirm(amount): return self.get_amount()
        self.amount = amount
        return self.amount

    def get_expiration(self):
        """
        Gets the expiration value if not none else sets it from args or prompts.

        Returns
        -------
        int
            The expiration as an int

        """

        if self.expiration: return self.expiration
        # retrieve from args and return if exists
        expiration = Settings.get_expiration() or None
        if expiration: 
            self.expiration = expiration
            return expiration
        # prompt skip
        # confirm expiration
        if not Settings.confirm(expiration): return self.get_expiration()
        self.expiration = expiration
        return self.expiration

    def get_limit(self):
        """
        Gets the expiration value if not none else sets it from args or prompts.

        Returns
        -------
        int
            The expiration as an int

        """

        if self.limit: return self.limit
        # retrieve from args and return if exists
        limit = Settings.get_promotion_limit() or None
        if limit: 
            self.limit = limit
            return limit
        # prompt skip
        # confirm limit
        if not Settings.confirm(limit): return self.get_limit()
        self.limit = limit
        return self.limit

    def get_message(self):
        """
        Gets the message value if not none else sets it from args or prompts.

        Returns
        -------
        str
            The message as a str

        """

        if self.message != None: return self.message
        # retrieve from args and return if exists
        message = Settings.get_text() or None
        if message: 
            self.message = message
            return message
        # prompt skip
        # confirm message
        if not Settings.confirm(message): return self.get_text()
        self.message = message
        return self.message

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
        duration = Settings.get_promo_duration() or None
        if duration: 
            self.duration = duration
            return duration
        # duration skip
        # confirm duration
        if not Settings.confirm(duration): return self.get_duration()
        self.duration = duration
        return self.duration

    def get_user(self):
        """
        Populate and get the username value

        If not found in args and prompt is enabled, ask for value.

        Returns
        -------
        User
            the user to apply the promotion to

        """

        if self.user: return self.user
        user = User.select_user()
        self.user = user.username
        return self.user

    @staticmethod
    def grandfathered():
        """
        Executes the 'Grandfather' promotion model

        In groups of 5, existing users will be added to the 'Grandfathered' OnlyFans list and
        then provided with the max discount for the max months. If the process interrupts, 
        running again will continue to discount users not yet added to the list.

        """

        print("Promotion - Grandfather")
        # prompt skip
        Settings.maybe_print("getting users to grandfather")
        # get all users
        users = User.get_all_users()
        from .driver import Driver
        # get all users from logged in user's 'grandfathered' list
        users_, name, number = Driver.get_list(name="grandfathered")
        # remove all users that have already been grandfathered from the list of all users
        # users = [user for user in users if user not in users_] # i guess doesn't work?
        for i, user in enumerate(users[:]):
            for user_ in users_:
                for key, value in user_.items():
                    if str(key) == "username" and str(user.username) == str(value):
                        users.remove(user)

        def chunks(lst, n):
            """Yield successive n-sized chunks from lst."""
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

        # get users in groups of 5 to allow performance over interrupts
        userChunks = chunks(users, 5)
        num = 1
        for userChunk in userChunks:
            print("Chunk: {}/{}".format(num, len(users)/5))
            num += 1
            # add users to 'grandfathered' list prior to discounting
            Settings.maybe_print("grandfathering: {}".format(len(userChunk)))
            try:
                successful = Driver.add_users_to_list(users=userChunk, number=number, name="grandfathered")
                # if successful then discount
                if not successful: return
                d = Discount() # discount will fill defaults with promotion values
                d.grandfatherer(users=userChunk)
            except Exception as e:
                Settings.dev_print(e)
        return True

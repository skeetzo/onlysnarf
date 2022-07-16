#!/usr/bin/python3
# OnlySnarf interface class

import sys
##
from OnlySnarf.lib.driver import Driver
from OnlySnarf.util.settings import Settings
from OnlySnarf.classes.discount import Discount
from OnlySnarf.classes.message import Message
from OnlySnarf.classes.profile import Profile
from OnlySnarf.classes.promotion import Promotion
from OnlySnarf.classes.user import User

#################
##### Snarf #####
#################

class Snarf:

    """
    OnlySnarf main class and runtime parser.

    All methods are static and handle the basic runtime operations, 
     importing variables from settings & args.

    """

    def __init__(self):
        """Snarf object"""

        pass

    @staticmethod
    def discount():

        """
        Applies the provided discount or creates one from args / prompts.

        Parameters
        ----------
        discount : classes.Discount
            A discount consisting of amount, months, and / or username. Prompts for missing.

        """

        discount = Discount()
        try: return discount.apply()
        except Exception as e: Settings.dev_print(e)
        return False

    @staticmethod
    def message():

        """
        Sends the provided message or creates one from args / prompts.

        Parameters
        ----------
        message : classes.Message
            A message consisting of text, recipient(s), and possibly also files, keywords, tags, 
                performers, and/or price 
        
        """

        message = Message()
        try: return message.send_message()
        except Exception as e: Settings.dev_print(e)
        return False
                
    @staticmethod
    def post():

        """
        Posts the provided text or from args / prompts.

        Parameters
        ----------
        message : classes.Post
            A post consisting of text and possibly also files, keywords, tags, performers,
                expiration, poll, and/or schedule
        
        """

        message = Message()
        try: return message.send_post()
        except Exception as e: Settings.dev_print(e)
        return False

    @staticmethod
    def profile():

        """
        Runs the profile method specified at runtime.

        backup - downloads all content and saves settings

        syncFrom - reads all profile settings and saves locally

        syncTo - updates profile settings with provided profile

        Extended description of function.

        Parameters
        ----------
        profile : profile.Profile
            Class representation of Onlyfans profile settings

        """

        profile = Profile()
        try: 
            # get profile method
            method = Settings.get_profile_method()
            if method == "backup": return Profile.backup_content()
            elif method == "syncfrom": return Profile.sync_from_profile()
            elif method == "syncto": return Profile.sync_to_profile()
            else: Settings.err_print("Missing Profile Method")
        except Exception as e: Settings.dev_print(e)
        return False
        
    @staticmethod
    def promotion():

        """
        Runs the promotion method specified at runtime.

        campain - creates discount campaign

        trial - creates free trial

        user - applies directly to user

        grandfather - applies discounted price to existing users and adds them all to list

        """

        try: 
            # get promotion method
            method = Settings.get_promotion_method()
            if method == "campaign": return Promotion.create_campaign()
            elif method == "trial": return Promotion.create_trial_link()
            elif method == "user": return Promotion.apply_to_user()
            elif method == "grandfather": return Promotion.grandfathered()
            else: Settings.err_print("Missing Promotion Method")
        except Exception as e: Settings.dev_print(e)
        return False

################################################################################################################################################

def exit_handler():
    """Exit cleanly"""

    Driver.exit_all()
    Settings.print("Shnarrf!")
    sys.exit(0)

import atexit
atexit.register(exit_handler)

def main():
    try:
        # purge local tmp files
        from .file import File
        File.remove_local()
        # disable menu prompts
        Settings.set_prompt(False)
        Settings.set_confirm(False)
        # get the thing, do the thing
        action = Settings.get_action()
        Settings.print("Running - {}".format(action))
        action = getattr(Snarf, action)
        successful = action()
        if successful: Settings.print("Shnarrf shnarfff shnarf!!")
        else: Settings.print("Shnarrf shnaaaaaaaarrrff!!")
    except Exception as e:
        Settings.dev_print(e)
        Settings.print("Shnarf??")
    finally:
        exit_handler()

################################################################################################################################################

if __name__ == "__main__":
    main()
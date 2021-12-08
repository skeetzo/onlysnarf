#!/usr/bin/python3
# OnlySnarf interface class
import sys
##
import Settings

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
        from lib.actions.discount import Discount
        discount = Discount()
        try: discount.apply()
        except Exception as e: Settings.dev_print(e)

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
        from lib.actions.message import Message
        from lib.user import User
        message = Message()
        try:
            message.get_message()
            if Settings.is_prompt():
                if not Settings.prompt("Send"): return
            if message.get_files() != "unset" and len(message.get_files()) == 0 and not message.get_text():
                Settings.err_print("Missing Files and Text")
                return
            successful = False
            try: 
                # for user in self.get_recipients():
                for user in message.users:
                    # if isinstance(user, str) and str(user) == "post": successful_ = Driver.post(self)
                    # print("Messaging: {}".format(user.username))
                    if isinstance(user, User):
                        successful = User.message_user(username=user.username, message=message)
                    else:
                        successful = User.message_user(username=user, message=message)
            except Exception as e:
                Settings.dev_print(e)
                successful = False
            if successful: message.cleanup_files()
        except Exception as e:
            Settings.dev_print(e)
                
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
        from lib.actions.message import Message
        message = Message()
        try:
            message.get_post()
            if Settings.is_prompt():
                if not Settings.prompt("Post"): return
            if message.get_files() != "unset" and len(message.get_files()) == 0 and not message.get_text():
                Settings.err_print("Missing Files and Text")
                return
            successful = False
            try:
                from .driver import Driver
                successful = Driver.get_driver().post(message=message)
            except Exception as e:
                Settings.dev_print(e)
                successful = False
            if successful: message.cleanup_files()
            return successful
        except Exception as e:
            Settings.dev_print(e)
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
        from lib.actions.profile import Profile
        profile = Profile()
        try: 
            # get profile method
            method = Settings.get_profile_method()
            successful = False
            if method == "backup":
                successful = profile.backup_content()
            elif method == "syncfrom":
                successful = Profile.sync_from_profile()
            elif method == "syncto":
                successful = Profile.sync_to_profile()
            else: Settings.err_print("Missing Profile Method")
            return successful
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
        from .classes import Promotion
        try: 
            # get promotion method
            method = Settings.get_promotion_method()
            successful = False
            if method == "campaign":
                successful = Promotion.create_campaign()
            elif method == "trial":
                successful = Promotion.create_trial_link()
            elif method == "user":
                successful = Promotion.apply_to_user()
            elif method == "grandfather":
                successful = Promotion.grandfathered()
            else: Settings.err_print("Missing Promotion Method")
            return successful
        except Exception as e: Settings.dev_print(e)
        return False

    # developer testing
    @staticmethod
    def test():
        from .user import User
        Settings.print('1/3 : Testing')
        Settings.print('TESTING: Settings - Get')
        profile = Profile.sync_from_profile()
        Settings.print('TESTING: Settings - Set')
        Profile.sync_to_profile(profile=profile)
        return True

################################################################################################################################################

def exit_handler():
    """Exit cleanly"""

    from .driver import Driver
    Driver.exit_all()
    Settings.print("Shnarrf!")
    sys.exit(0)

import atexit
atexit.register(exit_handler)

def main():
    try:
        # purge local files
        from .file import File
        File.remove_local()
        # disable menu prompts
        Settings.set_prompt(False)
        Settings.set_confirm(False)
        # get the thing, do the thing
        action = Settings.get_action()
        Settings.print("Running - {}".format(action))
        action = getattr(Snarf, action)
        success = action()
    except Exception as e:
        Settings.dev_print(e)
        Settings.print("Shnarf??")
    finally:
        exit_handler()

################################################################################################################################################

if __name__ == "__main__":
    main()
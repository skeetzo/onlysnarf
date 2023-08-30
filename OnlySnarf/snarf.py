#!/usr/bin/python3

# import logging
# logger = logging.getLogger('snarf_logger')

from .classes.discount import Discount
from .classes.message import Message, Post
from .classes.profile import Profile
# from .classes.promotion import Promotion
from .classes.user import User
from .lib.config import Config
# from .lib.menu import Menu
from .lib import api as API
from .util.args import get_args
from .util.config import get_config
from .util.settings import Settings

def api(config={}):
    API.main(config)

def config(config={}):
    Config.main(config)

# def menu(config={}):
#     Menu.main(config)

def discount(config={'user':None,'users':[]}):

    """
    Applies a discount to users as provided from args / prompts.


    """

    Settings.print("Beginning discount process...")
    return Discount.create_discount(config).apply()

def message(config={'user':None,'users':[]}):

    """
    Sends the configured message from args / prompts.

    
    """

    Settings.print("Beginning message process...")
    return Message.create_message(config).send()
            
def post(config={'text':"",'input':[]}):

    """
    Posts the configured text from args / prompts.

    
    """

    Settings.print("Beginning post process...")
    return Post.create_post(config).send()

# TODO: update this
# def profile():

    """
    Runs the profile method specified at runtime.

    backup - downloads all content and saves settings

    syncFrom - reads all profile settings and saves locally

    syncTo - updates profile settings with provided profile

    Extended description of function.

    """

    # profile = Profile()
    # try: 
    #     # get profile method
    #     method = Settings.get_profile_method()
    #     if method == "backup": return Profile.backup_content()
    #     elif method == "syncfrom": return Profile.sync_from_profile()
    #     elif method == "syncto": return Profile.sync_to_profile()
    #     else: Settings.err_print("Missing Profile Method")
    # except Exception as e: Settings.dev_print(e)
    # return False
    
# TODO: update this
# def promotion():

    """
    Runs the promotion method specified at runtime.

    campain - creates discount campaign

    trial - creates free trial

    user - applies directly to user

    grandfather - applies discounted price to existing users and adds them all to list

    """

    # try: 
    #     # get promotion method
    #     method = Settings.get_promotion_method()
    #     if method == "campaign": return Promotion.create_campaign()
    #     elif method == "trial": return Promotion.create_trial_link()
    #     elif method == "user": return Promotion.aato_user()
    #     elif method == "grandfather": return Promotion.grandfathered()
    #     else: Settings.err_print("Missing Promotion Method")
    # except Exception as e: Settings.dev_print(e)
    # return False

def users(config={'prefer_local':False}):

    """
    Scan users.

    
    """

    try:
        User.get_all_users(prefer_local=config["prefer_local"])
        return True
    except Exception as e: Settings.dev_print(e)
    return False

################################################################################################
################################################################################################
################################################################################################

def main():
    try:
        config = get_config(get_args())
        print(config)
        Settings.print("Running - {}".format(config["action"]))
        eval(f"{config['action']}(config)")
    except Exception as e:
        Settings.err_print(e)
        Settings.print("shnarf??")
    finally:
        Settings.print("shnarrf!")

if __name__ == "__main__":
    main()
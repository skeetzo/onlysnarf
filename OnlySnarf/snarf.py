#!/usr/bin/python3

from .util.args import get_args
from .util.config import set_config
CONFIG = set_config(get_args())

from .util.logger import configure_logging, logging
configure_logging(CONFIG["debug"], True if int(CONFIG["verbose"]) > 0 else False)
# log = logging.getLogger('onlysnarf')

from .classes.discount import Discount
from .classes.message import Message, Post
from .classes.profile import Profile
# from .classes.promotion import Promotion
from .classes.user import User
from .lib.config import Config
# from .lib.menu import Menu
from .lib import api as API


def api():
    API.main(CONFIG)

def config():
    Config.main(CONFIG)

# def menu(config={}):
#     Menu.main(CONFIG)

def discount():

    """
    Applies a discount to users as provided from args / prompts.


    """

    logging.info("Beginning discount process...")
    users = list(filter(None, CONFIG.get("users", [])))
    if CONFIG.get("user"):
        users.append(CONFIG.get("user"))
    successful = []
    for user in users:
        successful.append(Discount.create_discount({'username':user,'amount':CONFIG["amount"],'months':CONFIG["months"]}).apply())
    return all(successful)

def message():

    """
    Sends the configured message from args / prompts.

    
    """

    logging.info("Beginning message process...")
    return Message.create_message(CONFIG).send()
            
def post():

    """
    Posts the configured text from args / prompts.

    
    """

    logging.info("Beginning post process...")
    return Post.create_post(CONFIG).send()

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

def users():

    """
    Scan users.

    
    """

    try:
        User.get_all_users()
        return True
    except Exception as e: logging.debug(e)
    return False

################################################################################################################################################

def main():
    try:
        
        logging.info(f"Running - {CONFIG['action']}")
        eval(f"{CONFIG['action']}()")
    except Exception as e:
        logging.error(e)
        logging.info("shnarf??")
    finally:
        logging.info("shnarrf!")

if __name__ == "__main__":
    main()
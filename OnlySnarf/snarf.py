#!/usr/bin/python3

# Args
from .util.args import get_args
from .util.config import set_config
CONFIG = set_config(get_args())

# Logging
import logging
from .util.logger import configure_logging
configure_logging(CONFIG["debug"], True if int(CONFIG["verbose"]) > 0 else False)
logger = logging.getLogger(__name__)

# Basic Behaviors
from .classes.discount import Discount
from .classes.message import Message, Post
# from .classes.profile import Profile
# from .classes.promotion import Promotion
from .classes.user import User
from .lib.config import main as CONFIG_main
from .lib.menu import main as MENU_main
from .lib.api import main as API_main

def api():
    API_main(debug=CONFIG["debug"])

def config():
    CONFIG_main()

def menu(config={}):
    MENU_main()

def discount():

    """
    Applies a discount to users as provided from args / prompts.


    """

    logging.snarf("Beginning discount process...")
    recipients = CONFIG.get("recipients", [])
    recipients.append(CONFIG.get("user", ""))
    recipients = list(set(filter(None, recipients)))
    successful = []
    for username in recipients:
        successful.append(Discount.create_discount({'username':username,'amount':CONFIG["amount"],'months':CONFIG["months"]}).apply())
    return all(successful)

def message():

    """
    Sends the configured message from args / prompts.

    
    """

    logging.snarf("Beginning message process...")
    recipients = CONFIG.get("recipients", [])
    recipients.append(CONFIG.get("user", ""))
    recipients = list(filter(None, recipients))
    message_object = {
        "text"      : CONFIG["text"],
        "files"     : CONFIG["input"],
        "keywords"  : CONFIG["keywords"],
        "performers": CONFIG["performers"],
        "price"     : CONFIG["price"],
        "schedule"  : {
            "date" : str(CONFIG["date"]).split(" ")[0],
            "time" : str(CONFIG["time"]).split(" ")[1]
        },
        "recipients": recipients,
        "includes"  : CONFIG["includes"],
        "excludes"  : CONFIG["excludes"]
    }
    if not message_object["text"]: raise Exception("missing text!")
    if not message_object["recipients"] and not message_object["includes"]:        
        raise Exception("missing recipients!")

    # print(message_object)

    # return


    return Message.create_message(message_object).send()
            
def post():

    """
    Posts the configured text from args / prompts.

    
    """

    logging.snarf("Beginning post process...")
    post_object = {
        "text"      : CONFIG["text"],
        "files"     : CONFIG["input"],
        "keywords"  : CONFIG["keywords"],
        "performers": CONFIG["performers"],
        "price"     : CONFIG["price"],
        "schedule"  : {
            "date" : str(CONFIG["date"]).split(" ")[0],
            "time" : str(CONFIG["time"]).split(" ")[1]
        }
    }
    if not post_object["text"]: raise Exception("missing text!")
    return Post.create_post(post_object).send()

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

    return User.get_all_users()

################################################################################################################################################

def main():
    try:
        logging.info(f"Running - {CONFIG['action']}")
        eval(f"{CONFIG['action']}()")
    except Exception as e:
        logging.critical(e)
        logging.snarf("shnarf??")
    finally:
        logging.snarf("shnarrf!")

if __name__ == "__main__":
    main()
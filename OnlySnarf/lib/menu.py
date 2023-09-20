import os
import sys
import inquirer
import pkg_resources
import logging
logger = logging.getLogger(__name__)

# from ..classes.profile import Profile
# from ..snarf import main as MAIN, discount, message, post, profile, promotion, users
from ..util.colorize import colorize
from ..util.user_config import get_username_onlyfans, get_password, get_username_google, get_password_google, get_username_twitter, get_password_twitter
from ..util.config import CONFIG

####################
##### CLI Menu #####
####################

ASCII = "\n     ________         .__          _________                     _____ \n \
\\_____  \\   ____ |  | ___.__./   _____/ ____ _____ ________/ ____\\\n \
 /   |   \\ /    \\|  |<   |  |\\_____  \\ /    \\\\__  \\\\_   _ \\   __\\ \n \
/    |    \\   |  \\  |_\\___  |/        \\   |  \\/ __ \\ |  |\\/| |   \n \
\\_______  /___|  /____/ ____/_______  /___|  (____  \\\\__|  |_|   \n \
        \\/     \\/     \\/            \\/     \\/     \\/              \n"


def ask_action():
    """
    Ask action to take

    Returns
    -------
    str
        The action selected

    """

    options = ["back","discount","message","post","users"]
    questions = [
        inquirer.List('action',
            message= "Please select an action:",
            choices= [str(option).title() for option in options],
        )
    ]
    answers = inquirer.prompt(questions)
    return answers['action'].lower()

def action_menu():
    """
    Prompt the action menu. Cycles back to main menu


    """

    action = ask_action()
    if (action == 'back'): return main_menu()
    elif (action == 'discount'): PROMPT_discount()
    elif (action == 'message'): PROMPT_message()
    elif (action == 'post'): PROMPT_post()
    # elif (action == 'profile'): profile()
    # elif (action == 'promotion'): promotion()
    elif (action == 'users'): users()
    else: logger.info("Missing Action: {}".format(colorize(action, "red")))
    main()
    
def header():
    """
    Show the header text


    """

    if not CONFIG["debug"]: os.system('clear')
    print(colorize(ASCII, 'header'))
    print(colorize('version {}\n'.format(pkg_resources.get_distribution("onlysnarf").version), 'green'))
    user_header()
    settings_header()

def settings_header():
    """
    Show the settings header text


    """

    # Settings.header()
    # TODO: update how settings can be reflected in menu (again)
    pass

def user_header():
    """
    Show the user header text


    """

    logger.info("User:")
    logger.info(" - Username = {}".format(CONFIG["username"]))
    if get_username_onlyfans() != "":
        logger.info(" - Email = {}".format(get_username_onlyfans()))
    pass_ = ""
    if str(get_password()) != "":
        pass_ = "******"
    logger.info(" - Password = {}".format(pass_))
    if str(get_username_twitter()) != "":
        logger.info(" - Twitter = {}".format(get_username_twitter()))
        pass_ = ""
        if str(get_password_twitter()) != "":
            pass_ = "******"
        logger.info(" - Password = {}".format(pass_))
    logger.info('\r')

def menu():
    """
    Prompt the basic menu selection

    Returns
    -------
    str
        The menu option selected

    """

    questions = [
        inquirer.List('menu',
            message= "Please select an option:",
            choices= ['Action', 'Settings', 'Exit']
        )
    ]
    answers = inquirer.prompt(questions)

    # menu_prompt = {
    #     'type': 'list',
    #     'name': 'menu',
    #     'message': 'Please select an option:',
    #     'choices': ['Action', 'Profile', 'Settings', 'Exit']
    # }
    # answers = prompt(menu_prompt)

    return answers['menu']

def main_menu():
    """
    Show the main menu


    """

    action = menu()
    if (action == 'Action'): action_menu()
    # elif (action == 'Settings'): Settings.menu()
    else: sys.exit(0)
    main()

def main():
    """
    Primary script entry


    """

    try:
        header()
        settings_header()
        main_menu()
    except Exception as e:
        logger.error(e)


import os
import inquirer

from ..classes.profile import Profile
from ..snarf import main as MAIN, discount, message, post, profile, promotion, users
from ..util.colorize import colorize
from ..util.settings import Settings

####################
##### CLI Menu #####
####################

class Menu:

    ASCII = "\n     ________         .__          _________                     _____ \n \
    \\_____  \\   ____ |  | ___.__./   _____/ ____ _____ ________/ ____\\\n \
     /   |   \\ /    \\|  |<   |  |\\_____  \\ /    \\\\__  \\\\_   _ \\   __\\ \n \
    /    |    \\   |  \\  |_\\___  |/        \\   |  \\/ __ \\ |  |\\/| |   \n \
    \\_______  /___|  /____/ ____/_______  /___|  (____  \\\\__|  |_|   \n \
            \\/     \\/     \\/            \\/     \\/     \\/              \n"

    def __init__(self):
        pass

    def ask_action():
        """
        Ask action to take

        Returns
        -------
        str
            The action selected

        """

        options = ["back"]
        options.extend(Settings.get_actions())
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

        action = Menu.ask_action()
        if (action == 'back'): return MAIN()
        elif (action == 'discount'): discount()
        elif (action == 'message'): message()
        elif (action == 'post'): post()
        elif (action == 'profile'): profile()
        elif (action == 'promotion'): promotion()
        elif (action == 'users'): users()
        else: Settings.print("Missing Action: {}".format(colorize(action, "red")))
        Menu.main()
        
    def header():
        """
        Show the header text


        """

        if not Settings.is_debug(): os.system('clear')
        print(colorize(Menu.ASCII, 'header'))
        print(colorize('version {}\n'.format(Settings.get_version()), 'green'))
        Menu.user_header()
        Menu.settings_header()

    def settings_header():
        """
        Show the settings header text


        """

        Settings.header()

    def user_header():
        """
        Show the user header text


        """

        Settings.print("User:")
        if Settings.get_username_onlyfans() != "":
            Settings.print(" - Email = {}".format(Settings.get_username_onlyfans()))
        Settings.print(" - Username = {}".format(Settings.get_username()))
        pass_ = ""
        if str(Settings.get_password()) != "":
            pass_ = "******"
        Settings.print(" - Password = {}".format(pass_))
        if str(Settings.get_username_twitter()) != "":
            Settings.print(" - Twitter = {}".format(Settings.get_username_twitter()))
            pass_ = ""
            if str(Settings.get_password_twitter()) != "":
                pass_ = "******"
            Settings.print(" - Password = {}".format(pass_))
        Settings.print('\r')

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

        action = Menu.menu()
        if (action == 'Action'): Menu.action_menu()
        elif (action == 'Settings'): Settings.menu()
        else: exit_handler()
        Menu.main()

    def main():
        """
        Primary script entry


        """

        try:
            Menu.header()
            Menu.settings_header()
            Menu.main_menu()
        except Exception as e:
            Settings.dev_print(e)

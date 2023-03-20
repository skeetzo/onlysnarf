#!/usr/bin/python3
# Snarf.py cli menu

import time
import random
import os
import sys
# from PyInquirer import prompt
##
from OnlySnarf.snarf import Snarf
from OnlySnarf.lib.driver import Driver
from OnlySnarf.classes.profile import Profile
from OnlySnarf.util.colorize import colorize
from OnlySnarf.util.settings import Settings

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
        menu_prompt = {
            'type': 'list',
            'name': 'action',
            'message': 'Please select an action:',
            'choices': [str(option).title() for option in options],
            'filter': lambda val: str(val).lower()
        }
        menu_prompt["choices"].sort()
        answers = prompt(menu_prompt)
        return answers['action']

    def action_menu():
        """
        Prompt the action menu. Cycles back to main menu


        """

        action = Menu.ask_action()
        if (action == 'back'): return Menu.main()
        elif (action == 'discount'): Snarf.discount()
        elif (action == 'message'): Snarf.message()
        elif (action == 'post'): Snarf.post()
        elif (action == 'profile'): Snarf.profile()
        elif (action == 'promotion'): Snarf.promotion()
        else: print("Missing Action: {}".format(colorize(action,"red")))
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

        print("User:")
        if Settings.get_email() != "":
            print(" - Email = {}".format(Settings.get_email()))
        print(" - Username = {}".format(Settings.get_username()))
        pass_ = ""
        if str(Settings.get_password()) != "":
            pass_ = "******"
        print(" - Password = {}".format(pass_))
        if str(Settings.get_username_twitter()) != "":
            print(" - Twitter = {}".format(Settings.get_username_twitter()))
            pass_ = ""
            if str(Settings.get_password_twitter()) != "":
                pass_ = "******"
            print(" - Password = {}".format(pass_))
        print('\r')

    def menu():
        """
        Prompt the basic menu selection

        Returns
        -------
        str
            The menu option selected

        """

        menu_prompt = {
            'type': 'list',
            'name': 'menu',
            'message': 'Please select an option:',
            'choices': ['Action', 'Profile', 'Settings', 'Exit']
        }
        answers = prompt(menu_prompt)
        return answers['menu']

    def main_menu():
        """
        Show the main menu


        """

        action = Menu.menu()
        if (action == 'Action'): Menu.action_menu()
        elif (action == 'Profile'): Profile.menu()
        elif (action == 'Settings'): Settings.menu()
        else: exit()
        # Menu.main_menu()
        Menu.main()

    def main():
        """
        Primary script entry


        """

        time.sleep(1)
        try:
            Menu.header()
            Menu.settings_header()
            Menu.main_menu()
        except Exception as e:
            Settings.dev_print(e)

#################################################################################################

import atexit
def exit_handler():
    print("Shnarrf?")
    exit()
atexit.register(exit_handler)

import signal
def signal_handler(sig, frame):
    print('Shnnnarf?')
    exit()
signal.signal(signal.SIGINT, signal_handler)
  
def exit():
    Driver.exit()
    sys.exit(0)

######################################################

def main():
    Menu.main()

if __name__ == "__main__":
    try:
        Menu.main()
    except Exception as e:
        Settings.dev_print(e)
        print("Shhhhhnnnnnarf!")
    finally:
        exit()
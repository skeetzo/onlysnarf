#!/usr/bin/python3
# 3/28/2019 Skeetzo
# OnlySnarf.py menu system

### doesn't work:
# upload & backup (requires upload via local added to main script)
# settings menu -> "Incorrect Index"
import time
import random
import os
import shutil
import datetime
import json
import sys
import pathlib
from PyInquirer import prompt
##
from OnlySnarf.src.colorize import colorize
# from OnlySnarf.src.cron import Cron
from OnlySnarf.src.classes import Discount, Promotion
from OnlySnarf.src.message import Message
from OnlySnarf.src import google as Google
# from OnlySnarf.src.promotion import Promotion
from OnlySnarf.src.settings import Settings

#####################
##### Functions #####
#####################

class Menu:

    def __init__(self):
        pass

    # Action

    def ask_action():
        menu_prompt = {
            'type': 'list',
            'name': 'action',
            'message': 'Please select an action:',
            'choices': ['Back', 'Discount', 'Message', 'Post', 
                # 'Promotion'
            ]
        }
        if str(Settings.is_debug()) == "True":
            menu_prompt["choices"].append("Promotion")
        answers = prompt(menu_prompt)
        return answers['action']

    def action_menu():
        action = Menu.ask_action()
        if (action == 'Back'): Menu.main()
        elif (action == 'Discount'): Menu.discount_menu()
        elif (action == 'Message'): Menu.message_menu()
        elif (action == 'Post'): Menu.post_menu()
        elif (action == 'Promotion'): Menu.promotion_menu()
        else: Menu.main()

    # Discount

    def discount_menu():
        if not Settings.is_debug():
            print("### Not Available ###")
            return
        discount = Discount()
        discount.apply()
        Menu.main()

    # Message

    def message_menu():
        message = Message()
        message.send()
        Menu.main()

    # Post

    def post_menu():
        message = Message()
        message.post()
        Menu.main()

    # Profile

    def profile_menu():
        print("### Not Available ###")
        # Profile.menu(snarf)
        Menu.main()

    # Promotion

    def promotion_menu():
        if not Settings.is_debug():
            print("### Not Available ###")
            return
        promotion = Promotion()
        # add menu in promotion that asks for which kind
        # promotion.create_trial_link()
        promotion.apply_to_user()
        Menu.main()

    # Settings

    def settings_menu():
        Settings.menu()
        Menu.main()
        
    # Main

    def header():
        if not Settings.is_debug(): os.system('clear')
        print(colorize(Settings.ASCII, 'header'))
        print(colorize('version {}\n'.format(Settings.get_version()), 'green'))
        Menu.user_header()
        Menu.settings_header()

    def settings_header():
        Settings.header()

    def user_header():
        print("User:")
        print(" - Username = {}".format(Settings.get_username()))
        pass_ = ""
        if str(Settings.get_password()) != "":
            pass_ = "******"
        print(" - Password = {}".format(pass_))
        print('\r')

    def menu():
        menu_prompt = {
            'type': 'list',
            'name': 'menu',
            'message': 'Please select an option:',
            'choices': ['Action', 'Profile', 'Settings', 'Exit']
        }
        answers = prompt(menu_prompt)
        return answers['menu']

    def main_menu():
        action = Menu.menu()
        if (action == 'Action'): Menu.action_menu()
        elif (action == 'Profile'): Menu.profile_menu()
        elif (action == 'Settings'): Menu.settings_menu()
        else: Menu.exit()

    def main():
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
    sys.exit(0)

######################################################

def main():
    Menu.main()

if __name__ == "__main__":
    try:
        menu = Menu()
        menu.main()
    except Exception as e:
        print("Shhhhhnnnnnarf!")
    finally:
        exit()
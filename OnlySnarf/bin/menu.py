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
import pkg_resources
from PyInquirer import prompt
##
from OnlySnarf.src.colorize import colorize
# from OnlySnarf.src.cron import Cron
from OnlySnarf.src.message import Message
from OnlySnarf.src import google as Google
# from OnlySnarf.src.promotion import Promotion
from OnlySnarf.src.settings import Settings
from OnlySnarf.src.snarf import Snarf

###################
##### Globals #####
###################

ASCII = "\n ________         .__          _________                     _____ \n \
\\_____  \\   ____ |  | ___.__./   _____/ ____ _____ ________/ ____\\\n \
 /   |   \\ /    \\|  |<   |  |\\_____  \\ /    \\\\__  \\\\_   _ \\   __\\ \n \
/    |    \\   |  \\  |_\\___  |/        \\   |  \\/ __ \\ |  |\\/| |   \n \
\\_______  /___|  /____/ ____/_______  /___|  (____  \\\\__|  |_|   \n \
        \\/     \\/     \\/            \\/     \\/     \\/              \n"
snarf = Snarf()
version = str(pkg_resources.get_distribution("onlysnarf").version)

#####################
##### Functions #####
#####################

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
    action = ask_action()
    if (action == 'Back'): main()
    elif (action == 'Discount'): discount_menu()
    elif (action == 'Message'): message_menu()
    elif (action == 'Post'): post_menu()
    elif (action == 'Promotion'): promotion_menu()
    else: main()

# Discount

def discount_menu():
    if not Settings.get_user(): user = User.select_user()
    if not Settings.prompt("discount"): return None
    # 5-55% / 5
    question = {
        'type': 'input',
        'name': 'amount',
        'message': 'Amount (increments of 5) in %?',
        'validate': NumberValidator,
        'filter': lambda val: int(myround(val))
    },
    # 1-12 months
    {
        'type': 'input',
        'name': 'duration',
        'message': 'Months?',
        'validate': NumberValidator,
        'filter': lambda val: int(val)

    }
    answers = prompt(question)
    Snarf.discount(choice=user, discount={"amount":answers["amount"], "duration":answers["duration"]})
    main()

# Message

def message_menu():
    message = Message()
    message.get_message()
    message.send()
    main()

# Post

def post_menu():
    message = Message()
    message.get_post()
    message.post()
    main()

# Profile

def profile_menu():
    print("### Not Available ###")
    # Profile.menu(snarf)
    main()

# Promotion

def promotion_menu():
    print("### Not Available ###")
    # promotion = Promotion()
    # promotion.prompt()
    # promotion.apply()
    main()

# Settings

def settings_menu():
    Settings.menu()
    main()
    
# Main

def header():
    # os.system('clear')
    print(colorize(ASCII, 'header'))
    print(colorize('version '+version+'\n', 'green'))
    user_header()
    settings_header()

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
    action = menu()
    if (action == 'Action'): action_menu()
    elif (action == 'Profile'): profile_menu()
    elif (action == 'Settings'): settings_menu()
    else: exit()

def main():
    time.sleep(1)
    header()
    settings_header()
    main_menu()

#################################################################################################
#################################################################################################
#################################################################################################
from PyInquirer import Validator, ValidationError

class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end

# round to 5
def myround(x, base=5):
    return base * round(x/base)

#################################################################################################

import atexit
def exit_handler():
    print('Shnnarrrff!')
    exit()
atexit.register(exit_handler)

import signal
def signal_handler(sig, frame):
    print('Shnnnarf?')
    exit()
signal.signal(signal.SIGINT, signal_handler)
  
def exit():
    print("Shnarrf?")
    sys.exit(0)

######################################################

if __name__ == "__main__":
    try:
        main()
    except:
        print("Shhhhhnnnnnarf!")
    finally:
        exit()
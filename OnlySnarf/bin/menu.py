#!/usr/bin/python3
# 3/28/2019 Skeetzo
# OnlySnarf.py menu system

### doesn't work:
# upload & backup (requires upload via local added to main script)
# settings menu -> "Incorrect Index"

import random
import os
import shutil
import datetime
import json
import sys
import pathlib
import pkg_resources
from OnlySnarf.settings import SETTINGS as settings
# from OnlySnarf import OnlySnarf
from OnlySnarf.colorize import colorize
from OnlySnarf import cron as Cron
from OnlySnarf import google as Google
from OnlySnarf import message as Message
from OnlySnarf import promotion as Promotion
from OnlySnarf.snarf import Snarf
from PyInquirer import prompt

###################
##### Globals #####
###################

header = "\n ________         .__          _________                     _____ \n \
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
    if str(settings.DEBUG) == "True":
        menu_prompt["choices"].append("Promotion")
    answers = prompt(menu_prompt)
    return answers['action']

def action_menu():
    action = ask_action()
    if (action == 'Back'):main()
    elif (action == 'Discount'): discount_menu()
    elif (action == 'Message'): message_menu()
    elif (action == 'Post'): post_menu()
    elif (action == 'Promotion'): promotion_menu()
    else: main()

# Discount

def discount_menu():
    if not settings.get_user(): user = User.select_user()
    if not settings.prompt("discount"): return None
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
    message.prompt_message()
    Snarf.message(message=message)
    main()

# Post

def post_menu():
    message = Message()
    message.prompt_post()
    Snarf.message(message=message)
    main()

# Promotion

def promotion_menu():
    promotion = Promotion()
    promotion.prompt()
    Snarf.promotion(promotion=promotion)
    main()

# Settings

def settings_menu():
    settings.menu()
    
# Main

def header():
    # os.system('clear')
    print(colorize(header, 'header'))
    print(colorize('version '+version+'\n', 'green'))
    user_header()
    settings_header()

def settings_header():
    settings.header()

def user_header():
    print("User:")
    print(" - Username = {}".format(settings.USERNAME))
    if settings.PASSWORD and str(settings.PASSWORD) != "":
        pass_ = "******"
    else:
        pass_ = ""
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
    direction = menu()
    if (direction == 'Action'): action_menu()
    elif (direction == 'Profile'): profile_menu()
    elif (direction == 'Settings'): settings_menu()
    else: exit()

def main():
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
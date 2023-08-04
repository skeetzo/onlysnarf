#!/usr/bin/python
# setup & update script for config


# TODO: check

    # this script is supposed to have menu options for 
    # ) creating the .conf file
    # ) updating the .conf file
    # ) instructions for creating the google creds
    # ) a function for checking the google creds
    # when ran in it should check for the .conf file and google_creds



import os
import sys
import json
import shutil
import fileinput
from pathlib import Path
##
from .util.settings import Settings
from .util.colorize import colorize

EMPTY_USER_CONFIG = Path.join(__file__, "conf/users/example-user.conf")

class Config:

    def __init__(self):
        pass


    @staticmethod
    def prompt_google():
        data = {}
        data['username'] = input('Google Username: ')
        data['password'] = input('Google Password: ')
        return data

    @staticmethod
    def prompt_onlyfans():
        data = {}
        data['email'] = input('OnlyFans Email: ')
        data['username'] = input('OnlyFans Username: ')
        data['password'] = input('OnlyFans Password: ')
        # data['phone'] = input('OnlyFans Phone: ')
        return data

    @staticmethod
    def prompt_twitter():
        data = {}
        data['username'] = input('Twitter Username: ')
        data['password'] = input('Twitter Password: ')
        return data

    @staticmethod
    def reset_user_config(user="default"):
        Settings.print("resetting user config files for {}...".format(user))
        if os.path.exists(Settings.get_user_config(user)):
            os.remove(Settings.get_user_config(user))
            Settings.ensure_paths()
            shutil.copyfile(EMPTY_USER_CONFIG, Settings.get_user_config(user))
            Settings.print("successfully reset config!")
        else:
            Settings.err_print("no config exists to reset!")

    # receives input for twitter login and saves to config.conf
    @staticmethod
    def update_user_config():
        Config.update_onlyfans_user()
        Config.update_google_user()
        Config.update_twitter_user()

    @staticmethod
    def update_onlyfans_user():
        data = prompt_onlyfans()
        for line in fileinput.input(Settings.get_config_path(), inplace = 1): 
            # line.replace("$EMAIL", data['email'])
            line.replace("$USERNAME", data['username'])
            line.replace("$PASSWORD", data['password'])
            Settings.print(line)
        Settings.print("OnlyFans user config updated!")

    @staticmethod
    def update_google_user():
        data = prompt_google()
        for line in fileinput.input(Settings.get_config_path(), inplace = 1): 
            line.replace("$USERNAME_GOOGLE", data['username'])
            line.replace("$PASSWORD_GOOGLE", data['password'])
            Settings.print(line)
        Settings.print("Google user config updated!")

    @staticmethod
    def update_twitter_user():
        data = prompt_twitter()
        for line in fileinput.input(Settings.get_config_path(), inplace = 1): 
            line.replace("$USERNAME_TWITTER", data['username'])
            line.replace("$PASSWORD_TWITTER", data['password'])
            Settings.print(line)
        Settings.print("Twitter user config updated!")
        
    def main():
        Settings.print("-- OnlySnarf Config --")
        Settings.print("------------------------------")
        if os.path.isfile(Settings.get_config_path()):
            Settings.print(colorize("[*] Config File", 'conf')+": "+colorize("True", 'green'))
            if str(Settings.get_email()) != "None":
                Settings.print(colorize("[-] OnlyFans Email", 'conf')+": "+colorize(Settings.get_email(), 'green'))
            else:
                Settings.print(colorize("[-] OnlyFans Email", 'conf')+": "+colorize("", 'red'))
            if str(Settings.get_password()) != "None":
                Settings.print(colorize("[-] OnlyFans Password", 'conf')+": "+colorize("******", 'green'))
            else:
                Settings.print(colorize("[-] OnlyFans Password", 'conf')+": "+colorize("", 'red'))
            if str(Settings.get_username()) != "None":
                Settings.print(colorize("[-] OnlyFans Username", 'conf')+": "+colorize(Settings.get_username(), 'green'))
            else:
                Settings.print(colorize("[-] OnlyFans Username", 'conf')+": "+colorize("", 'red'))
            if str(Settings.get_username_google()) != "None":
                Settings.print(colorize("[-] Google Username", 'conf')+": "+colorize(Settings.get_username_google(), 'green'))
            else:
                Settings.print(colorize("[-] Google Username", 'conf')+": "+colorize("", 'red'))
            if str(Settings.get_password_google()) != "None":
                Settings.print(colorize("[-] Google Password", 'conf')+": "+colorize("******", 'green'))
            else:
                Settings.print(colorize("[-] Google Password", 'conf')+": "+colorize("", 'red'))
            if str(Settings.get_username_twitter()) != "None":
                Settings.print(colorize("[-] Twitter Username", 'conf')+": "+colorize(Settings.get_username_google(), 'green'))
            else:
                Settings.print(colorize("[-] Twitter Username", 'conf')+": "+colorize("", 'red'))
            if str(Settings.get_password_twitter()) != "None":
                Settings.print(colorize("[-] Twitter Password", 'conf')+": "+colorize("******", 'green'))
            else:
                Settings.print(colorize("[-] Twitter Password", 'conf')+": "+colorize("", 'red'))
        else:
            Settings.print(colorize("[*] Config File", 'conf')+": "+colorize("False", 'red'))
        if os.path.isfile(Settings.get_google_path()):
            Settings.print(colorize("[*] Google Creds", 'conf')+": "+colorize("True", 'green'))
        else:
            Settings.print(colorize("[*] Google Creds", 'conf')+": "+colorize("False", 'red'))
        Settings.print("------------------------------")
        Settings.print(colorize("Menu:", 'menu'))
        Settings.print(colorize("[ 0 ]", 'menu') + " Config - Create")
        Settings.print(colorize("[ 1 ]", 'menu') + " Config - Update - Google")
        Settings.print(colorize("[ 2 ]", 'menu') + " Config - Update - OnlyFans")
        Settings.print(colorize("[ 3 ]", 'menu') + " Config - Update - Twitter")
        Settings.print(colorize("[ 4 ]", 'menu') + " Config - Remove")
        Settings.print(colorize("[ 5 ]", 'menu') + " Google Creds - Check")
        Settings.print(colorize("[ 6 ]", 'menu') + " Google Creds - Instructions")
        Settings.print(colorize("[ 7 ]", 'menu') + " Google Creds - Remove")
        Settings.print(colorize("[ 8 ]", 'menu') + " Exit")
        # Settings.print(colorize("[ 8 ]", 'menu') + " Refresh All")
        while True:
            choice = input(">> ")
            try:
                if int(choice) < 0 or int(choice) >= 6: raise ValueError
                if int(choice) == 1:
                    update_google_user()
                elif int(choice) == 2:
                    update_onlyfans_user()
                elif int(choice) == 3:
                    update_twitter_user()
                elif int(choice) == 4:
                    # TODO: add user
                    reset_user_config()
                elif int(choice) == 5:
                    exit_handler()
            except (ValueError, IndexError, KeyboardInterrupt):
                Settings.err_print("incorrect index")
        Settings.print()
        Config.main()


#################################################################################################

def exit_handler():
    """Exit cleanly"""

    try:
        sys.exit("shnarf!")
    except Exception as e:
        print(e)

import atexit
atexit.register(exit_handler)

######################################################

def main():
    try:
        Config.main()
    except Exception as e:
        Settings.dev_print(e)
        Settings.print("shnarf??")
    finally:
        Settings.print("shnarrf!")
        exit_handler()

if __name__ == "__main__":
    main()
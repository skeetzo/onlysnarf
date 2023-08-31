import os
import sys
import json
import time
import shutil
import logging
import inquirer
import fileinput
from pathlib import Path

from ..util import defaults as DEFAULT
from ..util.colorize import colorize
from ..util.user_config import get_user_config_path, get_username_onlyfans, get_password, get_username_google, get_password_google, get_username_twitter, get_password_twitter

EMPTY_USER_CONFIG = Path(__file__).parent.joinpath("../conf/users/example-user.conf").resolve()

class Config:

    def __init__(self):
        pass

    def add_user():
        username = input("OnlyFans username: ")
        # check if user already exists
        if str(username)+".conf" in Config.get_users():
            logging.warning("user already exists!")
            return Config.main()
        Config.reset_user_config(username)
        Config.update_onlyfans_user(user=username)
        Config.update_google_user(user=username)
        Config.update_twitter_user(user=username)
        Config.main()


    def check_config(user):
        try:
            if not os.path.isfile(get_user_config_path(user)):
                Config.reset_user_config(user)
        except Exception as e:
            Config.reset_user_config(user)

    def display_user():
        Config.list_users()
        username = Config.list_user_menu()
        if (username == 'back'): return Config.main()
        Config.list_user_config(username)
        Config.main()

    def list_users():
        # list all user configs in conf/users
        for (dirpath, dirnames, filenames) in os.walk(os.path.join(DEFAULT.ROOT_PATH, "conf/users")):
            for filename in filenames:
                logging.info("> "+filename)
            break

    def list_user_config(user):
        logging.info("-- OnlySnarf Config --")
        logging.info(colorize("Green", "green")+": configured")
        logging.info(colorize("Blue", "blue")+": system defaults")
        logging.info(colorize("Red", "red")+": missing")
        logging.info("------------------------------")
        logging.info(colorize("Config File", 'conf')+": "+colorize(user, 'green'))
        if str(get_username_onlyfans(user)) != "None":
            color = "green"
            if str(get_username_onlyfans(user)) == "$USERNAME":            
                color = "blue"
            logging.info(colorize("OnlyFans Username", 'conf')+": "+colorize(get_username_onlyfans(user), color))
        else:
            logging.info(colorize("OnlyFans Username", 'conf')+": "+colorize("N/A", 'red'))

        if str(get_password(user)) != "None":
            color = "green"
            if str(get_password(user)) == "$PASSWORD":            
                color = "blue"
            logging.info(colorize("OnlyFans Password", 'conf')+": "+colorize("******", color))
        else:
            logging.info(colorize("OnlyFans Password", 'conf')+": "+colorize("N/A", 'red'))

        if str(get_username_google(user)) != "None":
            color = "green"
            if str(get_username_google(user)) == "$UGOOGLE":            
                color = "blue"
            logging.info(colorize("Google Username", 'conf')+": "+colorize(get_username_google(user), color))
        else:
            logging.info(colorize("Google Username", 'conf')+": "+colorize("N/A", 'red'))

        if str(get_password_google(user)) != "None":
            color = "green"
            if str(get_password_google(user)) == "$PGOOGLE":            
                color = "blue"
            logging.info(colorize("Google Password", 'conf')+": "+colorize("******", color))
        else:
            logging.info(colorize("Google Password", 'conf')+": "+colorize("N/A", 'red'))

        if str(get_username_twitter(user)) != "None":
            color = "green"
            if str(get_username_twitter(user)) == "$UTWITTER":            
                color = "blue"
            logging.info(colorize("Twitter Username", 'conf')+": "+colorize(get_username_twitter(user), color))
        else:
            logging.info(colorize("Twitter Username", 'conf')+": "+colorize("N/A", 'red'))

        if str(get_password_twitter(user)) != "None":
            color = "green"
            if str(get_password_twitter(user)) == "$PTWITTER":            
                color = "blue"
            logging.info(colorize("Twitter Password", 'conf')+": "+colorize("******", color))
        else:
            logging.info(colorize("Twitter Password", 'conf')+": "+colorize("N/A", 'red'))
        logging.info("------------------------------")

    def list_user_menu():
        options = ["back"]
        options.extend(Config.get_users())
        questions = [
            inquirer.List('list',
                message= "Please select a username for more info:",
                choices= options,
            )
        ]
        answers = inquirer.prompt(questions)
        return answers['list']

    def get_users():
        users = []
        for (dirpath, dirnames, filenames) in os.walk(os.path.join(DEFAULT.ROOT_PATH, "conf/users")):
            users.extend(filenames)
            break
        return users

    def ask_username():
        options = ["back"]
        options.extend(Config.get_users())
        if "example-user.conf" in options:
            options.remove("example-user.conf") # should not update the example / template file
        questions = [
            inquirer.List('username',
                message= "Please select a username:",
                choices= options,
            )
        ]
        answers = inquirer.prompt(questions)
        return answers['username']

    def update_menu():
        username = Config.ask_username()
        if (username == 'back'): return Config.main()
        Config.update_user_config(username.replace(".conf",""))
        Config.main()

    def user_header(user="default"):
        logging.info("User:")
        if get_username_onlyfans(user) != "":
            logging.info(" - Email = {}".format(get_username_onlyfans(user)))
        logging.info(" - Username = {}".format(get_username(user)))
        pass_ = ""
        if str(get_password()) != "":
            pass_ = "******"
        logging.info(" - Password = {}".format(pass_))
        if str(get_username_twitter(user)) != "":
            logging.info(" - Twitter = {}".format(get_username_twitter(user)))
            pass_ = ""
            if str(get_password_twitter(user)) != "":
                pass_ = "******"
            logging.info(" - Password = {}".format(pass_))
        logging.info('\r')

    def remove_menu():
        username = Config.ask_username()
        if (username == 'back'): return Config.main()
        if input("ARE YOU SURE? N/y ") == "y":
            Config.remove_user(user=username)
        else:
            logging.info("canceling deletion!")
        Config.main()

    def remove_user(user="default"):
        try:
            os.remove(get_user_config_path(user))
        except Exception as e:
            pass
        logging.info("successfully removed {}!".format(user))

    def menu():
        questions = [
            inquirer.List('menu',
                message= "Please select an option:",
                choices= ['Add', 'Display', 'List', 'Update', 'Remove', 'Exit']
            )
        ]
        answers = inquirer.prompt(questions)
        return answers['menu']

    def main_menu():
        action = Config.menu()
        if (action == 'Add'): Config.add_user()
        elif (action == 'Display'): Config.display_user()
        elif (action == 'List'): Config.list_users()
        elif (action == 'Update'): Config.update_menu()
        elif (action == 'Remove'): Config.remove_menu()
        else: exit()
        Config.main()

    def main():
        time.sleep(1)
        try:
            Config.main_menu()
        except Exception as e:
            logging.debug(e)

    def prompt_google(user):
        data = {}
        data['username'] = get_username_google(user)
        data['password'] = get_password_google(user)
        logging.info("Username: "+data['username'])
        logging.info("Password: "+data['password'])
        if data['username'] == "" or input("Update Google email? N/y ").lower() == "y":
            data['username'] = input('Google Email: ')
        if data['password'] == "" or input("Update Google password? N/y ").lower() == "y":
            data['password'] = input('Google Password: ')
        return data

    def prompt_onlyfans(user):
        data = {}
        data['username'] = get_username_onlyfans(user)
        data['password'] = get_password(user)
        logging.info("Username: "+data['username'])
        logging.info("Password: "+data['password'])
        if data['username'] == "" or input("Update OnlyFans email? N/y ").lower() == "y":
            data['username'] = input('OnlyFans Email: ')
        if data['password'] == "" or input("Update OnlyFans password? N/y ").lower() == "y":
            data['password'] = input('OnlyFans Password: ')
        return data

    def prompt_twitter(user):
        data = {}
        data['username'] = get_username_twitter(user)
        data['password'] = get_password_twitter(user)
        logging.info("Username: "+data['username'])
        logging.info("Password: "+data['password'])
        if data['username'] == "" or input("Update Twitter username? N/y ").lower() == "y":
            data['username'] = input('Twitter Username: ')
        if data['password'] == "" or input("Update Twitter password? N/y ").lower() == "y":
            data['password'] = input('Twitter Password: ')
        return data
    
    def reset_user_config(user="default"):
        logging.info("resetting user config files for {}...".format(user))
        if os.path.exists(get_user_config_path(user)):
            os.remove(get_user_config_path(user))
        else:
            logging.warning("no config exists to reset!")
        shutil.copyfile(EMPTY_USER_CONFIG, get_user_config_path(user))
        logging.info("successfully reset config!")


    def update_user_config(user="default"):
        # save user settings in variables
        username = get_username_onlyfans(user)
        password = get_password(user)

        googleU = get_username_google(user)
        googleP = get_password_google(user)
        
        twitterU = get_username_twitter(user)
        twitterP = get_password_twitter(user)

        # reset user config
        Config.reset_user_config(user)

        onlyfans_data = Config.prompt_onlyfans(user)
        google_data = Config.prompt_google(user)
        twitter_data = Config.prompt_twitter(user)

        if onlyfans_data["username"] == "$USERNAME": onlyfans_data["username"] = username 
        if onlyfans_data["password"] == "$PASSWORD": onlyfans_data["password"] = password 
        if google_data["username"] == "$UGOOGLE": google_data["username"] = googleU 
        if google_data["password"] == "$PGOOGLE": google_data["password"] = googleP 
        if twitter_data["username"] == "$UTWITTER": twitter_data["username"] = twitterU 
        if twitter_data["password"] == "$PTWITTER": twitter_data["password"] = twitterP 

        Config.update_onlyfans_user(onlyfans_data, user)
        Config.update_google_user(google_data, user)
        Config.update_twitter_user(twitter_data, user)
        logging.info("successfully updated user config for {}!".format(user))

    def update_onlyfans_user(data=None, user="default"):
        Config.check_config(user)
        if not data: data = Config.prompt_onlyfans(user)
        with fileinput.FileInput(get_user_config_path(user), inplace = True) as f:
            for line in f: 
                if data['username']:
                    line = line.replace("$USERNAME", data['username'])
                if data['password']:
                    line = line.replace("$PASSWORD", data['password'])
                print(line, end ='')
        logging.info("OnlyFans user config updated!")

    def update_google_user(data=None, user="default"):
        Config.check_config(user)
        if not data: data = Config.prompt_google(user)
        with fileinput.FileInput(get_user_config_path(user), inplace = True) as f:
            for line in f: 
                if data['username']:
                    line = line.replace("$UGOOGLE", data['username'])
                if data['password']:
                    line = line.replace("$PGOOGLE", data['password'])
                print(line, end ='')
        logging.info("Google user config updated!")

    def update_twitter_user(data=None, user="default"):
        Config.check_config(user)
        if not data: data = Config.prompt_twitter(user)
        with fileinput.FileInput(get_user_config_path(user), inplace = True) as f:
            for line in f: 
                if data['username']:
                    line = line.replace("$UTWITTER", data['username'])
                if data['password']:
                    line = line.replace("$PTWITTER", data['password'])
                print(line, end ='')
        logging.info("Twitter user config updated!")

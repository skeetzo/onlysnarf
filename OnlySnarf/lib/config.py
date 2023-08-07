import os
import sys
import json
import time
import shutil
import inquirer
import fileinput
# from pathlib import Path
##
from ..util.settings import Settings
from ..util.colorize import colorize
from pathlib import Path

EMPTY_USER_CONFIG = Path(__file__).parent.joinpath("../conf/users/example-user.conf").resolve()

class Config:

    def __init__(self):
        pass

    def add_user():
        username = input("OnlyFans username: ")
        # check if user already exists
        if str(username)+".conf" in Config.get_users():
            Settings.warn_print("user already exists!")
            return Config.main()
        Config.reset_user_config(username)
        Config.update_onlyfans_user(user=username)
        Config.update_google_user(user=username)
        Config.update_twitter_user(user=username)
        Config.main()


    def check_config(user):
        try:
            if not os.path.isfile(Settings.get_user_config_path(user)):
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
        for (dirpath, dirnames, filenames) in os.walk(os.path.join(Settings.get_base_directory(), "conf/users")):
            for filename in filenames:
                Settings.print("> "+filename)
            break

    def list_user_config(user):
        Settings.print("-- OnlySnarf Config --")
        Settings.print(colorize("Green", "green")+": configured")
        Settings.print(colorize("Blue", "blue")+": system defaults")
        Settings.print(colorize("Red", "red")+": missing")
        Settings.print("------------------------------")
        Settings.print(colorize("Config File", 'conf')+": "+colorize(user, 'green'))
        if str(Settings.get_username_onlyfans(user)) != "None":
            color = "green"
            if str(Settings.get_username_onlyfans(user)) == "$USERNAME":            
                color = "blue"
            Settings.print(colorize("OnlyFans Username", 'conf')+": "+colorize(Settings.get_username_onlyfans(user), color))
        else:
            Settings.print(colorize("OnlyFans Username", 'conf')+": "+colorize("N/A", 'red'))

        if str(Settings.get_password(user)) != "None":
            color = "green"
            if str(Settings.get_password(user)) == "$PASSWORD":            
                color = "blue"
            Settings.print(colorize("OnlyFans Password", 'conf')+": "+colorize("******", color))
        else:
            Settings.print(colorize("OnlyFans Password", 'conf')+": "+colorize("N/A", 'red'))

        if str(Settings.get_username_google(user)) != "None":
            color = "green"
            if str(Settings.get_username_google(user)) == "$UGOOGLE":            
                color = "blue"
            Settings.print(colorize("Google Username", 'conf')+": "+colorize(Settings.get_username_google(user), color))
        else:
            Settings.print(colorize("Google Username", 'conf')+": "+colorize("N/A", 'red'))

        if str(Settings.get_password_google(user)) != "None":
            color = "green"
            if str(Settings.get_password_google(user)) == "$PGOOGLE":            
                color = "blue"
            Settings.print(colorize("Google Password", 'conf')+": "+colorize("******", color))
        else:
            Settings.print(colorize("Google Password", 'conf')+": "+colorize("N/A", 'red'))

        if str(Settings.get_username_twitter(user)) != "None":
            color = "green"
            if str(Settings.get_username_twitter(user)) == "$UTWITTER":            
                color = "blue"
            Settings.print(colorize("Twitter Username", 'conf')+": "+colorize(Settings.get_username_twitter(user), color))
        else:
            Settings.print(colorize("Twitter Username", 'conf')+": "+colorize("N/A", 'red'))

        if str(Settings.get_password_twitter(user)) != "None":
            color = "green"
            if str(Settings.get_password_twitter(user)) == "$PTWITTER":            
                color = "blue"
            Settings.print(colorize("Twitter Password", 'conf')+": "+colorize("******", color))
        else:
            Settings.print(colorize("Twitter Password", 'conf')+": "+colorize("N/A", 'red'))
        Settings.print("------------------------------")

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
        for (dirpath, dirnames, filenames) in os.walk(os.path.join(Settings.get_base_directory(), "conf/users")):
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
        Settings.print("User:")
        if Settings.get_username_onlyfans(user) != "":
            Settings.print(" - Email = {}".format(Settings.get_username_onlyfans(user)))
        Settings.print(" - Username = {}".format(Settings.get_username(user)))
        pass_ = ""
        if str(Settings.get_password()) != "":
            pass_ = "******"
        Settings.print(" - Password = {}".format(pass_))
        if str(Settings.get_username_twitter(user)) != "":
            Settings.print(" - Twitter = {}".format(Settings.get_username_twitter(user)))
            pass_ = ""
            if str(Settings.get_password_twitter(user)) != "":
                pass_ = "******"
            Settings.print(" - Password = {}".format(pass_))
        Settings.print('\r')

    def remove_menu():
        username = Config.ask_username()
        if (username == 'back'): return Config.main()
        if input("ARE YOU SURE? N/y ") == "y":
            Config.remove_user(user=username)
        else:
            Settings.print("canceling deletion!")
        Config.main()

    def remove_user(user="default"):
        try:
            os.remove(Settings.get_user_config_path(user))
        except Exception as e:
            pass
        Settings.print("successfully removed {}!".format(user))

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
            Settings.dev_print(e)

    def prompt_google(user):
        data = {}
        data['username'] = Settings.get_username_google(user)
        data['password'] = Settings.get_password_google(user)
        Settings.print("Username: "+data['username'])
        Settings.print("Password: "+data['password'])
        if data['username'] == "" or input("Update Google email? N/y ").lower() == "y":
            data['username'] = input('Google Email: ')
        if data['password'] == "" or input("Update Google password? N/y ").lower() == "y":
            data['password'] = input('Google Password: ')
        return data

    def prompt_onlyfans(user):
        data = {}
        data['username'] = Settings.get_username_onlyfans(user)
        data['password'] = Settings.get_password(user)
        Settings.print("Username: "+data['username'])
        Settings.print("Password: "+data['password'])
        if data['username'] == "" or input("Update OnlyFans email? N/y ").lower() == "y":
            data['username'] = input('OnlyFans Email: ')
        if data['password'] == "" or input("Update OnlyFans password? N/y ").lower() == "y":
            data['password'] = input('OnlyFans Password: ')
        return data

    def prompt_twitter(user):
        data = {}
        data['username'] = Settings.get_username_twitter(user)
        data['password'] = Settings.get_password_twitter(user)
        Settings.print("Username: "+data['username'])
        Settings.print("Password: "+data['password'])
        if data['username'] == "" or input("Update Twitter username? N/y ").lower() == "y":
            data['username'] = input('Twitter Username: ')
        if data['password'] == "" or input("Update Twitter password? N/y ").lower() == "y":
            data['password'] = input('Twitter Password: ')
        return data
    
    def reset_user_config(user="default"):
        Settings.print("resetting user config files for {}...".format(user))
        if os.path.exists(Settings.get_user_config_path(user)):
            os.remove(Settings.get_user_config_path(user))
        else:
            Settings.warn_print("no config exists to reset!")
        shutil.copyfile(EMPTY_USER_CONFIG, Settings.get_user_config_path(user))
        Settings.print("successfully reset config!")


    def update_user_config(user="default"):
        # save user settings in variables
        username = Settings.get_username_onlyfans(user)
        password = Settings.get_password(user)

        googleU = Settings.get_username_google(user)
        googleP = Settings.get_password_google(user)
        
        twitterU = Settings.get_username_twitter(user)
        twitterP = Settings.get_password_twitter(user)

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
        Settings.print("successfully updated user config for {}!".format(user))

    def update_onlyfans_user(data=None, user="default"):
        Config.check_config(user)
        if not data: data = Config.prompt_onlyfans(user)
        with fileinput.FileInput(Settings.get_user_config_path(user), inplace = True) as f:
            for line in f: 
                if data['username']:
                    line = line.replace("$USERNAME", data['username'])
                if data['password']:
                    line = line.replace("$PASSWORD", data['password'])
                print(line, end ='')
        Settings.print("OnlyFans user config updated!")

    def update_google_user(data=None, user="default"):
        Config.check_config(user)
        if not data: data = Config.prompt_google(user)
        with fileinput.FileInput(Settings.get_user_config_path(user), inplace = True) as f:
            for line in f: 
                if data['username']:
                    line = line.replace("$UGOOGLE", data['username'])
                if data['password']:
                    line = line.replace("$PGOOGLE", data['password'])
                print(line, end ='')
        Settings.print("Google user config updated!")

    def update_twitter_user(data=None, user="default"):
        Config.check_config(user)
        if not data: data = Config.prompt_twitter(user)
        with fileinput.FileInput(Settings.get_user_config_path(user), inplace = True) as f:
            for line in f: 
                if data['username']:
                    line = line.replace("$UTWITTER", data['username'])
                if data['password']:
                    line = line.replace("$PTWITTER", data['password'])
                print(line, end ='')
        Settings.print("Twitter user config updated!")

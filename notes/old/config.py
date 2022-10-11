#!/usr/bin/python
# setup & update script for config

import os
import sys
import json
import shutil
##
from OnlySnarf.lib import google as Google
from OnlySnarf.lib import driver as OnlySnarf
from OnlySnarf.util import Settings
from OnlySnarf.util import colorize

def checkBothCreds():
    checkGoogle()
    checkOnlyFans()

# checks Google creds access
def checkGoogle():
    Settings.print("Checking Google Creds (uploads)")
    if not os.path.exists(Settings.get_google_path()):
        Settings.print("Missing Google Creds")
        Settings.print()
        return main()
    authed = Google.checkAuth()
    if authed:
        Settings.print("Google Auth Successful")
    else: 
        Settings.print("Google Auth Failure")

# checks OnlyFans login process
def checkOnlyFans():
    Settings.print("Checking OnlyFans Creds")
    if not os.path.exists(Settings.get_config_path()):
        Settings.print("Missing Config Path")
        return main()
    OnlySnarf.auth()
    OnlySnarf.exit()

def checkTwitter():
    Settings.print("Checking Twitter Creds")
    if not os.path.exists(Settings.get_config_path()):
        Settings.print("Missing Config Path")
        return main()
    OnlySnarf.auth()
    OnlySnarf.exit()

# function that creates the missing config
def createConfig():
    Settings.print("Preparing OnlySnarf Config")
    # ensure /opt/onlysnarf exists
    if not os.path.exists("/opt/onlysnarf"):
        Settings.print("Creating Missing Config Dir")
        try:
            os.makedirs("/opt/onlysnarf")
            Settings.print("Created OnlySnarf Root")
        except Exception as e:
            Settings.print(e)
            main()
    if not os.path.exists("/opt/onlysnarf/config.conf"):
        Settings.print("Copying Default Config")
        try:
            shutil.copyfile(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../config.conf")), Settings.get_config_path())
            shutil.chown(Settings.get_config_path(), user=os.environ['USER'], group=os.environ['USER'])
            Settings.print("Created OnlySnarf Config")
        except Exception as e:
            Settings.print(e)
            main()
    else:
        Settings.print("OnlySnarf Config Exists")
        return True
    return False

# provides instructions for creating or refreshing google creds
def googleInstructions():
    Settings.print("[Google Instructions From README Go Here]")

# creates the config then prompts for missing credentials
def setupConfig():
    alreadyCreated = createConfig()
    if not alreadyCreated:
        updateConfig()

# receives input for Google login
def receiveGoogle():
    data = {}
    data['username'] = input('Google Username: ')
    data['password'] = input('Google Password: ')
    return data

def receiveOnlyFans():
    data = {}
    data['email'] = input('OnlyFans Email: ')
    data['username'] = input('OnlyFans Username: ')
    data['password'] = input('OnlyFans Password: ')
    return data

# receives input for Twitter login
def receiveTwitter():
    data = {}
    data['username'] = input('Twitter Username: ')
    data['password'] = input('Twitter Password: ')
    return data

# refreshes all creds
def refreshAll():
    removeConfig()
    setupConfig()
    removeGoogle()
    googleInstructions()

# removes config.conf
def removeConfig():
    Settings.print("Removing Config")
    # ensure /opt/onlysnarf exists
    if os.path.exists(Settings.get_config_path()):
        os.remove(Settings.get_config_path())
        Settings.print("Removed Config")
    else:
        Settings.err_print("failed to find config")

# removes google creds
def removeGoogle():
    Settings.print("Removing Google Creds")
    # ensure /opt/onlysnarf exists
    if os.path.exists(Settings.get_google_path()):
        os.remove(Settings.get_google_path())
        Settings.print("Removed Google Creds")
    else:
        Settings.err_print("failed to find google creds")

# receives input for twitter login and saves to config.conf
def updateConfig():
    updateOnlyFans()
    updateGoogle()
    updateTwitter()

def updateOnlyFans():
    data = receiveOnlyFans()
    # update conf variables username and password
    # save the conf file
    import fileinput
    # Does a list of files, and
    # redirects STDOUT to the file in question
    for line in fileinput.input(Settings.get_config_path(), inplace = 1): 
        line.replace("email None", "username {}".format(data['email']))
        line.replace("username None", "username {}".format(data['username']))
        line.replace("password None", "password {}".format(data['password']))
        Settings.print(line)
    Settings.print("OnlyFans Config Updated")

def updateGoogle():
    data = receiveGoogle()
    # update conf variables username and password
    # save the conf file
    import fileinput
    # Does a list of files, and
    # redirects STDOUT to the file in question
    for line in fileinput.input(Settings.get_config_path(), inplace = 1): 
        line.replace("username_google None", "username {}".format(data['username']))
        line.replace("password_google None", "password {}".format(data['password']))
        Settings.print(line)
    Settings.print("Google Config Updated")

def updateTwitter():
    data = receiveTwitter()
    # update conf variables username and password
    # save the conf file
    import fileinput
    # Does a list of files, and
    # redirects STDOUT to the file in question
    for line in fileinput.input(Settings.get_config_path(), inplace = 1): 
        line.replace("username_twitter None", "username {}".format(data['username']))
        line.replace("password_twitter None", "password {}".format(data['password']))
        Settings.print(line)
    Settings.print("Twitter Config Updated")
    
# this script is supposed to have menu options for 
# ) creating the .conf file
# ) updating the .conf file
# ) instructions for creating the google creds
# ) a function for checking the google creds
# when ran in it should check for the .conf file and google_creds
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
    # Settings.print(colorize("[ 8 ]", 'menu') + " Refresh All")
    while True:
        choice = input(">> ")
        try:
            if int(choice) < 0 or int(choice) >= 9: raise ValueError
            # elif int(choice) == 2:
            #     checkBothCreds()
            if int(choice) == 0:
                setupConfig()
            elif int(choice) == 1:
                updateGoogle()
            elif int(choice) == 2:
                updateOnlyFans()
            elif int(choice) == 3:
                updateTwitter()
            elif int(choice) == 4:
                removeConfig()
            elif int(choice) == 5:
                checkGoogle()
            elif int(choice) == 6:
                googleInstructions()
            elif int(choice) == 7:
                removeGoogle()
            # elif int(choice) == 8:
            #     refreshAll()
        except (ValueError, IndexError, KeyboardInterrupt):
            Settings.err_print("incorrect index")
    Settings.print()
    main()

###########################

if __name__ == "__main__":
    try:
        Settings.initialize()
        main()
    except Exception as e:
        Settings.maybe_print(e)
        Settings.print(e)
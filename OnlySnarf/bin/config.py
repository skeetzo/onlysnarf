#!/usr/bin/python
# 2/7/2019 - Skeetzo
# 4/22/2019 - Skeetzo
# setup & update script for config
import os
import sys
import json
import shutil
from OnlySnarf.src import google as Google
from OnlySnarf.src import driver as OnlySnarf
from OnlySnarf.src.settings import Settings
from OnlySnarf.src import colorize

def checkBothCreds():
    checkGoogle()
    checkOnlyFans()

# checks Google creds access
def checkGoogle():
    print("Checking Google Creds")
    if not os.path.exists(settings.GOOGLE_PATH):
        print("Missing Google Creds")
        return
    Google.checkAuth()

# checks OnlyFans login process
def checkOnlyFans():
    print("Checking OnlyFans Login (Twitter Creds)")
    if not os.path.exists(settings.CONFIG_PATH):
        print("Missing Config Path")
        return
    OnlySnarf.auth()
    OnlySnarf.exit()

# function that creates the missing config
def createConfig():
    print("Creating Config")
    # ensure /etc/onlysnarf exists
    if not os.path.exists("/etc/onlysnarf"):
        print("Creating Missing Config Dir")
        os.makedirs("/etc/onlysnarf")
    # copy config-example.conf to /etc/onlysnarf/config.conf
    print("Copying Default Config")
    shutil.copyfile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config-example.conf"), settings.CONFIG_PATH)
    print("user: "+str(os.environ['USER']))
    shutil.chown(settings.CONFIG_PATH, user=os.environ['USER'], group=os.environ['USER'])

# provides instructions for creating or refreshing google creds
def googleInstructions():
    print("[Google Instructions Go Here]")
    pass

# creates the config then prompts for missing credentials
def setupConfig():
    createConfig()
    updateTwitter()

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
    print("Removing Config")
    # ensure /etc/onlysnarf exists
    if os.path.exists(settings.CONFIG_PATH):
        os.remove(settings.CONFIG_PATH)
        print("Removed Config")
    else:
        print("Error: Failed to Remove Config")

# removes google creds
def removeGoogle():
    print("Removing Google Creds")
    # ensure /etc/onlysnarf exists
    if os.path.exists(settings.GOOGLE_PATH):
        os.remove(settings.GOOGLE_PATH)
        print("Removed Google Creds")
    else:
        print("Error: Failed to Remove Google Creds")

# receives input for twitter login and saves to config.conf
def updateConfig():
    data = receiveTwitter()
    # update conf variables username and password
    # save the conf file
    import fileinput
    # Does a list of files, and
    # redirects STDOUT to the file in question
    for line in fileinput.input(settings.CONFIG_PATH, inplace = 1): 
        line.replace("username None", "username {}".format(data['username']))
        line.replace("password None", "password {}".format(data['password']))
        print(line)

# this script is supposed to have menu options for 
# ) creating the .conf file
# ) updating the .conf file
# ) instructions for creating the google creds
# ) a function for checking the google creds
# when ran in it should check for the .conf file and google_creds
def main():
    if os.path.isfile(settings.CONFIG_PATH):
        print(colorize("[*] Config File", 'conf')+":"+colorize("True", 'blue'))
        if str(settings.USERNAME) != "None":
            print(colorize("[-] Twitter Username", 'conf')+":"+colorize(settings.USERNAME, 'blue'))
        else:
            print(colorize("[-] Twitter Username", 'conf')+":"+colorize("", 'pink'))
        if str(settings.USERNAME) != "None":
            print(colorize("[-] Twitter Password", 'conf')+":"+colorize("******", 'blue'))
        else:
            print(colorize("[-] Twitter Password", 'conf')+":"+colorize("", 'pink'))
    else:
        print(colorize("[*] Config File", 'conf')+":"+colorize("False", 'pink'))
    if os.path.isfile(settings.GOOGLE_PATH):
        print(colorize("[*] Google Creds", 'conf')+":"+colorize("True", 'blue'))
    else:
        print(colorize("[*] Google Creds", 'conf')+":"+colorize("False", 'pink'))
    print("------------------------------")
    print(colorize("Menu:", 'menu'))
    print(colorize("[ 0 ] ", 'menu') + "Check Credentials - Google")
    print(colorize("[ 1 ] ", 'menu') + "Check Credentials - Twitter")
    print(colorize("[ 2 ] ", 'menu') + "Check Credentials - Both")
    print(colorize("[ 3 ] ", 'menu') + "Config - Create")
    print(colorize("[ 4 ] ", 'menu') + "Config - Update")
    print(colorize("[ 5 ] ", 'menu') + "Config - Remove")
    print(colorize("[ 6 ] ", 'menu') + "Google Creds - Instructions")
    print(colorize("[ 7 ] ", 'menu') + "Google Creds - Remove")
    print(colorize("[ 8 ] ", 'menu') + "Refresh All")
    while True:
        choice = input(">> ")
        try:
            if int(choice) < 0 or int(choice) >= 2: raise ValueError
            if int(choice) == 0:
                checkGoogle()
            elif int(choice) == 1:
                checkOnlyFans()
            elif int(choice) == 2:
                checkBothCreds()
            elif int(choice) == 3:
                setupConfig()
            elif int(choice) == 4:
                updateConfig()
            elif int(choice) == 5:
                removeConfig()
            elif int(choice) == 6:
                googleInstructions()
            elif int(choice) == 7:
                removeGoogle()
            elif int(choice) == 8:
                refreshAll()
        except (ValueError, IndexError, KeyboardInterrupt):
            print("Error: Incorrect Index")
        finally:
            sys.exit(1)

if __name__ == "__main__":
    try:
        settings.initialize()
        main()
    except Exception as e:
        settings.maybePrint(e)
        print(e)
        print("Shnarf?")
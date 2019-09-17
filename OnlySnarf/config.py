#!/usr/bin/python
# 2/7/2019 - Skeetzo
# 4/22/2019 - Skeetzo
# setup & update script for config
import os
import sys
import json
import shutil

def colorize(string, color):
    if not color in colors: return string
    return colors[color] + string + '\033[0m'
  
colors = {
    'menu': '\033[48;1;44m'
}

CONFIG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)),'config.json')
GOOGLE_CREDS = os.path.join(os.path.dirname(os.path.realpath(__file__)),'google_creds.txt')

def createConfig():
    print("Preparing Config")
    data = receiveInputs()
    global CONFIG_FILE
    with open(CONFIG_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)

def getConfig():
    try:
        global CONFIG_FILE
        with open(CONFIG_FILE) as config_file:    
            return json.load(config_file)
    except FileNotFoundError:
        createConfig()
        return getConfig()

def receiveInputs():
    data = {}
    data['username'] = input('Twitter Username: ')
    data['password'] = input('Twitter Password: ')
    return data

def updateConfig():
    print("Updating Config")
    print("(k to keep same)")
    global CONFIG_FILE
    config = getConfig()
    data = receiveInputs()
    for key, value in data.items():
        if value.lower() == "k":
            continue
        config[key] = value
    with open(CONFIG_FILE, 'w') as outfile:
        json.dump(config, outfile, indent=4, sort_keys=True)

def updateGoogle():
    try:
        print("Enter the path to your new 'google_creds.txt':")
        creds = input('>> ')
        if os.path.exists(str(creds)):
            global GOOGLE_CREDS
            print(GOOGLE_CREDS)
            shutil.move(creds, GOOGLE_CREDS)
            print("Google Creds Updated Successfully")
        else:
            print("Error: File not found!")
    except FileNotFoundError:
        print("Error: File not found!")

def main():
    print(colorize("Update Config:", 'menu'))
    print(colorize("[ 0 ] ", 'blue') + "Google")
    print(colorize("[ 1 ] ", 'blue') + "Twitter")
    while True:
        choice = input(">> ")
        try:
            if int(choice) < 0 or int(choice) >= 2: raise ValueError
            if int(choice) == 0:
                updateGoogle()
            elif int(choice) == 1:
                updateConfig()
        except (ValueError, IndexError, KeyboardInterrupt):
            print("Error: Incorrect Index")
        finally:
            sys.exit(0)

if __name__ == "__main__":
    main()
# parse config file while maintaining default values from args

import configparser
import os

## SAME as Settings.get_base_directory ##
USER = os.getenv('USER')
if str(os.getenv('SUDO_USER')) != "root" and str(os.getenv('SUDO_USER')) != "None":
    USER = os.getenv('SUDO_USER')
baseDir = "/home/{}/.onlysnarf".format(USER)
if os.environ.get('ENV') == "test":
  cwd = os.getcwd()
  # baseDir = os.path.dirname(__file__)
#########################################

config_file = configparser.ConfigParser()
config_file.read(os.path.join(baseDir, "config.conf"))

# continue to overwrite values from arguments with config values

# use this if its weird during unit tests
# if os.environ.get('ENV') != "test": 

# relabels args -> config for cleaner usage
from .args import args as config
# else: config = {"debug":False}

for section in config_file.sections():
  for key in config_file[section]:
    if section == "ARGS":
      config[key] = config_file[section][key]
    else:
      config[section.lower()+"_"+key.lower()] = config_file[section][key].strip("\"")

###############
## Debugging ##
# import sys
# print(config)
# sys.exit(0)
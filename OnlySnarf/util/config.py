# parse config file while maintaining default values from args

import configparser
import os

## SAME as Settings.get_base_directory ##
USER = os.getenv('USER')
if str(os.getenv('SUDO_USER')) != "root" and str(os.getenv('SUDO_USER')) != "None":
    USER = os.getenv('SUDO_USER')

configFile = "config.conf"
if os.environ.get('ENV') == "test":
  # cwd = os.getcwd()
  configFile = os.path.join(os.getcwd(), "OnlySnarf/conf", "test-config.conf")
else:
  configFile = os.path.join("/home/{}/.onlysnarf".format(USER), "config.conf")

config_file = configparser.ConfigParser()
config_file.read(configFile)

# continue to overwrite values from arguments with config values

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
# parse config file while maintaining default values from args

import configparser
import os

## SAME as Settings.get_base_directory ##
USER = os.getenv('USER')
if str(os.getenv('SUDO_USER')) != "root" and str(os.getenv('SUDO_USER')) != "None":
    USER = os.getenv('SUDO_USER')
configFile = "config.conf"
if os.environ.get('ENV') == "test":
  configFile = os.path.join(os.getcwd(), "OnlySnarf/conf", "test-config.conf")
elif os.path.isfile(os.path.join("/home/{}/.onlysnarf/conf".format(USER), "config.conf")):
  configFile = os.path.join("/home/{}/.onlysnarf/conf".format(USER), "config.conf")
else:
  configFile = os.path.join(os.getcwd(), "OnlySnarf/conf", "config.conf")

config_file = configparser.ConfigParser()
config_file.read(configFile)

configs = {}

# relabels config for cleaner usage
for section in config_file.sections():
  for key in config_file[section]:
    if section == "ARGS":
      configs[key] = config_file[section][key]
      # print(key, config[key])
    else:
      configs[section.lower()+"_"+key.lower()] = config_file[section][key].strip("\"")
      # print(key, config[section.lower()+"_"+key.lower()])

config = {}
# continue to overwrite values from config file with args
from .args import args
# print(args.items())
for key, value in args.items():
  config[key] = value
for key, value in configs.items():
  config[key] = value  

###############
## Debugging ##
# import sys
# print(config)
# sys.exit(0)
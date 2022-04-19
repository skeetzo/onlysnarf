baseDir = "/etc/onlysnarf"

# parse config file
import os
import configparser

# baseDir = os.path.dirname(__file__)
# if os.environ.get('ENV') == "test": baseDir = os.path.dirname(__file__)
configFile = os.path.join(baseDir, "config.cfg")
config_file = configparser.ConfigParser()
config_file.read(configFile)

# overwrite values from arguments with config values
# if os.environ.get('ENV') != "test": 
from .args import args as config
# else: config = {"debug":False}

for section in config_file.sections():
  for key in config_file[section]:
    if section == "ARGS":
      config[key] = config_file[section][key]
    else:
      config[section.lower()+"_"+key] = config_file[section][key].strip("\"")

##########
## Debugging #
# import sys
# print(config)
# sys.exit(0)
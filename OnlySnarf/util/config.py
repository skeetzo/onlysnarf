
import configparser
import getpass
import os

CONFIG_DEFAULT = os.path.join(os.getcwd(), "OnlySnarf/conf", "config.conf")
CONFIG_TEST = os.path.join(os.getcwd(), "OnlySnarf/conf", "test-config.conf")
CONFIG_USER = os.path.expanduser(os.path.join("~/.onlysnarf/conf", "config.conf"))

CONFIG = {}

def get_config_file():
  if os.environ.get('ENV') == "test":
    print(f"using test config: {CONFIG_TEST}")
    return CONFIG_TEST
  elif os.path.isfile(CONFIG_USER):
    print(f"using normal config: {CONFIG_USER}")
    return CONFIG_USER
  else:
    print(f"using local config: {CONFIG_DEFAULT}")
    return CONFIG_DEFAULT

def parse_config(config_path, parsed_config=None):
  if not parsed_config: parsed_config = {}
  config_file = configparser.ConfigParser()
  config_file.read(config_path)
  for section in config_file.sections():
    for key in config_file[section]:
      if section == "ARGS":
        parsed_config[key] = config_file[section][key]
      else:
        parsed_config[section.lower()+"_"+key.lower()] = config_file[section][key].strip("\"")
  return parsed_config  

def set_config(args):
  try:
    # load default values
    default_config = parse_config(CONFIG_DEFAULT)
    # load config from args or use user config, overwrite default values
    parsed_config = parse_config(args.get("path_config", get_config_file()), parsed_config=default_config)
    # overwrite with provided args
    for key, value in args.items():
      parsed_config[key] = value
    # turn strings of booleans into actual booleans, fix lists
    for key, value in parsed_config.items():
      if value == "True" or value == "False":
        parsed_config[key] = bool(value)
      elif value == '[]':
        parsed_config[key] = []
  except Exception as e:
    print(e)
  ###############
  global CONFIG
  CONFIG = parsed_config
  ###############
  ## Debugging ##
  # import sys
  # print(parsed_config)
  # sys.exit(0)
  return parsed_config

def get_args_config_file():
  return os.path.join(os.path.abspath(__file__), "../conf", "config-args.conf")



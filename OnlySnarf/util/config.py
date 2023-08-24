
import configparser
import getpass
import os

CONFIG = {}

def get_config_file(file_path):


  USER = getpass.getuser()
  # USER = os.getenv('USER')
  if str(os.getenv('SUDO_USER')) != "root" and str(os.getenv('SUDO_USER')) != "None":
      USER = os.getenv('SUDO_USER')

  configFile = "config.conf"

  print(os.path.expanduser(os.path.join(".onlysnarf/conf", "config.conf")))
  print(os.path.expanduser(os.path.join(".onlysnarf/conf", "config.conf")))
  print(os.path.expanduser(os.path.join(".onlysnarf/conf", "config.conf")))
  print(os.path.expanduser(os.path.join(".onlysnarf/conf", "config.conf")))

  if os.environ.get('ENV') == "test":
    configFile = os.path.join(os.getcwd(), "OnlySnarf/conf", "test-config.conf")
    print("using test config")
  elif os.path.isfile(os.path.expanduser(os.path.join("~/.onlysnarf/conf", "config.conf"))):
    configFile = os.path.expanduser(os.path.join("~/.onlysnarf/conf", "config.conf"))
    print("using normal config")
  else:
    configFile = os.path.join(os.getcwd(), "OnlySnarf/conf", "config.conf")
    print("using local config")

    return configFile

def get_config(args={}):
  parsed_config = {}
  try:
    # overwrite any fetched config path with args
    args_path = args["path_config"]
    config_path = get_config_file()
    if args_path != config_path:
      config_path = args_path
    config_file = configparser.ConfigParser()
    config_file.read(config_path)
    # relabels config for cleaner usage
    for section in config_file.sections():
      for key in config_file[section]:
        if section == "ARGS":
          parsed_config[key] = config_file[section][key]
          # print(key, parsed_config[key])
        else:
          parsed_config[section.lower()+"_"+key.lower()] = config_file[section][key].strip("\"")
          # print(key, parsed_config[section.lower()+"_"+key.lower()])
    # overwrite with provided args
    for key, value in args.items():
      parsed_config[key] = value
  except Exception as e:
    print(e)
  global CONFIG
  if not CONFIG:
    CONFIG = parsed_config
  return parsed_config

def get_args_config_file():
  return os.path.join(os.path.abspath(__file__), "../conf", "config-args.conf")



  ###############
  ## Debugging ##
  # import sys
  # print(config)
  # sys.exit(0)



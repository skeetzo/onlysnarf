
import configparser
import getpass
import os

def get_config(args={}):

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

  config_file = configparser.ConfigParser()
  config_file.read(configFile)

  config = {}
  # relabels config for cleaner usage
  for section in config_file.sections():
    for key in config_file[section]:
      if section == "ARGS":
        config[key] = config_file[section][key]
        # print(key, config[key])
      else:
        config[section.lower()+"_"+key.lower()] = config_file[section][key].strip("\"")
        # print(key, config[section.lower()+"_"+key.lower()])

  if args and str(os.environ.get('ENV')) != "test":
    for key, value in args.items():
      config[key] = value
  for key, value in config.items():
    config[key] = value

  ###############
  ## Debugging ##
  # import sys
  # print(config)
  # sys.exit(0)

  return config



import configparser
import getpass
import os

CONFIG_DEFAULT = os.path.join(os.getcwd(), "OnlySnarf/conf", "config.conf")
CONFIG_TEST = os.path.join(os.getcwd(), "OnlySnarf/conf", "test-config.conf")
CONFIG_USER = os.path.expanduser(os.path.join("~/.onlysnarf/conf", "config.conf"))

CONFIG = {}

# copy/paste default config file to target folder
def create_default_config(targetPath):
  logger.debug(f"creating default config: {targetPath}")
  if "config.conf" not in str(targetPath):
    targetPath = os.path.join(targetPath, "config.conf")
  shutil.copyfile(get_args_config_file(), targetPath)
  logger.debug("created default config at: "+targetPath)
  # TODO: update to return config file path at target path?
  # return 

def get_args_config_file():
  return os.path.join(os.path.abspath(__file__), "../conf", "config-args.conf")

def get_config_file():
  if os.environ.get('ENV') == "test":
    # logger.debug(f"using test config: {CONFIG_TEST}")
    return CONFIG_TEST
  elif os.path.isfile(CONFIG_USER):
    # logger.debug(f"using normal config: {CONFIG_USER}")
    return CONFIG_USER
  else:
    # logger.debug(f"using local config: {CONFIG_DEFAULT}")
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

# search for a config file in or near the provided dir or filename
def search_for_config(path):
  onlyconfigs = []
  if os.path.isdir(path):
    onlyconfigs = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f == "config.conf"]
  else:
    path = Path(path)
    path = path.parent.absolute()
    onlyconfigs = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f == "config.conf"]
  if len(onlyconfigs) > 0:
    return onlyconfigs[0]
  return None

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
      if "true" in str(value).lower():
        # print("FIXING TRUE")
        parsed_config[key] = True
      elif "false" in str(value).lower():
        # print("FIXING FALSE")
        parsed_config[key] = False
      elif value == '[]':
        # print("FIXING EMPTY LIST")
        parsed_config[key] = []
      elif value == 'None':
        # print("FIXING NONE")
        parsed_config[key] = None
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

# update new default config file to appropriately match containing folder (somehow)
def update_default_filepaths(filepaths, config):
  files = []
  for file in filepaths:
    # logger.debug(file)
    file = os.path.expanduser(file)
    # logger.debug(file)
    if not os.path.exists(file):
      file = os.path.join(os.path.dirname(config), os.path.basename(file))
      # logger.debug(file)
      files.append(file)
  return files
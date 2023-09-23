
import os
import shutil
import getpass
import logging
logger = logging.getLogger(__name__)
import configparser
from pathlib import Path

CONFIG_DEFAULT = os.path.join(os.getcwd(), "OnlySnarf/conf", "config.conf")
CONFIG_TEST = os.path.join(os.getcwd(), "OnlySnarf/conf", "test-config.conf")
CONFIG_USER = os.path.expanduser(os.path.join("~/.onlysnarf/conf", "config.conf"))

CONFIG = {}

# copy/paste default config file to target folder
def create_default_config(targetPath):
  targetPath = Path(targetPath).parent.absolute()
  logger.debug(f"creating default config: {targetPath}")
  if "config.conf" not in str(targetPath):
    targetPath = os.path.join(targetPath, "config.conf")
  shutil.copyfile(get_args_config_file(), targetPath)
  logger.debug("created default config at: "+targetPath)

def get_args_config_file():
  return Path(os.path.abspath(__file__)).joinpath("../../conf/args-config.conf").resolve()

# TODO: change to get_config_for_upload_path ?
# searched for a config file at the same path as provided
def get_config_file_for_path(search_path, create=False):
  logger.debug(f"getting config file for path{' (creating if missing)' if create else ''}: {search_path}")
  # check if config exists for dir / filename
  # if the upload has a config file, use it
  config_path = search_for_config(search_path)
  if not config_path and create:
    create_default_config(search_path)
    config_path = search_path
  elif not config_path:
    logger.warning("no config found at path!")
    return None
  # logger.debug(config_path)
  # load the config as args

  parsed_config = parse_config(config_path)
  logger.debug(f"found config: {parsed_config}")
  return parsed_config

def get_config_file_path():
  if os.environ.get('ENV') == "test":
    # logger.debug(f"using test config: {CONFIG_TEST}")
    return CONFIG_TEST
  elif os.path.isfile(CONFIG_USER):
    # logger.debug(f"using normal config: {CONFIG_USER}")
    return CONFIG_USER
  else:
    # logger.debug(f"using local config: {CONFIG_DEFAULT}")
    return CONFIG_DEFAULT

# including a parsed_config object has that object overwritten by the newly parsed config
def parse_config(config_path, parsed_config=None):
  if not parsed_config: parsed_config = {}
  # logger.debug(config_path)
  try:
    config_file = configparser.ConfigParser()
    config_file.read(config_path)
    for section in config_file.sections():
      for key in config_file[section]:
        if section == "ARGS":
          parsed_config[key] = config_file[section][key]
        else:
          parsed_config[section.lower()+"_"+key.lower()] = config_file[section][key].strip("\"")
    logger.debug(f"parsed config: {parsed_config}")
  except Exception as e:
    # don't know why this exception is caused by scripts/scan, doesn't seem to affect runtime
    logger.debug(e)
  return parsed_config  

# search for a config file in or near the provided dir or filename
def search_for_config(path):
  logger.debug(f"searching for config at path: {path}")
  onlyconfigs = []
  if os.path.isdir(path):
    # onlyconfigs = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f == "config.conf"]
    onlyconfigs = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and "config.conf" in f]
  else:
    path = Path(path)
    path = path.parent.absolute()
    # onlyconfigs = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and f == "config.conf"]
    onlyconfigs = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and "config.conf" in f]
    
  if len(onlyconfigs) > 1:
    logger.warning("found multiple config files!")
  if len(onlyconfigs) > 0:
    logger.debug(f"found config at path: {onlyconfigs[0]}")
    return onlyconfigs[0]
  return None

def set_config(args):
  try:
    # load default values
    default_config = parse_config(CONFIG_DEFAULT)
    # load config from args or use user config, overwrite default values
    parsed_config = parse_config(args.get("path_config", get_config_file_path()), parsed_config=default_config)
    # overwrite with provided args
    for key, value in args.items():
      parsed_config[key] = value
    # turn strings of booleans into actual booleans, fix lists
    for key, value in parsed_config.items():
      if "true" in str(value).lower():
        # logger.debug("FIXING TRUE")
        parsed_config[key] = True
      elif "false" in str(value).lower():
        # logger.debug("FIXING FALSE")
        parsed_config[key] = False
      elif value == '[]':
        # logger.debug("FIXING EMPTY LIST")
        parsed_config[key] = []
      elif value == 'None':
        # logger.debug("FIXING NONE")
        parsed_config[key] = None
  except Exception as e:
    logger.debug(e)
  ###############
  global CONFIG
  CONFIG = parsed_config
  ###############
  ## Debugging ##
  # import sys
  # logger.debug(parsed_config)
  # sys.exit(0)
  return parsed_config

# update new default config file to appropriately match containing folder (somehow)
def update_default_filepaths(filepaths, config_path):
  files = []
  for file in filepaths:
    # logger.debug(file)
    file = os.path.expanduser(file)
    # logger.debug(file)
    if not os.path.exists(file):
      file = os.path.join(os.path.dirname(config_path), os.path.basename(file))
      # logger.debug(file)
      files.append(file)
    else:
      files.append(file)
  return files
import argparse
import os
import pkg_resources
from typing import Dict, Any
from .optional_args import apply_args
from .optional_args import apply_shim_args
from .optional_args import apply_subcommand_args

##
# Argument Parser
##

def get_args():
  parser = argparse.ArgumentParser(prog='snarf', allow_abbrev=False, epilog="Shnarrf!", 
    description="No mention of old Shnarf, I notice. Go ahead, just take all the glory, and leave it to Snarf to clean up after you. I don't mind!", conflict_handler='resolve')

  if os.environ.get("ENV") != "test":
    apply_subcommand_args(parser)
  elif os.environ.get("ENV") == "test":
    apply_shim_args(parser)

  apply_args(parser)

  parser.version = str(pkg_resources.get_distribution("onlysnarf").version)
  parser.add_argument('-version','--version', action='version')

  args: Dict[str, Any] = {}
  try:
    parsedargs, unknownargs = parser.parse_known_args()
    # print("unknown args: {}".format(unknownargs))
    args.update(vars(parsedargs))
  except Exception as e:
      print(e)
      print("Error: Incorrect arg format")
      parser.exit(1)
  #############
  # Debugging #
  # print(args)
  # import sys
  # sys.exit(0)
  return args

import argparse
from typing import Dict, Any

args: Dict[str, Any] = {}

########################################################################################################

##
# Argument Parser
##

parser = argparse.ArgumentParser(prog='onlysnarf', allow_abbrev=False, epilog="Shnarrf!", 
  description=__doc__, conflict_handler='resolve')

############

import os
if os.environ.get("ENV") != "test":
  from .optional_args import apply_subcommand_args
  apply_subcommand_args(parser)
elif os.environ.get("ENV") == "test":
  from .optional_args import apply_shim_args
  apply_shim_args(parser)

from .optional_args import apply_args
apply_args(parser)

##
import pkg_resources
parser.version = str(pkg_resources.get_distribution("onlysnarf").version)
parser.add_argument('-version', action='version')

############################################################################################

try:
  # args.update(vars(parser.parse_args()))

  parsedargs, unknownargs = parser.parse_known_args()
  # print("unknown args: {}".format(unknownargs))
  args.update(vars(parsedargs))
except Exception as e:
  print(e)
  print("Error: Incorrect arg format")
  parser.exit(1)

#############
# Debugging #
# import sys
# print(args)
# sys.exit(0)
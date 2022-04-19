
import argparse, os, re
from typing import Dict, Any
from .validators import valid_path

args: Dict[str, Any] = {}

########################################################################################################

##
# Argument Parser
##

parser = argparse.ArgumentParser(prog='OnlySnarf', allow_abbrev=False, epilog="Shnarrf!", 
  description=__doc__, conflict_handler='resolve')

############

from .optional_args import apply_args
apply_args(parser)

##
# Positional
##

##
# input
parser.add_argument('input', default=[], nargs=argparse.REMAINDER, 
  type=valid_path, help='file input to post or message')

##
import pkg_resources
parser.version = str(pkg_resources.get_distribution("onlysnarf").version)
parser.add_argument('-version', action='version')

############################################################################################

try:
  args.update(vars(parser.parse_args()))
except Exception as e:
  print("Error: Incorrect arg format")
  import sys
  sys.exit(1)

if args["source"] and not args["destination"]:
  args["destination"] = args["source"]
if not args["source"]: args["source"] = "local"
if not args["destination"]: args["destination"] = "local"
if not args["category"]: args["source"] = None

#############
# Debugging #
# import sys
# print(args)
# sys.exit(0)
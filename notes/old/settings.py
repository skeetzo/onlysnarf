import pkg_resources
import time
import os, json, sys
from datetime import datetime
from pathlib import Path
##
from .colorize import colorize

from . import CONFIG

from . import defaults as DEFAULT
from .validators import valid_schedule, valid_time
from .logger import logging
log = logging.getLogger('onlysnarf')

class Settings:
    

    #####################
    ##### Functions #####
    #####################

    

    def header():
        Settings.print("### SETTINGS ###")
        Settings.print("...")
        Settings.print("...")
        Settings.print("...")

    def menu():
        Settings.print("### SETTINGS MENU ###")
        Settings.print("...")
        Settings.print("...")
        Settings.print("...")


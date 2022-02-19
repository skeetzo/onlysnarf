
from .config import config
import logging

loglevel = logging.INFO
if config["debug"]: loglevel = logging.DEBUG

import os
from pathlib import Path

baseDir = "/var/log"
if os.environ.get('ENV') == "test":
	baseDir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../log"))
logPath = os.path.join(baseDir, "onlysnarf.log")

Path(os.path.basename(os.path.dirname(logPath))).mkdir(parents=True, exist_ok=True)

# set up logging to file - see previous section for more details
logging.basicConfig(level=loglevel,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=logPath,
                    filemode='w')

# https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
class CustomFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    teal = ""

    grey = "\x1b[38;21m"
    yellow = "\x1b[33;21m"
    red = "\x1b[31;21m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
    	logging.SUCCESSFUL: green + format + reset,
    	logging.FAILURE: red + format + reset,
        logging.DEBUG: grey + format + reset,
        logging.VERBOSE: teal + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# create file handler which logs everything
# fh = logging.FileHandler('onlysnarf.log')
# fh.setLevel(logging.DEBUG)

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
# console.setLevel(logging.INFO)
# set a format which is simpler for console use
# formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(CustomFormatter())
# add the handler to the root logger
logging.getLogger('').addHandler(console)

if os.environ.get("ENV") == "test": logging.getLogger('').removeHandler(console)
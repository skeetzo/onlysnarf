import os
import logging
from pathlib import Path
from . import defaults as DEFAULT
from .config import config

loglevel = logging.INFO
if config["debug"]: loglevel = logging.DEBUG
if int(config["verbose"]) >= 2: loglevel = logging.DEBUG

logPath = DEFAULT.LOG_PATH
if os.environ.get('ENV') == "test":
    logPath = os.path.join(os.getcwd(), "log", "snarf.log")

Path(os.path.dirname(logPath)).mkdir(parents=True, exist_ok=True)

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
    # the filename & line isn't helpful when i'm redirecting through Settings.maybe_print & dev_print
    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
# tell the handler to use this format
console.setFormatter(CustomFormatter())
# add the handler to the root logger
logging.getLogger('').addHandler(console)
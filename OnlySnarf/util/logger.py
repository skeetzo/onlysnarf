import os
import logging
from pathlib import Path
from . import defaults as DEFAULT

# Adopted from https://stackoverflow.com/a/35804945/1691778
# Adds a new logging method to the logging module
def addLoggingLevel(levelName, levelNum, methodName=None):
    if not methodName:
        methodName = levelName.lower()

    if hasattr(logging, levelName):
        raise AttributeError("{} already defined in logging module".format(levelName))
    if hasattr(logging, methodName):
        raise AttributeError("{} already defined in logging module".format(methodName))
    if hasattr(logging.getLoggerClass(), methodName):
        raise AttributeError("{} already defined in logger class".format(methodName))

    def logForLevel(self, message, *args, **kwargs):
        if self.isEnabledFor(levelNum):
            self._log(levelNum, message, args, **kwargs)

    def logToRoot(message, *args, **kwargs):
        logging.log(levelNum, message, *args, **kwargs)

    logging.addLevelName(levelNum, levelName)
    setattr(logging, levelName, levelNum)
    setattr(logging.getLoggerClass(), methodName, logForLevel)
    setattr(logging, methodName, logToRoot)

addLoggingLevel("TRACE", logging.DEBUG - 5)
addLoggingLevel("SNARF", logging.DEBUG + 5)

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
    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    format = "%(asctime)s - %(levelname)s - %(message)s"

    FORMATS = {
        logging.TRACE: grey + format + reset,
        logging.DEBUG: grey + format + reset,
        logging.SNARF: bold_red + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        # formatter = logging.Formatter(log_fmt, "%Y-%m-%d %H:%M:%S")
        return formatter.format(record)

# https://betterstack.com/community/guides/logging/how-to-start-logging-with-python/
class LevelFilter(logging.Filter):

    def __init__(self, level):
        self.level = level

    def filter(self, record):
        if record.levelno == self.level:
            return True

once = False

def configure_logging(debug=False, verbose=False):
    global once
    if once: return
    once = True

    loglevel = logging.INFO
    if debug: loglevel = logging.DEBUG
    if verbose: loglevel = logging.SNARF
    if debug and verbose: loglevel = logging.TRACE

    logPath = DEFAULT.LOG_PATH_SNARF
    if str(os.environ.get('ENV')) == "test":
        logPath = os.path.join(os.getcwd(), "log", "snarf.log")
    Path(os.path.dirname(logPath)).mkdir(parents=True, exist_ok=True)

    logging.basicConfig(level=loglevel, filename=logPath, filemode='w')

    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    # tell the handler to use this format
    console.setFormatter(CustomFormatter())
    # add the handler to the root logger
    logging.getLogger('').addHandler(console)

    # for name in logging.root.manager.loggerDict:
    #     if name.startswith("OnlySnarf.lib.webdriver"):
    #         logging.getLogger(name).setLevel(logging.ERROR)

    # level_filter = LevelFilter(logging.WARNING)
    # logging.getLogger("OnlySnarf.classes").addFilter(level_filter)
    # logging.getLogger("OnlySnarf.lib.webdriver").addFilter(level_filter)
    # logging.getLogger("OnlySnarf.util").addFilter(level_filter)


# hide all irrrelevant logs when doing tests on the specific module
also_this = []
def configure_logs_for_module_tests(module_name="", flush=False):
    global also_this

    if flush:
        for name in also_this:
            logging.getLogger(name).setLevel(logging.root.level)
        also_this = []
        return

    if module_name not in also_this:
        also_this.append(module_name)
        
    for name in logging.root.manager.loggerDict:
        # if module_name in name:
        if name in also_this:
            logging.getLogger(name).setLevel(logging.TRACE)
        else:
            logging.getLogger(name).setLevel(logging.ERROR)

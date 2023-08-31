import sys

from .config import CONFIG
from .settings import Settings
from . import defaults as DEFAULT

def debug_delay_check():
	if CONFIG["debug"]:
		if CONFIG["debug_delay"]:
		    print("*snores deeply*")
		    time.sleep(10)
		    print("*snores less deeply*")
		    time.sleep(10)
		    print("*snores*")
		    time.sleep(7)
		    print("*coughs awake*")
		    time.sleep(1)
		    print(" what was shnarf doing again?")
		    time.sleep(1)
		    print(" oh yeah...")
		    time.sleep(1)
		else:
		    print("*snores*")
		    time.sleep(9)
		    print("*jolts awake*")
		    time.sleep(1)

def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()











## TODO

def set_debug(newValue):
    if str(newValue) == "tests":
        pass
        # CONFIG["confirm"] = False
    else:
        CONFIG["debug"] = newValue


def set_prefer_local(buul):
    CONFIG["prefer_local"] = buul



# TODO: double check complete removal
# def is_debug(process=None):
#     if process == "firefox": return CONFIG["debug_firefox"]
#     elif process == "chrome": return CONFIG["debug_chrome"]
#     elif process == "selenium": return CONFIG["debug_selenium"]
#     elif process == "cookies": return CONFIG["debug_cookies"]
#     # elif process == "tests": return 
#     return CONFIG["debug"]

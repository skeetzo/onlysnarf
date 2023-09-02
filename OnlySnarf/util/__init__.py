import sys
import time

from . import defaults as DEFAULT

def debug_delay_check():
	from .config import CONFIG

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

def get_logs_path(process):
    if process == "firefox":
        path_ = os.path.join(DEFAULT.ROOT_PATH, "log")
        Path(path_).mkdir(parents=True, exist_ok=True)
        return os.path.join(path_, "geckodriver.log")
    elif process == "google":
        path_ = os.path.join(DEFAULT.ROOT_PATH, "log")
        Path(path_).mkdir(parents=True, exist_ok=True)
        return os.path.join(path_, "chromedriver.log")
    return ""

# TODO: double check complete removal
# def is_debug(process=None):
#     if process == "firefox": return CONFIG["debug_firefox"]
#     elif process == "chrome": return CONFIG["debug_chrome"]
#     elif process == "selenium": return CONFIG["debug_selenium"]
#     elif process == "cookies": return CONFIG["debug_cookies"]
#     # elif process == "tests": return 
#     return CONFIG["debug"]

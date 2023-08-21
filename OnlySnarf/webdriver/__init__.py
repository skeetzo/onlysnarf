from .driver import Driver

def exit_handler():
    """Exit cleanly"""

    try:
        Driver.exit(Driver.BROWSER)
    except Exception as e:
        print(e)

import atexit
atexit.register(exit_handler)

colors = {
    'blue': '\033[94m',
    'magenta': '\033[35m',
	'header': '\033[48;1;34m',
	'teal': '\033[96m',
	'pink': '\033[95m',
	'green': '\033[92m',
	'yellow': '\033[93m',
	'menu': '\033[48;1;44m',
	'underline': '\033[4m',
	'fail': '\033[91m',
	'bold': '\033[1m',
	'red': '\033[31m'
}

class fg:
    BLACK   = '\033[30m'
    RED     = '\033[31m'
    GREEN   = '\033[32m'
    YELLOW  = '\033[33m'
    BLUE    = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN    = '\033[36m'
    WHITE   = '\033[37m'
    RESET   = '\033[39m'

class bg:
    BLACK   = '\033[40m'
    RED     = '\033[41m'
    GREEN   = '\033[42m'
    YELLOW  = '\033[43m'
    BLUE    = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN    = '\033[46m'
    WHITE   = '\033[47m'
    RESET   = '\033[49m'

class style:
    BRIGHT    = '\033[1m'
    DIM       = '\033[2m'
    NORMAL    = '\033[22m'
    RESET_ALL = '\033[0m'

###############
### Classes ###
###############

def colorize(string, color):
	if not color in colors: return str(string)
	return "{}{}{}".format(colors[color], string,'\033[0m')

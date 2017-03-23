class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def success(str):
	print bcolors.OKGREEN + "[>] " + str + bcolors.ENDC

def fail(str):
	print bcolors.FAIL + "[!] " + str + bcolors.ENDC

def warning(str):
	print bcolors.WARNING + "[?] " + str + bcolors.ENDC

def info(str):
	print bcolors.OKBLUE + "[~] " + str + bcolors.ENDC

def getInput(fileLocation: str) -> str:
	with open(fileLocation, 'r') as file:
		return file.read().strip()

def get_char() -> str:
	'''multi-platform getch that always returns a string'''
	import sys
	if sys.platform == "win32":
		import msvcrt
		return msvcrt.getch().decode("ASCII")
	else:
		import getch
		return getch.getch()
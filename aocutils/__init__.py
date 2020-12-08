def getInput(fileLocation: str) -> str:
	with open(fileLocation, 'r') as file:
		return file.read().strip()
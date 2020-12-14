import functools as ft
from aocutils import getInput

def getGroupAnswers(input: str) -> list[set]:
	groupsStrings = input.split("\n\n")
	out = []
	for groupString in groupsStrings:
		split1 = groupString.split("\n")
		allstrings = "".join(split1)
		chars = [c for c in allstrings]
		out.append(set(chars))
	return out

def main():
	print(ft.reduce(lambda x, y: x+y, [len(x) for x in getGroupAnswers(getInput("inputs\\6.txt"))]))

if __name__=="__main__":
	main()
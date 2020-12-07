import functools as ft
#from pprint import pprint#DEV

def getInput(fileLocation: str) -> str:
	with open(fileLocation, 'r') as file:
		#Thanks to /u/kaspayaz for helping me realize I needed to strip the input string!
		return file.read().strip()

def getGroupAnswers(input: str) -> list[dict[str,int]]:
	groupsStrings = input.split("\n\n")
	out = []
	for groupString in groupsStrings:
		answers = groupString.split("\n")
		groupAnswerCounts = {"groupSize": len(answers)}
		for answer in answers:
			for char in answer:
				if char in groupAnswerCounts:
					groupAnswerCounts[char] += 1
				else:
					groupAnswerCounts[char] = 1
		#print(groupString)#DEV
		#pprint(groupAnswerCounts)#DEV
		#print("\n")#DEV
		out.append(groupAnswerCounts)
	return out

def main():
	finalSum = 0
	for gac in getGroupAnswers(getInput("inputs\\6.txt")):
		groupAllAnsweredCount = 0
		for k,v in gac.items():
			if len(k) == 1 and v == gac["groupSize"]:
				groupAllAnsweredCount += 1
		finalSum += groupAllAnsweredCount
	print(finalSum)

if __name__=="__main__":
	main()
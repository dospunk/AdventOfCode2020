from aocutils import getInput
from dataclasses import dataclass

def getInvalidValues(ticket: list[int], ranges: dict[str, list[tuple[int, int]]]) -> list[int]:
	invalid = []
	for num in ticket:
		valid = False
		for rs in ranges.values():
			for minimum, maximum in rs:
				if num <= maximum and num >= minimum:
					valid = True
		if not valid:
			invalid.append(num)
	return invalid

@dataclass
class TicketData:
	fieldRanges: dict[str, list[tuple[int, int]]]
	myTicket: list[int]
	otherTickets: list[list[int]]

	def removeInvalidTickets(self):
		self.otherTickets = [t for t in self.otherTickets if len(getInvalidValues(t, self.fieldRanges)) == 0]

def parseInput(rawInput: str) -> TicketData:
	fieldRanges: dict[str, list[tuple[int, int]]] = {}
	rawFieldInfo, rawMyTicket, rawOtherTickets = rawInput.split("\n\n")
	for line in rawFieldInfo.splitlines():
		splitOnColon = line.split(":")
		fieldName = splitOnColon[0]
		rawRanges = splitOnColon[1]
		rawRangesSplit = rawRanges.split(" or ")
		fieldRanges[fieldName] = []
		for rawRange in rawRangesSplit:
			rawNums = rawRange.split("-")
			fieldRanges[fieldName].append((int(rawNums[0]), int(rawNums[1])))
	myTicket = [int(n) for n in rawMyTicket.split("\n")[1].split(",")]
	otherTickets: list[list[int]] = []
	for line in rawOtherTickets.splitlines()[1:]:
		otherTickets.append([int(n) for n in line.split(",")])
	return TicketData(fieldRanges, myTicket, otherTickets)

def part1(data: TicketData) -> int:
	invalidValues = []
	for ticket in data.otherTickets:
		invalidValues.extend(getInvalidValues(ticket, data.fieldRanges))
	return sum(invalidValues)

def numCouldBeInField(num: int, ranges: list[tuple[int, int]]) -> bool:
	for mini, maxi in ranges:
		if num >= mini and num <= maxi:
			return True
	return False

def narrowDown(possibleFields: list[list[str]], done: list[str] = []) -> list[str]:
	if all(len(l) == 1 for l in possibleFields):
		return [l[0] for l in possibleFields]
	theOne = ""
	for l in possibleFields:
		if len(l) == 1 and l[0] not in done:
			theOne = l[0]
	for l in possibleFields:
		if len(l) != 1 and theOne in l:
			l.remove(theOne)
	done.append(theOne)
	return narrowDown(possibleFields, done)


def part2(data: TicketData) -> int:
	data.removeInvalidTickets()
	possibleFields: list[list[str]] = []
	#initialize possibleFields with all fields in each index
	for i in range(len(data.myTicket)):
		possibleFields.append([])
		for field in data.fieldRanges.keys():
			possibleFields[i].append(field)
	for ticket in data.otherTickets:
		#for each number in each ticket, remove the fields it could not be a part of from the 
		#corresponding list in possibleFields
		for i in range(len(ticket)):
			num = ticket[i]
			removeTheseFields = []
			for field in possibleFields[i]:
				ranges = data.fieldRanges[field]
				if not numCouldBeInField(num, ranges):
					removeTheseFields.append(field)
			for field in removeTheseFields:
				possibleFields[i].remove(field)
	actualFields = narrowDown(possibleFields)
	out = 1
	for i in range(len(data.myTicket)):
		if actualFields[i].startswith("departure"):
			out *= data.myTicket[i]
	return out

def main():
	testInput = """
	class: 1-3 or 5-7
	row: 6-11 or 33-44
	seat: 13-40 or 45-50

	your ticket:
	7,1,14

	nearby tickets:
	7,3,47
	40,4,50
	55,2,20
	38,6,12""".strip().replace("\t", "")
	rawInput = getInput("inputs\\16.txt")
	print("Test 1:", part1(parseInput(testInput)), "should be 71")
	print("Part 1:", part1(parseInput(rawInput)))
	print("Part 2:", part2(parseInput(rawInput)))
	

if __name__ == "__main__":
	main()
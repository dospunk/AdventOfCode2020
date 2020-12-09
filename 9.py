from typing import Optional
from aocutils import getInput
import aocutils

def parseInput(rawInput: str) -> tuple[list[int], list[int]]:
	rawSplit = rawInput.split("\n")
	preamble = [int(x) for x in rawSplit[:25]]
	#print(preamble)#DEV
	data = [int(x) for x in rawSplit[25:]]
	return (preamble, data)

def part1(preamble: list[int], data: list[int]) -> int:
	while len(data) != 0:
		datum = data[0]
		valid = False
		for p in preamble:
			target = datum - p
			valid = target != datum/2 and target in preamble
			if valid:
				#print(f"{datum} is the sum of {target} and {datum-target}")#DEV
				break
		if not valid:
			return datum
		preamble.pop(0)
		preamble.append(data.pop(0))
	return -1

def part2(data: list[int], target: int) -> int:
	for i, datum in enumerate(data):
		total = datum
		largest = datum 
		smallest = datum
		for j in range(i+1,len(data)):
			total += data[j]
			largest = max(largest, data[j])
			smallest = min(smallest, data[j])
			if total == target:
				return largest+smallest
			if total > target:
				break
	return -1



INPUT = aocutils.getInput(r'inputs\9.txt')
part1Answer = part1(*parseInput(INPUT))
print(f"Part 1: {part1Answer}")
print(f"Part 2: {part2(parseInput(INPUT)[1], part1Answer)}")
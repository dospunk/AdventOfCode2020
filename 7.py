from __future__ import annotations
from typing import Dict, List, NamedTuple, NewType
from dataclasses import dataclass

MY_BAG = "shiny gold"

def getInput(fileLocation: str) -> str:
	with open(fileLocation, 'r') as file:
		return file.read().strip()

class HoldsData(NamedTuple):
	color: str
	quantity: int

class ConnectionData(NamedTuple):
	holds: set[HoldsData]
	heldBy: set[str]

def parseInput(rawInput: str) -> Dict[str, ConnectionData]:
	out: Dict[str, ConnectionData] = {}
	for line in rawInput.splitlines():
		color: str = line.split("bags", 1)[0].strip()
		rawHeldBags = line.split("contain", 1)[1].strip()
		holds: set[HoldsData] = set()
		if rawHeldBags != "no other bags.":
			splitRawHeldBags = rawHeldBags.split(", ")
			for rawHeldBag in splitRawHeldBags:
				splitUpHeldBag = rawHeldBag.split(" ")
				quantity = int(splitUpHeldBag[0])
				heldBagColor = splitUpHeldBag[1]+" "+splitUpHeldBag[2]
				holds.add(HoldsData(heldBagColor, quantity))
				if heldBagColor not in out:
					out[heldBagColor] = ConnectionData(set(), set([color]))
				else:
					out[heldBagColor].heldBy.add(color)
		if color not in out:
			out[color] = ConnectionData(holds, set())
		else:
			out[color].holds.update(holds)
	return out

def findHoldersForBag(startColor: str, bags: Dict[str, ConnectionData], holdables: set[str] = set()) -> int:
	holdables.update(bags[startColor].heldBy)
	for color in bags[startColor].heldBy:
		findHoldersForBag(color, bags, holdables)
	return len(holdables)

def part1():
	print(findHoldersForBag(MY_BAG, parseInput(getInput("inputs\\7.txt"))))

def findNumberOfBags(startColor: str, bags: Dict[str, ConnectionData])->int:
	count = 0
	for heldBag in bags[startColor].holds:
		count += heldBag.quantity
		count += findNumberOfBags(heldBag.color, bags) * heldBag.quantity
	return count

def part2():
	print(findNumberOfBags(MY_BAG, parseInput(getInput("inputs\\7.txt"))))

print("Part 1: ", end="")
part1()
print("Part 2: ", end="")
part2()

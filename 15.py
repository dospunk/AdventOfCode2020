from typing import Optional
from aocutils import getInput
import aocutils
from pprint import pprint
from dataclasses import dataclass

#this is not the best idea
import sys
sys.setrecursionlimit(2020)

def parseInput(rawInput: str) -> list[int]:
	return [int(n) for n in rawInput.split(",")]

def part1(nums: list[int]) -> int:
	"""Deprecated"""
	if len(nums) == 2020:
		return nums.pop()
	else:
		currPos = len(nums)-1
		last = nums[currPos]
		if nums.count(last) == 1:
			nums.append(0)
		else:
			nums.append((nums[len(nums)-2::-1].index(last) + 1))
		return part1(nums)

@dataclass
class numInfo:
	mostRecentTurn: int
	secondMostRecentTurn: int
	onlySpokenOnce: bool

def game(start: list[int], turns: int) -> int:
	numsSaid: dict[int, numInfo] = {}
	#populate numsSaid
	for i, n in enumerate(start):
		numsSaid[n] = numInfo(i+1, -1, True)
	lastSaid = start[-1]
	for i in range(len(start)+1, turns+1):
		if numsSaid[lastSaid].onlySpokenOnce:
			spokenBefore = 0 in numsSaid
			secondMostRecent = numsSaid[0].mostRecentTurn if spokenBefore else -1
			numsSaid[0] = numInfo(i, secondMostRecent, not spokenBefore)
			#print(i, ":", 0, ",", numsSaid[0]) #DEV
			lastSaid = 0
		else:
			newNum = (i-1) - numsSaid[lastSaid].secondMostRecentTurn
			#print(i, numsSaid[lastSaid][0]) #dev
			spokenBefore = newNum in numsSaid
			secondMostRecent = numsSaid[newNum].mostRecentTurn if spokenBefore else -1
			numsSaid[newNum] = numInfo(i, secondMostRecent, not spokenBefore)
			#print(i, ":", newNum, ",", numsSaid[newNum][1]) #DEV
			lastSaid = newNum
	return [k for k,v in numsSaid.items() if v.mostRecentTurn==turns][0]

def main():
	my_input = aocutils.getInput("inputs\\15.txt")
	test_input = [0,3,6]
	print("Test 1.1:", game(test_input, 10), "should be 0")
	print("Test 1.1:", game(test_input, 2020), "should be 436")
	print("Part 1:", game(parseInput(my_input), 2020))
	print("Part 2:", game(parseInput(my_input), 30000000))

if __name__ == "__main__":
	main()
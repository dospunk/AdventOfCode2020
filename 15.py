from aocutils import getInput
import aocutils

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

def gameHelper(maximum: int, nums: dict[int, int], currPos: int) -> int:
	if currPos == maximum+1:
		return list(nums.keys())[list(nums.values()).index(maximum)]
	

def game(maximum: int, nums: list[int]) -> int:
	numsDict = {}
	for i, n in enumerate(nums):
		numsDict[n] = i
	return gameHelper(maximum, numsDict, len(nums))

def main():
	print("Part 1:", part1(parseInput(aocutils.getInput("inputs\\15.txt"))))

if __name__ == "__main__":
	main()
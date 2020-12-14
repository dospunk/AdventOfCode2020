from aocutils import getInput
import math

import aocutils

def closest_greater_multiple(x: int, n: int) -> int:
	"""returns the multiple of x closest to n"""
	step1 = n + math.floor(x/2)
	step2 = step1 - (step1%x)
	if step2 < n:
		return step2+x
	return step2

def parse_input(raw_input: str)-> tuple[int, list[int]]:
	lines = raw_input.splitlines()
	earliest_departure = int(lines[0])
	busses = [int(x) if x != "x" else -1 for x in lines[1].split(",")]
	return (earliest_departure, busses)

def part1(arrival_time: int, busses: list[int]) -> int :
	busses = [x for x in busses if x != -1]
	departures = {}
	for bus in busses:
		departures[closest_greater_multiple(bus, arrival_time)] = bus
	min_departure = min([time for time in departures])
	return departures[min_departure] * (min_departure - arrival_time)

def part2(busses: list[int]) -> int:
	#Chinese Remainder Theorem
	#https://crypto.stanford.edu/pbc/notes/numbertheory/crt.html
	a_list = [i*-1 for i,x in enumerate(busses) if x != -1]
	valid_busses = [bus for bus in busses if bus != -1]
	M = math.prod(valid_busses)
	to_sum: list[int] = []
	for a,m in zip(a_list, valid_busses):
		b = M//m
		b_prime = pow(b, -1, m)
		to_sum.append(a*b*b_prime)
	return sum(to_sum) % M


def main():
	raw_input = aocutils.getInput("inputs\\13.txt")
	test_input = "939\n7,13,x,x,59,x,31,19"
	print("Test 1:", part1(*parse_input(test_input)), "should be 295")
	print("Part 1:", part1(*parse_input(raw_input)))
	print("Test 2:", part2(parse_input(test_input)[1]), "should be 1068781")
	print("Part 2:", part2(parse_input(raw_input)[1]))
	

if __name__ == "__main__":
	main()
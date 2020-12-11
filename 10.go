package main

import (
	"fmt"
	"sort"
	"strconv"
	"strings"

	"./aocutils"
)

func parseInput(rawInput string) []int {
	rawLines := strings.Split(rawInput, "\n")
	out := make([]int, len(rawLines))
	for i, line := range rawLines {
		num, err := strconv.Atoi(strings.TrimSpace(line))
		aocutils.CheckErr(err)
		out[i] = num
	}
	return out
}

func part1(adapters []int) int {
	diffs := make(map[int]int)
	adapters = append(adapters, 0)
	sort.Ints(adapters)
	for i := 0; i < len(adapters)-1; i++ {
		diffs[adapters[i+1]-adapters[i]]++
	}
	//for the built in charger
	diffs[3]++
	//fmt.Println(diffs)//DEV
	return diffs[1] * diffs[3]
}

/*recursive solution, can't memoize
func part2Helper(adapters []int, pos int, total *int) {
	if pos == len(adapters)-1 {
		*total++
	}
	curr := adapters[pos]
	for i := pos + 1; i < len(adapters); i++ {
		if adapters[i] > curr+3 {
			break
		}
		part2Helper(adapters, pos+1, total)
	}
}

func part2(adapters []int) int {
	adapters = append(adapters, 0)
	sort.Ints(adapters)
	out := 0
	part2Helper(adapters, 0, &out)
	return out
}
*/

/*can't figure why this one doesn't work
func part2(adapters []int) int {
	adapters = append(adapters, 0)
	sort.Ints(adapters)
	mapped := make(map[int]bool)
	for _, v := range adapters {
		mapped[v] = true
	}
	//fmt.Println(mapped) //DEV
	connections := 1
	for _, v := range adapters {
		total := 0
		for i := 1; i <= 3 ; i++ {
			if mapped[v+i] {
				total++
			}
		}
		//the only one that will be 0 is the last one
		if total != 0 {
			connections *= total
		}
	}
	return connections
}*/

func part2Helper() {

}

func part2(adapters []int) int {
	adapters = append(adapters, 0)
	sort.Ints(adapters)
	memo := make(map[int]string)
	var paths []string

	return 0
}

func main() {
	input := aocutils.ReadInput("inputs\\10.txt")
	fmt.Println("Part 1:", part1(parseInput(input)))
	fmt.Println("Part 2:", part2(parseInput(input)))
}

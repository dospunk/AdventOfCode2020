package main

import (
	"fmt"
	"strconv"
	"strings"

	"./aocutils"
	"./aocutils/vm"
)

func parseInput(rawInput string) []vm.Instruction {
	rawLines := strings.Split(rawInput, "\n")
	out := make([]vm.Instruction, len(rawLines))
	for i, line := range rawLines {
		splitLine := strings.Split(line, " ")
		op := strings.TrimSpace(splitLine[0])
		val, err := strconv.Atoi(strings.TrimSpace(splitLine[1]))
		aocutils.CheckErr(err)
		instr := vm.Instruction{op, val}
		out[i] = instr
	}
	return out
}

func part1(code []vm.Instruction) int {
	machine := vm.New(code)
	alreadyExecuted := map[int]bool{}
	for !alreadyExecuted[machine.Pc] {
		alreadyExecuted[machine.Pc] = true
		machine.Step()
	}
	fmt.Println(machine.Pc)
	return machine.Accum
}

func part2(code []vm.Instruction) int {
	var out int
BruteLoop:
	for i := 0; i < len(code); i++ {
		if code[i].Opcode == "acc" {
			continue
		} else if code[i].Opcode == "jmp" {
			code[i].Opcode = "nop"
		} else {
			code[i].Opcode = "jmp"
		}
		machine := vm.New(code)
		alreadyExecuted := map[int]bool{}
	ExecuteLoop:
		for !alreadyExecuted[machine.Pc] {
			if machine.Pc > len(code) || machine.Pc < 0 {
				break ExecuteLoop
			}
			alreadyExecuted[machine.Pc] = true
			machine.Step()
			if machine.Pc == len(code) {
				//fmt.Println("Finished by switching instruction at", i)
				out = machine.Accum
				break BruteLoop
			}
		}
		if code[i].Opcode == "acc" {
			fmt.Println("Something very wrong happened here")
			continue
		} else if code[i].Opcode == "jmp" {
			code[i].Opcode = "nop"
		} else {
			code[i].Opcode = "jmp"
		}
	}
	return out
}

func main() {
	fmt.Println("Part 1:", part1(parseInput(aocutils.ReadInput("inputs\\8.txt"))))
	fmt.Println("Part 2:", part2(parseInput(aocutils.ReadInput("inputs\\8.txt"))))
}

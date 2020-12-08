package vm

import (
	"fmt"
	"log"
)

//Instruction is a vm instruction
type Instruction struct {
	Opcode string
	Value  int
}

//Machine is the virtual machine
type Machine struct {
	Code  []Instruction
	Pc    int
	Accum int
}

//Step executes the command at Pc
func (m *Machine) Step() {
	instr := m.Code[m.Pc]
	switch instr.Opcode {
	case "nop":
		m.Pc++
	case "acc":
		m.Pc++
		m.Accum += instr.Value
	case "jmp":
		m.Pc += instr.Value
	default:
		log.Fatal("Opcode" + instr.Opcode + " not recognized")
	}
}

//StepAndLog runs Step and logs the machine state
func (m *Machine) StepAndLog() {
	instr := m.Code[m.Pc]
	m.Step()
	fmt.Println("Opcode:", instr.Opcode)       //DEV
	fmt.Println("PC:", m.Pc)                   //DEV
	fmt.Println("Accumulator:", m.Accum, "\n") //DEV
}

//New creates a Machine
func New(code []Instruction) Machine {
	return Machine{code, 0, 0}
}

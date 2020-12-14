//DOES NOT WORK
package main

import (
	"fmt"
	"log"
	"math"
	"strconv"
	"strings"

	"./aocutils"
)

type command struct {
	direction byte
	amount    float64
}

func lineToCommand(line string) command {
	cmd := line[0]
	amnt, err := strconv.Atoi(line[1:])
	aocutils.CheckErr(err)
	return command{cmd, float64(amnt)}
}

func parseInput(rawInput string) []command {
	rawLines := strings.Split(rawInput, "\n")
	out := make([]command, len(rawLines))
	for i, line := range rawLines {
		out[i] = lineToCommand(line)
	}
	return out
}

var (
	north aocutils.Point = aocutils.Point{0, 1}
	south aocutils.Point = aocutils.Point{0, -1}
	east  aocutils.Point = aocutils.Point{1, 0}
	west  aocutils.Point = aocutils.Point{-1, 0}
)

func manhatten(a aocutils.Point, b aocutils.Point) float64 {
	return math.Abs(a.X-b.X) + math.Abs(a.Y-b.Y)
}

func polarToCartesian(r float64, theta float64) aocutils.Point {
	return aocutils.Point{
		X: r * math.Cos(theta),
		Y: r * math.Sin(theta),
	}
}

func degToRad(deg float64) float64 {
	return deg * math.Pi / 180
}

func part1(commands []command) float64 {
	pos := aocutils.Point{0, 0}
	rot := 0.0
	for _, cmd := range commands {
		switch cmd.direction {
		case 'N':
			pos = pos.Add(north.Scale(cmd.amount))
		case 'S':
			pos = pos.Add(south.Scale(cmd.amount))
		case 'E':
			pos = pos.Add(east.Scale(cmd.amount))
		case 'W':
			pos = pos.Add(west.Scale(cmd.amount))
		case 'R':
			rot -= float64(cmd.amount)
		case 'L':
			rot += float64(cmd.amount)
		case 'F':
			pos = pos.Add(polarToCartesian(cmd.amount, degToRad(rot)))
		default:
			log.Fatal("Command not recognized:", cmd.direction)
		}
	}
	//fmt.Println(pos)//DEV
	return manhatten(aocutils.Point{0, 0}, pos)
}

func part2(commands []command) float64 {
	pos := aocutils.Point{0, 0}
	waypoint := aocutils.Point{10, 1}
	for _, cmd := range commands {
		switch cmd.direction {
		case 'N':
			waypoint = waypoint.Add(north.Scale(cmd.amount))
		case 'S':
			waypoint = waypoint.Add(south.Scale(cmd.amount))
		case 'E':
			waypoint = waypoint.Add(east.Scale(cmd.amount))
		case 'W':
			waypoint = waypoint.Add(west.Scale(cmd.amount))
		case 'R':
			waypoint = waypoint.Rotate(degToRad(cmd.amount * -1))
		case 'L':
			waypoint = waypoint.Rotate(degToRad(cmd.amount))
		case 'F':
			pos = pos.Add(waypoint.Scale(cmd.amount))
		default:
			log.Fatal("Command not recognized:", cmd.direction)
		}
	}
	//fmt.Println(pos)//DEV
	return manhatten(aocutils.Point{0, 0}, pos)
}

func main() {
	rawInput := aocutils.ReadInput("inputs\\12.txt")
	testInput1 := strings.ReplaceAll(`F10
	N3
	F7
	R90
	F11`, "\t", "")
	fmt.Println("Test 1:", part1(parseInput(testInput1)), "should be 25")
	fmt.Println("Part 1:", math.Round(part1(parseInput(rawInput))))
	fmt.Println("Test 2:", part2(parseInput(testInput1)), "should be 286")
	fmt.Println("Part 2:", math.Round(part2(parseInput(rawInput))))
}

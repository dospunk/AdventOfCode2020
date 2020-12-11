package main

import (
	"fmt"
	"log"
	"strings"

	"github.com/nsf/termbox-go"

	"./aocutils"
)

type point struct {
	x int
	y int
}

func (p point) add(b point) point {
	p.x += b.x
	p.y += b.y
	return p
}

func (p point) eq(b point) bool {
	return p.x == b.x && p.y == b.y
}

func areaToString(area [][]rune) string {
	lines := make([]string, len(area))
	for i, v := range area {
		lines[i] = string(v)
	}
	return strings.Join(lines, "\n")
}

func compare2DSlices(a [][]rune, b [][]rune) bool {
	if len(a) != len(b) {
		log.Fatal("Cannot compare these slices, number of rows is different")
	}
	for i := 0; i < len(a); i++ {
		if len(a[i]) != len(b[i]) {
			log.Fatal("Cannot compare these slices, number of items in row", i, "is different")
		}
		for j := 0; j < len(a[i]); j++ {
			if a[i][j] != b[i][j] {
				return false
			}
		}
	}
	return true
}

func parseInput(rawInput string) [][]rune {
	rawLines := strings.Split(rawInput, "\n")
	out := make([][]rune, len(rawLines))
	for i := 0; i < len(out); i++ {
		out[i] = make([]rune, len(rawLines[0]))
	}
	for i, line := range rawLines {
		for j, char := range line {
			out[i][j] = char
		}
	}
	return out
}

func checkAdjacents(area [][]rune, pos point) (occupied, empty int) {
	occupied = 0
	empty = 0
	for i := pos.y - 1; i <= pos.y+1; i++ {
		for j := pos.x - 1; j <= pos.x+1; j++ {
			inbounds := j >= 0 && i >= 0 && i < len(area) && j < len(area[i])
			if !pos.eq(point{j, i}) && inbounds {
				if area[i][j] == 'L' {
					empty++
				} else if area[i][j] == '#' {
					occupied++
				}
			}
		}
	}
	return
}

func testCell(area [][]rune, pos point) rune {
	cell := area[pos.y][pos.x]
	if cell == 'L' {
		occupied, _ := checkAdjacents(area, pos)
		if occupied == 0 {
			return '#'
		}
	} else if cell == '#' {
		occupied, _ := checkAdjacents(area, pos)
		if occupied >= 4 {
			return 'L'
		}
	}
	return cell
}

func showArea(area [][]rune) {
	for i, row := range area {
		for j, cell := range row {
			termbox.SetChar(j, i, cell)
		}
	}
	termbox.Flush()
}

func part1(area [][]rune) int {
	err := termbox.Init()
	aocutils.CheckErr(err)
	defer termbox.Close()
	prevArea := make([][]rune, len(area))
	for i := 0; i < len(prevArea); i++ {
		prevArea[i] = make([]rune, len(area[i]))
	}
	for !compare2DSlices(area, prevArea) {
		showArea(area)
		for i := 0; i < len(prevArea); i++ {
			copy(prevArea[i], area[i])
		}
		for i, row := range prevArea {
			for j := 0; j < len(row); j++ {
				oldCell := area[i][j]
				area[i][j] = testCell(prevArea, point{j, i})
				//this doesn't work on Windows Terminal, unsure why :/
				if area[i][j] == oldCell {
					termbox.SetFg(j, i, termbox.RGBToAttribute(255, 0, 0))
				} else {
					termbox.SetFg(j, i, termbox.RGBToAttribute(0, 255, 0))
				}
				termbox.Flush()
			}
		}
		//time.Sleep(time.Second / 2)
	}
	out := 0
	for _, row := range area {
		for _, cell := range row {
			if cell == '#' {
				out++
			}
		}
	}
	return out
}

func main() {
	fmt.Println("Part 1:", part1(parseInput(aocutils.ReadInput("inputs\\11.txt"))))
}

package main

import (
	"fmt"
	"log"
	"strings"

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

func testCell1(area [][]rune, pos point) rune {
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

func part1(area [][]rune) int {
	prevArea := make([][]rune, len(area))
	for i := 0; i < len(prevArea); i++ {
		prevArea[i] = make([]rune, len(area[i]))
	}
	for !compare2DSlices(area, prevArea) {
		for i := 0; i < len(prevArea); i++ {
			copy(prevArea[i], area[i])
		}
		for i, row := range prevArea {
			for j := 0; j < len(row); j++ {
				area[i][j] = testCell1(prevArea, point{j, i})
			}
		}
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

var (
	upDir    point = point{0, -1}
	downDir  point = point{0, 1}
	leftDir  point = point{-1, 0}
	rightDir point = point{1, 0}
)

func (p point) inBoundsOf(area [][]rune) bool {
	return p.x >= 0 && p.y >= 0 && p.y < len(area) && p.x < len(area[0])
}

func checkVisible(area [][]rune, pos point) int {
	occupied := 0
	dirs := [8]point{upDir, downDir, leftDir, rightDir, upDir.add(leftDir), upDir.add(rightDir), downDir.add(leftDir), downDir.add(rightDir)}
	for _, dir := range dirs {
		for p := pos.add(dir); p.inBoundsOf(area); p = p.add(dir) {
			cell := area[p.y][p.x]
			if cell == '#' {
				occupied++
				break
			} else if cell == 'L' {
				break
			}
		}
	}
	return occupied
}

func testCell2(area [][]rune, pos point) rune {
	cell := area[pos.y][pos.x]
	if cell == 'L' {
		occupied := checkVisible(area, pos)
		if occupied == 0 {
			return '#'
		}
	} else if cell == '#' {
		occupied := checkVisible(area, pos)
		if occupied >= 5 {
			return 'L'
		}
	}
	return cell
}

func part2(area [][]rune) int {
	prevArea := make([][]rune, len(area))
	for i := 0; i < len(prevArea); i++ {
		prevArea[i] = make([]rune, len(area[i]))
	}
	for !compare2DSlices(area, prevArea) {
		for i := 0; i < len(prevArea); i++ {
			copy(prevArea[i], area[i])
		}
		for i, row := range prevArea {
			for j := 0; j < len(row); j++ {
				area[i][j] = testCell2(prevArea, point{j, i})
			}
		}
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
	rawInput := aocutils.ReadInput("inputs\\11.txt")
	fmt.Println("Part 1:", part1(parseInput(rawInput)))
	fmt.Println("Part 2:", part2(parseInput(rawInput)))
}

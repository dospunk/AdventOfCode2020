package main

import (
	"fmt"
	"log"
	"math"
	"strings"

	"./aocutils"
)

type point3d struct {
	x int
	y int
	z int
}

type dimensionDimensions3d struct {
	maxZ int
	minZ int
	maxY int
	minY int
	maxX int
	minX int
}

func newDimensionDimensions3d(dim map[point3d]bool) dimensionDimensions3d {
	dims := dimensionDimensions3d{
		math.MinInt64,
		math.MaxInt64,
		math.MinInt64,
		math.MaxInt64,
		math.MinInt64,
		math.MaxInt64,
	}

	for p, alive := range dim {
		if alive {
			if p.z > dims.maxZ {
				dims.maxZ = p.z
			}
			if p.z < dims.minZ {
				dims.minZ = p.z
			}
			if p.y > dims.maxY {
				dims.maxY = p.y
			}
			if p.y < dims.minY {
				dims.minY = p.y
			}
			if p.x > dims.maxX {
				dims.maxX = p.x
			}
			if p.x < dims.minX {
				dims.minX = p.x
			}
		}
	}
	return dims
}

func printDimension3d(dim map[point3d]bool) {
	dims := newDimensionDimensions3d(dim)
	//if minZ > maxZ then no change has been made to the original values, meaning the map is empty
	if dims.maxZ >= dims.minZ {
		levels := make([]string, dims.maxZ-dims.minZ+1)
		for i := dims.minZ; i <= dims.maxZ; i++ {
			levels[i-dims.minZ] = ""
			for j := dims.minY; j <= dims.maxY; j++ {
				for k := dims.minX; k <= dims.maxX; k++ {
					p := point3d{k, j, i}
					if dim[p] {
						levels[i-dims.minZ] += "#"
					} else {
						levels[i-dims.minZ] += "."
					}
				}
				levels[i-dims.minZ] += "\n"
			}
		}
		fmt.Println("X:", dims.minX, "-", dims.maxX)
		fmt.Println("Y:", dims.minY, "-", dims.maxY)

		for i, v := range levels {
			fmt.Println("Z =", i+dims.minZ)
			fmt.Println(v)
		}
	}
}

func parseInput3d(rawInput string) map[point3d]bool {
	dimension := make(map[point3d]bool)
	for y, row := range strings.Split(rawInput, "\n") {
		for x, chr := range row {
			switch chr {
			case '.':
				dimension[point3d{x, y, 0}] = false
			case '#':
				dimension[point3d{x, y, 0}] = true
			default:
				log.Fatal("Unknown character in map:", string(chr))
			}
		}
	}
	return dimension
}

func livingNeighbors3d(loc point3d, dimension map[point3d]bool) int {
	out := 0
	//var n []point//DEV
	for z := -1; z <= 1; z++ {
		for y := -1; y <= 1; y++ {
			for x := -1; x <= 1; x++ {
				p := point3d{loc.x + x, loc.y + y, loc.z + z}
				if !(x == 0 && y == 0 && z == 0) && dimension[p] {
					out++
					//n = append(n, p) //DEV
				}
			}
		}
	}
	//fmt.Println("Neighbors for", loc, ":", out) //DEV
	//for _, v := range n {                       //DEV
	//	fmt.Println("\t", v) //DEV
	//} //DEV
	return out
}

func cycle3d(dimension map[point3d]bool) map[point3d]bool {
	next := make(map[point3d]bool)
	dims := newDimensionDimensions3d(dimension)
	for z := dims.minZ - 1; z <= dims.maxZ+1; z++ {
		for y := dims.minY - 1; y <= dims.maxY+1; y++ {
			for x := dims.minX - 1; x <= dims.maxX+1; x++ {
				location := point3d{x, y, z}
				alive := dimension[location]
				neighbors := livingNeighbors3d(location, dimension)
				//fmt.Println("Neighbors for", location, ":", neighbors) //DEV
				if alive {
					if neighbors == 2 || neighbors == 3 {
						next[location] = true
					} else {
						next[location] = false
					}
				} else {
					if neighbors == 3 {
						next[location] = true
					} else {
						next[location] = false
					}
				}
			}
		}
	}
	return next
}

func part1(dimension map[point3d]bool) int {
	for i := 0; i < 6; i++ {
		//fmt.Println("Cycles:", i)//DEV
		//printDimension(dimension) //DEV
		dimension = cycle3d(dimension)
	}
	out := 0
	for _, v := range dimension {
		if v {
			out++
		}
	}
	return out
}

func main() {
	rawInput := aocutils.ReadInput("inputs\\17.txt")
	testInput := strings.ReplaceAll(`.#.
	..#
	###`, "\t", "")
	fmt.Println("Test 1:", part1(parseInput3d(testInput)), "should be 112")
	fmt.Println("Part 1:", part1(parseInput3d(rawInput)))
}

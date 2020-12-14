package aocutils

import (
	"io/ioutil"
	"log"
	"math"
	"os"
	"strings"
)

//CheckErr checks for an error
func CheckErr(e error) {
	if e != nil {
		log.Fatal(e)
	}
}

//ReadInput reads the input file to a string
func ReadInput(fileName string) string {
	file, err := os.Open(fileName)
	CheckErr(err)
	defer func() {
		CheckErr(file.Close())
	}()

	bytes, err := ioutil.ReadAll(file)
	CheckErr(err)
	return strings.ReplaceAll(strings.TrimSpace(string(bytes)), "\r", "")
}

//Point is a point
type Point struct {
	X float64
	Y float64
}

//Add adds two points together and returns the result
func (p Point) Add(b Point) Point {
	p.X += b.X
	p.Y += b.Y
	return p
}

//Eq tells if two Points are equal
func (p Point) Eq(b Point) bool {
	return p.X == b.X && p.Y == b.Y
}

//Scale multiples a point by a scalar and returns the result
func (p Point) Scale(scalar float64) Point {
	p.X *= scalar
	p.Y *= scalar
	return p
}

//Rotate rotates a Point theta radians around 0,0 and returns a new Point
func (p Point) Rotate(theta float64) Point {
	newX := (p.X * math.Cos(theta)) - (p.Y * math.Sin(theta))
	newY := (p.Y * math.Cos(theta)) + (p.X * math.Sin(theta))
	return Point{newX, newY}
}

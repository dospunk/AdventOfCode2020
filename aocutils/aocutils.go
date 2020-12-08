package aocutils

import (
	"io/ioutil"
	"log"
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
	return strings.TrimSpace(string(bytes))
}

from typing import Optional
from dataclasses import dataclass
from aocutils import getInput

INPUT=getInput("inputs\\4.txt")

import re

@dataclass
class Passport:
	byr: Optional[str] = None
	iyr: Optional[str] = None
	eyr: Optional[str] = None
	hgt: Optional[str] = None
	hcl: Optional[str] = None
	ecl: Optional[str] = None
	pid: Optional[str] = None
	cid: Optional[str] = None

	def isValid(self) -> bool:
		if (self.byr is not None
		and self.iyr is not None
		and self.eyr is not None
		and self.hgt is not None
		and self.hcl is not None
		and self.ecl is not None
		and self.pid is not None):
			byrValid = len(self.byr) == 4 and (1920 <= int(self.byr) <= 2002)
			iyrValid = len(self.iyr) == 4 and (2010 <= int(self.iyr) <= 2020)
			eyrValid = len(self.eyr) == 4 and (2020 <= int(self.eyr) <= 2030)
			hgtSuffix = self.hgt[-2:]
			hgtValid = hgtSuffix == "cm" or hgtSuffix == "in"
			if hgtSuffix == "cm":
				hgtValid = hgtValid and (150 <= int(self.hgt[:-2]) <= 193)
			elif hgtSuffix == "in":
				hgtValid = hgtValid and (59 <= int(self.hgt[:-2]) <= 76)
			hclValid = bool(re.match(r'^#(\d|[a-f]){6}$', self.hcl))
			eclValid = self.ecl in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
			pidValid = len(self.pid) == 9 and self.pid.isdigit()
			return byrValid and iyrValid and eyrValid and hgtValid and hclValid and eclValid and pidValid
		return False

def inputToPassports(input: str) -> list[Passport]:
	output: list[Passport] = []
	#split input into individual passport strings
	firstSplit = input.split("\n\n")
	#split each passport string into its components
	secondSplit = map(lambda x: re.split(r'\s', x), firstSplit)
	for rawPassport in secondSplit:
		passportArgs: dict[str, str] = {}
		for item in rawPassport:
			name, data = item.split(":")
			passportArgs[name] = data
		output.append(Passport(**passportArgs))
	return output
	
def main():
	numValid = 0
	for passport in inputToPassports(INPUT):
		if passport.isValid():
			numValid += 1
	print(numValid)

if __name__ == "__main__":
	main()
from typing import Optional
from dataclasses import dataclass
from aocutils import getInput, get_char

INPUT=getInput("inputs\\4.txt")

import re
from rich.console import Console
from rich.table import Table
from rich import box
from rich.theme import Theme
from random import randint
import time 

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

def convertColor(color: Optional[str]) -> str:
	ignoreColors = ["z", "zzz", "grt", "oth", "utc", "dne", "gmt"]
	if color is not None and color not in ignoreColors:
		if color.startswith("#"):
			return color
		elif len(color) == 6:
			return "#"+color
		else:
			return {
				"grn": "green",
				"amb": "#FFBF00",
				"hzl": "#8E7618",
				"gry": "bright_black",
				"blu": "blue",
				"brn": "#654321",
				"lzr": "#00ff00",
				"xry": "#0083D9"
			}[color]
	else:
		return "white"

def randomFace() -> str:
	eyes = "0OoUQ="
	mouths = "vU=-O"
	noses = "|VC7U`"
	brows = "_~="
	#ears strings must be 2 chars long
	ears = ["[]", "<>", "{}", "()"]
	#hairs and bangs strings must be 5 characters long
	bangs = ["     ", "|||||", "!!!!!", "#####"]
	hairs = ["_____", "|||||", "_/~\\_", "|^^^|", "MMMMM"]
	selections = {
		"eyes": eyes[randint(0, len(eyes)-1)],
		"ears": ears[randint(0, len(ears)-1)],
		"mouths": mouths[randint(0, len(mouths)-1)],
		"noses": noses[randint(0, len(noses)-1)],
		"brows": brows[randint(0, len(brows)-1)],
		"bangs": bangs[randint(0, len(bangs)-1)],
		"hairs": hairs[randint(0, len(hairs)-1)]
	}
	return f"""   [hairclr]{selections["hairs"]}[/hairclr]   
  /[hairclr]{selections["bangs"]}[/hairclr]\\  
 / [hairclr]{selections["brows"]}[/hairclr]   [hairclr]{selections["brows"]}[/hairclr] \\ 
{selections["ears"][0]}  [eyeclr]{selections["eyes"]}[/eyeclr]   [eyeclr]{selections["eyes"]}[/eyeclr]  {selections["ears"][1]}
 \\   {selections["noses"]}   / 
  \\_ {selections["mouths"]} _/  
 ___| |___ 
/         \\"""

def formatPassportData(data: Optional[str]) -> str:
	if data is not None:
		return f"[u]{data.ljust(9, ' ')}[/u]" 
	else:
		return '[u]         [/u]'

def displayPassport(passport: Passport, console: Console):
	theme = Theme({
		"eyeclr": convertColor(passport.ecl) ,
		"hairclr": convertColor(passport.hcl) 
	})
	with console.use_theme(theme):
		table = Table(title="Advent of Code Passport", box=box.ROUNDED, show_header=False, min_width=33)
		table.add_column("picture", width=11)
		table.add_column("data", width=15)
		faceLines = randomFace().split("\n")
		table.add_row(faceLines[0], f"byr: {formatPassportData(passport.byr)}")
		table.add_row(faceLines[1], f"iyr: {formatPassportData(passport.iyr)}")
		table.add_row(faceLines[2], f"eyr: {formatPassportData(passport.eyr)}")
		table.add_row(faceLines[3], f"hgt: {formatPassportData(passport.hgt)}")
		table.add_row(faceLines[4], f"hcl: {formatPassportData(passport.hcl)}")
		table.add_row(faceLines[5], f"ecl: {formatPassportData(passport.ecl)}")
		table.add_row(faceLines[6], f"pid: {formatPassportData(passport.pid)}")
		table.add_row(faceLines[7], f"cid: {formatPassportData(passport.cid)}")
		console.print(table)
	
def main():
	numValid = 0
	console = Console(color_system="auto")
	for passport in inputToPassports(INPUT):
		console.clear()
		displayPassport(passport, console)
		console.print("(y):heavy_check_mark: [green]VALID[/green]           :x: [red]INVALID[/red](n)")
		direction = get_char()
		console.clear()
		if (direction == "y" and passport.isValid()) or (direction == "n" and not passport.isValid()):
			print()
			print()
			print()
			print()
			console.print("[green]:heavy_check_mark:CORRECT:heavy_check_mark:[/]")
		else:
			print()
			print()
			print()
			print()
			console.print("[red]:x:INCORRECT:x:[/]")
		time.sleep(0.5)
		if passport.isValid():
			numValid += 1
	print(numValid)

if __name__ == "__main__":
	main()
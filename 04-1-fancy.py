from typing import Optional, Union
from dataclasses import dataclass
import re
from rich.console import Console
from rich.table import Table
from rich import box
from rich.theme import Theme
from rich.color import Color
from random import randint
import time 
from aocutils import getInput

INPUT=getInput("inputs\\4.txt")

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
		return Color.default().get_truecolor().rgb

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

	def isValid(self):
		return (self.byr is not None
		and self.iyr is not None
		and self.eyr is not None
		and self.hgt is not None
		and self.hcl is not None
		and self.ecl is not None
		and self.pid is not None)

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
		table.add_row(faceLines[0], f"byr: {passport.byr if passport.byr is not None else '[red]??????????[/red]'}")
		table.add_row(faceLines[1], f"iyr: {passport.iyr if passport.iyr is not None else '[red]??????????[/red]'}")
		table.add_row(faceLines[2], f"eyr: {passport.eyr if passport.eyr is not None else '[red]??????????[/red]'}")
		table.add_row(faceLines[3], f"hgt: {passport.hgt if passport.hgt is not None else '[red]??????????[/red]'}")
		table.add_row(faceLines[4], f"hcl: {passport.hcl if passport.hcl is not None else '[red]??????????[/red]'}")
		table.add_row(faceLines[5], f"ecl: {passport.ecl if passport.ecl is not None else '[red]??????????[/red]'}")
		table.add_row(faceLines[6], f"pid: {passport.pid if passport.pid is not None else '[red]??????????[/red]'}")
		table.add_row(faceLines[7], f"cid: {passport.cid if passport.cid is not None else '??????????'}")
		console.print(table)
		if passport.isValid():
			console.print(":heavy_check_mark: [green]VALID[/green]")
		else:
			console.print(":x: [red]INVALID[/red]")

	
def main():
	numValid = 0
	console = Console(color_system="auto")
	for passport in inputToPassports(INPUT):
		console.clear()
		displayPassport(passport, console)
		if passport.isValid():
			numValid += 1
		
		time.sleep(0.1)
	console.print(f"Valid passports: {numValid}")

if __name__ == "__main__":
	main()
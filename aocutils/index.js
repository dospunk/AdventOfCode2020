import fs from 'fs';

export async function getInput(fileName){
	const buf = await fs.promises.readFile(fileName);
	return buf.toString().trim();
}

export class Point{
	constructor(x,y){
		this.X = x
		this.Y = y
	}
	
	//Add adds two points together and returns the result
	Add(b) {
		const outX = this.X + b.X
		const outY = this.Y + b.Y
		return Point(outX, outY)
	}

	//Eq tells if two Points are equal
	Eq(b) {
		return this.X == b.X && this.Y == b.Y
	}

	//Scale multiples a point by a scalar and returns the result
	Scale(scalar) {
		const outX = this.X * scalar
		const outY = this.Y * scalar
		return Point(outX, outY)
	}

	//Rotate rotates a Point theta radians around 0,0 and returns a new Point
	Rotate(theta) {
		const newX = (p.X * Math.cos(theta)) - (p.Y * Math.sin(theta))
		const newY = (p.Y * Math.cos(theta)) + (p.X * Math.sin(theta))
		return Point(newX, newY)
	}
}
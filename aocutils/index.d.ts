export declare function getInput(fileName:string):Promise<string>;

export declare class Point{
	X: number
	Y: number

	Add(b: Point): Point
	Eq(b: Point): boolean
	Scale(scalar: number): Point
	Rotate(theta: number): Point
}
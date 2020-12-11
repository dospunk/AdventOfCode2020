import fs from 'fs';

export async function getInput(fileName){
	const buf = await fs.promises.readFile(fileName);
	return buf.toString().trim();
}
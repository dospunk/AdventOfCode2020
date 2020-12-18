import {getInput} from "./aocutils/index.js"

const debugInfo: {
	[key: string]: any
} = {}

/**************************/
/*         Part 1         */
/**************************/

interface maskAndDataV1 {
	onesMask: bigint  //to be or-ed
	zerosMask: bigint //to be and-ed
	data: memoryMapV1
}

interface memoryMapV1 {
	[addr: number]: bigint
}

function extractAddrAndValueV1(line: string): {addr: number, val: bigint}{
	const chopFront = line.substring(4)
	const split = chopFront.split("] = ")
	const addr = parseInt(split[0])
	const val = BigInt(split[1])
	return {addr, val}
}

function maskStrToMasksV1(maskStr: string): {onesMask: bigint, zerosMask: bigint}{
	let onesMask = BigInt(0)
	let zerosMask = BigInt(0)
	for (let i = 0; i < maskStr.length; i++) {
		const offset = BigInt((maskStr.length - 1) - i)
		const bit = maskStr[i];
		if(bit === "X"){
			zerosMask += 1n<<offset
		} else if(bit === "1") {
			zerosMask += 1n<<offset
			onesMask += 1n<<offset
		}
	}
	
	return {onesMask, zerosMask}
}

function parseInputV1(rawInput: string): maskAndDataV1[] {
	const rawLines = rawInput.split("\n")
	const out: maskAndDataV1[] = []
	let outIdx = -1
	for (let i = 0; i < rawLines.length; i++) {
		const line = rawLines[i]
		if (line.startsWith("mask")){
			outIdx++
			const masks = maskStrToMasksV1(line.split(" = ")[1].trim())
			out[outIdx] = {onesMask: masks.onesMask, zerosMask: masks.zerosMask, data: {}}
		} else {
			const {addr, val} = extractAddrAndValueV1(line)
			out[outIdx].data[addr] = val
		}
	}
	return out
}

function applyMaskV1(zerosMask: bigint, onesMask: bigint, value: bigint): bigint {
	value = value | onesMask
	value = value & zerosMask
	return value
}

function part1(input:maskAndDataV1[]): bigint {
	const mem: memoryMapV1 = {}
	for (const item of input) {
		const {onesMask, zerosMask, data} = item
		for (const addr in data) {
			if (Object.prototype.hasOwnProperty.call(data, addr)) {
				let value = data[addr]
				mem[addr] = applyMaskV1(zerosMask, onesMask, value)
			}
		}
	}
	let sum = 0n
	for (const addr in mem) {
		if (Object.prototype.hasOwnProperty.call(mem, addr)) {
			const val = mem[addr];
			sum += val
		}
	}
	return sum
}

/**************************/
/*         Part 2         */
/**************************/

interface memoryMapV2{
	[addr: string]: bigint 
}

interface maskAndDataV2 {
	mask: string
	data: memoryMapV2
}

function extractAddrAndValueV2(line: string): {addr: string, val: bigint}{
	const chopFront = line.substring(4)
	const split = chopFront.split("] = ")
	const addr = split[0].trim()
	const val = BigInt(split[1])
	return {addr, val}
}

function parseInputV2(rawInput: string): maskAndDataV2[]{
	const out: maskAndDataV2[] = []
	let outIdx = -1
	const rawLines = rawInput.split("\n")
	for (const line of rawLines) {
		if (line.startsWith("mask")) {
			outIdx++
			const mask = line.split(" = ")[1].trim()
			out[outIdx] = {
				mask: mask,
				data: {}
			}
		} else {
			const {addr, val} = extractAddrAndValueV2(line)
			out[outIdx].data[addr] = val
		}
	} 
	return out
}

function binaryStrToBigInt(bin: string): bigint {
	//clever? maybe. Bad? almost definitely.
	//console.log(`'${bin}'`)//DEV
	return eval("0b"+bin+"n")
}

function setCharAt(src: string, idx: number, char: string): string {
	return src.substr(0, idx) + char + src.substr(idx+1)
}

async function applyMaskV2Helper(addr: string, value: bigint): Promise<memoryMapV2>{
	const out: memoryMapV2 = {}
	if(addr.includes("X")){
		const firstX = addr.indexOf("X")
		Object.assign(out, await applyMaskV2Helper(setCharAt(addr, firstX, "0"), value))
		Object.assign(out, await applyMaskV2Helper(setCharAt(addr, firstX, "1"), value))
	} else {
		out[binaryStrToBigInt(addr).toString()] = value
	}
	return out
}

async function applyMaskV2(addr: string, value: bigint, mask: string): Promise<memoryMapV2> {
	if (mask.length !== 36) throw new Error(`Mask with bad length: '${mask}'`)
	//console.log(mask)//DEV
	let addrWithMask = ""
	const binaryAddr = BigInt(addr).toString(2).padStart(36, "0")
	if(binaryAddr.length !== mask.length) throw new Error(`Mask does not have same length as binary address\nMask: ${mask}\nbinary address: ${binaryAddr}`)
	//console.log("Binary address:", binaryAddr)//DEV
	for (let i = 0; i < mask.length; i++) {
		switch (mask[i]) {
			case "1":
				addrWithMask += "1"
				break;
			case "X":
				addrWithMask += "X"
				break;
			case "0":
				addrWithMask += binaryAddr[i]
				break;
			default:
				throw new Error(`Unrecognized character in mask: '${mask[i]}'`)
		}
	}
	return await applyMaskV2Helper(addrWithMask, value)
}

async function part2(input: maskAndDataV2[]){
	const mem: memoryMapV2 = {}
	for (const item of input) {
		const mask = item.mask
		for (const addr in item.data) {
			if (Object.prototype.hasOwnProperty.call(item.data, addr)) {
				const val = item.data[addr]
				Object.assign(mem, await applyMaskV2(addr, val, mask))
			}
		}
	}
	//console.dir(mem)//DEV
	let sum = 0n
	for (const addr in mem) {
		if (Object.prototype.hasOwnProperty.call(mem, addr)) {
			sum += mem[addr]
		}
	}
	return sum
}

async function main() {
	const testInput1 = `mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
	mem[8] = 11
	mem[7] = 101
	mem[8] = 0`.replace(/\t/g, "")
	const rawInput = await getInput("inputs\\14.txt")
	console.log("Test 1:", part1(parseInputV1(testInput1)), "should be 165")
	console.log("Part 1:", part1(parseInputV1(rawInput)))
	const testInput2 = `mask = 000000000000000000000000000000X1001X
	mem[42] = 100
	mask = 00000000000000000000000000000000X0XX
	mem[26] = 1`.replace(/\t/g, "")
	console.log("Test 2:", await part2(parseInputV2(testInput2)), "should be 208")
	console.log("Part 2:", await part2(parseInputV2(rawInput)))
} 

main()
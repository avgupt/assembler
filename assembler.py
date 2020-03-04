import sys



############ TO DO##########33
#	HANDLE ASSEMBLER DIRECTIVES

#	DIV
'''def RepresentsInt(s):

    try:
        int(s)
        return True
    except ValueError:
        return False'''

opcodes = {}
opcodes["CLA"] = "0000"
opcodes["LAC"] = "0001"
opcodes["SAC"] = "0010"
opcodes["ADD"] = "0011"
opcodes["SUB"] = "0100"
opcodes["BRZ"] = "0101"
opcodes["BRN"] = "0110"
opcodes["BRP"] = "0111"
opcodes["INP"] = "1000"
opcodes["DSP"] = "1001"
opcodes["MUL"] = "1010"
opcodes["DIV"] = "1011"
opcodes["STP"] = "1100"

opcodeTable = {}
symbolTable = {}
lableTable = {}
ans = []


def passOne(file):

	#asmFile = open(file, "r")
	#asmDirective = ["START","END\n"]

	start = file.readlines()
	#print("jkfghj "+str(len(start)))
	#print(str(start[0])==str("START"))
	#inputTable[address] = start[address+1].split("\t")
	
	startList = start[0].split("\t")
	
	if("START" not in startList[0]):
		#print("ERROR : Missing START")
		sys.exit("ERROR: Missing START")		#stop program
		return
	elif(len(startList)==2):
		location_counter = int(startList[1])
		#print("startList"+str(startList[1]))
		#num = int(startList[1])
	else:
		location_counter = 0
		#num = 255

	address = 0
	inputTable = {}
	num = 255



	while(address<len(start)-1):


		inputTable[address] = list(map(lambda x:x.rstrip(),start[address+1].split("\t")))
		#print(inputTable[address])
		#print(start[address+1])
		#print((inputTable[address]))

		#print(inputTable[address])

				

		if(len(inputTable[address])==2):
			if(inputTable[address][1]!="CLA" and inputTable[address][1]!="STP"):
				sys.exit("ERROR at line " + str(location_counter) +": Incorrect syntax of input. Check documentation.")
			if(inputTable[address][1]=="STP"):
				opcodeTable[location_counter] = [inputTable[address][1],opcodes[inputTable[address][1]]]
				address+=1
				location_counter+=1
				while(True):
					inputTable[address] = list(map(lambda x:x.rstrip(),start[address+1].split("\t")))
					#print(address)
					#print("len "+str(len(inputTable)))
					#print(inputTable[address])
					if(address==len(start)-2):
						if(inputTable[address][0]=="END"):
							return secondPass()
						sys.exit("ERROR: Incorrect syntax of input.'END' expected at the end of program. Check documentation.")


					readVariables(inputTable, address, location_counter)					#	to read variables after STP
					address+=1
					location_counter+=1


		if(len(inputTable[address])== 1):
			if("END" in inputTable[address][0]):
				return secondPass()
			sys.exit("ERROR at line " + str(location_counter) +": Incorrect syntax of input. Check documentation.")


		if(isSymbolValid(inputTable[address][1])):
			sys.exit("ERROR at line " + str(location_counter) +": Invalid assembly opcode '"+inputTable[address][1]+"'. Check documentation.")

		if(len(inputTable[address])==3):
			symbolTable[inputTable[address][2]] = False					# if variable is used but not declared


		if(inputTable[address][0]):
			lableTable[inputTable[address][0]] = location_counter
			#print(lableTable)
		#print(inputTable[address][2])

		opcodeTable[location_counter] = [inputTable[address][1],opcodes[inputTable[address][1]],inputTable[address][2]]
		address +=1
		num -=1
		location_counter+=1

		#sys.exit("Success!")
	return

def readVariables(inputTable, address, memory):
	if(inputTable[address][0] not in symbolTable):
		print("WARNING: Variable is declared but not used in code.")
	symbolTable[inputTable[address][0]] = [inputTable[address][1],memory]


def secondPass():
	#print(symbolTable)
	#print(opcodeTable)

	for i in symbolTable.keys():
		if (symbolTable[i]==False):
			sys.exit("ERROR: "+i+" is used in program but value is not provided.")

	
	for i in opcodeTable.keys():
		
		if(len(opcodeTable[i])==3):
			ans.append(opcodeTable[i][1]+decimalToBinary(symbolTable[opcodeTable[i][2]][1]))
		else:
			ans.append(opcodeTable[i][1]+("0"*8))
		
	for i in ans:
		print(i)
	return 



def isSymbolValid(inputSymbol):
	ErrorFlag = False

	if(inputSymbol not in opcodes):
		ErrorFlag = True
		return ErrorFlag
		
	return ErrorFlag


def decimalToBinary(n): 
	#print(n)
	binary = bin(n).replace("0b", "")
	if (len(binary)==8):
		return binary
	return "0"*(8-len(binary))+binary





########################################MAIN CODE STARTS HERE#######################################

inputFlag = True
while(inputFlag):
	try:
		file = input("Enter name of the file: ")
		asmFile = open(file, 'r')
		(passOne(asmFile))
		#print(symbolTable)
		print(lableTable)
		print(symbolTable)
		print(opcodeTable)
		
		inputFlag = False
	except FileNotFoundError:
		print("No File Found, Kindly Retry")


#print(literals)

## VALID SYBOLS ##












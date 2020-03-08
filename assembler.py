import sys



############ TO DO##########33


#	HANDLE ASSEMBLER DIRECTIVES


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
global divVariables
divVariables = False


def passOne(file):
	global divVariables

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
	



	while(address<len(start)-1):


		inputTable[address] = list(map(lambda x:x.rstrip(),start[address+1].split("\t")))
		#print(inputTable[address])
		#print(len(inputTable[address]))
		#print(start[address+1])
		#print((inputTable[address]))

		#print(inputTable[address])

				

		if(len(inputTable[address])==2):
			if(inputTable[address][1]!="CLA" and inputTable[address][1]!="STP"):
				sys.exit("ERROR at line " + str(location_counter) +": Incorrect syntax of input. Check documentation.")
			if(inputTable[address][1]=="STP"):
				"""error if there's a label with STP"""
				if(inputTable[address][0]):
					sys.exit("ERROR at line "+str(location_counter)+": You cannot have a label with 'STP'.")

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
							if(divVariables):
								symbolTable["R1"] = ['0',location_counter]
								symbolTable["R2"] = ['0',location_counter+4]
							return 
						sys.exit("ERROR: Incorrect syntax of input.'END' expected at the end of program. Check documentation.")


					readVariables(inputTable, address, location_counter)					#	to read variables after STP
					address+=1
					location_counter+=4
			else:
				"""error if there's a label with CLA"""
				if(inputTable[address][0]):
					sys.exit("ERROR at line "+str(location_counter)+": You cannot have a label with 'CLA'.")

				opcodeTable[location_counter] = [inputTable[address][1],opcodes[inputTable[address][1]]]
				address+=1
				location_counter+=1
				continue



		if(len(inputTable[address])== 1):
			if("END" in inputTable[address][0]):
				"""if END is read, first pass is finished."""
				return 
			sys.exit("ERROR at line " + str(location_counter) +": Incorrect syntax of input. Check documentation.")


		if(isSymbolValid(inputTable[address][1])):
			""" Exit program if an invalid opcode is detected."""
			sys.exit("ERROR at line " + str(location_counter) +": Invalid assembly opcode '"+inputTable[address][1]+"'. Check documentation.")

		if(len(inputTable[address])==3):
			if(inputTable[address][1]=="BRZ" or inputTable[address][1]=="BRN" or inputTable[address][1]=="BRP"):
				
				if(inputTable[address][2] not in lableTable):
					sys.exit("ERROR at line "+str(location_counter)+" : Label not defined.")
				symbolTable[inputTable[address][2]] = lableTable[inputTable[address][2]]
				address+=1
				location_counter+=1
				continue

			#print(inputTable[address][1])
			#print(inputTable[address][1]=="DIV")

			if(inputTable[address][1]=="DIV"):
				divVariables= True

			isVariableValid(inputTable[address][2],location_counter)
			symbolTable[inputTable[address][2]] = False					# if variable is used but not declared



		if(inputTable[address][0]):
			if(inputTable[address][0] in lableTable):
				"""	error if a label is declared twice in code"""
				sys.exit("ERROR at line "+str(location_counter)+": Label '"+inputTable[address][0]+"' is already used. Cannot be used again. Check documentation and try again.")

			isLabelValid(inputTable[address][0],location_counter)
			lableTable[inputTable[address][0]] = location_counter		#	lable table as dictionary : keys are labels and their value is location counter

			#print(lableTable)
		#print(inputTable[address])
				


		opcodeTable[location_counter] = [inputTable[address][1],opcodes[inputTable[address][1]],inputTable[address][2]]
		address +=1
		location_counter+=1

		#sys.exit("Success!")
	return

def isVariableValid(variable,lc):
	global divVariables
	""" to check if variable is valid"""
	if(variable in opcodeTable or variable=="START" or variable=="END" or variable in opcodes.keys()):
		sys.exit("ERROR at line "+str(lc)+": '"+variable+"' is an invalid variable. Check documentation.")
	#print(divVariables)
	if(variable=="R1" or variable=="R2"):
		if(not divVariables):
			sys.exit("ERROR at line "+str(lc)+": '"+variable+"' is an invalid variable. Check documentation.")


def isLabelValid(label,lc):
	"""check if label is valid.
	error if label is same as opcode or assembly directive or same as a variable"""

	if (label in opcodes.keys() or label == "END" or label == "START" or label in symbolTable):
		sys.exit("ERROR at line "+str(lc)+": Invalid label "+label+" .Check documentation and try again.")
	

def readVariables(inputTable, address, memory):
	if(inputTable[address][0] not in symbolTable):
		print("WARNING: Variable is declared but not used in code.")
	if(len(inputTable[address])==1 or len(inputTable[address][1])==0):
		sys.exit("ERROR: Please provide value to the variable "+str(inputTable[address][0])+".")
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
	"""check if given opcode is valid"""
	ErrorFlag = False

	if(inputSymbol not in opcodes):
		ErrorFlag = True
		
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
		print()
		print(symbolTable)
		print()
		print(opcodeTable)
		print()
		secondPass()
		
		inputFlag = False
	except FileNotFoundError:
		print("No File Found, Kindly Retry")


#print(literals)

## VALID SYBOLS ##












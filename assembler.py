import sys
import time as t


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


		if(len(inputTable[address])>3):
			sys.exit("ERROR at line " + str(location_counter) +": Incorrect syntax of input. Check documentation.")
			#	error if more than one variable is used in one instruction

		if(len(inputTable[address])== 1):
			if("END" in inputTable[address][0]):
				"""if END is read, first pass is finished."""
				return 
			sys.exit("ERROR at line " + str(location_counter) +": Incorrect syntax of input. Check documentation.")


		if(len(inputTable[address])==2):
			if(inputTable[address][1]!="CLA" and inputTable[address][1]!="STP"):
				sys.exit("ERROR at line " + str(location_counter) +": Incorrect syntax of input. Check documentation.")


		if(inputTable[address][0]):
			if(inputTable[address][0] in lableTable):
				"""	error if a label is declared twice in code"""
				sys.exit("ERROR at line "+str(location_counter)+": Label '"+inputTable[address][0]+"' is already used. Cannot be used again. Check documentation and try again.")

			isLabelValid(inputTable[address][0],location_counter)
			lableTable[inputTable[address][0]] = location_counter		#	lable table as dictionary : keys are labels and their value is location counter




		if(len(inputTable[address])==2):
			if(inputTable[address][1]!="CLA" and inputTable[address][1]!="STP"):
				sys.exit("ERROR at line " + str(location_counter) +": Incorrect syntax of input. Check documentation.")



			if(inputTable[address][1]=="STP"):

				opcodeTable[location_counter] = [inputTable[address][1],opcodes[inputTable[address][1]]]
				address+=1
				location_counter+=1
				while(True):
					inputTable[address] = list(map(lambda x:x.rstrip(),start[address+1].split("\t")))
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

				opcodeTable[location_counter] = [inputTable[address][1],opcodes[inputTable[address][1]]]
				address+=1
				location_counter+=1
				continue




		if(isSymbolValid(inputTable[address][1])):
			""" Exit program if an invalid opcode is detected."""
			sys.exit("ERROR at line " + str(location_counter) +": Invalid assembly opcode '"+inputTable[address][1]+"'. Check documentation.")

		if(len(inputTable[address])==3):


			"""	error if variable is used with CLA/STP"""
			if(inputTable[address][1]=="CLA"):
				sys.exit("ERROR at line "+str(location_counter)+" : You cannot have a variable with CLA.")
			if(inputTable[address][1]=="STP"):
				sys.exit("ERROR at line "+str(location_counter)+" : You cannot have a variable with STP.")



			if(inputTable[address][1]=="BRZ" or inputTable[address][1]=="BRN" or inputTable[address][1]=="BRP"):
				
				if(inputTable[address][2] not in lableTable):
					symbolTable[inputTable[address][2]] = "label"
					#sys.exit("ERROR at line "+str(location_counter)+" : Label not defined.")
				else:
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

				

		if(len(inputTable[address][2])==0):
			sys.exit("ERROR at line "+str(location_counter)+" : Incorrect syntax of input. Check documentation.")
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
	if(label in symbolTable and symbolTable[label]=="label"):
		symbolTable[label] = lc
		return

	if (label in opcodes.keys() or label == "END" or label == "START" or label in symbolTable):
		sys.exit("ERROR at line "+str(lc)+": Invalid label "+label+" .Check documentation and try again.")
	

def readVariables(inputTable, address, memory):
	if(inputTable[address][0] not in symbolTable):
		print("WARNING: Variable '"+inputTable[address][0]+"' is declared but not used in code.")
	if(len(inputTable[address])==1 or len(inputTable[address][1])==0):
		sys.exit("ERROR: Please provide value to the variable "+str(inputTable[address][0])+".")
	symbolTable[inputTable[address][0]] = [inputTable[address][1],memory]




def isSymbolValid(inputSymbol):
	"""check if given opcode is valid"""
	ErrorFlag = False

	if(inputSymbol not in opcodes):
		ErrorFlag = True
		
	return ErrorFlag


def decimalToBinary(n): 
	ans = ""
	if(n>1):
		ans += decimalToBinary(n//2)
	ans += str(n%2)
	return ans


def printDict(dictionary):
	for i in dictionary.keys():
		if(dictionary[i]==False):
			continue
		if(type(dictionary[i])==list):
			print(str(i)+" : ",end="")
			for i in dictionary[i]:
				print(i,end=" ; ")
			print()
			continue

		print(str(i)+" : "+str(dictionary[i]))
	print()



def secondPass():
	#print(symbolTable)
	#print(opcodeTable)

	for i in symbolTable.keys():
		if (symbolTable[i]==False):
			sys.exit("ERROR: "+i+" is used in program but value is not provided.")
		elif (symbolTable[i]=="label"):
			sys.exit("ERROR: label '"+i+"' is used but not defined.")

	
	for i in opcodeTable.keys():
		
		if(len(opcodeTable[i])==3):
			objAddress = decimalToBinary(symbolTable[opcodeTable[i][2]][1])
			objAddress = "0"*(8-len(objAddress)) + objAddress
			ans.append(opcodeTable[i][1]+ objAddress)
		else:
			""" in case of CLA and STP"""
			ans.append(opcodeTable[i][1]+("0"*8))


	print("OBJECT CODE")	
	for i in ans:
		""" print object code"""
		print(i)
	return


def printCool(toPrint):
	for i in toPrint:
		print(i,end="")
		t.sleep(0.05)
		sys.stdout.flush()
	for i in range(4):
		t.sleep(0.5)
		print(".",end=" ")
		sys.stdout.flush()
	print()



########################################MAIN CODE STARTS HERE#######################################

inputFlag = True
while(inputFlag):
	try:
		file = input("Enter name of the file: ")
		asmFile = open(file, 'r')
		print()
		printCool("Initialising assembler")
		
		#print(symbolTable)
		print("GIVEN OPCODES")
		printDict(opcodes)
		printCool("Initialising first pass")
		(passOne(asmFile))
		print("LABEL TABLE")
		printDict(lableTable)
		#print(lableTable)
		print("SYMBOL TABLE")
		printDict(symbolTable)
		#print(symbolTable)
		print("OPCODE TABLE")
		printDict(opcodeTable)
		#print(opcodeTable)
		#print()
		print()
		printCool("Initialising second pass")
		
		secondPass()
		
		inputFlag = False
	except FileNotFoundError:
		print("No File Found, Kindly Retry")


#print(literals)

## VALID SYBOLS ##












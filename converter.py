#7/8/2016
#Author: Chandler Moeller
#Python Program to do converions between integers and binary
#Also added functionality to do subnet calculations

def converter():
	print("Welcome to converter")
	print("This program does simple binary/integer/factorial/subnet calculations")
	type = raw_input("Functions:\n	(B)inary to integer\n	(I)nteger to binary\n	(F)actorial Calculator\n	(S)ubnet Calculator\n	(E)xit\n")
	if type.upper() == "B":
		print("Integer: %s" %(BinaryInput()))
	elif type.upper() == "I":
		print("Binary: %s" %(IntegerInput()))
	elif type.upper() == "F":
		print(FactorialInput())
	elif type.upper() == "S":
		SubnetInput()
	elif type.upper() == "E":
		quit()
	elif type.upper() == "T":
		Test()
	else:
		print_error("Not a valid command", "please enter either 'B', 'I', 'F', 'S', or 'E'")
		converter()

def print_error(err_id, err_msg):
	print ("Error: %s: %s" %(err_id, err_msg))

def print_test(str):
	print ("Test: %s" %(str))

def BinaryInput():
	#Level 1
	userinput = raw_input("Please enter your binary number to convert\n")
	output = BinaryInputConversion(userinput)
	if output is "bad":
		BinaryInput()
	else:
		return output

def BinaryInputConversion(userinput):
	try:
		output = 0
		exponent = 0
		iter = len(userinput)-1
		while iter >= 0:
			number = userinput[iter]
			#check to make sure that the number is either a 0 or 1
			if (number is not "1") and (number is not "0") and (number is not ".") and (number is not " "):
				print_error("Number is not a 1, 0, '.', or ' '", "You must enter a binary number")
				return "bad"
			if (number is not ".") and (number is not " "):
				output = output + int(number)*(2**exponent)
				exponent += 1
			iter -= 1
		return output
	except ValueError:
		print_error("ValueError", "You must enter a binary number")
		return "bad"

def IntegerInput():
	#Level 1
	userinput = raw_input("Please enter your integer number to convert\n")
	try:
		#Used to ensure that the userinput is an integer
		int(userinput)
		return IntegerInputRecurse("", userinput)
	except ValueError:
		print_error("ValueError", "You must enter an integer number")
		IntegerInput()

def IntegerInputRecurse(binary, integer):
	integer = int(integer)
	remainder = str(integer%2)
	binary = remainder + binary
	nextnumber = integer/2
	if nextnumber == 0:
		return binary
	else:
		return IntegerInputRecurse(binary, integer/2)

def FactorialInput():
	#Level 1
	userinput = raw_input("Please enter a factorial\n")
	it = int(userinput)-1
	while it > 0:
		userinput = int(userinput)*it
		it = it - 1
	return userinput

def SubnetInput():
	#Level 1
	IPV4input = raw_input("Please enter your IPV4 for classful subnets (x.x.x.x)\nOR with optional CIDR for classless subnets(x.x.x.x/x)\n")
	IPV4input = IPV4input.strip()
	Maskinput = ""
	if "/" in IPV4input:
		array = [x.strip() for x in IPV4input.split("/")]
		if len(array) is not 2:
			print_error("len(array) is not 2", "You must enter a valid IPV4")
			SubnetInput()
		else:
			#CLASSLESS
			#input has a valid CIDR format
			array[0] = ValidateIPV4(array[0])
			if array[0] is "bad":
				return "bad"
			IPV4input = ""
			for element in array[0]:
				IPV4input = IPV4input + element
			#Convert to CIDR Netmask
			#TODO: add CIDR netmask input functionality
			Maskinput = int(array[1])*"1"
			Maskinput = Maskinput + (32-int(array[1]))*"0"
			SubnetCalculation(IPV4input, Maskinput)

	else:
		#CLASSFUL
		#needs subnet mask
		IPV4inputbroken = ValidateIPV4(IPV4input)
		if IPV4inputbroken is "bad":
			return "bad"
		IPV4input = ""
		for element in IPV4inputbroken:
			IPV4input = IPV4input + element
		Maskinput = raw_input("Please enter your Subnet Mask (xxx.xxx.xxx.xxx)\n")
		Maskinputbroken = ValidateIPV4(Maskinput)
		if Maskinputbroken is "bad":
			return "bad"
		Maskinput = ""
		for element in Maskinputbroken:
			Maskinput = Maskinput + element
		SubnetCalculation(IPV4input, Maskinput)

	
def ValidateIPV4(userinput):
	#Checks to make sure userinput is a valid IPV4
	#Outputs Binary IPV4 if the inupt is valid
	isvalidbinary = True
	isvalidinteger = True
	BrokenIPV4 = []
	if "." in userinput:
		BrokenIPV4 = [x.strip() for x in userinput.split(".")]
		if len(BrokenIPV4) is not 4:
			#There are not 3 periods
			print_error("There are not 3 periods", "You must enter a valid IPV4")
			return "bad"
		else:
			#There are 3 periods
			for elementchange, element in enumerate(BrokenIPV4):
				if len(element) is 8:
					#check if binary
					isvalidinteger = False
					iter = len(element)-1
					while iter >= 0:
						number = element[iter]
						if (number is not "1") and (number is not "0"):
							isvalidbinary = False
						iter =- 1
				elif 0 <= int(element) <= 255:
					#byte is valid integer
					isvalidbinary = False
					#convert to binary
					element = IntegerInputRecurse("", int(element))
					while len(element) < 8:
						element = "0%s" %(element)
					BrokenIPV4[elementchange] = element
				else:
					isvalidbinary = False
					isvalidinteger = False
	if ((isvalidinteger is False) and (isvalidbinary is True)) or ((isvalidinteger is True) and (isvalidbinary is False)):
		#This is a valid Bianry IPV4
		return BrokenIPV4
	else:
		print_error("TrueTrue or FalseFalse", "You must enter a valid IPV4")
		return "bad"

def SubnetCalculation(IPV4input, Maskinput):
	subnets = 0
	hosts = 0

	#Find amount of hosts
	NumberofTrailingZeroesinMaskinput = FindNumberofTrailingZeroesinIPV4(Maskinput)
	hosts = (2 ** NumberofTrailingZeroesinMaskinput)

	print ("The maximum number of hosts is %d" %(hosts-2))

	#Find amount of subnets
	subnet_amountofone = len(IPV4input) - 1
	bit = IPV4input[subnet_amountofone]
	while ((bit is not "1") and (subnet_amountofone>0)):
		subnet_amountofone -= 1
		bit = IPV4input[subnet_amountofone]
	subnet_amountofone = subnet_amountofone + 1
	subnet_amountoftrailingzero = 32 - subnet_amountofone

def FindNumberofTrailingZeroesinIPV4(IPV4input):
	amountofone = len(IPV4input) - 1
	bit = IPV4input[amountofone]
	while ((bit is not "1") and (amountofone>0)):
		amountofone -= 1
		bit = IPV4input[amountofone]
	amountofone = amountofone + 1
	numberoftrailingzeroes = 32 - amountofone
	return numberoftrailingzeroes

def Test():
	userinput = raw_input("Please enter a factorial\n")
	test = int(userinput) << 2
	print(bin(test))

#infinite loop, why would anyone want to leave?
while 0 != 1:
	converter()
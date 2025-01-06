import re

testRequisites = [
	#don't work:
	#"PHM PRAC 656 or concurrent enrollment",
	#"Nursing BSN (Traditional, Accelerated or Collaborative), senior standing and declared in Health Promotion and Health Equity BS, or graduate/professional standing",
	#"(ACCT I S 340 or concurrent enrollment), (ACCT I S 100 and GEN BUS 307 or 317), (ACCT I S 700 or concurrent enrollment), or declared in the Business Exchange program",
	#"(CHEM 103, 109, or 115) and (MATH 112, 114, 171 or placement into MATH 221), or graduate/professional standing"
	
	#work:
	#"MATH 96 or placement into MATH 112 or satisfied Quantitative Reasoning (QR) A requirement. Not open to students with credit for ECON 101, 102, or 111"
	#"Not open to students declared in the Nursing, Physician Assistant, or Doctor of Pharmacy programs",
	#"PHM PRAC 554, 556 and PHMCOL-M/PHM SCI  522",
	#"PHM PRAC 550, 555, 556, and 655",
	#"PHM PRAC 653, 655 and PHM SCI 623",
	#"Declared in Doctor of Pharmacy program with second year standing",
	#"Declared in MS Pharmaceutical Sciences: Psychoactive Pharmaceutical Investigation or Capstone Certificate in Psychoactive Pharmaceutical Investigation",
	#"PHM PRAC 655 or (NURSING 312 and NURSING 422)",
]
"""
things that don't work:
when there is an operator right after () in a list
current enrolment
lists where they arent classes (just need to figure out how to get rid of them)
"""


operators = [" or ", " and ", "("]

def getFirstOperator(requisiteString, operators):
	firstOperator = None
	firstOperatorIndex = None
	
	for operator in operators:
		#get index
		operatorIndex = requisiteString.find(operator)
		
		if operatorIndex != -1:
			#assign if first
			if firstOperatorIndex == None or firstOperatorIndex > operatorIndex:
				firstOperator = operator
				firstOperatorIndex = operatorIndex
				
	return firstOperator

def splitByParenthesis(string):
	firstIndex = string.find("(")
	secondIndex = string.find(")")
	
	thing = [string[:firstIndex], string[firstIndex + 1:secondIndex], string[secondIndex + 1:]]
	
	return [x for x in thing if x != '']

def findNumberIndex(string):
	match = re.search(r'\d', string)
	if match:
		return match.start()
	return -1  # Return -1 if no number is found

#takes string such as "COMP SCI 100, 200, and 300" and converts to 
def combinedCoursesToList(combinedCourse):
	#not a list
	if combinedCourse.find(",") == -1:
		print(combinedCourse)
		return combinedCourse
	
	finalCourseList = []
	
	firstNumberIndex = findNumberIndex(combinedCourse)
	
	#get the course catagory
	courseCatagory = combinedCourse[0:firstNumberIndex - 1]
	
	#get the operator: if it is "course 1 and course 2" or "course 1 or course 2"
	operator = getFirstOperator(combinedCourse, ["and", "or"])
	
	if operator:
		#get rid of operator
		combinedCourse = combinedCourse.replace(operator, "")
	
	#get rid of course catagory
	combinedCourse = combinedCourse.replace(courseCatagory, "")
	
	#split by commas
	finalCourseList = combinedCourse.split(",")
	
	#add course catagory
	finalCourseList = [courseCatagory + x for x in finalCourseList]
	
	if operator:
		#add operator
		finalCourseList.append(" " + operator + " ")
	
	
	return finalCourseList

def splitByCommas(requisites):
	finalRequisites = []
	
	if isinstance(requisites, list):
		for requisite in requisites:
			splitClasses = splitByCommas(requisite)
			if (" and " in splitClasses or " or " in splitClasses) and len(splitClasses) != 1: #includes an operator and isnt just an operator
				finalRequisites.append(splitClasses)
			else:
				finalRequisites.extend(splitClasses)
				
	elif "," in requisites:
		finalRequisites = combinedCoursesToList(requisites)
		#print(f"{requisites}   -->   {finalRequisites}")
	else:
		finalRequisites = [requisites]
		
	return finalRequisites
		

#takes string, returns list of requisites (through the layers)
def splitByOperators(requisites, operators):
	requisites = requisites.strip()
	requisiteList = []
	
	#get first operator
	firstOperator = getFirstOperator(requisites, operators)
	
	#no layers left
	if firstOperator == None:
		requisiteList.append(requisites.replace(")", ""))
	#more layers
	else:
		#split
		if firstOperator == "(":
			requisitesSplit = splitByParenthesis(requisites)
		else:
			requisitesSplit = requisites.split(firstOperator)
			requisitesSplit = [x for x in requisitesSplit if x != ''] #get rid of blanks
			
			requisiteList.append(firstOperator)
			
		#print(f"{firstOperator}: {requisites} -> {requisitesSplit}")
		
		#go to next layer
		for requisite in requisitesSplit:
			if requisite not in operators:
				
				nextLayer = splitByOperators(requisite, operators)
				
				#get rid of layers that have only one element
				if len(nextLayer) == 1:
					requisiteList.extend(nextLayer)
				else:
					requisiteList.append(nextLayer)
			
	return requisiteList

def seperateProhibited(requisites):
	#going off of assumptions (from looking at the data):
	#always the last part of a requisite string, so you can just split it
	#also always "Not" (note the capital N)
	
	splitRequisites = requisites.split("Not")
	
	#no prohibited
	if len(splitRequisites) == 1:
		return requisites, None
	#prohibited
	elif len(splitRequisites) == 2:
		return splitRequisites[0], "Not" + splitRequisites[1]
	#idk
	else:
		print("OH NO!!!!!!!!!!!!!") #I need sleep
		return None, None
		

def parseRequisites(requisiteString, operators):
	#seperate prohibited
	requisiteString, prohibited = seperateProhibited(requisiteString)
	
	#get rid of space in between comma and operator. makes them not get seperated initially
	for operator in ["and ", "or "]:
		requisiteString = requisiteString.replace(", " + operator, "," + operator)
	
	requisites = splitByOperators(requisiteString, operators)
	
	print("After seperating by operators: " + str(requisites) + "\n")
	requisites = splitByCommas(requisites)
	
	return requisites, prohibited

for requisiteString in testRequisites:
	print(f"\nStart: {requisiteString}\n")
	requisites, prohibited = parseRequisites(requisiteString, operators)
	print(f"Requisites: {requisites}")
	print(f"Prohibited: {prohibited}")
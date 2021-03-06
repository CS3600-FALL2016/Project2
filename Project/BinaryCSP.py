from collections import deque

"""
	Base class for unary constraints
	Implement isSatisfied in subclass to use
"""
class UnaryConstraint:
	def __init__(self, var):
		self.var = var

	def isSatisfied(self, value):
		util.raiseNotDefined()

	def affects(self, var):
		return var == self.var


"""	
	Implementation of UnaryConstraint
	Satisfied if value does not match passed in paramater
"""
class BadValueConstraint(UnaryConstraint):
	def __init__(self, var, badValue):
		self.var = var
		self.badValue = badValue

	def isSatisfied(self, value):
		return not value == self.badValue

	def __repr__(self):
		return 'BadValueConstraint (%s) {badValue: %s}' % (str(self.var), str(self.badValue))


"""	
	Implementation of UnaryConstraint
	Satisfied if value matches passed in paramater
"""
class GoodValueConstraint(UnaryConstraint):
	def __init__(self, var, goodValue):
		self.var = var
		self.goodValue = goodValue

	def isSatisfied(self, value):
		return value == self.goodValue

	def __repr__(self):
		return 'GoodValueConstraint (%s) {goodValue: %s}' % (str(self.var), str(self.goodValue))


"""
	Base class for binary constraints
	Implement isSatisfied in subclass to use
"""
class BinaryConstraint:
	def __init__(self, var1, var2):
		self.var1 = var1
		self.var2 = var2

	def isSatisfied(self, value1, value2):
		util.raiseNotDefined()

	def affects(self, var):
		return var == self.var1 or var == self.var2

	def otherVariable(self, var):
		if var == self.var1:
			return self.var2
		return self.var1


"""
	Implementation of BinaryConstraint
	Satisfied if both values assigned are different
"""
class NotEqualConstraint(BinaryConstraint):
	def isSatisfied(self, value1, value2):
		if value1 == value2:
			return False
		return True

	def __repr__(self):
		return 'NotEqualConstraint (%s, %s)' % (str(self.var1), str(self.var2))


class ConstraintSatisfactionProblem:
	"""
	Structure of a constraint satisfaction problem.
	Variables and domains should be lists of equal length that have the same order.
	varDomains is a dictionary mapping variables to possible domains.

	Args:
		variables (list<string>): a list of variable names
		domains (list<set<value>>): a list of sets of domains for each variable
		binaryConstraints (list<BinaryConstraint>): a list of binary constraints to satisfy
		unaryConstraints (list<BinaryConstraint>): a list of unary constraints to satisfy
	"""
	def __init__(self, variables, domains, binaryConstraints = [], unaryConstraints = []):
		self.varDomains = {}
		for i in xrange(len(variables)):
			self.varDomains[variables[i]] = domains[i]
		self.binaryConstraints = binaryConstraints
		self.unaryConstraints = unaryConstraints

	def __repr__(self):
		return '---Variable Domains\n%s---Binary Constraints\n%s---Unary Constraints\n%s' % ( \
			''.join([str(e) + ':' + str(self.varDomains[e]) + '\n' for e in self.varDomains]), \
			''.join([str(e) + '\n' for e in self.binaryConstraints]), \
			''.join([str(e) + '\n' for e in self.binaryConstraints]))


class Assignment:
	"""
	Representation of a partial assignment.
	Has the same varDomains dictionary stucture as ConstraintSatisfactionProblem.
	Keeps a second dictionary from variables to assigned values, with None being no assignment.

	Args:
		csp (ConstraintSatisfactionProblem): the problem definition for this assignment
	"""
	def __init__(self, csp):
		self.varDomains = {}
		for var in csp.varDomains:
			self.varDomains[var] = set(csp.varDomains[var])
		self.assignedValues = { var: None for var in self.varDomains }

	"""
	Determines whether this variable has been assigned.

	Args:
		var (string): the variable to be checked if assigned
	Returns:
		boolean
		True if var is assigned, False otherwise
	"""
	def isAssigned(self, var):
		return self.assignedValues[var] != None

	"""
	Determines whether this problem has all variables assigned.

	Returns:
		boolean
		True if assignment is complete, False otherwise
	"""
	def isComplete(self):
		for var in self.assignedValues:
			if not self.isAssigned(var):
				return False
		return True

	"""
	Gets the solution in the form of a dictionary.

	Returns:
		dictionary<string, value>
		A map from variables to their assigned values. None if not complete.
	"""
	def extractSolution(self):
		if not self.isComplete():
			return None
		return self.assignedValues

	def __repr__(self):
		return '---Variable Domains\n%s---Assigned Values\n%s' % ( \
			''.join([str(e) + ':' + str(self.varDomains[e]) + '\n' for e in self.varDomains]), \
			''.join([str(e) + ':' + str(self.assignedValues[e]) + '\n' for e in self.assignedValues]))



####################################################################################################


"""
	Checks if a value assigned to a variable is consistent with all binary constraints in a problem.
	Do not assign value to var. Only check if this value would be consistent or not.
	If the other variable for a constraint is not assigned, then the new value is consistent with the constraint.

	Args:
		assignment (Assignment): the partial assignment
		csp (ConstraintSatisfactionProblem): the problem definition
		var (string): the variable that would be assigned
		value (value): the value that would be assigned to the variable
	Returns:
		boolean
		True if the value would be consistent with all currently assigned values, False otherwise
"""
def consistent(assignment, csp, var, value):
	"""Question 1"""
	"""YOUR CODE HERE"""
	for cst in csp.binaryConstraints:
		if cst.affects(var) and (value == assignment.assignedValues[cst.otherVariable(var)]):
			return False
	return True


"""
	Recursive backtracking algorithm.
	A new assignment should not be created. The assignment passed in should have its domains updated with inferences.
	In the case that a recursive call returns failure or a variable assignment is incorrect, the inferences made along
	the way should be reversed. See maintainArcConsistency and forwardChecking for the format of inferences.

	Examples of the functions to be passed in:
	orderValuesMethod: orderValues, leastConstrainingValuesHeuristic
	selectVariableMethod: chooseFirstVariable, minimumRemainingValuesHeuristic

	Args:
		assignment (Assignment): a partial assignment to expand upon
		csp (ConstraintSatisfactionProblem): the problem definition
		orderValuesMethod (function<assignment, csp, variable> returns list<value>): a function to decide the next value to try
		selectVariableMethod (function<assignment, csp> returns variable): a function to decide which variable to assign next
	Returns:
		Assignment
		A completed and consistent assignment. None if no solution exists.
"""
def recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod):
	"""Question 1"""

	"""YOUR CODE HERE"""

	#if assigment is complete then return assignment
	if assignment.isComplete():
		return assignment
	# Select unassigned variable
	var = selectVariableMethod(assignment, csp)
	#continue until var is empty(all variable are assigned)
	if not var is None:
		#for each value in O-D-V Do
		for value in orderValuesMethod(assignment, csp, var):
			#if value is consistent with assignment then
			if consistent(assignment, csp, var, value):
				#add {var = value} to assignment
				assignment.assignedValues[var] = value
				result = recursiveBacktracking(assignment,csp, orderValuesMethod, selectVariableMethod)
				if not result is None:
					return result
				assignment.assignedValues[var] = None
		return None


"""
	Uses unary constraints to eleminate values from an assignment.

	Args:
		assignment (Assignment): a partial assignment to expand upon
		csp (ConstraintSatisfactionProblem): the problem definition
	Returns:
		Assignment
		An assignment with domains restricted by unary constraints. None if no solution exists.
"""
def eliminateUnaryConstraints(assignment, csp):
	domains = assignment.varDomains
	for var in domains:
		for constraint in (c for c in csp.unaryConstraints if c.affects(var)):
			for value in (v for v in list(domains[var]) if not constraint.isSatisfied(v)):
				domains[var].remove(value)
				if len(domains[var]) == 0:
					# Failure due to invalid assignment
					return None
	return assignment


"""
	Trivial method for choosing the next variable to assign.
	Uses no heuristics.
"""
def chooseFirstVariable(assignment, csp):
	for var in csp.varDomains:
		if not assignment.isAssigned(var):
			return var


"""
	Selects the next variable to try to give a value to in an assignment.
	Uses minimum remaining values heuristic to pick a variable. Use degree heuristic for breaking ties.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
	Returns:
		the next variable to assign
"""
def minimumRemainingValuesHeuristic(assignment, csp):
	nextVar = None
	domains = assignment.varDomains
	"""Question 2"""
	#Choose variable with fewest legal values
	#To break ties, choose variable with most constraints on remaining variables
	minLegal = -1
	listOfVars = []
	#First look for what variable has the fewest legal values, make sure to keep track if there are ties.
	var = domains.keys()
	for i in range(0, len(var)):
		#Check to see if it hasnt been assigned
		if assignment.assignedValues[var[i]] == None:
			#then see if its the min
			if minLegal > len(domains[var[i]]) or minLegal < 0:
				#initialize a list of variables with the minLegal values
				#clear the previous list
				listOfVars = []
				#new minimum
				minLegal = len(domains[var[i]])
				#add the variable to the minimum
				listOfVars.append(var[i])
			elif minLegal == len(domains[var[i]]):
				#If the length is the same (tie)
				listOfVars.append(var[i])
	#You finished with the first check. now check for ties
	if (len(listOfVars) == 0):
		return nextVar
	elif (len(listOfVars) == 1):
		#Theres only 1 min, no ties
		return listOfVars[0]
	else:
		#theres tie's. use heuristic to break them
		#Choose variable with most constraints on remaining variables
		maxConstraint = 0
		for var in listOfVars:
			constCount = 0
			if len(csp.binaryConstraints) == 0:
				return listOfVars[0]
			for const in csp.binaryConstraints:
				if const.affects(var):
					constCount += 1
			if maxConstraint < constCount:
					maxConstraint = constCount
					nextVar = var

	return nextVar


"""
	Trivial method for ordering values to assign.
	Uses no heuristics.
"""
def orderValues(assignment, csp, var):
	return list(assignment.varDomains[var])


"""
	Creates an ordered list of the remaining values left for a given variable.
	Values should be attempted in the order returned.
	The least constraining value should be at the front of the list.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var (string): the variable to be assigned the values
	Returns:
		list<values>
		a list of the possible values ordered by the least constraining value heuristic
"""
def leastConstrainingValuesHeuristic(assignment, csp, var):
	values = list(assignment.varDomains[var])
	"""Hint: Creating a helper function to count the number of constrained values might be useful"""
	"""Question 3"""
	varAffected = []
	valWithCost = []
	#First see what variables are affected
	for const in csp.binaryConstraints:
		if const.affects(var):
			varAffected.append(const.otherVariable(var))
	for val in values:
		constCount = 0
		for v in varAffected:
			if(val in list(assignment.varDomains[v])):
				constCount += 1
		valWithCost.append((val, constCount))
	valWithCost = sorted(valWithCost, key=lambda t: t[1])
	varAffected = []
	for val in valWithCost:
		varAffected.append(val[0])
	return varAffected


"""
	Trivial method for making no inferences.
"""
def noInferences(assignment, csp, var, value):
	return set([])


"""
	Implements the forward checking algorithm.
	Each inference should take the form of (variable, value) where the value is being removed from the
	domain of variable. This format is important so that the inferences can be reversed if they
	result in a conflicting partial assignment. If the algorithm reveals an inconsistency, any
	inferences made should be reversed before ending the fuction.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var (string): the variable that has just been assigned a value
		value (string): the value that has just been assigned
	Returns:
		set<tuple<variable, value>>
		the inferences made in this call or None if inconsistent assignment
"""
def forwardChecking(assignment, csp, var, value):
	inferences = set([])
	domains = assignment.varDomains
	"""Question 4"""
	"""YOUR CODE HERE"""
	#value is assigned, all variables connected to the variable by a binary constraint
	#are considered. If value in thos evariables is inconsistent with that constraint and the
	#newly assigned value then inconistent value is removed.

	# for each unassigned variable V that is connected to X by a constraint, delete from V's domain any value that is inconsistent with the value chosen for X.
	for const in csp.binaryConstraints:
		#check if constrainst affects variable and is not assigned
		if const.affects(var) and assignment.assignedValues[const.otherVariable(var)] is None:
			varConnect = const.otherVariable(var)
			if value in list(domains[varConnect]):
				if len(list(domains[varConnect])) != 1:
					#remove V from the domain
					domains[varConnect].remove(value)
					inferences.add((varConnect,value))
				elif len(assignment.varDomains[varConnect]) == 1:
					for var, val in inferences:
						assignment.varDomains[var].add(val)
					return None
	return inferences

"""
	Recursive backtracking algorithm.
	A new assignment should not be created. The assignment passed in should have its domains updated with inferences.

	In the case that a recursive call returns failure or a variable assignment is incorrect, the inferences made along
	the way should be reversed. See maintainArcConsistency and forwardChecking for the format of inferences.


	Examples of the functions to be passed in:
	orderValuesMethod: orderValues, leastConstrainingValuesHeuristic
	selectVariableMethod: chooseFirstVariable, minimumRemainingValuesHeuristic
	inferenceMethod: noInferences, maintainArcConsistency, forwardChecking


	Args:
		assignment (Assignment): a partial assignment to expand upon
		csp (ConstraintSatisfactionProblem): the problem definition
		orderValuesMethod (function<assignment, csp, variable> returns list<value>): a function to decide the next value to try
		selectVariableMethod (function<assignment, csp> returns variable): a function to decide which variable to assign next
		inferenceMethod (function<assignment, csp, variable, value> returns set<variable, value>): a function to specify what type of inferences to use
				Can be forwardChecking or maintainArcConsistency
	Returns:
		Assignment

		A completed and consistent assignment. None if no solution exists.
"""
def recursiveBacktrackingWithInferences(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod):
	"""Question 4"""
	"""YOUR CODE HERE"""
	#if assigment is complete then return assignment
	if assignment.isComplete():
		return assignment
	# Select unassigned variable
	var = selectVariableMethod(assignment, csp)
	#continue until var is empty(all variable are assigned)
	if not var is None:
		#for each value in O-D-V Do
		for value in orderValuesMethod(assignment, csp, var):
			#if value is consistent with assignment then
			if consistent(assignment, csp, var, value):
				#add {var = value} to assignment
				inferences = inferenceMethod(assignment, csp, var, value)
				if inferences is not None:
					assignment.assignedValues[var] = value
					result = recursiveBacktrackingWithInferences(assignment,csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
					if not result is None:
						return result
					else:
						for varia, valu in inferences:
							assignment.varDomains[varia].add(valu)
				assignment.assignedValues[var] = None
		return None



"""
	Helper funciton to maintainArcConsistency and AC3.
	Remove values from var2 domain if constraint cannot be satisfied.
	Each inference should take the form of (variable, value) where the value is being removed from the
	domain of variable. This format is important so that the inferences can be reversed if they
	result in a conflicting partial assignment. If the algorithm reveals an inconsistency, any
	inferences made should be reversed before ending the fuction.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var1 (string): the variable with consistent values
		var2 (string): the variable that should have inconsistent values removed
		constraint (BinaryConstraint): the constraint connecting var1 and var2
	Returns:
		set<tuple<variable, value>>
		the inferences made in this call or None if inconsistent assignment
"""
def revise(assignment, csp, var1, var2, constraint):
	inferences = set([])
	"""Question 5"""
	"""YOUR CODE HERE"""
	#returns true iff we revise the domain of var1
	#for each x in D, do
	#if no value y in Dj, allows(r,y) to satisfy the constraint between X and Xj, then
	#delete x from D,
	#revised = true
	revised = False
	domainV1 = list(assignment.varDomains[var1])
	domainV2 = list(assignment.varDomains[var2])
	i = 0
	if constraint.affects(var1) and constraint.affects(var2):
		for val2 in domainV2:
			revised = False
			for val1 in domainV1:
				revised = revised or constraint.isSatisfied(val1, val2)
			if not revised:
				i += 1
				inferences.add((var2, val2))
				# domainV1.remove(val2)
			if i == len(domainV2):
				return None
		for inference in inferences:
			assignment.varDomains[inference[0]].remove(inference[1])
	return inferences


"""
	Implements the maintaining arc consistency algorithm.
	Inferences take the form of (variable, value) where the value is being removed from the
	domain of variable. This format is important so that the inferences can be reversed if they
	result in a conflicting partial assignment. If the algorithm reveals an inconsistency, and
	inferences made should be reversed before ending the fuction.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
		var (string): the variable that has just been assigned a value
		value (string): the value that has just been assigned
	Returns:
		set<<variable, value>>
		the inferences made in this call or None if inconsistent assignment
"""
#from Queue import *
def maintainArcConsistency(assignment, csp, var, value):
	inferences = set([])
	# """Hint: implement revise first and use it as a helper function"""
	# """Question 5"""
	# """YOUR CODE HERE"""
	# #local variables, a queue, queue of arcs
	# #while queue is not empty
	# #(Xi, Xj) removeFirst(queue)
	# check if poped is affected by any constraint and add it to the q
	# #if size of Di=0 then return false
	# #for each Xi in X.Neighbors do

	# #add (Xk, Xi) to queue
	# #return true
	q = deque()
	for const in csp.binaryConstraints:
		if const.affects(var):
			q.append(( var, const.otherVariable(var), const))
	while len(q) != 0:
		var, nextVar, constraint = q.pop()
		xtraInfer = revise(assignment, csp, var, nextVar, constraint)
		if xtraInfer is not None:
			#then just check normal inferences
			if len(xtraInfer) > 0:
				inferences = inferences.union(xtraInfer)
				for const in csp.binaryConstraints:
					if const.affects(nextVar):
						q.append((nextVar, const.otherVariable(nextVar), const))
		else:
			for var, val in inferences:
				assignment.varDomains[var].add(val)
			return None
	return inferences



"""
	AC3 algorithm for constraint propogation. Used as a preprocessing step to reduce the problem
	before running recursive backtracking.

	Args:
		assignment (Assignment): the partial assignment to expand
		csp (ConstraintSatisfactionProblem): the problem description
	Returns:
		Assignment
		the updated assignment after inferences are made or None if an inconsistent assignment
"""
def AC3(assignment, csp):
	inferences = set([])
	"""Hint: implement revise first and use it as a helper function"""
	"""Question 6"""
	"""YOUR CODE HERE"""
	#Same as MAC Except add all variables, then its the same aS MAC
	q = deque()
	for const in csp.binaryConstraints:
		for var in csp.varDomains:
			if const.affects(var):
				q.append((var, const.otherVariable(var), const))
	while len(q) != 0:
		var, nextVar, constraint = q.pop()
		xtraInfer = revise(assignment, csp, var, nextVar, constraint)
		if xtraInfer is not None:
			#then just check normal inferences
			if len(xtraInfer) > 0:
				inferences = inferences.union(xtraInfer)
				for const in csp.binaryConstraints:
					if const.affects(nextVar):
						q.append((nextVar, const.otherVariable(nextVar), const))
		else:
			for var, val in inferences:
				assignment.varDomains[var].add(val)
			return None
	return assignment


"""
	Solves a binary constraint satisfaction problem.

	Args:
		csp (ConstraintSatisfactionProblem): a CSP to be solved
		orderValuesMethod (function): a function to decide the next value to try
		selectVariableMethod (function): a function to decide which variable to assign next
		inferenceMethod (function): a function to specify what type of inferences to use
		useAC3 (boolean): specifies whether to use the AC3 preprocessing step or not
	Returns:
		dictionary<string, value>
		A map from variables to their assigned values. None if no solution exists.
"""
def solve(csp, orderValuesMethod=leastConstrainingValuesHeuristic, selectVariableMethod=minimumRemainingValuesHeuristic, inferenceMethod=None, useAC3=True):
	assignment = Assignment(csp)

	assignment = eliminateUnaryConstraints(assignment, csp)
	if assignment == None:
		return assignment

	if useAC3:
		assignment = AC3(assignment, csp)
		if assignment == None:
			return assignment
	if inferenceMethod is None or inferenceMethod==noInferences:
		assignment = recursiveBacktracking(assignment, csp, orderValuesMethod, selectVariableMethod)
	else:
		assignment = recursiveBacktrackingWithInferences(assignment, csp, orderValuesMethod, selectVariableMethod, inferenceMethod)
	if assignment == None:
		return assignment

	return assignment.extractSolution()

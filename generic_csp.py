from typing import Generic, TypeVar, Dict, List, Optional
from abc import ABC, abstractmethod

V = TypeVar('V') # variable type
D = TypeVar('D') # domain type


# Base class for all constraints
class Constraint(Generic[V, D], ABC):
    # The variables that the constraint is between
    def __init__(self, variables: List[V]) -> None:
        self.variables = variables

    # Must be overridden by subclasses
    @abstractmethod
    def satisfied(self, assignment: Dict[V, D]) -> bool:
        ...


# A constraint satisfaction problem consists of variables of type V
# that have ranges of values known as domains of type D and constraints
# that determine whether a particular variable's domain selection is valid
class CSP(Generic[V, D]):
	def __init__(self, variables: List[V], domains: Dict[V, List[D]], MRV: bool = False, AC3:bool = False, LCV: bool = False) -> None:
		'''
        It takes a list of variables and a dictionary of domains (possible values) for each variable as its constructor arguments.
        It maintains a dictionary of constraints associated with each variable
        Attributes:
            variables: variables to be constrained
            domains: domain of each variable
        '''
		self.solution = None	
		self.variables: List[V] = variables # variables to be constrained
		self.domains: Dict[V, List[D]] = domains # domain of each variable
		self.constraints: Dict[V, List[Constraint[V, D]]] = {}
		self.MRV = MRV # is MRV heuristic enable
		self.AC3Enabled = AC3
		self.LCVEnabled = LCV #lCV heuristic
		for variable in self.variables:
			self.constraints[variable] = []
			if variable not in self.domains:
				raise LookupError("Every variable should have a domain assigned to it.")		
			
	def add_constraint(self, constraint: Constraint[V, D]) -> None:
		for variable in constraint.variables:
			if variable not in self.variables:
				raise LookupError("Variable in constraint not in CSP")
			else:
				self.constraints[variable].append((constraint))
		
	def solve(self):
		assignment = {}
		self.solution = self.backtracking_search(assignment)
		return self.solution
	
	def solution_domain_to_solution(self) -> Dict[V, D]:
		assignment: Dict[V, D] = {}
		for variable, domain in self.domains.items():
			assignment[variable] = domain[0]
		return assignment

	def is_consistent(self, assignment: Dict[V, D]) -> bool:
		print("here")
		for constraint_list in self.constraints.values():
				for constraint in constraint_list:
					if not constraint.satisfied(assignment):
						print("not satisfied")
						return False
		return True

	def is_network_consistent(self, assignment: Dict[V, D] = None) -> bool:
		if assignment is not None:
			return self.is_consistent(assignment)

		is_every_domain_singleton = True
		for domain in self.domains.values():
			print("dom",len(domain) != 1)
			if len(domain) != 1:
				is_every_domain_singleton = False
				break

		if not is_every_domain_singleton:
			return False

		assignment: Dict[V, D] = self.solution_domain_to_solution()
		return self.is_consistent(assignment)
	
	def backtracking_search(self, assignment: Dict[V, D] = {}) -> Optional[Dict[V, D]]:
		'''
		It performs a depth-first search with backtracking to find a solution to the CSP.
		It takes an assignment dictionary as an argument (initially empty), which represents the current state of variable assignments.
		The algorithm checks if the assignment is complete (all variables have values), and if so, returns the assignment.
		Otherwise, it selects the first unassigned variable, iterates through its domain values, and recursively searches for a solution while maintaining consistency with constraints.
		'''
		# assignment is complete if every variable is assigned (our base case)
		if len(assignment) == len(self.variables):
			return assignment
		
		 # get all variables in the CSP but not in the assignment
		unassigned: List[V] = [v for v in self.variables if v not in assignment]
		# get the every possible domain value of the first unassigned variable
		first: V = unassigned[0]
		
		if self.MRV:
            # Apply MRV heuristic to select the variable with the fewest remaining values
			print("using MRV")
			first: V = self.select_unassigned_variable(unassigned)

		if self.LCVEnabled == True:
			self.domains[first] = self.order_domain_values(first)  
	
		for value in self.domains[first]:
			local_assignment = assignment.copy()
			local_assignment[first] = value
			# if we're still consistent, we recurse (continue)
			if self.consistent(first, local_assignment):
				if self.AC3Enabled: # calling AC3 if it's enabled
					self.AC3()
					if self.is_network_consistent():
						print('AC3 found solution!')
						return self.solution_domain_to_solution()
					else:
						print('backtracking...')
						break
				result: Optional[Dict[V, D]] = self.backtracking_search(local_assignment)
				# if we didn't find the result, we will end up backtracking
				if result is not None:
					return result
		return None

	def AC3(self, queue:list = None):
		removals = []
		if queue is None:
			# initialize queue by adding all arcs
			queue=[]
			for var in self.constraints:
				for arcConstraint in self.constraints[var]:
					queue.append((var, arcConstraint))
					
		while queue: # while queue is not empty
			xi, constraint = queue.pop() # remove xi and a constraint
			xj = None # determine the variable xj
			for i in constraint.variables:
				if i != xi:
					xj = i
			# b,r=self.revise(xi, xj, constraint)
		
			# if r:
			# 	removals.extend(r)
			if self.revise(xi, xj, constraint):
				if len(self.domains[xi]) == 0: # if domain is empty
					return False
				for arc in self.constraints[xi]: # neighbors
					xk = None
					for i in arc.variables:
						if i != xi:
							xk = i
					if arc != constraint: # if xk != xj
						queue.append((xk, constraint)) # add arc to queue
		return True
	
	def revise(self, xi, xj, constraint):
		revised = False
		removals=[]
		for x in self.domains[xi]: # for all x in the domain of xi
			tempAssignment = {xi: x} 
			satisfiableY = False
			for y in self.domains[xj]: # for all y in the domain of xj
				tempAssignment[xj] = y
				if constraint.satisfied(tempAssignment):
					print("satisfied", xj)
					satisfiableY = True
			if satisfiableY == False: # if there is no satisfiable assignment
				self.domains[xi].remove(x) # remove x from the domain of xi
				print("removing", x, "from", xi)
				removals.append((x,y))
				revised = True
		return revised

	def select_unassigned_variable(self, unassigned_vars):
		'''
		This method returns the variable with the smallest domain size among the unassigned variables.
		It helps choose which variable to assign a value next, using the minimum remaining values (MRV) heuristic.
	    '''
		return min(unassigned_vars, key=lambda var: len(self.domains[var]))

	def order_domain_values(self, variable):
		'''
		This method returns the entire domain of a variable. It's used to determine the order in which values are tried for assignment.

		The LCV algorithm iterates through every possible value in the domain for a variable. 
		It then keeps a counter for how many values for neighbors of the variable satisfied the constraint between neighbors and the variable. 
		After doing this process, the method returns a list of values for a variable sorted by their maximum number of satisfiable neighbors to minimum (which is equivalent to the minimum amount of variables removed).
	    '''
		def sortDomains(value): # sort function ranks by number of neighbor values still satisfiable
			count = 0
			tempAssignment = {variable: value}
			for neighbors in self.constraints[variable]:
				otherVar = None
				for other in neighbors.variables:
					if other != variable:
						otherVar = other
				for vals in self.domain[otherVar]:
					tempAssignment[otherVar] = vals
					if neighbors.isSatisfied(tempAssignment):
						count += 1
			return count
						
		tempVar = self.domains[variable]
		tempVar.sort(key = sortDomains, reverse=True)
		return tempVar
	
	# Check if the value assignment is consistent by checking all constraints
    # for the given variable against it
	def consistent(self, variable: V, assignment: Dict[V, D]) -> bool:
		for constraint in self.constraints[variable]:
			if not constraint.satisfied(assignment):
				return False
			
		return True
	


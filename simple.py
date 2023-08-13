'''
Solve Map Coloring using Arc-Consistency 3 and Backtracking Search

Juliana Sau
'''
import time

#  python3 ./simple.py 

class csp:
    	
	def __init__(self, variables, domains, constraints):
		self.variables = variables
		self.domains = domains
		self.constraints = constraints
	
	def solved(self):
		return not any(len(self.domains[var])!=1 for var in self.variables)
	
	def __str__(self):
		print("============================================================\n")
		output = ""
		for variable in self.variables:
			if len(self.domains[variable]) == 1:
				value=self.domains[variable].pop()
				output += variable + " : " + str(value) + " "
				self.domains[variable].add(value)
			else:
				output += variable + " : " + str(self.domains[variable]) + " "
			output+="\n"
		output += "\n======================================================="+"\n"
		return(output)

def AC3 (csp, queue=None):
 	
	def arc_reduce(x,y):
		removals=[]
		change=False
		for vx in csp.domains[x].copy():
			found=False

			for vy in csp.domains[y]:
				if diff(vx,vy):
					found=True
					print("found", vx, vy, x, y)
			if(not found):
				print("removing", vx, x, y)
				csp.domains[x].remove(vx)	
				removals.append((x,vx))
				change=True

		return change,removals
	removals=[]
	
	if queue is None:
		queue=[]
		for x in csp.variables:
			queue = queue + [(x, y) for y in csp.constraints[x]]

	while queue:
		x,y= queue.pop()

		b,r=arc_reduce(x,y)
		
		if r:
			removals.extend(r)
		if(b):
		#not arc consistent
			if(len(csp.domains[x])==0):
				return False, removals
			#if we remove a value, check all neighbours
			else:
				queue = queue + [(x, z) for z in csp.constraints[x] if z!=y]

	return True, removals

def diff(x,y):
	return (x!=y)

def initialise():
    variables = ["Western Australia", "Northern Territory", "South Australia",
    "Queensland", "New South Wales", "Victoria", "Tasmania"]

#     neighbours = {
#     "Northern Territory": ["Western Australia", "South Australia", "Queensland"],
#     "Western Australia": ["Northern Territory", "South Australia"],
#     "South Australia": ["Western Australia", "Northern Territory", "Queensland", "New South Wales", "Victoria"],
#     "Queensland": ["Northern Territory", "South Australia", "New South Wales"],
#     "New South Wales": ["Queensland", "South Australia", "Victoria"],
#     "Victoria": ["South Australia", "New South Wales"],
#     "Tasmania": []
#    }
#     neighbor_tuples = [(variable, neighbor) for variable, neighbors in neighbours.items() for neighbor in neighbors]


    # initialise and populate
    domains = {}
    for variable in variables:
        domains[variable] = ["red", "green", "blue"]


    # declare and populate constraints
    constraints_list = [
        [0, 1], [0, 2], [2, 1], [3, 1], [3, 2], [3, 4], [4, 2], [5, 2], [5, 4], [5, 6]
    ]
    
    #return all binary constraints that contain var
    def constraints(x, listOfNeighbours):
    	# {y : xRy}
        constrain_to = set()
        for pair in listOfNeighbours:
            if x in pair:
                if x==pair[0]:
                    constrain_to.add(pair[1])
                elif x==pair[1]:
                    constrain_to.add(pair[0])
        return constrain_to

   # Convert constraints to variable pairs
    constraints_tuple = [(variables[a], variables[b]) for a, b in constraints_list]

    # print(constraints_tuples)

    constraints = {x:constraints(x, constraints_tuple) for x in variables} 
	
    return csp(variables,domains,constraints)

def selectUnassignedVariable(csp,assigned):
	for var in csp.variables:
		if var not in assigned: return var

#no ordering
def OrderDomainValues(csp, assignment, var):
	values = [val for val in csp.domains[var]] 
	return values

def backTrackingSearch(csp): #returns a solution or failure
	return backtrack({},csp)

#todo (mostly pseudo)
def backtrack(assignment, csp): #returns a solution or failure 
	if csp.solved():
		return csp

	var = selectUnassignedVariable(csp, assignment)
	
	for value in OrderDomainValues(csp, assignment, var):
    	
		assignment[var] = value

		removals = [(var, a) for a in csp.domains[var] if a != value]
		
		#Assume Var = Value => D(Var) = Value
		csp.domains[var] = {value}

		consistent, removed = AC3(csp, [(x,var) for x in csp.constraints[var]])

		#if values were removed by AC3, add them to the list to be restored
		if removed:
			removals.extend(removed)
		
		#if AC3 consistent
		if(consistent):
    		
			#continue search
			result = backtrack(assignment,csp)
			
			#if the search didn't fail, return the solution
			if(result != False):
				return result
		
		#If CSP is not AC3 consistent, restore the values removed by inference
		for variable, value in removals:
			csp.domains[variable].add(value)

	# Unable to find an available solution for this path, step back and choose a different path
	del assignment[var]
	return False


def main():

	MapColoring = initialise()

	print("Initial Problem:")
	print(MapColoring)
	print("Attempting AC-3...")
	
	AC3(MapColoring)

	if(MapColoring.solved()):
		print("MapColoring solved by AC-3 only: ")
		print(MapColoring)
	else:
		print("MapColoring partially solved by AC-3")
		print(MapColoring)
		
		print("Attempting backtrack search...")
		
		t1=time.time()
		solution = backTrackingSearch(MapColoring)
		t2=time.time()
		print("Time elapsed {0:.2f}s".format(t2-t1))
		
		if(solution):
			print("Solution found by Backtrack Search: ")
			print(solution)
		else:
			print("Backtrack Search unable to find a solution.")

if __name__ == "__main__":
	main()
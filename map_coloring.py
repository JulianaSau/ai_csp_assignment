from generic_csp import Constraint, CSP
from typing import TypeVar, Dict, List, Optional

V = TypeVar('V') # variable type
D = TypeVar('D') # domain type

class MapColoringConstraint(Constraint[str, str]):
    def __init__(self, place1: str, place2: str) -> None:
        super().__init__([place1, place2])
        self.place1: str = place1
        self.place2: str = place2

    def satisfied(self, assignment: Dict[str, str]) -> bool:
        # If either place is not in the assignment then it is not
        # yet possible for their colors to be conflicting
        if self.place1 not in assignment or self.place2 not in assignment:
            return True
        # check the color assigned to place1 is not the same as the
        # color assigned to place2
        return assignment[self.place1] != assignment[self.place2]
    

def print_constraints(constraints_dict):
    for variable, constraints in constraints_dict.items():
        print(f"{variable}:")
        for constraint in constraints:
            print(f"    {constraint}")
        print()

if __name__ == "__main__":
    # initialise variables
    variables: List[str] = ["Western Australia", "Northern Territory", "South Australia",
    "Queensland", "New South Wales", "Victoria", "Tasmania"]
    
    
    # neighbours = {
    #     "Northern Territory":["Western Australia", "South Australia","Queensland"]
    #     ,"Western Australia":["Northern Territory", "South Australia"]
    #     ,"South Australia":["Western Australia", "Northern Territory", "Queensland", "New South Wales", "Victoria"]
    #     ,"Queensland":["Northern Territory", "South Australia", "New South Wales"]
    #     ,"New South Wales":["Q", "South Australia", "Victoria"]
    #     ,"Victoria":["South Australia", "New South Wales"].
    #     "Tasmania":[]
    # }
    # initialise and populate
    domains: Dict[str, List[str]] = {}
    for variable in variables:
        domains[variable] = ["red", "green", "blue"]

    # initialise csp class with variables and domains
    csp: CSP[str, str] = CSP(variables, domains, MRV = False, AC3 = False, LCV = False)

    # declare and populate constraints
    constraints = [
        [0, 1], [0, 2], [2, 1], [3, 1], [3, 2], [3, 4], [4, 2], [5, 2], [5, 4], [5, 6]
    ]
    for c in constraints:
        csp.add_constraint(MapColoringConstraint(variables[c[0]], variables[c[1]]))

    # Print the formatted JSON string
    # print_constraints(csp.constraints)
    
    # solve problem
    solution: Optional[Dict[str, List[str]]] = csp.solve()

    if solution is None:
        print("No solution found!")
    else:
        print()
        print("solution", solution)



import unittest
from typing import TypeVar, Dict, List, Optional
from generic_csp import Constraint, CSP
from map_coloring import MapColoringConstraint

class TestMapColoring(unittest.TestCase):
    def setUp(self):
        self.test_solution = {
            'Western Australia': 'red',
            'Northern Territory': 'green',
            'South Australia': 'blue',
            'Queensland': 'red',
            'New South Wales': 'green',
            'Victoria': 'red',
            'Tasmania': 'green'
        }

        self.variables: List[str] = [
            "Western Australia", "Northern Territory", "South Australia",
            "Queensland", "New South Wales", "Victoria", "Tasmania"
        ]

        self.constraints = [
            [0, 1], [0, 2], [2, 1], [3, 1], [3, 2], [3, 4], [4, 2], [5, 2], [5, 4], [5, 6]
        ]

        self.domains: Dict[str, List[str]] = {}
        for variable in self.variables:
            self.domains[variable] = ["red", "green", "blue"]

    def test_solution(self):
        csp: CSP[str, str] = CSP(self.variables, self.domains, MRV = False, AC3 = False, LCV = False)

        for c in self.constraints:
            csp.add_constraint(MapColoringConstraint(self.variables[c[0]], self.variables[c[1]]))
        
        solution: Optional[Dict[str, str]] = csp.solve()
        print("solution", solution)
        self.assertEqual(self.test_solution, solution)


if __name__ == '__main__':
    unittest.main()
    # python3 -m unittest tests/test_map_coloring.py
There are three solutions here:
**1. Generic Solution**
`generic_csp.py` and `map_coloring.py` are dependent on each other
`generic_csp.py` contains a generic implementation of a CSP problem. It has the capability of using *heuristics*, *recursive backtracking search* and *AC3* algorithm to solve problems. you just have to pass the params in the instantiation of the class
`map_coloring.py` extends Generic Class CSP and defines variables, constraints etc and finds the solution depending on the algorithm passed to it

Commands: `python3 map_coloring.py`
For testing: `python3 -m unittest tests/test_map_coloring.py`

NB: might be a bit hard to understand because it uses a typed version of Python

**2. Simple Implementation**
`simple.py` is a simpler implementation of the map coloring problem using *AC3* and *recursive backtracking search*.

`python3 simple.py`

**3. Sudoku Solution**
To see the *AC3* algorithm in practice, this is the one to run. Since the map coloring problem is less complex, AC3 is a waste of resources to use.

Commands: `python3 others/sudoku.py [full path to easy_sudoku.txt file]
e.g `python3 others/sudoku.py C:/Users/users/Documents/easy_sudoku.txt``

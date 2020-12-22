# sudoku
This is a little Sudoku solver.

It models the problem of Sudoku as a Constraint Satisfaction Problem (CSP),
which Sudoku clearly lends itself to.

Currently all it does is solve naked singles (cells in the grid that have
only one possible value).

I'll soon add a DFS with backtracking, starting from the most constrained
cells to limit the search breadth.

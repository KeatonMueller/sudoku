# sudoku
This is a little Sudoku solver.

It models the problem of Sudoku as a Constraint Satisfaction Problem (CSP),
which Sudoku clearly lends itself to.

First it solves any naked singles (cells in the grid that only have one
possible value), then it does a DFS with backtracking, starting from the
most constrained cells in the grid.

To use it, run `python3 sudoku.py`.
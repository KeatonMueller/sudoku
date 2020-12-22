# sudoku
This is a little Sudoku solver.

It models the problem of Sudoku as a Constraint Satisfaction Problem (CSP),
which Sudoku clearly lends itself to.

## Solver

The Sudoku solver does a two-step approach.

First, it solves any naked singles (cells in the grid that only have one
possible value), then it does a DFS with backtracking, starting from the
most constrained cells in the grid.

There are a few example boards you can load and have solved. All of the
9x9 boards can be solved quite quickly, but the Hard and Harder 16x16
boards take quite some time due to the large state space that must be 
searched. 

## API

There's also basic little API using Flask that allows you to interface
with the solver. I may write a front-end at some point that uses this API.

For simplicity's sake, the API reads and writes to a JSON file rather
than communicating with and storing info in a database.

You can find more details on the API in `/api/api.py`.

## How to use it

This project requires you have Python 3 installed. If you'd like to run
the API, then you need Flask installed as well.

To use the solver, run `python3 sudoku.py`.

To use the API, run `python3 sudoku.py api`.
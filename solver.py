class Solver:
    def __init__(self, grid=None):
        self.grid = grid

    def solve(self):
        "Solve the grid and print the solution"
        # do nothing if grid isn't set
        if self.grid == None:
            return

        # first just search for naked singles
        self.solve_naked_singles()

        # if it's still not solved, do dfs with backtracking
        if not self.grid.is_solved():
            self.dfs()

        print('solved!')
        print(self.grid)

    def dfs(self):
        "Perform dfs with backtracking to solve the grid"
        # select cell
        cell = self.grid.get_most_constrained()
        values = set(cell.possible_values)
        # for each possible value
        for val in values:
            # try the value
            cell.value = val
            if self.grid.is_solved():
                return True
            # recurse
            if self.dfs():
                return True
            # undo the value assignment
            cell.value = 0
        # none of the values worked
        return False
        
    def solve_naked_singles(self):
        "Solve all naked singles in the grid"
        cell = self.grid.get_most_constrained()
        while cell != None and len(cell.possible_values) == 1:
            cell.value = cell.possible_values.pop()
            cell = self.grid.get_most_constrained()
from game import Grid

def solve_naked_singles(grid):
    "Solve all naked singles in the grid"
    cell = grid.get_most_constrained()
    while cell != None and len(cell.possible_values) == 1:
        cell.value = cell.possible_values.pop()
        cell = grid.get_most_constrained()

def main():
    grid = Grid()
    grid.read('examples/easy.txt')
    print(grid)
    solve_naked_singles(grid)
    print()
    print(grid)


if __name__ == '__main__':
    main()
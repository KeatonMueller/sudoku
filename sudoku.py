from game import Grid
from solver import Solver

def startup():
    sizes = {
        1: 3,
        2: 4
    }
    difficulties = {
        1: 'easy',
        2: 'medium',
        3: 'hard',
        4: 'harder'
    }

    print('Pick a board size:')
    print('  1. 9x9')
    print('  2. 16x6')
    size = sizes[int(input())]

    print('Pick a difficulty to solve:')
    print('  1. Easy')
    print('  2. Medium')
    print('  3. Hard')
    print('  4. Harder')
    difficulty = difficulties[int(input())]

    choice = f'examples/{size}/{difficulty}.txt'
    grid = Grid(size)
    grid.read_file(choice)
    return grid

def main():
    grid = startup()
    solver = Solver(grid)
    solver.solve()

if __name__ == '__main__':
    main()
from sys import argv

from game import Grid
from solver import Solver
from api import api

def get_box_len():
    sizes = {
        1: 3,
        2: 4
    }

    print('Pick a board size:')
    print('  1. 9x9')
    print('  2. 16x6')
    return sizes[int(input())]

def load():
    box_len = get_box_len()

    difficulties = {
        1: 'easy',
        2: 'medium',
        3: 'hard',
        4: 'harder'
    }

    print('Pick a difficulty to solve:')
    print('  1. Easy')
    print('  2. Medium')
    print('  3. Hard')
    print('  4. Harder')
    difficulty = difficulties[int(input())]

    choice = f'examples/{box_len}/{difficulty}.txt'
    grid = Grid(box_len)
    grid.read_file(choice)
    return grid

def enter():
    box_len = get_box_len()
    grid = Grid(box_len)

    for row in range(box_len * box_len):
        for col in range(box_len * box_len):
            print(grid)
            val = input(f'Value for ({row + 1}, {col + 1}): ') or 0
            try:
                val = int(val)
            except ValueError:
                val = ord(val.upper()) - 55
            grid.get_cell(row, col).value = val

    if not grid.is_valid():
        print('invalid board')
        exit()
    return grid

def startup():
    print('How to load a board:')
    print('  1. Load an example')
    print('  2. Enter custom puzzle')
    choice = int(input())
    if choice == 1:
        return load()
    else:
        return enter()

def main():
    if len(argv) > 1 and argv[1] == 'api':
        api.run()
    else:
        grid = startup()
        solver = Solver(grid)
        solver.solve()

if __name__ == '__main__':
    main()
from game import Grid
from solver import Solver

def startup():
    choices = {
        1: 'examples/easy.txt',
        2: 'examples/medium.txt',
        3: 'examples/hard.txt'
    }
    grid = Grid()
    print('Pick a difficulty to solve:')
    print('  1. Easy')
    print('  2. Medium')
    print('  3. Hard')
    choice = int(input())
    grid.read(choices[choice])
    return grid

def main():
    grid = startup()
    solver = Solver(grid)
    solver.solve()

if __name__ == '__main__':
    main()
from copy import copy
class Cell:
    '''
        A single cell in the sudoku grid.
    '''
    def __init__(self, row, col, groups):
        self._value = 0
        self.row = row
        self.col = col
        self._groups = groups
        for group in self._groups:
            group.add(self)
        self.possible_values = set()

    def update(self):
        if self._value != 0:
            self.possible_values.clear()
            return
        self.possible_values = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
        for group in self._groups:
            self.possible_values -= group.values
        
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        self.update()
        self._update_groups()

    def _update_groups(self):
        for group in self._groups:
            group()

    def __str__(self):
        return str(self._value) if self._value > 0 else '.'

class CellGroup:
    '''
        A group of cells (either a row, column, or box).

        CellGroup objects aggregate Cell objects. They also subscribe
        to changes in the cells, and update their `values` field whenever
        a cell changes value.
    '''
    def __init__(self):
        self.cells = []
        self.values = set()

    def add(self, cell):
        self.cells.append(cell)
        self.values.add(cell.value)

    def is_valid(self):
        "Check whether this cell group has a valid group of cell values"
        num_empty = len([cell for cell in self.cells if cell.value == 0])
        if num_empty == 0:
            # if there are no empty cells, there must be 9 unique values
            return len(self.values) == 9
        # otherwise all non-empty values must be unique
        return len(self.values) == 9 - num_empty + 1

    def __call__(self):
        self.values.clear()
        for cell in self.cells:
            self.values.add(cell.value)
        for cell in self.cells:
            cell.update()
    
class Row(CellGroup):
    '''
        Subclass of CellGroup to override __str__ method
        for convenience when printing the grid. All other
        functionality is the same.
    '''
    def __str__(self):
        left_group = [str(cell) for cell in self.cells[:3]]
        mid_group = [str(cell) for cell in self.cells[3:6]]
        right_group = [str(cell) for cell in self.cells[6:9]]
        return ' | '.join([
                    ' '.join(left_group),
                    ' '.join(mid_group),
                    ' '.join(right_group)
                ])

class Grid:
    def __init__(self):
        # initialize rows, cols, boxes
        self.rows = [Row() for _ in range(9)]
        self.cols = [CellGroup() for _ in range(9)]
        self.boxes = [CellGroup() for _ in range(9)]
        self.cells = []
        # initialize cells
        for i in range(81):
            # calculate indices
            r = int(i / 9)
            c = i % 9
            b = int(r / 3) * 3 + int(c / 3)
            # create new cell
            cell = Cell(r, c, [self.rows[r], self.cols[c], self.boxes[b]])
            self.cells.append(cell)

    def get_most_constrained(self):
        # sort in order of increasing possible values
        open_cells = [cell for cell in self.cells if cell.value == 0]
        if len(open_cells) == 0:
            return None
        return sorted(open_cells, key=lambda cell: len(cell.possible_values))[0]

    def get_cell(self, row, col):
        return self.cells[row * 9 + col]

    def read(self, filename):
        lines = open(filename, 'r').read().strip().split('\n')
        for row, line in enumerate(lines):
            for col, val in enumerate(line):
                self.get_cell(row, col).value = int(val)

        for cell in self.cells:
            cell.update()

    def is_valid(self):
        groups = self.rows + self.cols + self.boxes
        for group in groups:
            if not group.is_valid():
                return False
        return True

    def __str__(self):
        grid_str = ''
        for row in range(3):
            grid_str += str(self.rows[row]) + '\n'
        grid_str += '---------------------\n'
        for row in range(3, 6):
            grid_str += str(self.rows[row]) + '\n'
        grid_str += '---------------------\n'
        for row in range(6, 9):
            grid_str += str(self.rows[row]) + '\n'
        return grid_str[:-1]
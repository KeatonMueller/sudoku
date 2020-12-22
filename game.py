BOX_LEN = 3                 # side length of each box. also determines board size
SIZE = BOX_LEN * BOX_LEN    # size of rows, columns, boxes

class Cell:
    '''
        A single cell in a Sudoku grid.
    '''
    def __init__(self, row, col, groups):
        self._value = 0         # value of this cell
        self.row = row          # row index of this cell
        self.col = col          # column index of this cell
        self._groups = groups   # list of CellGroup objects this cell is in

        # register this cell in each group
        for group in self._groups:
            group.add(self)

        # initialize possible_values to empty set
        self.possible_values = set()

    def update(self):
        '''
            Calculate possible values if cell is empty.
            Assumes that the `values` field for each group this
            cell is a member of is up to date.
        '''
        if self._value != 0:
            self.possible_values.clear()
            return
        self.possible_values = set(range(1, SIZE + 1))
        for group in self._groups:
            self.possible_values -= group.values
        
    @property
    def value(self):
        "Get the cell's value"
        return self._value

    @value.setter
    def value(self, new_value):
        "Update this cell and all groups the cell is in when the value changes"
        self._value = new_value
        self.update()
        self._update_groups()

    def _update_groups(self):
        "Have each group update its values"
        for group in self._groups:
            group.update_values()

    def __str__(self):
        "Return value or . if empty"
        return str(self._value) if self._value > 0 else '.'

class CellGroup:
    '''
        A group of cells (either a row, column, or box).

        CellGroup objects aggregate Cell objects. They also subscribe
        to changes in the cells, and update their `values` field whenever
        a cell changes value.
    '''
    def __init__(self):
        self.cells = []     # list of cells this group aggregates
        self.values = set() # list of cell values used in this group

    def add(self, cell):
        "Add a new cell to this group"
        self.cells.append(cell)
        self.values.add(cell.value)

    def is_valid(self):
        "Check whether this cell group has a valid group of cell values"
        num_empty = len([cell for cell in self.cells if cell.value == 0])
        if num_empty == 0:
            # if there are no empty cells, there must be SIZE unique values
            return len(self.values) == SIZE
        # otherwise the number of non-zero values must be SIZE - num_empty
        return len(self.values - {0}) == SIZE - num_empty 

    def update_values(self):
        "Update values of cells in this group"
        self.values.clear()
        # record value of each cell
        for cell in self.cells:
            self.values.add(cell.value)
        # update each cell once this group's `values` field is up to date
        for cell in self.cells:
            cell.update()
    
class Row(CellGroup):
    '''
        Subclass of CellGroup to override __str__ method
        for convenience when printing the grid. All other
        functionality is the same.
    '''
    def __str__(self):
        groups = []
        for col in range(0, SIZE, BOX_LEN):
            groups.append([str(cell) for cell in self.cells[col:col + BOX_LEN]])
        
        return ' | '.join([' '.join(group) for group in groups])

class Grid:
    '''
        The entire Sudoku grid.
    '''
    def __init__(self):
        # initialize rows, cols, boxes
        self.rows = [Row() for _ in range(SIZE)]           # list of Row objects for each row
        self.cols = [CellGroup() for _ in range(SIZE)]     # list of CellGroup objects for each column
        self.boxes = [CellGroup() for _ in range(SIZE)]    # list of CellGroup objects for each box
        self.cells = []                                 # list of Cell objects for each cell
        # initialize cells
        for i in range(SIZE * SIZE):
            # calculate indices
            r = int(i / SIZE)
            c = i % SIZE
            b = int(r / BOX_LEN) * BOX_LEN + int(c / BOX_LEN)
            # create new cell
            cell = Cell(r, c, [self.rows[r], self.cols[c], self.boxes[b]])
            self.cells.append(cell)

    def get_most_constrained(self):
        "Return the most constrained empty cell in the grid, or None if grid is full"
        # get empty cells
        empty_cells = [cell for cell in self.cells if cell.value == 0]
        if len(empty_cells) == 0:
            return None
        # sort in order of increasing possible values
        return sorted(empty_cells, key=lambda cell: len(cell.possible_values))[0]

    def get_cell(self, row, col):
        "Return cell at given row and column index"
        return self.cells[row * SIZE + col]

    def read(self, filename):
        "Populate grid with information in given file"
        lines = open(filename, 'r').read().strip().split('\n')
        for row, line in enumerate(lines):
            for col, val in enumerate(line):
                self.get_cell(row, col).value = int(val)

        for cell in self.cells:
            cell.update()
        
        print(f'loaded grid from {filename}:')
        print(self)

    def is_valid(self):
        "Check if grid is in a valid state"
        groups = self.rows + self.cols + self.boxes
        for group in groups:
            if not group.is_valid():
                return False
        return True

    def is_solved(self):
        "Check if grid is solved"
        # get empty cells
        empty_cells = [cell for cell in self.cells if cell.value == 0]
        return len(empty_cells) == 0 and self.is_valid()

    def __str__(self):
        grid_str = ''
        line_len = SIZE * 2 - 1 + 2 * (BOX_LEN - 1)

        # add rows one by one to grid_str
        for row in range(0, SIZE, BOX_LEN):
            for i in range(BOX_LEN):
                grid_str += str(self.rows[row + i]) + '\n'
            # add box dividers after every BOX_LEN rows
            grid_str += '-' * line_len + '\n'

        # strip off final box divider and newline
        return grid_str[:-(line_len + 2)]
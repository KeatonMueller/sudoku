from math import sqrt

class Cell:
    '''
        A single cell in a Sudoku grid.
    '''
    def __init__(self, row, col, groups, grid):
        self._value = 0         # value of this cell
        self.row = row          # row index of this cell
        self.col = col          # column index of this cell
        self._groups = groups   # list of CellGroup objects this cell is in
        self._grid = grid       # grid this cell is in

        # register this cell in each group
        for group in self._groups:
            group.add(self)

        # initialize possible_values to all values
        self.possible_values = set(range(1, self._grid.size + 1))

    def update(self):
        '''
            Calculate possible values if cell is empty.
            Assumes that the `values` field for each group this
            cell is a member of is up to date.
        '''
        if self._value != 0:
            self.possible_values.clear()
            return
        self.possible_values = set(range(1, self._grid.size + 1))
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
        self._update_groups()

    def _update_groups(self):
        "Have each group update its values"
        for group in self._groups:
            group.update_values()

    def __str__(self):
        "Return value or . if empty. Values > 9 are turned into letters"
        if self._value == 0:
            return '.'
        if self._value < 10:
            return str(self._value)
        return chr(65 + self._value - 10)

    def __repr__(self):
        "Same as __str__ but 0s are not changed to ."
        if self._value < 10:
            return str(self._value)
        return chr(65 + self._value - 10)

class CellGroup:
    '''
        A group of cells (either a row, column, or box).

        CellGroup objects aggregate Cell objects. They also subscribe
        to changes in the cells, and update their `values` field whenever
        a cell changes value.
    '''
    def __init__(self, grid):
        self.cells = []     # list of cells this group aggregates
        self.values = set() # set of cell values used in this group
        self._grid = grid   # grid this group is in

    def add(self, cell):
        "Add a new cell to this group"
        self.cells.append(cell)
        self.values.add(cell.value)

    def is_valid(self):
        "Check whether this cell group has a valid group of cell values"
        num_empty = len([cell for cell in self.cells if cell.value == 0])
        if num_empty == 0:
            # if there are no empty cells, there must be self.size unique values
            return len(self.values) == self._grid.size
        # otherwise the number of non-zero values must be self.size - num_empty
        return len(self.values - {0}) == self._grid.size - num_empty 

    def update_values(self):
        "Update values of cells in this group"
        self.values.clear()
        # record value of each cell
        for cell in self.cells:
            self.values.add(cell.value)
        # update each cell once this group's `values` field is up to date
        for cell in self.cells:
            cell.update()
    
    def __str__(self):
        "String representation (in row format) for this CellGroup"
        groups = []
        for col in range(0, self._grid.size, self._grid.box_len):
            groups.append([str(cell) for cell in self.cells[col:col + self._grid.box_len]])
        
        return ' | '.join([' '.join(group) for group in groups])

    def __repr__(self):
        "Single string of cell values without formatting"
        return ''.join([repr(cell) for cell in self.cells])

class Grid:
    '''
        The entire Sudoku grid.
    '''
    def __init__(self, box_len=0, load_from=None):
        # one of these must be specified
        if box_len == 0 and load_from == None:
            raise ValueError('must specify either box_len or load_from for Grid()')
        # parse box_len from the repr
        if box_len == 0:
            box_len = int(sqrt(len(load_from.split('\n')[0])))

        self.box_len = box_len
        self.size = box_len * box_len
        # initialize rows, cols, boxes
        self.rows = [CellGroup(self) for _ in range(self.size)]     # list of CellGroup objects for each row
        self.cols = [CellGroup(self) for _ in range(self.size)]     # list of CellGroup objects for each column
        self.boxes = [CellGroup(self) for _ in range(self.size)]    # list of CellGroup objects for each box
        self.cells = []                                 # list of Cell objects for each cell
        # initialize cells
        for i in range(self.size * self.size):
            # calculate indices
            r = int(i / self.size)
            c = i % self.size
            b = int(r / self.box_len) * self.box_len + int(c / self.box_len)
            # create new cell
            cell = Cell(r, c, [self.rows[r], self.cols[c], self.boxes[b]], self)
            self.cells.append(cell)

        if load_from:
            self.read_repr(load_from)

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
        return self.cells[row * self.size + col]

    def read_file(self, filename):
        "Populate grid with information in given file"
        grid_repr = open(filename, 'r').read().strip()
        self.read_repr(grid_repr)

    def read_repr(self, grid_repr):
        "Copy grid information from repr"
        lines = grid_repr.split('\n')
        for row, line in enumerate(lines):
            for col, val in enumerate(line):
                try:
                    val = int(val)
                except ValueError:
                    val = ord(val.upper()) - 55
                self.get_cell(row, col).value = val

        for cell in self.cells:
            cell.update()

        print(f'loaded grid:')
        print(self)

    def is_valid(self):
        "Check if grid is in a valid state"
        groups = self.rows + self.cols + self.boxes
        for group in groups:
            if not group.is_valid():
                return False
        cell = self.get_most_constrained()
        return cell == None or len(cell.possible_values) > 0

    def is_solved(self):
        "Check if grid is solved"
        # get empty cells
        empty_cells = [cell for cell in self.cells if cell.value == 0]
        return len(empty_cells) == 0 and self.is_valid()

    def __str__(self):
        "Return board in readable format"
        grid_str = ''
        line_len = self.size * 2 - 1 + 2 * (self.box_len - 1)

        # add rows one by one to grid_str
        for row in range(0, self.size, self.box_len):
            for i in range(self.box_len):
                grid_str += str(self.rows[row + i]) + '\n'
            # add box dividers after every self.box_len rows
            grid_str += '-' * line_len + '\n'

        # strip off final box divider and newline
        return grid_str[:-(line_len + 2)]

    def __repr__(self):
        "Return board in same format as in the /examples directory"
        return '\n'.join([repr(row) for row in self.rows])
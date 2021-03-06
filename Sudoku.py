import math
class Sudoku:
    def __init__(self, sudoku_size, sudoku_grid = None):
        self.grid_size = sudoku_size
        self.grid = [[0 for i in range(self.grid_size)] for j in range(self.grid_size)]
        if sudoku_grid:
            self.grid = sudoku_grid

    def get_columns(self):
        """
            Returns list of column names
        """
        return list(range(self.grid_size))

    def get_rows(self):
        """
            Returns list of row names
        """
        return list(range(self.grid_size))

    def get_values(self):
        """
            Returns list of possible values
        """
        return list(range(self.grid_size))

    def get_boxes(self):
        """
            Returns list of box names
        """
        return list(range(self.grid_size))

    def get_grid_size(self):
        """
            Returns Sudoku grid size
        """
        return self.grid_size

    def get_value(self, row, col):
        """
            Returns value at position (row, col)
        """
        return self.grid[row][col]

    def set_value(self, row, col, value):
        """
            Set the value in position (row, col)
        """
        self.grid[row][col] = value

    def iterate_box_cells(self, box_id):
        """
            Returns list of (row, col) position of box id
        """
        n = int(math.sqrt(self.grid_size))
        r, c = box_id // n, box_id % n
        row, col = r * n, c * n
        for r in range(row, row + n):
            for c in range(col, col + n):
                yield (r, c)

    def get_box_id(self, row, col):
        """
            Returns box id (row, col) position
        """
        n = int(math.sqrt(self.grid_size))
        r = row // n
        c = col // n
        return r * n + c

    def __str__(self):
        """
            Return a string representation of the Sudoku grid
        """
        result = ""
        for row in self.grid:
            result = result + str(row) + "\n"
        return result

    @staticmethod
    def get_grid_from_text(text):
        """
            Static helper method that takes a string of integers separated by '_' and returns the Sudoku grid
        """
        split_text = text.split("_")
        N = int(math.sqrt(len(split_text)))
        grid = [list(map(int, split_text[i : i + N])) for i in range(0, len(split_text), N)]
        return N, grid

    @staticmethod
    def get_text_from_grid(grid):
        """
            Static helper method that takes a grid and returns a corresponding string of integers separated by '_'
        """
        result = ""
        for row in grid:
            char_row = list(map(lambda x : str(x), row))
            result = result + "_".join(char_row) + "_"
        return result[:-1]

if __name__ == '__main__':
    grid = [[1, 25], [12, 2]]
    print(Sudoku.get_text_from_grid(grid))
    print(Sudoku.get_grid_from_text(Sudoku.get_text_from_grid(grid)))

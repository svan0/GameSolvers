import itertools
from copy import deepcopy
from ExactCover import DLXMatrix
class SudokuExactCoverConverter:
    """
        A class that contains methods that converts Sudoku instance to DLX Matrix and ExactCover Solution back to Sudoku instance
    """
    @staticmethod
    def get_constrains_rows(sudoku_config, sudoku_row, sudoku_column, sudoku_value):
        """
            Helper that gets the constraints row we get by setting cell (sudoku_row, sudoku_column) to sudoku_value
            There are four type of constraints that we use
            1- Each cell has only one value (first 81 columns correspond to this constraint)
            2- Each value appears exactly once in a row (second 81 columns correspond to this constraint)
            3- Each value appears exactly once in a column (third 81 columns correspond to this constraint)
            4- Each value appears exactly once in a box (fourth 81 columns correspond to this constraint)
        """
        sudoku_grid_size = sudoku_config.get_grid_size()

        row_column_position = sudoku_row * sudoku_grid_size + sudoku_column

        row_value_position = sudoku_row * sudoku_grid_size + sudoku_value + sudoku_grid_size * sudoku_grid_size

        column_value_position = sudoku_column * sudoku_grid_size + sudoku_value + 2 * sudoku_grid_size * sudoku_grid_size

        sudoku_box = sudoku_config.get_box_id(sudoku_row, sudoku_column)
        box_value_position = sudoku_box * sudoku_grid_size + sudoku_value + 3 * sudoku_grid_size * sudoku_grid_size

        result = [row_column_position, row_value_position, column_value_position, box_value_position]
        return result

    @staticmethod
    def convert_sudoku_to_exact_cover(sudoku_config):
        """
        Converts a Sudoku instance to DLX Matrix and returns it
        Each row in DLX Matrix will correspond to setting cell (R, C) to value V
        And each row has name R_C_V
        """
        sudoku_grid_size = sudoku_config.get_grid_size()
        number_of_constraints = 4 * sudoku_grid_size * sudoku_grid_size
        list_sudoku_columns = sudoku_config.get_columns()
        list_sudoku_rows = sudoku_config.get_rows()
        list_sudoku_values = sudoku_config.get_values()
        cartesian_product_list = [list_sudoku_columns, list_sudoku_rows, list_sudoku_values]

        dlx_matrix = DLXMatrix(number_of_constraints)
        for (R, C, V) in itertools.product(*cartesian_product_list):
            if sudoku_config.get_value(R, C) == 0 or sudoku_config.get_value(R, C) == V + 1:
                row_constraints = SudokuExactCoverConverter.get_constrains_rows(sudoku_config, R, C, V)
                row_constraints_dictionary = {"row_name" : "{}_{}_{}".format(R, C, V) , "row_value" : row_constraints}
                dlx_matrix.add_sparse_row(row_constraints_dictionary)
        return dlx_matrix

    @staticmethod
    def convert_exact_cover_solution_to_sudoku(sudoku_config, list_of_dlx_rows):
        """
            This method takes as input the initial Sudoku instance and the list of solution
            rows selected by the Exact Cover Solver and returns the final Sudoku result
        """
        sudoku_result = deepcopy(sudoku_config)
        for dlx_row in list_of_dlx_rows:
            row, col, val = list(map(int, dlx_row.split('_')))
            sudoku_result.set_value(row, col, val + 1)
        return sudoku_result

from SudokuExactCoverConverter import *
from ExactCoverSolver import *
from DancingLinks import *
from Sudoku import *

class SudokuSolver:
    @staticmethod
    def solve_sudoku_exact_cover(sudoku_config):
        """
            Takes a sudoku config and returns a sudoku config solution
        """
        if isinstance(sudoku_config, str):
            N, grid = Sudoku.get_grid_from_text(sudoku_config)
            sudoku_config = Sudoku(N, grid)
        if isinstance(sudoku_config, list):
            sudoku_config = Sudoku(len(sudoku_config), sudoku_config)

        dlx_matrix = SudokuExactCoverConverter.convert_sudoku_to_exact_cover(sudoku_config)
        solver = ExactCoverSolver(dlx_matrix)
        list_of_dlx_rows, _ = solver.algorithmX()

        final_grid = SudokuExactCoverConverter.convert_exact_cover_solution_to_sudoku(sudoku_config, list_of_dlx_rows)
        return final_grid

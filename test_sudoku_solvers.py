import pandas as pd
import random
import time
from tqdm import tqdm
from glob import glob
import os
from SudokuSolver import *
if __name__ == '__main__':
    file_path = "sudoku.csv"
    n = sum(1 for line in open(file_path)) - 1
    s = 10000
    skip = sorted(random.sample(range(1, n+1), n-s))
    sudoku_tests = pd.read_csv(file_path, skiprows=skip)

    curr_time = time.time()
    for _, row in tqdm(sudoku_tests.iterrows()):
        sudoku_test = row["quizzes"]
        sudoku_solution = row["solutions"]
        sudoku_test = "_".join([str(c) for c in sudoku_test])
        exact_cover_solution_config = SudokuSolver.solve_sudoku_exact_cover(sudoku_test)
        exact_cover_solution = Sudoku.get_text_from_grid(exact_cover_solution_config.grid)
        exact_cover_solution = exact_cover_solution.replace("_", "")
        assert(sudoku_solution == exact_cover_solution)
    print("ExactCover : Average time per sudoku quiz {}".format((time.time() - curr_time) / s))

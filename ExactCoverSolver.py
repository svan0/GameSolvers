from DancingLinks import *

class ExactCoverSolver:
    def __init__(self, problem):
        """
            ExactCoverSolver takes an instance of an Exact Cover problem
            in the form of a sparse Dancing Links Matrix
            and solves it using Knuth's algorithmX

        """
        self.problem = problem
        self.backtrack_solution_trace = {}
        self.solution = {}
        self.list_of_solution_rows = []

    def select_column(self):
        current_column_head_cell = self.problem.root.R
        best_column = current_column_head_cell

        while current_column_head_cell != self.problem.root:
            if current_column_head_cell.size < best_column.size:
                best_column = current_column_head_cell
            current_column_head_cell = current_column_head_cell.R
        return best_column

    def create_solution(self, d):
        """
            We construct the final solution based on what we saved in the backtracking solution trace
        """
        for k, row in self.backtrack_solution_trace.items():
            if k >= d:
                continue
            row_column_list = [row.C.name]
            row_column_list.extend(r.C.name for r in self.problem.iterate_cells(row, 'R'))
            row_name = self.problem.row_number_to_row_name[row.row_number]
            self.solution[row_name] = row_column_list
            self.list_of_solution_rows.append(row_name)

    def search_helper(self, d):
        """
            This is main backtracking method that solves the exact cover problem
            Each column has to have only one selected solution row in which it is set to 1
            So in each recursive step of the algorithm:
                We select a column c
                We cover c so that it will not be considered anymore
                Now we try all rows r in which c is set to 1:
                    We select r as a part of the solution
                    We cover all columns j in which r is set to 1 because by picking we already satisfy j
                    We recurse
                    If that did not work we uncover all column that we have covered and try next r
        """
        if self.problem.root.R == self.problem.root:
            self.create_solution(d)
            return
        c = self.select_column()
        self.problem.cover(c)
        for r in self.problem.iterate_cells(c, 'D'):
            self.backtrack_solution_trace[d] = r
            for j in self.problem.iterate_cells(r, 'R'):
                self.problem.cover(j)
            self.search_helper(d + 1)
            for j in self.problem.iterate_cells(r, 'L'):
                self.problem.uncover(j)
        self.problem.uncover(c)

    def algorithmX(self):
        """
            Method to be called in order to solve the problem instance
            Return the list of row names to be selected and a dictionary of list that correspond to the values of those rows
            If the problem is unsolvable we will get an empty list and an empty dictionary
        """
        self.search_helper(0)
        return self.list_of_solution_rows, self.solution

if __name__ == '__main__':
    columns = 7
    rows = [
            {"row_name": "1" , "row_value" : [2, 4, 5]},
            {"row_name": "2" , "row_value" : [0, 3, 6]},
            {"row_name": "3" , "row_value" : [1, 2, 5]},
            {"row_name": "4" , "row_value" : [0, 3]},
            {"row_name": "5" , "row_value" : [1, 6]},
            {"row_name": "6" , "row_value" : [3, 4, 6]},
            ]

    dlx = DLXMatrix(columns)
    for row in rows:
        dlx.add_sparse_row(row)
    print(dlx)
    solver = ExactCoverSolver(dlx)
    list_rows, full_solution = solver.algorithmX()
    for a, v in full_solution.items():
        print(a, v)
    print(list_rows)

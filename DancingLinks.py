
class Cell:
    """
        Cells in the sparse Dancing links matrix
    """
    def __init__(self):
        self.L = self.R = self.U = self.D = self.C = self
        self.row_number = -1
        self.column_number = -1

class HeaderCell(Cell):
    """
        This cell represents a column head cell
    """
    def __init__(self, name):
        self.size = 0
        self.name = name
        self.isRoot = False
        super().__init__()

class DLXMatrix:
    def __init__(self, columns):
        #Prepare the root cell of the matrix
        self.root = HeaderCell("Root")
        self.root.isRoot = True

        #Matrix dimensions
        self.number_of_columns = 0
        self.number_of_rows = 0

        #List of column head cells
        self.column_cells = []

        #Dictionaries that map between row name and row id [from 0 to number of rows - 1]
        self.row_number_to_row_name = dict()
        self.row_name_to_row_number = dict()

        #Instanciate the column head cells
        self.prepare_columns(columns)

    def prepare_columns(self, columns):
        """
            This method create the column head cells of the matrix and puts them in a list 'column_cells'
        """
        if isinstance(columns, int):
            columns = list(range(columns))
        self.number_of_columns = len(columns)

        ## Here we are simply creating a circular doubly linked list of column head cells
        prev_column_head_cell = self.root
        for column_id, column in enumerate(columns):
            current_column_head_cell = HeaderCell(str(column))
            current_column_head_cell.column_number = column_id

            prev_column_head_cell.R = current_column_head_cell
            current_column_head_cell.L = prev_column_head_cell

            self.column_cells.append(current_column_head_cell)
            prev_column_head_cell = current_column_head_cell

        self.root.L = prev_column_head_cell
        prev_column_head_cell.R = self.root

    def add_sparse_row(self, row_dict):
        """
            This method appends a sparse row to the matrix
            input :
                row_dict is a dictionary with two entries
                row_name : the name of the row
                row : a list of column indexes where this row is set to 1
        """
        row_name = row_dict["row_name"]
        row = row_dict["row_value"]

        assert(min(row) >= 0 and max(row) < self.number_of_columns)

        #Populate the row name <-> row id mappers
        self.row_number_to_row_name[self.number_of_rows] = row_name
        self.row_name_to_row_number[row_name] = self.number_of_rows

        #Make sure the row entries are sorted
        row = sorted(row)


        row_start_cell = None
        row_prev_cell = None

        #We iterate through the column position indexes of elements in the new row
        for idx in row:
            #We create the cell that will contain the new element
            current_cell = Cell()
            current_cell.row_number = self.number_of_rows
            current_cell.column_number = idx

            #If we have already inserted at least one cell in the row
            #then the last cell inserted will point to the new one on the right
            #and the new cell will point to the previous last one on the left
            #Else the new cell is the start cell of the row
            if row_prev_cell:
                row_prev_cell.R = current_cell
                current_cell.L = row_prev_cell
            else :
                row_start_cell = current_cell

            #Here we select the current column where we are going to insert a cell
            #We take the column head and the last cell inserted in this column
            #(which is column head.U -- circular doubly linked list)
            current_column_head_cell = self.column_cells[idx]
            current_column_last_cell = current_column_head_cell.U

            #In order to insert the new cell in the column
            #the previous last one has to point to it with down
            current_column_last_cell.D = current_cell
            #the new cell has to point to the previous last one with up
            current_cell.U = current_column_last_cell
            #the new cell has to point to column head with down
            current_cell.D = current_column_head_cell
            #column head has to point to new cell with up
            current_column_head_cell.U = current_cell
            #We also save for each cell a pointer to the column head
            current_cell.C = current_column_head_cell

            current_column_head_cell.size += 1
            row_prev_cell = current_cell

        #We finally add links between last cell and first cell in the new row
        row_start_cell.L = current_cell
        current_cell.R = row_start_cell
        self.number_of_rows += 1

    def cover(self, column):
        """
            This method covers a column
            Which means that we remove all rows in which this column is set to 1
            (By doing this we also remove the column)
        """
        if isinstance(column, int):
            column = self.column_cells[column]
        if isinstance(column, Cell) and not isinstance(column, HeaderCell):
            column = column.C

        column.R.L = column.L
        column.L.R = column.R

        for current_cell in self.iterate_cells(column, 'D'):
            for row_cell in self.iterate_cells(current_cell, 'R'):
                assert(row_cell != current_cell)
                row_cell.D.U = row_cell.U
                row_cell.U.D = row_cell.D
                row_cell.C.size -= 1

    def uncover(self, column):
        """
            This method uncovers a column
            Which means that we add back all rows in which this column is set to 1
            and the column itself
        """
        if isinstance(column, int):
            column = self.column_cells[column]
        if isinstance(column, Cell) and not isinstance(column, HeaderCell):
            column = column.C

        for current_cell in self.iterate_cells(column, 'U'):
            for row_cell in self.iterate_cells(current_cell, 'L'):
                row_cell.C.size += 1
                row_cell.D.U = row_cell
                row_cell.U.D = row_cell

        column.R.L = column
        column.L.R = column

    def iterate_cells(self, cell, direction):
        """
            This method iterate through the matrix starting from
            'cell' and going in a specified 'direction' until we get
            back to cell
        """
        current_cell = getattr(cell, direction)
        while current_cell != cell:
            yield current_cell
            current_cell = getattr(current_cell, direction)

    def __str__(self):
        """
            Returns a string representation of the matrix
            where X means that the cell has value 1
            and - meands that the cell has value 0
        """
        result = [['-' for i in range(self.number_of_columns)] for j in range(self.number_of_rows)]
        for current_column_head_cell in self.iterate_cells(self.root, 'R'):
            for current_cell in self.iterate_cells(current_column_head_cell, 'D'):
                result[current_cell.row_number][current_cell.column_number] = 'X'

        string_result = ""
        for row in result:
            string_result = string_result + str(row) + "\n"
        return string_result


if __name__ == '__main__':

    columns = 5
    rows = [
            {"row_name": "1" , "row_value" : [0, 2, 4]},
            {"row_name": "2" , "row_value" : [1, 3]},
            {"row_name": "3" , "row_value" : [0, 3, 4]}
            ]

    dlx = DLXMatrix(columns)
    for row in rows:
        dlx.add_sparse_row(row)
    print(dlx)
    dlx.cover(1)
    print(dlx)
    dlx.uncover(1)
    print(dlx)

class CSP:
    """
        Class that represents an instance of a Constraint Satisfaction Problem
        A CSP has variables, a domain for each variable, a list of neighbors for each variable
        and a constraints function that 'tells' if two neighbors X and Y can have values x and y respectively
    """
    def __init__(self):
        self.variables = []
        self.domains = {}
        self.neighbors = {}
        self.constraints = lambda X, x, Y, y : True

    def check_consistency(self, X, x):
        for Y in self.neighbors[X]:
            if self.assigned(Y) and not self.constraints(X, x, Y, self.get(Y)):
                return False
        return True

    def assigned(self, X):
        """
            Returns True if variable has already been assigned a value
        """
        return len(self.domains[X]) == 1

    def get(self, X):
        """
            Get Value of an already assigned variable
        """
        return self.domains[X][0]

    def count_inconsistencies(self):
        """
            Count number of inconsistencies between all pairs of variables
        """
        result = 0
        for X in self.variables:
            for Y in self.neighbors[X]:
                if not self.constraints(X, self.get(X), Y, self.get(Y)):
                    result += 1
        return result // 2

    def is_complete(self):
        """
            Returns True if all variables are set to their value (domain has only one value)
            and that all the constraints between variables are satisfied
            Else returns False
        """
        for X in self.variables:
            if len(self.domains[X]) != 1:
                 return False
        return self.count_inconsistencies() == 0


    def get_unassigned_variable(self):
        """
            Returns an unassigned variable with the least number of values in its domain
        """
        result = None
        for X in self.variables:
            if not self.assigned(X):
                if result == None or len(self.domains[X]) < len(self.domains[result]):
                    result = X
        return result


    def ordered_domain_values(self, X):
        """
            Sort domain values x of X according to the number of ruled out
            values in X's neighbors' domains if we assign x to X.
        """
        nb_ruled_out = {}
        for x in self.domains[X]:
            nb_ruled_out_x = 0
            for Y in self.neighbors[X]:
                for y in self.domains[Y]:
                    if not self.constraints(X, x, Y, y):
                        nb_ruled_out_x += 1
            nb_ruled_out[x] = nb_ruled_out_x

        return sorted(self.domains[X], key = (lambda x : nb_ruled_out[x]))

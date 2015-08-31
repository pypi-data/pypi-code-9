"""
Class definition for LinearSolver
"""
import Solver

class LinearSolver(Solver.Solver):
    """
    This class represents a linearsolver structure that represents all the information about the method
    used to solve.
    """

    def __init__(self, parameters = None):
        """
        It initializes a Linear Solver with a dictionary that contains parameters that specify the used methods.
        """
        Solver.Solver.__init__(self, parameters)

    def solve(self, rhs):
        """
        This method solves a linear system for the right-hand side value rhs.  
        OUTPUT: Status : 0: method has converged
                         k>0: method has not converged for some reason
        The method needs to be re-implemented in concrete subclass.                         
        """
        raise NotImplementedError, "a solve() method needs to be implemented for each linear solver"


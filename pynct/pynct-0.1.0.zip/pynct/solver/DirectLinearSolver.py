"""
Class definition of DirectLinearSolver
"""

import scipy
import LinearSolver
import scipy.sparse.linalg
from scipy.sparse import csr_matrix
from time import clock

class DirectLinearSolver(LinearSolver.LinearSolver):
    """
    This class implements a direct linear solver. 
    """

    def __init__(self, param = None):
        """ 
        It initializes a DirectLinearSolver object with a dictionary that contains
        parameters that specify the used methods.
        input:parameters (dict) 
                You can get a sample dictionary by looking at 
                getDefaultParameters()      
        """
        LinearSolver.LinearSolver.__init__(self, param)
        
    def getDefaultParameters():
        """
        This method returns a dictionary of default parameters 
            'print'      : 'none' (prints nothing)
                           'long' (prints solution)
        """
        param = {}
        param['print'] = 'none'
        return param
    getDefaultParameters = staticmethod(getDefaultParameters)

    def solve(self, rhs):
        """ 
        This method overrides LinearSolver.solve. It solves a linear system J*x = rhs 
        with a direct solve using scipy.sparse.linalg.spsolve.
        INPUT: rhs: the right-hand side value
        OUTPUT: x: vector with the solution
                status:  always 0, indicating that the method has converged.
        """
        A = self.point.computeJacobian()
        J = csr_matrix(A)
        x = scipy.sparse.linalg.spsolve(J,rhs)
        status = 0
        return (x, status)


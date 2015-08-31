"""
Class definition for GMRESLinearSolver
"""
from scipy.sparse.linalg import gmres
from scipy.linalg import norm
from scipy.sparse.linalg import LinearOperator
from scipy.sparse.linalg import spsolve
import LinearSolver
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class GMRESLinearSolver(LinearSolver.LinearSolver):
    """
    This class implements a GMRES solver.
    """
     
    def __init__(self, param = None):
        """ 
        It initializes a GMRESLinearSolver object with a dictionary that contains
        parameters that specify the used methods.
        INPUT:parameters (dict) 
                You can get a sample dictionary by looking at 
                getDefaultParameters()      
        """
        LinearSolver.LinearSolver.__init__(self, param)
    
    def getDefaultParameters():
        """
        This method returns a dictionary of default parameters: 
            'print'      : 'none' (prints nothing)
                           'short' (print a line for every iteration)
                           'long' (prints solution)
            'restart'    : number of iterations before GMRES restarts
            'tol'        : relative tolerance to achieve
            'relative'   : False
                           If True, the 'tol' parameter is considered relative
                            with respect to the right-hand side.
        """
        param = {}
        param['print'] = 'short'
        param['restart'] = 200
        param['tol'] = 1e-6
        param['relative'] = False
        param['rel_tol'] = 0.5
        param['max_iter'] = 100
        param['preconditioning'] = False
        return param
    getDefaultParameters = staticmethod(getDefaultParameters)

    def solve(self, rhs):
        """ 
        This method overrides LinearSolver.solve. It solves the linear system J*x = rhs 
        with GMRES iterations using a preconditioner. It stops when the maximum number 
        of iterations has been reached, OR the relative OR absolute tolerance have been reached.
        INPUT: rhs: the right-hand side
        OUTPUT: x: vector with the solution
                status  0: method has converged
                        k>0 : maximum number of iterations reached
                        k<0 : illegal input or breakdown
        """
        tol = self.param['tol']
        if self.param['relative']:
            tol = max(self.param['rel_tol']*norm(rhs), tol)
        print_it = self.param['print']
        restart = self.param['restart']
        maxiter = self.param['max_iter']
        preconditioning = self.param['preconditioning']

        n = rhs.size
        A = LinearOperator((n,n), matvec=self.point.matvec, dtype=float)
        if preconditioning:
            M_x = lambda x: self.point.psolve(x)
            M = LinearOperator((n,n), M_x)
            x,info=gmres(A,rhs,M=M,tol=tol,restart=restart,maxiter=maxiter)
        else:
            x,info=gmres(A,rhs,tol=tol,restart=restart,maxiter=maxiter)
        err0 = norm(A.matvec(x) - rhs) / norm(rhs)
        if print_it=='long':
            logger.info("GMRES ||r|| / ||rhs|| = {0}".format(err0))
        return (x, info)


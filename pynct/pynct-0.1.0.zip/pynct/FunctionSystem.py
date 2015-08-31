'''
Class definition for FunctionSystem
'''
import scipy
import logging
from scipy.linalg import norm
import System

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class FunctionSystem(System.System):

    def __init__(self, u, lambd, parameters = None):
        """
        It initializes a system with the current state and parameter values.
        """
        logger.debug("FunctionSystem init")
        System.System.__init__(self, u, lambd, parameters)
        self.border_cache = None
        self.border_param = lambd

    def getDefaultParameters():
        """
        This method returns a dictionary of default parameters:
            eps: the norm of the perturbation on the state
                for the computation of matrix-vector products.
        """
        param = {}
        param['eps'] = 1e-6

        return param
    getDefaultParameters = staticmethod(getDefaultParameters)

    def setState(self, u, lambd, *args, **kwargs):
        """
        This method sets the current system state 
        (current state, parametervalues, residual of system (see apply) 
            and if there is a preconditioner for the jacobian (default = False)).
        """
        self.u = u
        self.lambd = lambd
        self.pjac_built = False

        if 'dont_eval_dudt' in args:
            self.u_Dt = None
        else:
            self.u_Dt = self.apply(u, lambd)

    def getResidual(self):
        """
        This method returns the residual of the system.
        """
        return self.u_Dt

    def apply(self, u, lambd):
        """
        This method returns solution u_Dt of the system.
        The method needs to be re-implemented in concrete subclass.
        """
        raise NotImplementedError, "apply() needs to be implemented by a subclass"

    def computeJacobian(self):
        """
        This method returns the approximated Jacobian of the system for the given
        state and parameter values. 
        The jacobian is approximated with finit differences. You can override it in concrete subclass.
        """
        n = len(self.u)
        J = sp.zeros((n,n), float)
        w = self.apply(self.u, self.lambd)
        eps = 1.0e-10
        for i in range(n):
            ei = sp.zeros(n)
            ei[i]=1
            v = (self.apply(u + eps*ei, lambd)-w)/eps
            J[:,i] = v
        return J

    def applyJacobian(self, v):
        """
        If the system Jacobian is J, this function returns J*v (an
        approximation with finite difference).
        """
        eps = self.param['eps']
        u_eps = self.u + eps*v
        u_eps_Dt = self.apply(u_eps, self.lambd)
        return (u_eps_Dt - self.u_Dt)/eps

    def getParameterDerivative(self, i):
        """
        This method returns the derivative with respect to parameter i.
        Approximation with finite difference.
        """

        if self.border_cache is None or (self.border_param-self.lambd).all:
            self.border_param=self.lambd
            eps = self.param['eps']
            pert = scipy.zeros((len(self.lambd),),scipy.float64)
            scipy.put(pert,i,eps)
            lambd=self.lambd+pert
            u_eps_Dt = self.apply(self.u,lambd)
            self.border_cache =(u_eps_Dt-self.u_Dt)/eps
        return self.border_cache

    def applyPreconditioner(self, v):
        """
        This method performs a matrix-vector product with the systems
        preconditioner. If the preconditioning matrix is M, this system
        returns M*v
        """
        A=self.pjac()
        return scipy.dot(A, v)

    def solvePreconditioner(self, rhs, rows, cols):
        """
        This method solves a linear system with the preconditioning matrix.
        So far, only a direct, full solver has been implemented.
        input:   rhs: contains the right-hand side of the system to solve
                 rows: contains a number of extra rows that come from external
                constraints
                 cols:    contains a number of extra columns that contain entries
                stemming from free parameters
        """
        if not self.pjac_built:
            A = self.pjac() #* self.param['Dt']
            self.A = A
            self.pjac_built = True
        else:
            A = self.A
        n = scipy.shape(A)[0]
        I=scipy.identity(n, scipy.float64)
        cols[:n,:] = - scipy.dot(I-A, cols[:n,:])
        rhs[:n] = - scipy.dot(I-A, rhs[:n])
        A = scipy.r_[A, rows]
        A = scipy.c_[A, cols]
        x = scipy.linalg.solve(A, rhs)
        return x

    def pjac(self):
        """
        This method computes a preconditioned jacobian.
        The method needs to be re-implemented in concrete subclass.
        """
        raise NotImplementedError, "The pjac method " + \
            "needs to be implemented for a concrete system. \n" +\
            "Alternatively, you can overrride solvePreconditioner()."



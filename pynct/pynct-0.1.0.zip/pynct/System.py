'''
Class definition for System
'''
from abc import ABCMeta
from abc import abstractmethod
import scipy
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class System(object):

    __metaclass__ = ABCMeta

    def __init__(self, u, lambd, parameters = None):
        """
        It initializes a system with the current state and parameter values.
        """
        logger.debug("System init")
        if parameters == None:
            logger.debug("Using default parameters")
            self.param = self.getDefaultParameters()
        else:
            self.param = parameters
        self.setState(u, lambd)

    @staticmethod
    def getDefaultParameters():
        return

    def setState(self, u, lambd):
        """
        This method sets the current system state (current state and parameter values).
        """
        self.u = u
        self.lambd = lambd
        
    @abstractmethod
    def getResidual(self):
        """
        This method returns the residual of the system.
        The method needs to be re-implemented in concrete subclass.
        """
        raise NotImplementedError, "getResidual() needs to be implemented in subclass"
            
    @abstractmethod
    def apply(self, u, lambd):
        """
        This method applies the system.
        The method needs to be re-implemented in concrete subclass.
        """
        raise NotImplementedError, "apply() needs to be implemented by a subclass"

    @abstractmethod
    def computeJacobian(self):
        """
        This method returns the Jacobian of the system for the given state and 
        parameter values.
        The method needs to be re-implemented in concrete subclass.
        """
        raise NotImplementedError, "computeJacobian() needs to be implemented in subclass"
    
    @abstractmethod
    def applyJacobian(self, v):
        """
        This method returns the Jacobian-vector product of the system Jacobian 
        with the vector v.
        The method needs to be re-implemented in concrete subclass.
        """
        raise NotImplementedError, "applyJacobian() needs to be implemented in subclass"

    @abstractmethod
    def getParameterDerivative(self, i):
        """
        This method returns the derivative with respect to parameter i.
        The method needs to be re-implemented in concrete subclass.
        """
        raise NotImplementedError, "getParameterDerivative() needs to be implemented by a subclass"

    @abstractmethod
    def applyPreconditioner(self, v):
        """
        This method returns the preconditioned vector product of the system with the vector v.
        The method needs to be re-implemented in concrete subclass.
        """
        raise NotImplementedError, "applyPreconditioner() needs to be implemented by a subclass"

    @abstractmethod
    def solvePreconditioner(self, v, rows , cols, lambd):
        """
        This method solves a linear system with the preconditioning matrix
        Input:  rhs  :  the right-hand side of the system to solve
                rows :  extra rows relating to external constraints
                cols :  extra columns relating to free parameters
        The method needs to be re-implemented in concrete subclass.
        """
        raise NotImplementedError, "solvePreconditioner() needs to be implemented by a subclass"

            



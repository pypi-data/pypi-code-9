"""
Class definition for NewtonSolver
"""
import scipy
import Solver
import LinearSolver
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class NewtonSolver(Solver.Solver):
    """
    This class implements a Newton solver. 
    """

    def __init__(self, linear_solver, parameters = None):
        """ 
        It initializes a Newton Solver object with a dictionary that contains
        parameters that specify the used methods.
        input: linear_solver (LinearSolver) : contains the linear solver that 
                will be used in each Newton iteration
               parameters (dict): You can get a sample dictionary by looking at 
                getDefaultParameters()
        """
        Solver.Solver.__init__(self, parameters)
        if isinstance(linear_solver, LinearSolver.LinearSolver):
            self.linsolv = linear_solver
        else:
            raise TypeError, "input argument " + linear_solver + " should be a linear solver"
        self.nb_newt = 0
    
    def getDefaultParameters():
        """  
        This method returns a dictionary of default parameters: 
            'maxIter'      : 10
            'relTol'       : 1e-6
            'absTol'       : 1e-8
            'damping'      : 1 (means no damping)
            'print'   : 'short'  (one line per iteration containing norms)
                    'long' (residual in each iteration)
                    'none' (prints nothing)
        """
        param = {}
        param['max_iter']=10
        param['rel_tol']=1e-6
        param['abs_tol']=1e-8
        param['print']='short'
        param['damping']=1 
        param['stop']="res"
        return param
    getDefaultParameters = staticmethod(getDefaultParameters)
       
    def solve(self):
        """
        This method performs Newton iterations, starting from x0.  It stops when the 
        maximum number of iterations has been reached, OR the 
        relative OR absolute tolerance have been reached.
        OUTPUT: Status  0: method has converged
                        1: method has used maximum number of iterations without convergence
        """
        iter = 0
        max_iter = self.param['max_iter']
        abs_tol = self.param['abs_tol']
        rel_tol = self.param['rel_tol']
        print_it = self.param['print']
        alpha = self.param['damping']
        stop = self.param['stop']
        
        res = self.point.getResidual()
        x = self.point.getCurrentGuess()
        res_norm = scipy.linalg.norm(res)
        if stop == "step":
            stop_norm = 0
        elif stop == "res":
            stop_norm = res_norm
            
        while iter==0 or (iter < max_iter and stop_norm > abs_tol):
            iter += 1
            self.nb_newt += 1
            dx, status = self.linsolv.solve(-res)
            step_norm = scipy.linalg.norm(dx)
            x=x+alpha*dx
            # Handling of errors and printing
            if not status == 0:
                logger.warning("An error has occurred in solving the linear system")
            # print the iterations
            if not print_it=='none':
                logger.info("Iteration: {0}, |residual|: {1}, |step|: {2}".format(iter, res_norm, step_norm))
            if print_it=='long':
                print "Newton Residual"
                for i in range(len(res)):
                    print i, res[i]
                print "---------------------"
                print "Newton Current Guess"
                for i in range(len(x)):
                    print i, x[i]
                print "---------------------"
                print " Newton Step"
                for i in range(len(x)):
                    print i, dx[i]
                print "---------------------"
            self.point.setCurrentGuess(x)
                                        
            res = self.point.getResidual()
            res_norm = scipy.linalg.norm(res)
            if stop == "step":
                stop_norm = scipy.linalg.norm(dx)
            elif stop == "res":
                stop_norm = scipy.linalg.norm(res)
        if not print_it == None:
            logger.info("Final |residual|: " + str(res_norm))
        if iter == max_iter:
            status = 1
        else:
            status = 0
        return status

    def setPoint(self,point):
        self.linsolv.setPoint(point)
        Solver.Solver.setPoint(self,point)


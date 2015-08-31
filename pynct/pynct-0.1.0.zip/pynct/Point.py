'''
Class definition for Point.
'''

import scipy
from scipy.linalg import norm
from scipy.linalg import eig
import solver.Solver as Solver
import System


class Point(object):
    """ 
    This class represents a point structure, which can be used to store different types
    of attractors and correct them.
    As a user, you should only care about the methods
        - getDefaultParameters()
        - getState()/setState()
        - mspectrum(), pspectrum(), spectra()
        - correct()
        - copy()

    The following methods are used by the solvers
        - matvec(), pmatvec()
        - psolve()
        - getResidual()
        - setCurrentGuess()
        - getCurrentGuess()
        - axpy() (used in continuation)
        - computeJacobian()
        
    The following methods are used only internally
        - MatrixVectorProduct()
        - spectrum()
    """ 

    def __init__(self, system, solver, param = None):
        """ 
        It initializes a point object with a system object, a solver object, a dictionary
        that contains parameters that specify the used methods, the vector with the current 
        state and a list with the parameters of the system.
        input: 
            system (System)             
                contains the concrete equations
            solver (Solver) 
                contains the nonlinear solver that will be used 
            parameters (dict) 
                look at the docstring of getDefaultParameters() 
                to find out which fields there are
        """
        if isinstance(system, System.System):
            self.system = system
        else:
            raise TypeError, "first argument should be a system"
        if isinstance(solver, Solver.Solver):
            self.solver = solver
        else:
            raise TypeError, "second argument should be a solver"
        self.solver.setPoint(self) # make sure that the solver knows the point
        if param == None:
            param = self.getDefaultParameters()
        self.param = {}
        self.param['free'] = param['free'][:]
        self.param['artificial'] = param['artificial'][:]
        self.param['extra_condition'] = param['extra_condition']
        self.param['artificial_condition'] = param['artificial_condition']
        self.extra_condition = param['extra_condition']
        self.artificial_condition = param['artificial_condition']
        self.nb_matvec = 0
        self.u = self.system.u
        self.lambd = self.system.lambd[:]
    
    @staticmethod
    def getDefaultParameters():
        """  
        This method returns a dictionary of default parameters: 
            free : list of indices of the free model parameters,
            artficial : list of indices of artificially added free parameters,
            extra_condition : a list of functions containing 
                              extra conditions,
            artificial_condition : a list of function containing 
                                   artificial extra conditions.
        """
        param = {}
        param['free'] = []
        param['artificial'] = []
        param['extra_condition'] = []
        param['artificial_condition'] = []
        return param

    def setState(self, u, lambd, *args, **kwargs):
        """
        This method sets the current state (current state and parameter values).
        """
        self.u = u
        self.lambd = lambd
        self.system.setState(u, lambd, *args, **kwargs)
    
    def getState(self):
        """
        This method returns the current state(u, lambd).
        """
        return self.u, self.lambd

    def setCurrentGuess(self, x):
        """
        This method sets the current state with vector x.
        INPUT: The vector x contains the current guess of the solution.
        DATA LAYOUT: The vector "x" has a part "u"  that describes the
        current solution, "free" for values of the free parameters 
        and a part "art" containing the values of the artificial
        parameters.
        
             [       ]
             [   u   ]
         x = [       ]
             [ ----- ]
             [  free ]
             [  art  ]
        """     
        n = len(self.u)
        l = len(self.param['free'])
        u = x[:n]
        lambd = self.lambd
        scipy.put(lambd,self.param['free'], x[n:n+l])
        scipy.put(lambd,self.param['artificial'], x[n+l:])
        self.setState(u, lambd)

    def getCurrentGuess(self):
        """
        This method returns the current guess of the solution.         
        DATA LAYOUT: The vector "x" has a part "u"  that describes the
        current solution, "free" for values of the free parameters 
        and a part "art" containing the values of the artificial
        parameters.
        
             [       ]
             [   u   ]
         x = [       ]
             [ ----- ]
             [  free ]
             [  art  ]

        """
        u = self.u
        lfree = scipy.take(self.lambd,self.param['free'])
        lart  = scipy.take(self.lambd,self.param['artificial'])
        return scipy.r_[u, lfree, lart]

    def getResidual(self):
        """
        This method returns the residual associated with the current guess 
        The residual consists of (system.getResidual(), residual of extra conditions and 
        residual of artificial extra conditions)
        """
        l = len(self.param['free'])
        a = len(self.param['artificial'])
        extra = []
        for i in range(l):
            extra.append(self.extra_condition[i](self))
        artificial = []
        for i in range(a):
            artificial.append(self.artificial_condition[i](self, self.param['artificial'][i]))
        res = self.system.getResidual()
        for i in range(a):
            res +=artificial[i]['eq_term']
        for i in range(l):
            r = extra[i]['res']
            res = scipy.r_[res,r]
        for i in range(a):
            r = artificial[i]['res'] 
            res = scipy.r_[res,r] 
        return res

    def computeJacobian(self): 
        """ 
        This method computes the full system matrix for a linear
        solve.  This consistes of the Jacobian of the underlying
        system, supplemented with the rows and columns that 
        come from additional constraints and free parameters.
        The Jacobian is approximated with finite difference.
        """
        free = self.param['free']
        art = self.param['artificial']
        n = len(self.u)
        l = len(free)
        a = len(art)
        extra = []
        for i in range(l):
            extra.append(self.extra_condition[i](self))
        artificial = []
        for i in range(a):
            artificial.append(self.artificial_condition[i](self))

        J = scipy.zeros((n+l+a,n+l+a),scipy.float64)
        J[:n,:n] = self.system.computeJacobian()

        # we want the total jacobian matrix to be
        #
        #[            |          |  j_art     ]  
        #[  msys      | j_free   | art[column]]  
        #[            |          |            ]  
        #[------------------------------------]  
        #[ extra[row] | extra[d] |      0     ]  
        #[ art[row]   |    0     |    art[d]  ]  
        # 
        J_free = scipy.zeros((n,l),scipy.float64)
        for i in range(l):
            J_free[:,i]=self.system.getParameterDerivative(free[i])
        J[:n,n:n+l]=J_free
    
        J_art = scipy.zeros((n,a),scipy.float64)
        for i in range(a):
            J_art[:,i]=artificial['column']
        #J[n+l:n+l+a,:n]=J_art
        J[:n,n+l:n+l+a]=J_art
        
        d_free = scipy.zeros((l,l+a),scipy.float64)
        for i in range(l):
            d_free[i,:]=extra[i]['d']
        J[n:n+l,n:n+l+a]=d_free
        
        d_art = scipy.zeros((a,l+a),scipy.float64)
        for i in range(a):
            d_art[i,:]=artificial[i]['d']
        J[n+l:n+l+a,n:n+l+a]=d_art
        
        rows = scipy.zeros((l+a,n),scipy.float64)
        for i in range(l):
            rows[i,:]=extra[i]['row']
        for i in range(a):
            rows[i,:]=artificial[i]['row']
        J[n:n+l+a,:n]=rows

        return J

    def matvec(self,s):
        """
        This method returns the matrix vector product, used in Krylov solvers.
        DATA LAYOUT: The vector "x" has a part "u"  that describes the
        current solution and a part "free" for the free parameters and a part for
        the artificial parameters.
        
            [   u   ]
            [       ]
        x=  [ ----- ]
            [  free ]
            [  art  ]
                                

        It uses the Jacobian vector product of the underlying
        system, and adds the effect of extra conditions and free
        parameters.
        The result is a matrix-vector product with the linearization of
        the full nonlinear determining system around the current guess. 
        """
        return self.MatrixVectorProduct(s, "jac")

    def pmatvec(self,s):
        """
        This method returns the matrix vector product with the preconditioner matrix,
        used in Krylov solvers.
        DATA LAYOUT: The vector "x" has a part "u"  that describes the
        current solution and a part "free" for the free parameters and a part for
        the artificial parameters.
        
            [   u   ]
            [       ]
        x=  [ ----- ]
            [  free ]
            [  art  ]
                                
       
        It uses the matrix vector product applyPreconditioner(v) of the underlying
        system, and adds the effect of extra conditions and free
        parameters.
        The result is a matrix-vector product with the linearization of
        the full nonlinear determining system around the current guess. 
        """
        return self.MatrixVectorProduct(s, "precond") 

    def MatrixVectorProduct(self, x, option):
        """
        This method returns the matrix vector product, used in Krylov solvers.
        INPUT:  x :the vector to be multiplied,
                option : "jac"  - compute Jacobian-vector product,  
                         "precond" - preconditioner-vector product.          
        USE: This method is used in the matvec routine. Do not use this method directly.
        DATA LAYOUT:  The vector "x" has a part "u"  that describes the
        current solution and a part "free" for the free parameters and a part for
        the artificial parameters.
        
            [   u   ]
            [       ]
        x=  [ ----- ]
            [  free ]
            [  art  ]
        It uses the matrix vector product (applyJacobian or applyPreconditioner depending on the option) 
        of the underlying
        system, and adds the effect of extra conditions and free
        parameters.
        The result is a matrix-vector product with the linearization of
        the full nonlinear determining system around the current guess.                         
        """
        free = self.param['free']
        art = self.param['artificial']
        n = len(self.u)
        l = len(free)
        a = len(art)
        extra = []
        for i in range(l):
            extra.append(self.extra_condition[i](self))
        artificial = []
        for i in range(a):
            artificial.append(self.artificial_condition[i](self, self.param['artificial'][i]))
        xu = x[:n]
        xfree = x[n:n+l]
        xart = x[n+l:]
        xu_norm = norm(xu)
                
        result=scipy.zeros(scipy.shape(x),scipy.float64)
        
        # obtain the first N rows of the matrix-vector product
        #[        |        |      ]    [   u   ]
        #[ J_u    | J_free |  row ]    [       ]
        #[        |        |      ]    [       ]
        #-------------------------]  * [ ----- ]
        #                              [  free ]
        #                              [  art  ]
        if not xu_norm==0:
            if option == "jac":
                Mv_u=self.system.applyJacobian(xu)
            if option == "precond":
                Mv_u=self.system.applyPreconditioner(xu)    
        else:
            Mv_u=xu  # xu will contain zeros
        
        for i in range(l):
            if not xfree[i]==0:
                Mv_u += xfree[i] * self.system.getParameterDerivative(free[i])
        for i in range(a):
            Mv_u += xart[i]*artificial[i]['column']
            
        result[:n]=Mv_u

        xparam = scipy.r_[xfree,xart]
        
        # the rows of the extra conditions are added
        #                              [   u   ]
        #                              [       ]
        #                              [       ]
        #-------------------------]  * [ ----- ]
        #[  row   |   d    |  0   ]    [  free ]
        #                              [  art  ]
        Mv_free=scipy.zeros(scipy.shape(free),scipy.float64)
        for i in range(l):
            Mv_free[i]=scipy.dot(extra[i]['row'],xu) + scipy.dot(extra[i]['d'],xparam)
        result[n:n+l]=Mv_free
        # the rows of the artificial conditions are added
        #                              [   u   ]
        #                              [       ]
        #                              [       ]
        #-------------------------]  * [ ----- ]
        #                              [  free ]
        # [ row    | 0      | d   ]    [  art  ]
        Mv_art=scipy.zeros(scipy.shape(art),scipy.float64)
        for i in range(a):
            Mv_art[i]=scipy.dot(artificial[i]['row'],xu) + scipy.dot(artificial[i]['d'],xparam)
        result[n+l:]=Mv_art
        return result

    def psolve(self, rhs):
        """
        This method solves a linear system M*x = b, which 
        closely ressembles the linear system A*x = b as a
        preconditioner.
        This solve is done together with each matrix-vector product
        inside any Krylov method.
        The matrix M contains the preconitioner matrix of the system,
        bordered with the extra and artificial conditions.
        
        INPUT:   rhs     Right-hand side

        REMARK: The underlying system should define a preconditioning method.
        This method is to solve the full linear preconditioning system.  
        The method defined here adds the borders that arise due to extra 
        conditions and passes the psolve request to the underlying system.        
        """
        free = self.param['free']
        art = self.param['artificial']
        n = len(self.u)
        l = len(free)
        a = len(art)
        extra = []
        for i in range(l):
            extra.append(self.extra_condition[i](self))
        artificial = []
        for i in range(a):
            artificial.append(self.artificial_condition[i](self, self.param['artificial'][i]))
            
        # we want the total preconditioning matrix to be
        #
        #[            |          |            ]    [   x   ]
        #[      Msys  | J_free   |    J_art   ]    [       ]
        #[            |          |            ]    [       ]
        #[------------------------------------]  * [ ----- ]
        #[ extra[row] | extra[d] |      0     ]    [  free ]
        #[ art[row]   |    0     |    art[d]  ]    [  art  ]
        # 
        cols = scipy.zeros((n+l+a,l+a),scipy.float64)
        
        J_free = scipy.zeros((n,l),scipy.float64)
        for i in range(l):
            J_free[:,i] = self.system.getParameterDerivative(free[i])
        cols[:n,:l] = J_free

        J_art = scipy.zeros((n,a),scipy.float64)
        for i in range(a):
            J_art[:,i] = artificial[i]['column']
        cols[:n,l:l+a] = J_art
        
        for i in range(l):
            cols[n+i,:] = extra[i]['d']
        for i in range(a):
            cols[n+l+i,:] = artificial[i]['d']

        rows = scipy.zeros((l+a,n),scipy.float64)
        for i in range(l):
            rows[i,:] = extra[i]['row']
        for i in range(a):
            rows[l+i,:] = artificial[i]['row']
            
        x = self.system.solvePreconditioner(rhs,rows,cols)
        return x

    def mspectrum(self):
        """ 
        This method returns the spectrum of the Jacobian.
        OUTPUT: e -- eigenvalues of the Jacobian
                v -- eigenvectors of the Jacobian
        """
        return self.spectrum("jac")
        
    def pspectrum(self):
        """ 
        This method returns the spectrum of the preconditioner
        OUTPUT: e : eigenvalues of the Jacobian
                v : eigenvectors of the Jacobian
        """
        return self.spectrum("precond")    
        
    def spectrum(self, option):
        """ 
        This method returns the spectrum of the (approximated) Jacobian.
        Note: this is used internally.
        
        INPUT: option -- 
                "jac"  - compute Jacobian spectrum
                "precond" - compute preconditioner spectrum

        OUTPUT: e -- eigenvalues of the Jacobian
                v -- eigenvectors of the Jacobian
        """
        n = len(self.u)
        l = len(self.param['free'])
        a = len(self.param['art'])
        A = scipy.zeros((n+l+a,n+l+a),scipy.float64)
        for i in range(n+l+a):
            y = scipy.zeros((n+l+a,),scipy.float64)
            y[i] = 1
            # matrix of original system
            if option == "jac":
                A[i,:] = self.matvec(y)
            if option == "precond":
                A[i,:] = self.pmatvec(y)
        eA,vA = eig(A)
        return eA,vA

    def spectra(self):
        """ 
        This method returns the spectrum of the Jacobian A, the preconditioner M,
        and the resulting matrix M^(-1)*A .
        
        OUTPUT:  ej : eigenvalues of the Jacobian
                 ep : eigenvalues of the preconditioner
                 ec : eigenvalues of the product matrix
                 vj : eigenvectors of the Jacobian
                 vp : eigenvectors of the preconditioner
                 vc : eigenvectors of the product matrix
        """
        n=len(self.u)
        l=len(self.param['free'])
        a=len(self.param['artificial'])
        A=scipy.zeros((n+l+a,n+l+a),scipy.float64)
        B=scipy.zeros((n+l+a,n+l+a),scipy.float64)
        C=scipy.zeros((n+l+a,n+l+a),scipy.float64)
        for i in range(n+l+a):
            y=scipy.zeros((n+l+a,),scipy.float64)
            y[i]=1
            # matrix of original system
            A[i,:]=self.matvec(y)
            # matrix of preconditioned system
            B[i,:]=self.psolve(A[i,:])
            # matrix of preconditioner
            C[i,:]=self.pmatvec(y)

        ej,vj = eig(A)
        ec,vc = eig(B)
        ep,vp = eig(C)
        return ej,ep,ec,vj,vp,vc    
        
    def correct(self):
        """
        This method corrects the initial guess using self.solver.
        It returns 0 upon convergence.
        """
        return self.solver.solve()
        
    def axpy(self, a, pointy, *args, **kwargs):
        """
        This method returns a point object  that satisfies: a * point + pointy.
        """
        p = Point(self.system, self.solver, self.param)
        p.setState(a * self.u + pointy.u, a * self.lambd + pointy.lambd, *args, **kwargs)
        return p
        
    def copy(self):
        """
        This methods makes a copy of the current point and stores it in a new point object.
        """
        return Point(self.system, self.solver, self.param)
 

"""
Class definition for lemma_system
"""


import logging
import scipy as sp
import numpy as np
import pynct.FunctionSystem as fs
from sympy import *

from sympy.parsing.sympy_parser import parse_expr

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class lemma_system(fs.FunctionSystem):
    """
    This class solves a general system (that satisfies equations 1 and 2 in corresponding notes) of equations (apply) and calculates the exact Jacobian with SYMPY
    The system itself is given with parameters.
    """
    def __init__(self, u, lambd, tissue, model):
        """
        initializes a system with the current state and parameter values
            u    : array of values for the unknowns 
            lambd: a list of model parameters
            tissue: a tissue object
            model: a model object specifying the system
        """
        self.tissue = tissue
        self.model = model

        # CALCULATE wall lengths & cell areas and store in array for efficiency
        n_c = self.tissue.num_cells
        self.cells_area = np.array([self.tissue.get_area_of_cell(c_i) for c_i in xrange(n_c)])
        self.contact_area = np.zeros([n_c, n_c])
        for w_i in xrange(self.tissue.num_walls):
            [c_i,c_j] = self.tissue.walls_cells[w_i]
            if -1 not in [c_i,c_j]:
                l_ij = self.tissue.get_length_of_wall(w_i)
                self.contact_area[c_i,c_j] = l_ij
                self.contact_area[c_j,c_i] = l_ij

        # Filter out -1 cells in cell neighbors:
        # (this reduces 'if -1 != c_i:' all over the code, which is very slow)
        self.tissue.cells_cells = np.array(self.tissue.cells_cells)
        for c_i in xrange(n_c):
            self.tissue.cells_cells[c_i] = np.ma.masked_equal(self.tissue.cells_cells[c_i], -1).compressed()

        fs.FunctionSystem.__init__(self, u, lambd)
       
        
        
    def apply(self,u,lambd):
        """
        calculates the solution of the model for a given point and list of parameters
            u: array of values for the unknowns
            lambd: a list of model parameters
        """
        
        # the transport parameter
        T        = lambd[10]
        
        # RESTRUCTURE transport parameter
        parameterdict = {'b': lambd[0], 'kPIN':lambd[1], 'kT':lambd[2], 'kIAA':lambd[3], 'rhoPIN0':lambd[4], 
                         'rhoPIN':lambd[5], 'muPIN':lambd[6], 'muIAA':lambd[7], 'rhoIAA':lambd[8], 'D':lambd[9], 
                         'T':lambd[10]}
        
        # GET Number of cells / walls
        n_c = self.tissue.num_cells
        n_w = self.tissue.num_walls
        
        # EXTRACT AUXIN & PIN from u
        A = u[:n_c]
        P = u[n_c:]
                
        # INITIALIZE New vector with solutions
        AN = np.zeros(n_c)
        PN = np.zeros(n_c)

        # INITIALIZE unknowns in the SyMPy expressions
        a,p = symbols("a p")
        a_i, a_j = symbols("a_i a_j")
        wall_length = symbols("wall_length")
        
        # LOAD model 
        decayP = lambdify(p,self.decayPIN(parameterdict),'math')
        productionP = lambdify((a,p), self.productionPIN(parameterdict), 'math')
        productionA = lambdify(a,self.productionIAA(parameterdict), 'math')
        decayA = lambdify(a, self.decayIAA(parameterdict), 'math')
        pass_transport = lambdify((a_i,a_j, wall_length), self.passiveTransport(parameterdict), 'math')
        psi_ij = lambdify((a_i, a_j), self.psi_ij(parameterdict), 'math')
        phi = lambdify((a_j, wall_length), self.phi_ij(parameterdict), 'math')
                    
        # CALCULATE solution in every cell
        for c in xrange(n_c):
            # PIN equation =====================================================
            PN[c] = productionP(A[c], P[c]) - decayP(P[c])

            # AUX equation =====================================================
            passive_transport = 0.0
            active_transport = 0.0

            area = self.cells_area[c]
            # Accumulate passive & active transport over neighbors 
            for n in self.tissue.cells_cells[c]:
                l_cn = self.contact_area[c,n]
                # Passive transport:
                passive_transport += pass_transport(A[c],A[n],l_cn)/area
           
                # Active transport:
                denom = 0.0
                for nb in self.tissue.cells_cells[c]:
                    l_cnb = self.contact_area[c,nb]
                    denom += phi(A[nb],l_cnb)
                P_cn = P[c] * phi(A[n],l_cn) / denom

                denom = 0.0
                for nb in self.tissue.cells_cells[n]:
                    l_nnb = self.contact_area[n,nb]
                    denom += phi(A[nb], l_nnb)
                P_nc = P[n] * phi(A[c], l_cn) / denom

                active_transport += P_nc * psi_ij(A[n],A[c]) - P_cn * psi_ij(A[c], A[n])
            # Total IAA:
            AN[c] = productionA(A[c]) - decayA(A[c]) + passive_transport + T/area*active_transport
        
        unew = np.concatenate((AN, PN), axis=0)
        return unew

    def productionPIN(self, parameterdict):
        """
            setup the production part of the PIN equation
            parameterdict: a dictionary of the parameters
        """
        expr = parse_expr(self.model['productionPIN'], parameterdict)
        return expr
    
    def decayPIN(self, parameterdict):
        """
            setup the decay part of the PIN equation
            parameterdict: a dictionary of the parameters
        """
        expr = parse_expr(self.model['decayPIN'], parameterdict)
        return expr
    
    def productionIAA(self, parameterdict):
        """
            setup the production part of the IAA equation
            parameterdict: a dictionary of the parameters
        """
        expr = parse_expr(self.model['productionIAA'], parameterdict)
        return expr

    def decayIAA(self,parameterdict):
        """
            setup the decay part of the IAA equation
            parameterdict: a dictionary of the parameters
        """
        expr = parse_expr(self.model['decayIAA'], parameterdict)
        return expr
    
    def passiveTransport(self, parameterdict):
        """
            setup the passive transport part of the IAA equation
            parameterdict: a dictionary of the parameters
        """
        expr = parse_expr(self.model['passive_transport'], parameterdict)
        return expr
    
    
    def phi_ij(self,parameterdict):
        """
            setup a piece of the active transport part of the IAA equation
            parameterdict: a dictionary of the parameters
        """
        expr = parse_expr(self.model['phi'], parameterdict)
        return expr

    
    def psi_ij(self,parameterdict):
        """
            setup a piece of the active transport part of the IAA equation
            parameterdict: a dictionary of the parameters
        """
        expr = parse_expr(self.model['psi'], parameterdict)
        return expr
    
    
    
    def computeJacobian(self):
        """
            calculates the Jacobian of the current state. Here we opted to
            use the exact Jacobian.
        """
        return self.exactJacobian(self.u, self.lambd)

    def exactJacobian(self,u,lambd):
        """
            calculates analytically the exact Jacobian
            u    : array of values for the unknowns 
            lambd: a list of model parameters
        """    
        # GET Number of cells
        n_c = self.tissue.num_cells
        n_w = self.tissue.num_walls

        # EXTRACT AUXIN & PIN from u
        A = u[:n_c]
        P = u[n_c:]
        
        # INITIALIZE unknowns in the sympy expressions        
        a,p = symbols("a p")
        a_i, a_j, wall_length = symbols("a_i a_j wall_length")
        
        # RESTRUCTURE parameters        
        parameterdict = {'b': lambd[0], 'kPIN':lambd[1], 'kT':lambd[2], 'kIAA':lambd[3], 'rhoPIN0':lambd[4], 
                         'rhoPIN':lambd[5], 'muPIN':lambd[6], 'muIAA':lambd[7], 'rhoIAA':lambd[8], 'D':lambd[9], 
                         'T':lambd[10]}
        
        # INITIALIZE different parts of the jacobian matrix
        J_aa = sp.zeros((n_c,n_c), float) #derivative of equation a to a
        J_ap = sp.zeros((n_c,n_c), float) #derivative of equation a to p
        J_pa = sp.zeros((n_c,n_c), float) #derivative of equation p to a
        J_pp = sp.zeros((n_c,n_c), float) #derivative of equation p to p
        
        # LOAD IAA production and decay equation for Jacobian
        productionA_diff = lambdify(a, self.productionIAA(parameterdict).diff(a), 'math') 
        decayA_diff = lambdify(a,self.decayIAA(parameterdict).diff(a), 'math')
        
        # CALCULATE for every cell the IAA production - decay influence in jacobian 
        for c in xrange(n_c):
            J_aa[c,c] += productionA_diff(A[c]) - decayA_diff(A[c])
        # LOAD PIN1 production and decay equation for Jacobian
        productionP_diff_p = lambdify((a,p), self.productionPIN(parameterdict).diff(p), 'math')
        productionP_diff_a = lambdify((a,p), self.productionPIN(parameterdict).diff(a), 'math')
        decayP_diff = lambdify(p, self.decayPIN(parameterdict).diff(p), 'math')
        
        # CALCULATE for every cell the PIN production -decay influence in Jacobian
        for c in xrange(n_c):
            J_pp[c,c] += productionP_diff_p(A[c], P[c]) - decayP_diff(P[c])
            J_pa[c,c] += productionP_diff_a(A[c], P[c])
        
        # LOAD IAA Diffusion equation for Jacobian
        pass_transport_diff_ai = lambdify((a_i,a_j,wall_length), self.passiveTransport(parameterdict).diff(a_i), 'math')
        pass_transport_diff_aj = lambdify((a_i,a_j,wall_length), self.passiveTransport(parameterdict).diff(a_j), 'math')
        
        #CALCULATE for every cell the IAA diffusion influence in Jacobian
        for c in xrange(n_c):
            area = self.cells_area[c]
            for n in self.tissue.cells_cells[c]:
                l_cn = self.contact_area[c,n]
                J_aa[c,c] += pass_transport_diff_ai(A[c],A[n],l_cn)/area
                J_aa[c,n] += pass_transport_diff_aj(A[c],A[n],l_cn)/area
        
        # LOAD IAA Active Transport part for Jacobian     
        phi = lambdify((a_j, wall_length), self.phi_ij(parameterdict), 'math')
        phi_diff = lambdify((a_j, wall_length), self.phi_ij(parameterdict).diff(a_j), 'math')
        psi = lambdify((a_i,a_j), self.psi_ij(parameterdict), 'math')
        psi_diff_ai = lambdify((a_i, a_j), self.psi_ij(parameterdict).diff(a_i), 'math')
        psi_diff_aj = lambdify((a_i, a_j), self.psi_ij(parameterdict).diff(a_j), 'math')
        
        # CALCULATE for every cell the IAA active transport influence in Jacobian
        for  c in xrange(n_c):
            area = self.cells_area[c]
            for n in self.tissue.cells_cells[c]:
                # Active Transport n-> c : AT_{nc}
                J_aa[c,c] += self.derivActiveTransport_a_l(u, n, c, lambd, phi, phi_diff, psi, psi_diff_aj)/area   #derivActiveTransport_a_l(u,k,l, lambd) gives partial derivative of AT_{kl} to a_l 
                J_aa[c,n] += self.derivActiveTransport_a_k(u, n, c, lambd, phi, psi_diff_ai)/area   #derivActiveTransport_a_k(u,k,l, lambd) gives partial derivative of AT_{kl} to a_k
                J_ap[c,n] += self.derivActiveTransport_p_k(u, n, c, lambd, phi, psi)/area   #derivActiveTransport_p_k(u,k,l, lambd) gives partial derivative of AT_{kl} to p_k
                for nb in self.tissue.cells_cells[n]:
                    J_aa[c,nb] += self.derivActiveTransport_a_t(u, n, c, nb, lambd, phi, phi_diff, psi)/area
                # Active Transport c->n : AT_{cn} !!! negative term
                J_aa[c,n] -= self.derivActiveTransport_a_l(u, c, n, lambd, phi, phi_diff, psi, psi_diff_aj)/area
                J_aa[c,c] -= self.derivActiveTransport_a_k(u, c, n, lambd, phi, psi_diff_ai)/area
                J_ap[c,c] -= self.derivActiveTransport_p_k(u, c, n, lambd, phi, psi)/area
                for nb in self.tissue.cells_cells[c]:
                    J_aa[c,nb] -= self.derivActiveTransport_a_t(u, c, n, nb, lambd, phi, phi_diff, psi)/area
        
        # CONSTRUCT Jacobian from different parts
        J1 = np.concatenate((J_aa, J_ap),1)
        J2 = np.concatenate((J_pa, J_pp),1)
        J = np.concatenate((J1,J2))
        
        return J
    
                
    def derivActiveTransport_a_l(self, u, k, l, lambd, phi, phi_diff, psi, psi_diff_aj):
        """
            calculates for a cell the derivative to IAA in second cellnumber given of the active transport
            u    : array of values for the unknowns
            k: index of first cell
            l: index of second cell
            lambd: a list of model parameters
            phi, phi_diff, psi, psi_diff_aj: model parts
        """    
        T        = lambd[10]
        # Number of cells
        n = self.tissue.num_cells
        ## AUXIN & PIN extracted from u
        A = u[:n]
        P = u[n:]
        # calculate the derivative of the active transport to a_l
        l_kl = self.contact_area[k,l] # Note l_lk = l_kl
        neighbor_sum = 0
        for s in self.tissue.cells_cells[k]:
            l_sk = self.contact_area[s,k] # Note l_sk = l_ks
            neighbor_sum += phi(A[s],l_sk)
        deriv_a_l = T*P[k]*(phi_diff(A[l], l_kl))/(neighbor_sum) * psi(A[k], A[l]) + T*P[k]*(phi(A[l], l_kl))/(neighbor_sum)*psi_diff_aj(A[k], A[l])
        
        return deriv_a_l
    
    def derivActiveTransport_a_k(self,u, k, l, lambd, phi, psi_diff_ai):
        """
            calculates for a cell the derivative to IAA in first cellnumber given of the active transport
            u    : array of values for the unknowns
            k: index of first cell
            l: index of second cell
            lambd: a list of model parameters
            phi, psi_diff_ai: model parts
        """
        T      = lambd[10]
        # Number of cells
        n = self.tissue.num_cells
        ## AUXIN & PIN extracted from u
        A = u[:n]
        P = u[n:]
        # calculate the derivative of the active transport to a_k
        l_kl = self.contact_area[k,l] # Note l_lk = l_kl
        neighbor_sum = 0
        for s in self.tissue.cells_cells[k]:
            l_sk = self.contact_area[s,k] # Note l_sk = l_ks
            neighbor_sum += phi(A[s],l_sk)
        deriv_a_k = T*P[k]*phi(A[l],l_kl)/(neighbor_sum)*psi_diff_ai(A[k],A[l])
        
        return deriv_a_k
    
    
    def derivActiveTransport_a_t(self,u, k, l, t, lambd, phi, phi_diff, psi):
        """
            calculates for a cell the derivative to IAA in third cellnumber given of the active transport
            u    : array of values for the unknowns
            k: index of first cell
            l: index of second cell
            t: index of third cell
            lambd: a list of model parameters
            phi, phi_diff, psi: model parts
        """ 
        T        = lambd[10]
        # Number of cells
        n = self.tissue.num_cells
        ## AUXIN & PIN extracted from u
        A = u[:n]
        P = u[n:]
        # calculate the derivative of the active transport to a_t where t is a neighbor of the neighbor
        l_kl = self.contact_area[k,l] # Note l_kl = l_lk
        l_kt = self.contact_area[k,t] # Note l_kt = l_tk
        neighbor_sum = 0
        for s in self.tissue.cells_cells[k]:
            l_sk = self.contact_area[s,k] # Note l_sk = l_ks
            neighbor_sum += phi(A[s], l_sk)
        deriv_a_t = -T*P[k]*phi(A[l], l_kl)*phi_diff(A[t], l_kt)/(neighbor_sum**2)*psi(A[k], A[l])
        
        return deriv_a_t
    
    def derivActiveTransport_p_k(self, u, k, l, lambd, phi, psi):
        """
            calculates for a cell the derivative to PIN in first cellnumber given of the active transport
            u    : array of values for the unknowns
            k: index of first cell
            l: index of second cell
            lambd: a list of model parameters
            phi, psi: model parts
        """ 
        T        = lambd[10]
        # Number of cells
        n = self.tissue.num_cells
        ## AUXIN & PIN extracted from u
        A = u[:n]
        P = u[n:]
        # calculate the derivative of the active transport to p_k
        l_kl = self.contact_area[k,l] # Note l_kl = l_lk
        neighbor_sum = 0
        for s in self.tissue.cells_cells[k]:
            l_sk = self.contact_area[s,k] # Note l_sk = l_ks
            neighbor_sum += phi(A[s], l_sk)
        deriv_p_k = T*phi(A[l], l_kl)/(neighbor_sum)*psi(A[k], A[l])
        
        return deriv_p_k


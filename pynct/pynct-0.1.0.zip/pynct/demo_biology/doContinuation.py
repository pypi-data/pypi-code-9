"""
CALCULATION of SOLUTION BRANCH with CONTINUATION for a GENERAL TRANSPORT MODEL described in lemma_system.  
INPUT: parameter file that contains all the parameters of the model and the methods and a model file that contains the equations of 
the system. 
OUTPUT: file that contains the tissue and the continuation data
"""

import numpy as np
import pynct.solver.DirectLinearSolver as DL
import pynct.solver.NewtonSolver
import pynct.Point
import pynct.Continuer
import pynct.condition.arclength
import pynct.demo_biology.system.lemma_system
import pypts.tissue
import logging
import json
from sympy import symbols, lambdify
from sympy.parsing.sympy_parser import parse_expr

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def doContinuation(param_fname, model_fname):
    """
    Do the continuation. Calculate the solutions on the branch.
    """
    # ==========================================================================
    # ==========================================================================
    # LOAD the input files:
    # ==========================================================================
    # ==========================================================================
    # STEP 1: READ parameters and model from files
    with open(param_fname) as pf:
        param_info = json.load(pf)
    with open(model_fname) as mf:
        model_info = json.load(mf)
    ############################################################################
    ############################################################################



    # ==========================================================================
    # ==========================================================================
    # SETUP CONTINUATION:
    # ==========================================================================
    # ==========================================================================
    #STEP 1: LOAD tissue
    t = pypts.tissue.Tissue(param_info['input'])
    n = t.num_cells
    logger.info('Tissue has %d cells' % n)

    #STEP 2: RESTRUCTURE the modelparameters
    param_names = ['b', 'kPIN', 'kT', 'kIAA',
                   'rhoPIN0', 'rhoPIN', 'muPIN', 'muIAA',
                   'rhoIAA', 'D', 'T']
    # lambd = List of parameter values ordered by the above list of names
    lambd = np.array([param_info[name] for name in param_names])

    #STEP 3: FIND Solution point
    #OPTION 1: CALCULATE:
    if param_info['startpoint'] == 'value':
        a_expr = parse_expr(param_info['startpoint_a'], param_info)
        param_info['a'] = a_expr
        p_expr = parse_expr(param_info['startpoint_p'], param_info)
        x = symbols('x')
        a = lambdify(x,a_expr, 'math')
        p = lambdify(x,p_expr, 'math')
        av    = a(0)*np.ones(n)
        pv    = p(0)*np.ones(n)
        u     = np.concatenate((av, pv),axis=0)
    #OPTION 2: LOAD from tissue file 
    # by default the last step in the tissue is read. TODO: add parameter so it is possible to choose the step.
    elif param_info['startpoint'] == 'file':
       av = t.cells_attributes['IAA']
       pv = t.cells_attributes['PIN']
       u = np.concatenate((av, pv), axis=0)

    #STEP 4: CREATE System object
    smith_f = pynct.demo_biology.system.lemma_system.lemma_system(u, lambd, t, model_info)

    #STEP 5: CREATE Linear solver
    direct_param = DL.DirectLinearSolver.getDefaultParameters()
    linsolv = DL.DirectLinearSolver(direct_param)                                                       

    #STEP 6: CREATE Newton solver
    newt_param = pynct.solver.NewtonSolver.NewtonSolver.getDefaultParameters()
    newt_param['rel_tol'] = param_info['rel_newton_tol']
    newt_param['abs_tol'] = param_info['abs_newton_tol']
    newt_param['print'] = param_info['print_newton']
    newt_param['max_iter'] = param_info['max_newton_iterations']
    nsolv = pynct.solver.NewtonSolver.NewtonSolver(linsolv, newt_param)

    #STEP 7: FIND 2 starting points
    #OPTION 1: CALCULATE
    if param_info['startpoint'] == 'value':
        #first point
        point_param = pynct.Point.Point.getDefaultParameters()
        p = pynct.Point.Point(smith_f, nsolv, point_param)
        p.correct()
        #second point
        p2 = p.copy()
        lambd2 = np.array(lambd)
        lambd2[param_info['continuation_parameter']] = lambd[param_info['continuation_parameter']]+param_info['stepsize'] # normal + 0.05
        p2.setState(p.u, lambd2)
        p2.correct()
        points = [p, p2]
    #OPTION 2: LOAD from tissue file 
    elif param_info['startpoint'] == 'file':
        #TODO: load points from tissue file. Now use calculation to find second point
        #first point
        point_param = pynct.Point.Point.getDefaultParameters()
        p = pynct.Point.Point(smith_f, nsolv, point_param)
        p.correct()
        #second point
        p2 = p.copy()
        lambd2 = np.array(lambd)
        lambd2[param_info['continuation_parameter']] = lambd[param_info['continuation_parameter']]+param_info['stepsize'] # normal + 0.05
        p2.setState(p.u, lambd2)
        p2.correct()
        points = [p, p2]
    else: # parameter is wrong, raise error.
        raise ValueError, "startpoint input in parameterlist can only be: value or file"

    # STEP 8: SET Continuation parameters
    branch_param = pynct.Continuer.Continuer.getDefaultParameters()
    branch_param['free'] = [param_info['continuation_parameter']]
    branch_param['extra_condition'] = [pynct.condition.arclength.condition]
    branch_param['growth_factor'] = param_info['continuation_growth_factor'] #normal 1.05
    branch_param['print'] = param_info['print_continuation']
    ###############################################################################
    ###############################################################################



    # =============================================================================
    # =============================================================================
    # DO CONTINUATION AND SAVE:
    # =============================================================================
    # =============================================================================
    # STEP 1: INITIALIZE the branch
    branch = pynct.Continuer.Continuer(points, branch_param)

    ## STEP 2: SAVE the 2 points from setup
    # First point
    t.cells_attributes['IAA'] = branch.points[0].u[:t.num_cells]
    t.cells_attributes['PIN'] = branch.points[0].u[t.num_cells:]
    t.save(param_info['output'], 0, branch.points[0].lambd[param_info['continuation_parameter']])
    # Second point
    t.cells_attributes['IAA'] = branch.points[1].u[:t.num_cells]
    t.cells_attributes['PIN'] = branch.points[1].u[t.num_cells:]
    t.save(param_info['output'], 1, branch.points[1].lambd[param_info['continuation_parameter']])

    ## STEP 3: CALCULATE and SAVE other points on the branch
    def saveStep(point, p_idx, *args):
        t.cells_attributes['IAA'] = point.u[:t.num_cells]
        t.cells_attributes['PIN'] = point.u[t.num_cells:]
        # Saving to p_idx+2 to account for the two starting points
        t.save(param_info['output'], p_idx+2, point.lambd[param_info['continuation_parameter']])

        if 'refine' in args:
            logger.info('Removing last step')

    branch.bcontinue(param_info['continuation_points'], saveStep)

###############################################################################
###############################################################################

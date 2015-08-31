'''
Class definition for Continuer.
'''

import scipy
import logging
from scipy.linalg import norm

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Continuer(object):
    """
    This class represents a branch structure, containing a list of points obtained through 
    continuation. 
    """

    def __init__(self, points = None, params = None):
        """
        It initializes a continuer object with a list of points (a branch) and a dictionary 
        that contains parameters that specify  the used methods.
        INPUT: points: a list of points to start the branch
                    the minimum is 2
                    note that the points should have sufficient free
                    parameters
               params: dict
                    look at the docstring of getDefaultParameters()
                    to find out which parameters there are
        """
        for i in range(len(points)):
            points[i].param['free'] += params['free']   
            points[i].param['extra_condition'] += params['extra_condition']    
            points[i].extra_condition += params['extra_condition']    
        self.points = points
        self.bound_condition = params['bound_condition']
        if params == None:
            params = self.getDefaultParameters()
        self.param = params

    @staticmethod
    def getDefaultParameters():
        """
        This method returns a dictionary of default parameters.
            growth_factor: indicates the growth for the adaptive step
                    length after each successful step
                    default = 1.2
            print : *'short'* -- a line per corrected point
                    'none'  -- no printing 
        """    
        param = {}
        param['growth_factor'] = 1.2
        param['print'] = 'short'
        param['bound_condition'] = []
        return param

    def addPoint(self, point):
        """ 
        This method adds a point to the branch. 
        INPUT: point : a point object.
        """
        self.points.append(point)

    def removeLast(self):
        """ 
        This method removes the last point from the branch.
        """
        self.points = self.points[:-1]

    def bcontinue(self, nb_points, callback=None):
        """ 
        This method performs a continuation for this branch, adding nb_points
        points (or less, if there are failed Newton iterations)
        INPUT: nb_points: the number of points on the branch that will be calculated.
                callback: a callback function (for saving the calculated points)
        OUTPUT: succ : number of succesfull continuation steps
                fail : number of failures
                rjct: wether or not a point is rejected. This happens after 2 failures in a row.
                      if = 1, the continuation stops.
        """
        # internal parameters        
        tries = 0
        fail = 0
        rjct = 0
        successful = True
        kontinue = True
        bound = False
        # Number of points on the branch before continuation was started
        nstart_points = len(self.points)

        growth = self.param['growth_factor']

        l = len(self.points)
        if l <= 1:
            raise ValueError, "There should be two points in the branch"
        while kontinue and tries <= nb_points:
            logger.info('')
            logger.info('======= [ CONTINUATION STEP: {0} of {1} ] ======='.format(tries,nb_points))
            tries +=1
            l = len(self.points)
            prev_point = self.points[l-2]
            last_point = self.points[l-1]

            secant = last_point.axpy(-1,prev_point, 'dont_eval_dudt')
            dist = norm(secant.u) + norm(secant.lambd)
            if successful and not bound:  
                steplength = growth*dist
            elif not successful:
                steplength = -dist/2
            elif bound:
                steplength = steplength/2
                
            new_point = secant.axpy(-steplength/dist, last_point)
            new_point.secant = {}
            new_point.secant['u'] = secant.u
            new_point.secant['lambd'] = secant.lambd
            status = new_point.correct()
            if status == 0:
                new_success = True
            else: 
                new_success = False
            bound = self.boundCrossed(new_point)  # check if the bound is reached
            if not self.param['print']=='none':
                logger.info('Status: ' + ('OK' if status == 0
                                               else 'no convergence') +
                            ', Bound hit: ' + str(bound) +
                            ', Steplength: ' + str(steplength))
                logger.info('|u|: ' + str(norm(new_point.u)) +
                            ', lambd: ' + str(new_point.lambd.tolist()))

            if not new_success:
                fail += 1
                if not successful:  # this means that we had two failures
                                    # in a row
                    kontinue = False
                    rjct = rjct + 1
            else :  # if new_success
                if successful and not bound:
                    self.addPoint(new_point)
                    if callback:
                        callback(new_point, tries-1)
                elif not successful:   
                    self.removeLast()
                    self.addPoint(new_point)
                    self.addPoint(last_point)
                    if callback:
                        callback(new_point, tries-1, 'refine')
            successful = new_success
        succ = tries - fail
        return succ, fail, rjct

    def boundCrossed(self, point):
        """
        This method returns a boolean that represents whether the boundary is crossed.
        INPUT: point object. The method checks whether the boundary is crossed in this point. 
        """
        bound = False
        for bc in self.bound_condition:
            bound = bound or bc(point)
            if bound:
                break
        return bound



            
        



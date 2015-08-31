"""
Class definition for Solver
"""
class Solver(object):
    """
    This class represents a solver structure, that represents all the information about the method
    used to solve.
    """

    def __init__(self, parameters = None):
        """
        It initializes a Solver with a dictionary that contains parameters that specify the 
        used methods.
        """
        if parameters == None:
            self.param = self.getDefaultParameters()
        else:
            self.param = parameters

    def getDefaultParameters():
        raise NotImplementedError, "The default parameters have to be set for each solver"
    getDefaultParameters = staticmethod(getDefaultParameters)
    
    def setPoint(self, point):
        """
        This methods sets the point with the input parameter point.
        """
        self.point = point


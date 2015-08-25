"""
Created on Feb 16, 2015

@author: Jason Bowles
"""

class RawDataError(Exception):
    """
    Standard Error thrown... (TODO:) FIXME:
    """


    def __init__(self, err_cond):
        """
        Constructor
        """
        self.err_cond = err_cond
        
    
    def __str__(self):
        return  repr(self.err_cond)
        
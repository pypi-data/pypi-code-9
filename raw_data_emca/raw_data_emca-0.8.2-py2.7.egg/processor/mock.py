"""
Created on Feb 17, 2015

@author: Jason Bowles
"""
from rawdata_emca.processor import BaseProcessor

class MockProcessor(BaseProcessor):
    """
    A Mock processor just processes dummy data... designed to just show the way
    """
    
    def set_params(self, kwargs):
        """
        pass in the property file name to establish the connection criteria
        """
        self.load_params(kwargs)
        keys = kwargs.keys()
        for key in keys:
            self.param_dict[key] = kwargs[key]
                
        
    def execute_processor(self):
        """
        run the thing
        """
        print 'Now running a procesor.. '+self.name
        import time
        time.sleep(5)
        print self.param_dict
        print ' Working Directory is: '+self.entry.working_directory
        return 0
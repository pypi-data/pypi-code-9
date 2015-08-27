"""
Created on Feb 17, 2015

@author: Jason Bowles
"""
from rawdata_emca.runner.entry import RawEntry

class BaseProcessor(RawEntry):
    """
    All processors of data that plan on manipulating or cleaning data will extend this class
    """


    def __init__(self, params):
        """
        Constructor
        """
        super(BaseProcessor, self).__init__(params)
        ## class variables
        self.param_dict = {}
        self.set_params(params)
        self.log_message('Initialization complete',log_type='processor',status='running',step='execute entries',name=self.name,log_level=self.log_info())
        

    def set_params(self, kwargs):
        """
        Method designed to be over-ridden if needed, but basically just calls load_params(**kwargs) as the base implementation
        
        If overridden be sure to call load_params(**kwargs)
        """   
        self.load_params(kwargs)
        
        
    def execute_processor(self):
        """
        run the thing, this method should be overridden by the subclass
        """
        self.log_message( 'Now running a procesor.. '+self.name,name=self.name)
        print self.param_dict
        return 0
    
    def get_type(self):
        return self.PROCESSOR

if __name__ == "__main__":
    """
    allow to run outside of framework
    """
    params = {}
    base = BaseProcessor(params)
    base.execute_processor()
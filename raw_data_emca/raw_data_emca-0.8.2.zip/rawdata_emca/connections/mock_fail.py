"""
Created on Mar 13, 2015

@author: Jason Bowles
"""
from rawdata_emca.connections import BaseConnector

class MockFailConnector(BaseConnector):
    """
    This connector is designed to fail
    """


    def set_params(self, kwargs):
        """
        pass in the property file name to establish the connection criteria
        """
        self.load_params(kwargs)
        self.options = {}
        keys = kwargs.keys()
        self.rows = []
        self.throw_exc = False
        self.set_message("I will Fail!!!")
        for key in keys:
            if key.startswith("msg"):
                self.set_message(kwargs[key])
            elif key.startswith("exception"):
                self.throw_exc = bool(kwargs[key])
            else:
                self.options[key] = kwargs[key]
                
    def execute_connection(self):
        """ 
        just throw the error
        """
        import time
        time.sleep(4)
        if self.throw_exc:
            raise Exception(self.message)
        return 1
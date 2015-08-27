"""
Created on Feb 17, 2015

@author: Jason Bowles
"""
from rawdata_emca.connections import BaseConnector

class MockConnector(BaseConnector):
    """
    This is a simple connector that can mock up data and create the csv output
    """


    def set_params(self, kwargs):
        """
        pass in the property file name to establish the connection criteria
        """
        self.load_params(kwargs)
        self.options = {}
        keys = kwargs.keys()
        self.rows = []
        for key in keys:
            if key.startswith("header"):
                self.header = kwargs[key]
            elif key.startswith("row"):
                self.rows.append(kwargs[key])
            else:
                self.options[key] = kwargs[key]
                
    def execute_connection(self):
        """ 
        This just collects the hard coded data listed in configuration file
        """
        self.entry.temp_results = "TempCSV"
        csv_in = self.get_temp_csv_name()
        
        header = []
        i = 0
        hdict = {}
        for col in self.header.split(","):
            header.append(col)
            hdict[i] = col
            i = i + 1
            
        self.setup_csv_temp_writer(csv_in, header)
        import time
        time.sleep(3)
        for row in self.rows:
            rdict = {}
            i = 0
            for cell in row.split(","):
                rdict[hdict[i]] = cell
                i = i + 1
            self.write_temp_rec(rdict)
            
        self.close_temp_csv(sort=True)
        return 0
                
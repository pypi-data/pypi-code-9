"""
Created on Feb 11, 2015

@author: Jason Bowles
"""



from sqlalchemy import create_engine
from rawdata_emca.runner.entry import RawEntry

class BaseConnector(RawEntry):
    """
    All classes that plan to connect to data and extract will need to extend this class
    
    THere are convenience functions for connection to databases and storing results... as more connectors are created, the 
      plan is to include even more
    """
    
    
    def __init__(self, params):
        """
        Constructor
        sent the non-standard information from the config file
        
        executes the init from the BaseEntry then sends along to the set_params method of sub class
        """
        
        super(BaseConnector, self).__init__(params)
        ## class variables
        self.param_dict = {}
        self.sa_engine = None
        self.sa_connection = None
        self.db_results = None
        self.name = 'Standard'
        self.sql_file = None
        self.sql = None
        self.csv_header = None
        self.set_params(params)
        self.log_message('Initialization complete',log_type='connector',status='running',step='execute entries',name=self.name,log_level=self.log_info())
        
      
    def set_params(self, kwargs):
        """
        Method designed to be over-ridden if needed, but basically just calls load_params(**kwargs) as the base implementation
    
        If overridden be sure to call load_params(**kwargs)
        """
        self.load_params(kwargs)
    
       
    
    def execute_connection(self):
        """
        This method should be overridden
        """
        self.log_message(' now running actions using params')
        print self.param_dict
        return 0
    
    
    def get_db_connection(self):
        """
        conveniece method for setting up database Connection
        assumes the connection url is in the params as "db_url"
  
        """    
        self.log_message('Connecting to database: '+self.param_dict['database'])    
        url = self.param_dict['db_url']
        self.sa_engine = create_engine(url)
        self.sa_connection = self.sa_engine.connect()
        
    def close_db_connection(self):
        """
        close the database connection.. could throw error
        """
        self.sa_connection.close()
        
    
    def execute_sql(self):
        """
        convenience method for executing a database sql query
        sql must be stored in params as "db_sql"
        """
        self.log_message('Executing SQL Query against database: '+self.param_dict['database'])
        self.db_results = self.sa_connection.execute(self.sql)
        
    def get_sql(self):
        """
        read the sql file and return it
        this combines all of the lines into a single line.. 
        """
        with open(self.sql_file, 'r') as f:
            self.sql=f.read().replace('\n',' ')
        
        

    def build_db_url(self):
        """
        Builds the db_url from the following parameters
          - [Parameter name],     [Parameter Description]
        0 - dialect, the sqlalchemy database dialect name
        1 - username, the user name used to make the connection
        2 - password, the password for the user making the connection
        3 - server, the name of the server where the database is hosted
        4 - port, the port of the database implementation
        5 - database, the name of the database that the connection is being made
        
        {database dialect}://{user name}:{user password}@{server name}:{server port}/{server database}
        """
        arg_list = []
        try:
            arg_list.append(self.param_dict['dialect'])
            arg_list.append(self.param_dict['username'])
            arg_list.append(self.param_dict['password'])
            arg_list.append(self.param_dict['server'])
            arg_list.append(self.param_dict['port'])
            arg_list.append(self.param_dict['database'])
            self.param_dict['db_url'] = '{0}://{1}:{2}@{3}:{4}/{5}'.format(*arg_list)
        except Exception as err1:
            print 'Keyword: ' + str(err1) + " Is missing from the options list"
            raise
    
    def get_type(self):
        return self.CONNECTOR
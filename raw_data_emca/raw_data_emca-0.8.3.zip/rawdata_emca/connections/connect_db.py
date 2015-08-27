"""
Created on Sep 19, 2014

@author: Jason Bowles
at some point there will be a base class.. but not yet 9/29/2014
"""
from rawdata_emca.connections import BaseConnector
from sqlalchemy import exc
import traceback

class ConnectDB(BaseConnector):
    """
    purpose of this class is to get a connection to database as SQLAlchemy and pass back to a calling
    program to execute a SQL statement and get a pandas dataframe
    -- Assumption is that a lookup of some sort will be used to look up database info
    --- Server name
    --- Port
    --- UserName
    --- Password
    """
    
    
    def set_params(self, kwargs):
        """
        pass in the property file name to establish the connection criteria
        """
        self.load_params(kwargs)
        self.servername=kwargs['server']
        self.port=kwargs['port']
        self.username=kwargs['username']
        self.password=kwargs['password']
        self.sql_file=kwargs['sql_file']
        self.dialect =kwargs['dialect']
        
        
    def execute_connection(self):
        """ 
        do something
        """
        print ' now running actions using params (within ConnectDB): '+self.name 
        self.build_db_url()
        self.get_sql()
        open_connection = False
        try:
            self.get_db_connection()    
            open_connection = True        
            self.execute_sql()
            self.process_results()
        except exc.DBAPIError as db_err:
            print db_err
            self.log_message('problem wile running entry (DB_ERR): \"' + str(db_err) + "\", Will continue execution",log_level=self.log_error(),name=self.name)
            traceback.print_exc()
            raise
            self.return_status = 1
        except exc.SQLAlchemyError as sqla_err:
            print sqla_err
            self.log_message('problem wile running entry (SQLA_ERR): \"' + str(sqla_err) + "\", Will continue execution",log_level=self.log_error(),name=self.name)
            traceback.print_exc()
            raise
            self.return_status = 1
        except:
            traceback.print_exc()
            self.log_message('problem wile running entry: "UNEXPECTED..", Will continue execution',log_level=self.log_error(),name=self.name)
            print 'An unexpected error now in ConnectDB'
            raise
            self.return_status = 1
        finally:
            if open_connection:
                self.close_db_connection()
        return self.return_status
            
            
    def process_results(self):
        """
        default behavior is to just write the results to a csv file using pandas
        override this method to manipulate the results before writing to a temp csv file
        writes results to the base connection Dataframe
        
        If overriding do two things
        1) Set the header
        2) fill the df (dataframe)
        """
        hdr = self.db_results.keys()
        self.setup_csv_temp_writer(self.get_temp_csv_name(), hdr)
        temp_rec = {}
        for row in self.db_results:
            # I think there is a more pythonic way of doing this.. but for now this works.
            temp_rec = {k:v for k,v in zip(hdr,row)}                
            self.write_temp_rec(temp_rec)
        self.close_temp_csv()
        
        
    
        
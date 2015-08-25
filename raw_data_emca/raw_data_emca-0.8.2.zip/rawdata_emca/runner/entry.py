'''
Created on Mar 20, 2015

@author: Jason Bowles
'''
from rawdata_emca import Base_Type
from rawdata_emca.utilities import csvsort
import sys
import csv
import copy
import traceback

class RawEntry(Base_Type):
    """
    Both Connectors and Processors extend this class, this allows us to intercept the execution of both and hijack messages
    printed to stdout
    
    It also allows us to wrap them to guard against failures and to allow the framework to continue running
    """


    def __init__(self, params):
        """
        Constructor
        """
        Base_Type.__init__(self)
        self.return_status = 0
        self.return_results = None
        self.entry = params.get('entry',None)
        self.name = params.get('name',None)
        self.message = None
        self.csv_files = {}
    
    def load_params(self, params):
        """
        loads parameters to the base connection parameter dictionary
        """ 
        self.param_dict = params.copy()
        self.name = self.param_dict.get('name','Not Found')
    
    def set_params(self, kwargs):
        """
        Method designed to be over-ridden if needed, but basically just calls load_params(**kwargs) as the base implementation
        
        If overridden be sure to call load_params(kwargs)
        """ 
        self.load_params(kwargs)
    
    def run_execution(self):
        """
        Hijacking the messages that will be displayed to stdout.. so that logging has everything it should
        """
        self.log_message('Will begin to run entry: '+self.name+', type: '+self.entry.get_entry_type(),name=self.name,step='run entry',status='start')
        # save stdout
        old_stdout = sys.stdout
        
        # create the new stdout and then assign it to sys.stdout
        new_stdout = CaptureOutput(self)
        new_stdout.set_old_stdout(old_stdout)
        sys.stdout = new_stdout
        try:
            entry_ret = 0
            if self.entry.get_entry_type() == Base_Type.CONNECTOR:
                entry_ret = self.execute_connection()
            else:
                entry_ret = self.execute_processor()
            self.log_message('Entry Run is complete',status='complete')
            return entry_ret
        except Exception as err1:
            self.log_message('problem wile running entry: \"' + str(err1) + "\", Will continue execution",log_level=self.log_error(),name=self.name)
            self.set_message(traceback.format_exc())
            traceback.print_exc()
            return 1
        finally:
            # set stdout back to itself... ahhhh
            sys.stdout = old_stdout
            # now lets print those messages.. just in case the developer is counting on them for debugging
            #for msg in new_stdout.get_messages():
            #    print msg
    
    def execute_connection(self):
        """
        This method should be overridden
        """
        self.log_message(' now running actions of connector using params')
        print self.param_dict
        return 0
    
    def execute_processor(self):
        """
        This method should be overridden
        """
        self.log_message(' now running actions of processor using params')
        print self.param_dict
        return 0
    
    def get_temp_csv_name(self):
        return self.entry.get_temp_csv_name()
    
    def write_df_to_csv(self, keys=None):
        """
        here it is
        """
        self.log_message('Writing dataframe to CSV file')
        self.return_results.to_csv(self.get_temp_csv_name(), index_label="Index", header=keys)
        
    def setup_csv_writer(self,filename, fieldnames, write_header=True, name="default"):
        """ setup a csv file writer.. the close and writes need the filename by default.. or by another name set by the caller"""
        if name == "default":
            name = filename
        csvfile = open(filename, 'w')
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,lineterminator = '\n')
        if write_header:
            writer.writeheader()
        self.csv_files[name] = {"writer":writer, "csvfile":csvfile}
        
    def setup_csv_temp_writer(self, filename, fieldnames, write_header=True):
        """
        Sets up a dictionary writer.. so pass in the field names as the setup
        returns the writer
        """
        csvfile = open(filename, 'w')
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,lineterminator = '\n')
        if write_header:
            writer.writeheader()
        self.temp_writer = writer
        self.temp_csvfile = csvfile
        
    def write_csv_rec(self, name, dict_row):
        """ write a record to the file specified in the name"""
        csvfile = self.csv_files[name]["csvfile"]
        writer = self.csv_files[name]["writer"]
        
        if not csvfile.closed:
            try:
                writer.writerow(dict_row)
            except Exception as err1:
                self.log_message('problem writing record: ' + str(err1) + " Will continue execution",log_level=self.log_error(),name=self.name,status='error')
                traceback.print_exc()
                csvfile.close()
        
    def write_temp_rec(self, dict_row):
        """
        make sure you are passing in a dictionary of values
        or you can pass in a list of dictionary values
        """
        if not self.temp_csvfile.closed:
            try:
                self.temp_writer.writerow(dict_row)
            except Exception as err1:
                self.log_message('problem writing record: ' + str(err1) + " Will continue execution",log_level=self.log_error(),name=self.name,status='error')
                print dict_row
                traceback.print_exc()
                self.temp_csvfile.close()


    def close_csv(self, name):   
        csvfile = self.csv_files[name]["csvfile"]   
        if not csvfile.closed:
            try:
                csvfile.close()
            except Exception as err1:
                self.log_message('could not close the file: ' + str(err1) + " Will continue execution",log_level=self.log_error(),name=self.name,status='error')
                traceback.print_exc()
                
                     
    def close_temp_csv(self, sort=False):
        if not self.temp_csvfile.closed:
            try:
                self.temp_csvfile.close()
                if sort:
                    filename = self.temp_csvfile.name
                    columns = self.param_dict.get('sort_columns','0').split(',')
                    columns = [int(column) if column.isdigit() else column for column in columns]
                    csvsort(filename, columns)
            except Exception as err1:
                self.log_message('could not close the file: ' + str(err1) + " Will continue execution",log_level=self.log_error(),name=self.name,status='error')
                traceback.print_exc()
    
    def get_type(self):
        """
        pass back whether or not this is a connector or processor
        
        Designed to be overridden by the BaseConnector and BaseProcessor
        """
        return None
    
    def set_message(self,msg):
        """
        This method sets the message to display after running.. by default is set to nothing.. but could be good for debugging errors
        """
        self.message = msg 

class CaptureOutput:
    
    def __init__(self, base_type):
        self.entry = base_type
        self.message_list = []
        
    def write(self, message):
        self.stdout.write(message)
        if message and message.strip():
            self.message_list.append(message.strip())
            self.entry.log_message('(Intercept) '+message.strip(), status='running')
    
    def get_messages(self):
        msgs = copy.copy(self.message_list)
        self.message_list = []
        return msgs
    
    def set_old_stdout(self, old_stdout):
        self.stdout = old_stdout
        
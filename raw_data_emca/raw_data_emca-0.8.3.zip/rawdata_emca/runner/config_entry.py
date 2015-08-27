"""
Created on Feb 11, 2015

@author: Jason Bowles
"""
import os
import csv
import shutil
import traceback
from rawdata_emca.utilities import RawDataUtilities
from rawdata_emca import Base_Type

class ConfigEntry(Base_Type):
    """
    This is an entry in the configuration file that will need to be processed

    Each frequency has a number of days to way to know when to run based on the difference in the last run date and today's date
    These are designed to be approximates.
    The scheduler package will look daily to see if the entry needs to be run... so it will likely off on any given day.. but for the most part okay
    
    03/20/2015 - Added Never so that some can be there to run as successors
    
    See ConfigFileReader for more info on dependencies and successors
    """
    frequencies = {'Never':999999,'Daily':1,'Weekly':7,'Monthly':31,'Quarterly':92,'Annual':360,"Every":-1,"Fifteen":RawDataUtilities.fifteen_mins(),'Hour':RawDataUtilities.one_hour()}
    file_actions = {'Append':'a','Overlay':'w','New':'w'}

    def __init__(self, params):
        """
        Constructor
        """
        Base_Type.__init__(self)
        ## class variables
        self.updates={}
        self.return_val = None
        self.description = None
        self.connection_type = None
        self.last_processed = None
        self.num_run = 0
        self.message = None
        self.no_run_reason = 'Schedule Not Ready'
    
        ### valid options... Default is Append
        # Append - Add records to the end
        # Overlay - replace the current with the new
        # New - Add a new file with the run number on the end Most current result has the name with no number
        self.file_write=None
    
        ## Valid Options... Default is Temp CSV file
        # Dataframe
        # ListList
        # DictionaryList
        # TempCSV
        # None
        self.temp_results=None
        self.out_filename = None
        self.src_implementation = None
        self.run_frequency = None
    
        ## location where results are written
        self.working_directory = None
    
        self.options = {}
        self.today_dt = None
        self.source_file = None
        self.instance = None
        self.temp_csv = None
        self.csv = None
        
        ## required fields
        self.today_dt = params['run_date']
        self.name = params['name']
        self.source_file = params['source_file']
        self.description = params['description']
        self.src_implementation = params['src_implementation']
        self.working_directory = params['working_directory']
        ## optional fields with defaults
        self.dependencies = [] if (params.get('dependencies', None)) == None else params['dependencies'].split(",")
        self.dependencies.append('kicker')
        self.successors= [] if (params.get('successors', None)) == None else params['successors'].split(",")
        self.connection_type = params.get('connection_type','none')    
        
        #  if it hasn't run before it will be empty
        self.first_run = False
        if params.get('last_processed',None):
            self.last_processed = params['last_processed']
        else:
            self.last_processed = RawDataUtilities.string_from_date(self.today_dt)
            self.first_run = True
        
        self.last_processed = RawDataUtilities.date_from_string(self.last_processed)
        
        self.num_run = int(params.get('num_run',0))
        self.out_filename = params.get('out_filename',self.name)
        self.run_frequency = params.get('run_frequency','Daily')
        self.temp_results = params.get('temp_results','TempCSV')
        self.file_write = params.get('file_write','Append')
        #self.entry_type = params.get('entry_type', 'Connector')
        self.last_run = params.get('last_run','success')
        self.instantiate_instance = True if params.get("instantiate","true") == "true" else False
        ## parameters to pass down to the entry implementation
        self.options = params.get('non_std',{})
        
        self.updates['last_processed'] = RawDataUtilities.string_from_date(self.today_dt)
        self.updates['num_run'] = str(self.num_run + 1)
        
        self.order = 0
        self.ready = True
        if self.instantiate_instance and self.get_instance():
            self.log_message("Initialization Complete (success): "+self.name, log_type='entry', status='running', step='load configs',name='config_entry',log_level=self.log_info())
        else:
            if self.instantiate_instance:
                self.ready = False
                self.log_message("Initialization Complete (failure): "+self.name, log_type='entry', status='running', step='load configs',name='config_entry',log_level=self.log_info())
        

    def run_now(self,run_date=None):
        """
        Determine if this entry should be run today
        """   
        if self.last_run == 'success':
            diff_date = self.today_dt
            if run_date:
                diff_date = run_date
            freq = self.frequencies[self.run_frequency]
            num_since_last_run = RawDataUtilities.get_diff(self.last_processed,diff_date)
            if num_since_last_run >= freq or self.first_run or freq < 0:
                return True
        return False
    
    def get_instance(self):
        try:
            self.log_message('Will try to import: '+self.src_implementation,step='execute entries',status='running',name=self.name)
            class_ = RawDataUtilities.get_class(self.src_implementation)            
        
            self.options['name'] = self.name
            self.options['entry'] = self
            self.instance = class_(self.options)
            return True
        except Exception as err1:
            self.log_message('problem instantiating class: ' + str(err1) + " Will continue execution",log_level=self.log_error(),name=self.name,status='error')
            traceback.print_exc()
            return False
        
    def execute_entry(self):
        """
        run this entry
        """
        self.run_entry()  
        
        return self.return_val
    
    def run_entry(self):
        """
        This will call the connector or processor execution function
        
        That function will return results back to this entry to process as a new output or append to the existing
        
        Then instance could run correctly but still fail if the entry can not handle the results returned
        """
        self.return_val =  self.instance.run_execution()
        rslts = self.instance.return_results
    
        try:  
            if self.return_val == 0:
                action = self.file_actions[self.file_write]
                
                if self.csv_exist():                
                    if self.file_write == 'Overlay':
                        self.csv_exist(delete=True)
                else:
                    if action == 'a':
                        action = 'w'
                
                if self.temp_results == 'TempCSV':
                    self.return_val = self.processCSV(rslts,action)
                elif self.temp_results == 'ListList':
                    self.return_val = self.processListOfLists(rslts,action)
                elif self.temp_results == "DictrionaryList":
                    self.return_val = self.processDictionaryList(rslts,action)
                elif self.temp_results == 'Dataframe':
                    ### process the DataFrame
                    self.return_val = self.processDataFrame(rslts,action)
                else:
                    ## do nothing because the temp_results is equal to None or something else
                    self.log_message('nothing to do because temp_results is: '+str(self.temp_results))
                    self.return_val = 0
                    
                
                if self.file_write == 'New' and self.temp_results != 'None':
                    '''Here we are making sure that results are written to a standard name (essentially making a copy)'''
                    new_path = self.get_csv_path()
                    self.file_write = 'Overlay'
                    self.csv = None
                    csv_path = self.get_csv_path()
                    self.csv_exist(delete=True)
                    shutil.copy(new_path, csv_path)
                    
        except Exception as err1:
            self.log_message('problem processing entry results: \"' + str(err1) + "\", Will continue execution",log_level=self.log_error(),name=self.name, status='error')
            self.instance.set_message(traceback.format_exc())
            traceback.print_exc()
            self.return_val = 1
        
    
    def csv_exist(self, delete=False):
        return self.does_file_exist(self.get_csv_name(),self.working_directory,delete)
    
    def tempcsv_exist(self):
        return self.does_file_exist(self.temp_csv,self.working_directory,delete=False)
    
    def get_entry_type(self):
        #return self.entry_types[self.entry_type]
        return self.instance.get_type()
        
    def processDataFrame(self,results,action):
        """
        If the it is a dataframe.. let's write it out to a temporary csv file
        Then process like it was like that all along
        
        Until I find a better way (or have more time).. this is the way it'll be done
        """
        results.to_csv(self.get_temp_csv_name(),index_label="Idx")
        return self.processCSV(results, action)
        
    def processDictionaryList(self,results,action):
        """
        Structure should be [{Header1:Row1_1,Header2:Row1_2},{Header1:Row2_1,Header2:Row2_2}]
        see: https://docs.python.org/2/library/csv.html#csv.DictWriter
        
        if you want it to be in a specific order you must set csv_header to a value in the connection
        otherwise it'll be pulled from dictionary.keys() of the first occurrence
        """
        if not self.conn_instance.csv_header:
            self.conn_instance.csv_header = results[0].keys()
            
        with open(self.get_csv_path(), action) as f:
            writer = csv.DictWriter(f,lineterminator='\n', fieldnames=self.conn_instance.csv_header)
            if action != 'a':
                writer.writeheader()
            writer.writerows(results)
            f.close()
            
        return 0
        
    def processCSV(self, results,action):
        """ 
        assumption is that the results is the filename
        """
        self.log_message('processing temp CSV')
        if action == 'w':
            # just rename the temp file because it has already been deleted at this point
            os.rename(self.get_temp_csv_name(),self.get_csv_path() )
        else:
            with open(self.get_csv_path(), action) as f:
                writer = csv.writer(f,lineterminator='\n')
                tempfile = open(self.get_temp_csv_name(), 'r') 
                reader = csv.reader(tempfile)
                reader.next()
                for row in reader:
                    writer.writerow(row)
                f.close()
                tempfile.close()
            self.does_file_exist(self.temp_csv, self.working_directory,delete=True)
        return 0
    

    def processListOfLists(self,results,action):
        """
        assumes that the first entry is the headers
        will delete on appends.. so this could result in a data loss if you don't add the header
        seriously.. why wouldn't you add the header.. it's python.. so it is easy!

        Structure should be [[header1, header2],[row1_1, row1_2],[row2_1, row2_2]]
        """
        with open(self.get_csv_path(), action) as f:
            writer = csv.writer(f,lineterminator='\n')
            if action == 'a':
                # remove the header recs
                results.pop(0)
            writer.writerows(results)
            f.close()
        return 0
    
    def get_temp_csv_name(self):
        if self.temp_csv == None:
            self.temp_csv = self.name+"__TEMP.csv"
            self.does_file_exist(self.temp_csv, self.working_directory, delete=True) # when getting the temporary name for the first time.. delete it if it exists
        return os.path.join(self.working_directory,self.temp_csv)
    
    def get_csv_path(self):
        return os.path.join(self.working_directory,self.get_csv_name())
    
    def get_csv_name(self):
        if self.csv == None:
            suffix = ""
            if self.file_write == 'New':
                suffix = "_"+self.updates['num_run']
            self.csv = self.out_filename+suffix+".csv"
            
        return self.csv
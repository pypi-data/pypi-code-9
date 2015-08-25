"""
Created on Feb 11, 2015

@author: Jason Bowles
"""
from rawdata_emca.runner.config_file_reader import ConfigFileReader
from rawdata_emca import Base_Type
import os
import sys
import traceback

class RawProcessor(Base_Type):
    """
    The raw processor is the entry point into the framework
    
    All directories and parameters that need to be processed should be passed in on instantiation
    
    params['files] should be a list of config files that should be processed, each will be added
    param['file'] gives the option to just add 1 file to be processed
    param['run_date'] optional parameter to define the actual run date of the framework (allow past date processing)
    param['log_file'] lists the file to be used for logging of the framework
    
    this class will then setup logging for the remainder of the run
    """
    
    config_files = []
    config_entries = []
    run_date = None

    def __init__(self, params):
        """
        Constructor
        """
        Base_Type.__init__(self)
            
        if params:
            if 'files' in params:
                self.addall_config_files(params['files'])
            if 'file' in params:
                self.add_config_file(params['file'])
            if 'run_date' in params:
                self.run_date = params['run_date']
            
            self.force_name = params.get('force',None)
            if 'log_file' in params:
                directory = os.path.dirname(os.path.realpath(params['log_file']))
                if not os.path.exists(directory):
                    os.makedirs(directory)
                self.log_file = params['log_file']
            else:
                run_path = os.path.dirname(os.path.realpath(sys.argv[0]))
                directory = os.path.join(run_path,'log')
                if not os.path.exists(directory):
                    os.makedirs(directory)
                self.log_file = os.path.join(directory,'rawdata.log')
        
        self.setup_logging()
        self.log_message("Kicking Off Raw Data Processor", log_type='main', status='start', step='root', name='raw_processor')
        
        
    
    def prep_reader(self):
        params = {}
        #params['uuid'] = self.log_uuid
        if self.run_date:
            params['run_date'] =  self.run_date
        if self.force_name:
            params['entry_name'] = self.force_name
        reader = ConfigFileReader(params)
        self.log_message("Begin Processing Config Files",status='running')
        for f in self.config_files:
            reader.process_config(f)
            
        return reader
    
    def execute_entries(self):
        final_stat = 0
        try:            
            self.log_message("About to Prep the Reader", log_level=self.log_info(),status='start',step='load configs')
            reader = self.prep_reader()
            self.log_message("Reader Prepped", status='complete')
            final_stat = reader.execute_entries()
            self.log_message('Raw Data Processor has Finished (Number of Failed Entries: {})'.format(final_stat),log_type='main',status='complete',step='root',name='raw_processor',log_level=self.log_debug())
        except Exception as err1:
            step = 'entry loading'
            if self.log_status == 'complete':
                step = 'entry executing'
            self.log_message('Problem while running: ' + str(err1) + ', issue found in: ('+step+')',log_level=self.log_error(),name='raw_processor',status='error')
            traceback.print_exc()
        return final_stat
    
    def execute_single_entry(self, entry_name):
        reader = self.prep_reader()
        return reader.execute_entry(entry_name)
        
    def addall_config_files(self,files):
        if files:
            for f in files:
                self.add_config_file(f)
        
    def add_config_file(self, filename):
        if filename:
            self.config_files.append(filename)
'''
Created on Apr 13, 2015

@author: Jason Bowles
'''
from rawdata_emca.processor import BaseProcessor
import csv
import os
import sys
from rawdata_emca.errors.data_error import RawDataError
from rawdata_emca.utilities import csvsort
from pandasql import sqldf
import pandas

class TwoFileProcessor(BaseProcessor):
    '''
    This class adds fields from one file to the other (essentially combining them on a key.
    This class will sort if the param sort = True
    
    Pass in the first file (which will be the main file)
      and the second file which will add fields to the second
      
    Then pass in the key for each file (if only the first file key is passed in.. the assumption is the 2nd file has the same key)
    (Key can be multiple fields.. but must be by name)
    
    (optional) file1_nomatch = discard / keep  (default is to keep)
    
    '''

    def set_params(self, kwargs):
        """
        Load parameters into a parameter dictionary to be used later if needed
        """
        self.load_params(kwargs)
        self.header = None
        keys = kwargs.keys()
        for key in keys:
            self.param_dict[key] = kwargs[key]
            
    def do_sort(self):
        ''' sort the files '''
        filename1 = self.param_dict['file1']
        filename2 = self.param_dict['file2']
        
        self.sort_one_file(filename1,self.file1_key)
        self.sort_one_file(filename2,self.file2_key)
        
        
    def sort_one_file(self, filename, arg_columns):
        # get the path to the file we'll read in
        csv_in = os.path.join(self.entry.working_directory,filename)
        
        has_header = True
        max_size = int(self.param_dict.get('max_size','100'))
        delimiter = self.param_dict.get('delimiter',',')
        
        
        columns = arg_columns.split(',')
        columns = [int(column) if column.isdigit() else column for column in columns]
        
        
        global TMP_DIR 
        TMP_DIR = os.path.join(self.entry.working_directory,'.csvsort.%d' % os.getpid())

        csvsort(csv_in, columns, None, max_size, has_header, delimiter)
    
    def open_files(self, file1, file2):
        self.file1_csv = open(file1)
        self.file2_csv = open(file2)
        self.file1_reader = csv.DictReader(self.file1_csv)
        self.file2_reader = csv.DictReader(self.file2_csv) 
        
    def read_file1(self, first=False):
        if first:
            self.last_file1 = self.file1_reader.next()
        else:
            if self.last_file1:
                try:
                    self.last_file1 = self.file1_reader.next()
                except StopIteration:
                    self.last_file1 = None

        if not self.last_file1:
            if not self.file1_csv.closed:
                self.file1_csv.close()
            
        return self.last_file1
    
    def read_file2(self, first=False):
        if first:
            self.last_file2 = self.file2_reader.next()
        else:
            if self.last_file2:
                try:
                    self.last_file2 = self.file2_reader.next()
                except StopIteration:
                    self.last_file2 = None

        if not self.last_file2:
            if not self.file2_csv.closed:
                self.file2_csv.close()
            
        return self.last_file2   
    
    def get_key(self, in_rec, key):
        keys = key.split(",")
        ret_key = ""
        
        for k in keys:
            ret_key = ret_key+in_rec[k]
            
        return ret_key
    
    def process_params(self):
        if "file1" not in self.param_dict.keys():
            raise RawDataError("Required field 'file1' is missing")
        
        if "file2" not in self.param_dict.keys():
            raise RawDataError("Required field 'file2' is missing")
        
        self.file1_key = self.param_dict['key_file1']
        self.file2_key = self.param_dict.get('key_file2',self.file1_key)
            
        self.sort = True if (self.param_dict.get("sort","false")).upper() == "TRUE" else False
        if self.sort:
            self.do_sort()
            
            
        self.copy_fields = []
        self.copy_prefix = self.param_dict.get("field_prefix","")
        self.keep_nomatch = True if (self.param_dict.get("file1_nomatch","keep")).upper() == "KEEP" else False
        self.renames = {}
        
        self.copyall = False
        if "all_fields" not in self.param_dict.keys():
            for key in self.param_dict.keys():
                if key.startswith("field_"):
                    field = key[len("field_"):]
                    rename = self.copy_prefix + self.param_dict[key]
                    self.copy_fields.append(field) 
                    self.renames[field] = rename
        else:
            self.copyall = True
    
    def add_fields(self, file2_rec):
        ''' 
        add in all of the header records to the copy field
        '''
        for key in file2_rec.keys():
            self.copy_fields.append(key)
            self.renames[key] = key
            
    def get_header(self, file1_rec, file2_rec):
        if self.copyall:
            self.add_fields(file2_rec)
        
        if not self.header:
            self.header = []
            for key in file1_rec.keys():
                self.header.append(key)
            
            for field in self.copy_fields:
                if not self.renames[field] in self.header:                    
                    self.header.append(self.renames[field])
                
        return self.header
                        
    
    def execute_processor(self):
        """
        open up the two files file1 and file2 (file1 is the main file, file2 is adding fields to file1)
        (optional) sort: True (default is False
        key_file1 = The field(s) that are used for the key to sort and merge on
        (optional) key_file2 = should match up to the fields in key_file1 (default is the same as key_file1)
        (optional) all_fields = True means move all fields from file2 to file1 (default is false and "field_" values are ignored
        field_XXXX = all parameters prefixed with "field_" will be added to file1 from file2 (the value will be the renamed entry
        field_prefix = A prefix to add to the records being added to file1 (recommended to use this option.. may have duplicate names
        
        this works best if there are no more than 1 match per record in file2
        
        Essentially either a 1 to 1 or a Many to 1 (incorrect results would occur with a 1 to many)
        """
        
        # pull in the parameter that has the file names we will process
        filename1 = self.param_dict['file1']
        filename2 = self.param_dict['file2']

        self.open_files(os.path.join(self.entry.working_directory,filename1), os.path.join(self.entry.working_directory,filename2))
        self.process_params()
        file1_rec = self.read_file1(first=True)
        file2_rec = self.read_file2(first=True)
        
        # call the convenience method to setup the temp_csv file.  This will also write the header row by default
        self.setup_csv_temp_writer(self.get_temp_csv_name(), self.get_header(file1_rec,file2_rec))
        
        while file1_rec:
            combined = {k:v for k,v in file1_rec.items()}
            if file2_rec and self.get_key(file2_rec,self.file2_key) == self.get_key(file1_rec,self.file1_key):
                # merge these two bad boys
                combined.update(self.get_values(file2_rec))
                ### WRITE ###
                self.write_temp_rec(combined)
                file1_rec = self.read_file1()
            elif file2_rec and self.get_key(file1_rec,self.file1_key) > self.get_key(file2_rec,self.file2_key):
                file2_rec = self.read_file2()
            elif not file2_rec or self.get_key(file1_rec,self.file1_key) < self.get_key(file2_rec,self.file2_key):
                ### WRITE REC WITH NO MATCH ###
                if self.keep_nomatch:
                    self.write_temp_rec(combined)
                file1_rec = self.read_file1()
            else:
                raise Exception
        self.close_temp_csv()
        return 0
    
    def get_values(self,in_rec):
        ret_dict = {}
        for entry in self.copy_fields:
            value = in_rec[entry]
            key = self.renames[entry]
            ret_dict[key] = value
        return ret_dict


class SQLProcessor(BaseProcessor):
    """
    Gives you the ability to run sql against a pandas dataframe.. but here is the extra bit.
    
    This class will pull in the csv file that you indicate and then load that into a dataframe.
    
    It will then execute the SQL that you pass in and then output the results to a new csv file
    
    input_file1 is the file to load into a pandas dataframe
    either one of the following can be used.
    
    sql_file:  the file to load which has the sql to execute against the dataframe
    sql: the sql to execute which by default is "Select * from emca_df1"
    
    The dataframe will be called emca_df1
    
    I am also attempting to set this up so that any additional arguments you want to pass into read_csv can be done via the config file
    see: http://pandas.pydata.org/pandas-docs/stable/generated/pandas.io.parsers.read_csv.html 
    """
    
    sql_err = ""
    
    def set_params(self, kwargs):
        """
        Load parameters into a parameter dictionary to be used later if needed
        """
        self.load_params(kwargs)
        keys = kwargs.keys()
        for key in keys:
            self.param_dict[key] = kwargs[key]
    
    def read_csv_args(self):
        rca = ['sep','dialect','compression','doublequote'
        ,'escapechar','quotechar','quoting','skipinitialspace'
        ,'lineterminator','header','names','prefix'
        ,'skiprows','skipfooter','skip_footer','na_values'
        ,'na_fvalues','true_values','false_values','delimiter'
        ,'converters','dtype','usecols','engine','delim_whitespace'
        ,'as_recarray','na_filter','compact_ints','use_unsigned'
        ,'low_memory','buffer_lines','warn_bad_lines', 'error_bad_lines', 
        'keep_default_na', 'thousands', 'comment', 'decimal', 'parse_dates', 
        'keep_date_col', 'dayfirst', 'date_parser', 'memory_map', 'float_precision'
        , 'nrows', 'iterator', 'chunksize', 'verbose', 'encoding', 'squeeze', 
        'mangle_dupe_cols', 'tupleize_cols', 'skip_blank_lines']
        
        csv_params = {}
        for key in self.param_dict.keys():
            if key in rca:
                csv_params[key] = self.param_dict[key]
        
        return csv_params
    
    def load_sql(self):
        sql_file = self.param_dict.get("sql_file",None)
        if sql_file:
            with open(sql_file, 'r') as f:
                self.sql=f.read().replace('\n',' ')
        else:
            self.sql = self.param_dict.get('sql',"Select * From emca_df1")
    
    def load_csv_file(self, filename,file_index=None):
        csv_params = self.read_csv_args()
        return pandas.read_csv(os.path.join(self.entry.working_directory,filename),infer_datetime_format=True,index_col=file_index,**csv_params)
    
    def execute_processor(self):
        """
        here we'll grab the file and look for the sql to run against the dataframe
        sql_file or sql
        """
        
        #global emca_df1
        emca_df1 = self.load_csv_file(self.param_dict['input_file1'])
        print emca_df1.head(1)    
        
        self.load_sql()
        
        self.return_results = sqldf(self.sql, locals(),inmemory=False)
        if not isinstance(self.return_results, pandas.DataFrame):
            """
            Okay so pandasql decided not to store or do anything to let you know why an sql failed.. so I decided that really SUX
            
            So the only way I can fix this is to catch a "None" being returned.. then rerun the sqldf with the trace set to 
            a function designed to look for a database error.. still finessing this.. so hopefully this will work
            """
            sys.settrace(SQLProcessor.sqltrace)
            sqldf(self.sql,locals())
            print 'sql_err... '+SQLProcessor.sql_err
            self.log_message(SQLProcessor.sql_err,log_level=self.log_error(),name=self.name, status='error')
            sys.settrace(None)
            return 1
        self.entry.temp_results = "Dataframe"
        return 0
    
    @staticmethod
    def sqltrace(frame, event, arg, indent=[0]):
        from pandas.io.sql import DatabaseError
        if event == "exception":
            if isinstance(arg[1],DatabaseError):
                print 'there was an exception: '+arg[1].message
                sys.settrace(None)
                SQLProcessor.sql_err = arg[1].message
                return None
        return SQLProcessor.sqltrace

class SQLMultiProcessor(SQLProcessor):
    """ 
    design of this class is to enable joining 2 or more dataframes together to combine results
    every input should start with "input_"
    
    the 2nd part of the file "input_XXXX"  Will determine the dataframe name.
    
    so "input_myfile_1" will have a dataframe name of myfile_1 and should be used as such in the sql
    """
    
    
    def execute_processor(self):
        """
        here we'll grab the input parameters and load each of the df's
        
        We'll have to load them all into a dictionary so that the pandasql framework can find them.
        
        if you are merging on a column of data.. you MUST create an index.. or it may never complete..
        
        for the index of the file start the key with "index_".. then the name should follow "index_XXXX" this therefore..
        
        every input_XXXX should have a corresponding index_XXXX... If not then you aren't ready to join
        """
        
        df_dict = {}
        df_index = {}
        for inp in self.param_dict.keys():
            if inp.startswith("input_") or inp.startswith("index_"):
                df_name = inp[len("input_"):]
                if inp.startswith("input_"):
                    print 'loading file: '+df_name
                    filename = self.param_dict[inp]
                    #df_dict[df_name] = self.load_csv_file(filename)
                    df_dict[df_name] = filename
                    if not df_name in df_index.keys():
                        df_index[df_name] = None # default to None for index
                else:
                    print 'Pulling in index for: '+df_name
                    df_index[df_name] = self.param_dict[inp].split(",")
        
        for df_name in df_dict.keys():
            df_dict[df_name] = self.load_csv_file(df_dict[df_name], df_index[df_name])
                    
                
        self.load_sql()
        print 'sql loaded, now running results'
        self.return_results = sqldf(self.sql,df_dict)
        if not isinstance(self.return_results, pandas.DataFrame):
            """
            Okay so pandasql decided not to store or do anything to let you know why a sql failed.. so I decided that really SUX
            
            So the only way I can fix this is to catch a "None" being returned.. then rerun the sqldf with the trace set to 
            a function designed to look for a database error.. still finessing this.. so hopefully this will work
            """
            sys.settrace(SQLProcessor.sqltrace)
            sqldf(self.sql,df_dict)
            print 'sql_err... '+SQLProcessor.sql_err
            self.log_message(SQLProcessor.sql_err,log_level=self.log_error(),name=self.name, status='error')
            sys.settrace(None)
            return 1
        self.entry.temp_results = "Dataframe"
        return 0

    
        
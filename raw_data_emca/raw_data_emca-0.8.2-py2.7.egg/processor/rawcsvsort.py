"""
Created on Mar 19, 2015

@author: Jason Bowles
"""
from rawdata_emca.processor import BaseProcessor
from rawdata_emca.runner.config_entry import ConfigEntry
from rawdata_emca.utilities import csvsort
import os
import datetime


class RawCsvSort(BaseProcessor):
    """
    This is a wrapper class around the module csvsort found here: https://pypi.python.org/pypi/csvsort/1.2
    
    This will sort as much as you want via memory.. but when that is exceeded it will create files and sort those row by row
    3/19/2015 - there were some flaws with the original code.. so I ended copying it into the utilities module and using it here
    
    Problem #1 - Reader wasn't closed so couldn't remove temp files
    Problem #2 - Temporary directory was in the same place as the codee.. no way to override that
    Problem #3 - Line terminator needed to be added as an argument to the csv writer
    
    03/20/2015 - plan is to contact the developer and inquire about the fixes for this approach.. as this seems to be a solid start
    """

    def execute_processor(self):
        """
        get the parameters needed for this and run csvsort
        """
        # pull in the parameter that has the file name that we will process
        filename = self.param_dict['sort_file']
        
        # get the path to the file we'll read in
        csv_in = os.path.join(self.entry.working_directory,filename)
        csv_out = self.get_temp_csv_name()
        
        has_header = True if self.param_dict.get('has_header','True') == 'True' else False
        max_size = int(self.param_dict.get('max_size','100'))
        delimiter = self.param_dict.get('delimiter',',')
        
        
        columns = self.param_dict.get('sort_columns','0').split(',')
        columns = [int(column) if column.isdigit() else column for column in columns]
        
        
        global TMP_DIR 
        TMP_DIR = os.path.join(self.entry.working_directory,'.csvsort.%d' % os.getpid())

        csvsort(csv_in, columns, csv_out, max_size, has_header, delimiter)
        return 0

if __name__ == "__main__":
    """
    allow to run outside of framework
    """
    params = {}
    params['run_date'] = datetime.datetime.today()
    params['name'] = 'raw_csv_sort'
    params['source_file'] = None
    params['description'] = "local version of raw csv sorter"
    params['src_implementation'] = None
    params['working_directory'] = r'D:\python_scripts\rawdataprocessor\output'
    params['sort_file'] = 'adp data.csv'
    params['out_sort_file'] = 'srt_adp data.csv'
    params['max_size'] = '1'
    params['sort_columns'] = 'claim_number'
    c_entry = ConfigEntry(params)
    params['entry'] = c_entry
    rawcsv = RawCsvSort(params)
    rawcsv.execute_processor()
        
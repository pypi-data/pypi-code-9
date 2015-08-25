'''
Created on Apr 24, 2015

@author: Jason Bowles
'''
from rawdata_emca.connections import BaseConnector
from rawdata_emca.utilities import RawDataUtilities
import os
import csv

class FileDateStrip(BaseConnector):
    '''
    Connector is designed to strip off old data based on a date in a csv file
    
    You would use this if you are appending to a file and want to limit the size.
    
    Another option would be to do an overlay.. and before running an overlay run this connector to save off the old records
    
    This is a good strategy when data that was previously extracted could have changed and you DO want the updated changes.
    '''

    def set_params(self, kwargs):
        """
        pass in the property file name to establish the connection criteria
        """
        self.load_params(kwargs)
        keys = kwargs.keys()
        for key in keys:
            self.param_dict[key] = kwargs[key]
    
    def get_match_date(self,units, date_unit, in_date):
        """
        from the passed in date subtract the numbe of units from that of date unit
             
        example:
        ___UNITS____:___DATE_UNIT___:____IN_DATE___:___RESULT___
            6           Day            1/10/2014       1/4/2014
            1           Month         10/23/2013       9/23/2013
            1           Year           7/04/2012       7/04/2011

        """
        delta = int(units)
        if delta > 0:
            delta = delta * -1
        if "MONTH" == date_unit.upper():
            return RawDataUtilities.monthdelta(in_date, delta)
        elif "DAY" == date_unit.upper():
            return RawDataUtilities.daydelta(in_date, delta)
        else:
            return RawDataUtilities.yeardelta(in_date, delta)
            
    
    def execute_connection(self):
        """
        Re-read the class description :)
        
        parameters needed:
        file to strip (strip_file): assumption is that it will be found in the working_directory
        date field to use (date_field):  Most common date formats can be used.. recommended is MM/DD/YYYY or 01/01/2015
        strip parameters (strip_criteria):  pass in 2 elements (separated by a comma), Unit, Date Unit (Day, Month, Year)  example strip_criteria = 6,Month 
            (default is 1,Month)
        
        by default this will be from the run date (which defaults to today's date unless set otherwise), but can be from the "last_processed" date by passing in the optional parameter 
            "use_last_processed = true"
        
        another option is to simply pass in the date to use for stripping.. strip_date = 01/01/2015 
        
        Anything occuring before (not equal to) that date will be pulled off of the file
        
        the stripped off records will be saved under the connector name passed in the parameters        
        """
        filename = self.param_dict['strip_file']
        date_field = self.param_dict['date_field']
        units, date_unit = self.param_dict.get('strip_criteria','1,Month').split(",")
        use_last = True if self.param_dict.get("use_last_processed","false").upper == "TRUE" else False
        strip_date = self.entry.last_processed if use_last else RawDataUtilities.date_from_string(self.param_dict.get("strip_date",RawDataUtilities.string_from_date(self.entry.today_dt)))
        
        match_date = self.get_match_date(units, date_unit, strip_date)
        
        file_in = os.path.join(self.entry.working_directory,filename)
        with open(file_in) as csvfile:
            reader = csv.DictReader(csvfile)
            self.setup_csv_temp_writer(self.get_temp_csv_name(), reader.fieldnames)
            for row in reader:
                compare_date = RawDataUtilities.date_from_string(row[date_field])
                # should subtract the date on the file from match date
                # Example any dates less than 10/1/2014
                # Compare date = 09/1/2014
                # Difference is less than 0
                diff = RawDataUtilities.get_diff(match_date, compare_date)
                if diff < 0:
                    self.write_temp_rec(row)
            self.close_temp_csv()
        return 0


if __name__ == "__main__":
    """
    allow to run outside of framework
    """
    fs = FileDateStrip({"name":"helper"})
    print fs.get_match_date(10, "year", RawDataUtilities.get_today_date())
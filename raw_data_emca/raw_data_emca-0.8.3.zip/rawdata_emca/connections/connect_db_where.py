'''
Created on Apr 3, 2015

@author: Jason Bowles
'''
from rawdata_emca.connections.connect_db import ConnectDB
from datetime import datetime
from __builtin__ import str
from rawdata_emca.errors.data_error import RawDataError
from rawdata_emca.utilities import RawDataUtilities

class DB_Where(ConnectDB):
    '''
    Extends ConnectDB and allows for the substitution of values into SQL
    
    all parameters that start with "where_" (ex: where_run_date)
    are used as substitutions and the subsitution phrase is all upper case %%RUN_DATE%% (for where_run_date)
    Notice how the wording is take after "where_" and surrounded with %%
    
    The value will be pulled from existing attributes first, (if you don't want this don't use an existing attribute)
    if you want to use the attribute use the value as a way to set the format (for dates, specify the date format via https://docs.python.org/2/library/datetime.html#strftime-and-strptime-behavior)
    other wise set it as str, int, or float (the str will place single quotes around it automatically) otherwise it will call the string value of the 
    attribute via str(%%attribute%%)
    
    
    This means that the passed in value is one of the attributes of the class
    
    possible entries could be: (note when passing in datetime format string double up the '%' so the config parser can process it correctly
    where_today_dt           (ex: where_run_date = %%m/%%d/%%Y)  -- fyi: today_dt would be set to run_date if that is passed in
    where_username           (ex: where_username = str)
    where_last_processed     (ex: where_last_processed = %%m/%%d/%%Y %%H:%%M:%%S)
    where_num_run            (ex: where_num_run = int)
    where_name
    where_today_dt
    
    if you are passing in the value, think about how the printed value will be shown.. so if you want a string.. either wrap the SQL replace
    with single quotes (ex: '%%EMP_NUM%%') or set the value to be where_emp_num = '8063'
    
    '''
    
    def set_params(self, kwargs):
        """
        pass in the property file name to establish the connection criteria
        
        look for parameters that start with "where_" and set them up to replace values in the SQL
        """
        super(DB_Where,self).set_params(kwargs)
        self.replace_dict = {}
        for key in kwargs.keys():
            if key.startswith("where_"):
                try:
                    k = key[len("where_"):]
                    v = kwargs[key]
                    v = self.get_value(k, v, kwargs)
                    self.replace_dict[k] = v
                except Exception as err1:
                    self.log_message('problem processing replace value: \"' + str(err1) + "\", Will continue execution",log_level=self.log_error(),name=self.name)
    
    def get_value(self, attribute, value, params, convert=True):
        k = attribute
        # if it was passed in as a parameter.. use that
        v = params.get(k,value)
        match = True
        if hasattr(self, k):
            v = getattr(self, k)
        elif hasattr(self.entry, k):
            v = getattr(self.entry, k)
        else:
            match = False
        
        if match and convert:
            v = self.convert_value(v, value)
        
        return v
    
    def convert_value(self, attr_v, convert):
        if isinstance(attr_v, datetime):
            str_date = RawDataUtilities.string_from_date(attr_v, str_format=convert)
            return "'"+str_date+"'"
        elif convert == 'str':
            return "'"+str(attr_v)+"'"
        # if the attribute isn't a string, no conversion will be done
        elif isinstance(attr_v,str):
            if convert == 'int':
                return int(attr_v)
            else:
                # assuming that it is float
                return float(attr_v)
        else:
            return attr_v
        
    def get_sql(self):
        """
        Call the super method for this.. then update the SQL with the replacement values
        """
        super(DB_Where,self).get_sql()
        for replace in self.replace_dict.keys():
            look = "%%"+replace.upper()+"%%"
            self.sql = self.sql.replace(look,self.replace_dict[replace])
        
        self.log_message("SQL Updated ("+self.sql+")")
                
class DB_WhereOffset(DB_Where):
    """
    Same as DB_Where but allows you use an offset from a date
    
    for example 6 months from today or from last processed date
    
    the value used is assumed to be either last_processed or today_dt (which is run_date if passed)
    """
    def get_conver_date(self,units, date_unit, in_date):
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


    def set_params(self, kwargs):
        super(DB_WhereOffset,self).set_params(kwargs)
        for key in kwargs.keys():
            if key.startswith("offset_"):
                try:
                    k = key[len("offset_"):]
                    if k not in self.replace_dict:
                        raise RawDataError("No matching \"where_\" for this parameter: "+k)
                    if not (k == "last_processed" or k == "today_dt"):
                        raise RawDataError("Can not offset from that parameter: "+k)
                    units, date_unit = kwargs[key].split(",")
                    v = self.get_value(k, None, kwargs,convert=False)
                    v = self.convert_value(self.get_conver_date(units, date_unit, v), kwargs['where_'+k])
                    
                    self.replace_dict[k] = v
                except Exception as err1:
                    self.log_message('problem processing replace value: \"' + str(err1) + "\", Will continue execution",log_level=self.log_error(),name=self.name)
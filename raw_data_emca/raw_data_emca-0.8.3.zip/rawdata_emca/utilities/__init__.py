"""
Created on Feb 12, 2015

@author: Jason Bowles

module with utility methods to be used by the framework
"""
import sys
import datetime
import calendar
import getpass
import base64
import importlib
import os
from rawdata_emca import Base_Type
import csv
from rawdata_emca.errors.data_error import RawDataError

csv.field_size_limit(sys.maxint)
import heapq

# temporary directory to store the sub-files
TMP_DIR = '.csvsort.%d' % os.getpid()

class RawDataUtilities(Base_Type):
    """
    This class represents a list of static methods.. I think it makes it easier to use the utilities if they are static methods of a class
    vs. just being functions in a module which I'd have to import individually?  I don't know for sure
    
    but this is how I'd do it in Java... not that it is the correct way to do it that way there either.
    
    I'm just a guy living the dream
    """
    # example date entry: 01/01/2013 00:00:00
    DATE_PARSE = '%m/%d/%Y %H:%M:%S'
    MMDDYYY_HHMMSS_SLASH = DATE_PARSE
    DATE_PARSEa = '%m/%d/%Y %H:%M'
    MMDDYYY_HHMM_SLASH = DATE_PARSEa
    
    #"2015-03-01 15:36:47.0"
    # 2015-03-02 17:33:01
    DATE_PARSE2 = '%Y-%m-%d %H:%M:%S.%f'
    YYYYMMDD_HHMMSSFF_DASH = DATE_PARSE2
    DATE_PARSE2a = '%Y-%m-%d %H:%M:%S'
    YYYYMMDD_HHMMSS_DASH = DATE_PARSE2a
    
    #2013-01-01-06.00.00.000000
    #2014-01-30-20.23.51.000000
    DATE_PARSE3 = "%Y-%m-%d-%I.%M.%S.%f"
    DATE_PARSE3a = "%Y-%m-%d-%H.%M.%S.%f"
    
    #    11/2/2010
    DATE_PARSE4 = "%m/%d/%Y"
    
    #    20130709
    DATE_PARSE5 = "%Y%m%d"
    
    #May 18, 2014
    DATE_PARSE6 = "%b %d, %Y"
    
    #26-May-14
    DATE_PARSE7 = "%d-%b-%y"
    
    DATE_FORMATS = [DATE_PARSE,DATE_PARSE2,
                    DATE_PARSE3a,DATE_PARSEa,
                    DATE_PARSE3,DATE_PARSE4,
                    DATE_PARSE5,DATE_PARSE6,
                    DATE_PARSE7,DATE_PARSE2a]
    
    # update the updates dictionary to be used
    USED = '$$$$$   USED   $$$$$'

    def __init__(self, params):
        """
        Constructor
        """
    
    @staticmethod
    def date_from_string(str_date):
        ret_datetime = None
        for fmt in RawDataUtilities.DATE_FORMATS:
            try:
                ret_datetime = datetime.datetime.strptime(str_date,fmt)
                break
            except Exception:
                """ failed to laod date... oh well try the next """
                ret_datetime = None
        
        if not ret_datetime:
            raise RawDataError("Could not parse the date passed: "+str_date)
        
        return ret_datetime
    @staticmethod
    def add_seconds_to_date(date_obj, arg_secs):
        return date_obj + datetime.timedelta(seconds=arg_secs)
    
    @staticmethod
    def string_from_date(date_obj, str_format=None):
        if not str_format:
            str_format = RawDataUtilities.get_dateparse()
        return date_obj.strftime(str_format)
    
    
    
    @staticmethod
    def fifteen_mins():
        return 15.0/(24.0*60.0)
    
    @staticmethod
    def one_hour():
        return 60.0/(24.0*60.0)
    
    @staticmethod
    def get_now():
        return datetime.datetime.today()
    
    @staticmethod
    def get_dateparse():
        return '%m/%d/%Y %H:%M:%S'
     
    @staticmethod 
    def get_used_value():
        return '$$$$$   USED   $$$$$'
    
    @staticmethod
    def encrypt_password(password):
        return base64.b64encode(password)
    
    @staticmethod
    def decrypt_password(password):
        return base64.b64decode(password)
    
    @staticmethod
    def get_diff(first_date, second_date=None, seconds=False):
        """
        returns minutes in the difference as a percentage of a day
        """
        if not second_date:
            second_date = datetime.datetime.now()
        if not isinstance(first_date, datetime.date) and not isinstance(first_date, datetime.datetime):
            first_date = RawDataUtilities.date_from_string(first_date)
        if not isinstance(second_date, datetime.date) and not isinstance(second_date, datetime.datetime):
            second_date = RawDataUtilities.date_from_string(second_date)
        delta = (second_date-first_date)
        secs = delta.total_seconds()
        if seconds:
            return secs
        return float(secs/60)/(24*60)
    
    @staticmethod
    def monthdelta(in_date, delta):
        m, y = (in_date.month+delta) % 12, in_date.year + ((in_date.month)+delta-1) // 12
        if not m: m = 12
        d = min(in_date.day, calendar.monthrange(y, m)[1])
        return in_date.replace(day=d,month=m, year=y)
    
    @staticmethod
    def daydelta(in_date,delta):
        return in_date + datetime.timedelta(days=delta)
    
    @staticmethod
    def yeardelta(in_date,delta):
        y, m, = in_date.year, in_date.month
        y = y + delta
        
        d = min(in_date.day,calendar.monthrange(y, m))
    
        return in_date.replace(day=d,month=m, year=y)
        
    @staticmethod
    def get_class(py_source):
        """
        Try to import python code dynamically
        The trick is that this may be code added at any time by any user from any path
        If there is a path seperator in dynamic path.. then we need to append it to the path
        """
        backs = '\\'
        forwards = '/'
        from_path = False
        path = ""
        if py_source.find(backs) > -1:
            mod_src = py_source.split(backs)[-1]
            from_path = True 
        elif py_source.find(forwards) > -1:
            mod_src = py_source.split(forwards)[-1]
            from_path = True
    
        if from_path:
            path =  py_source[:py_source.find(mod_src)-1]
            sys.path.append(os.pathsep+path)
        else:
            mod_src = py_source
    
        class_data = mod_src.split(".")
        class_str = class_data[-1]
        src_mod = '.'.join(class_data[:len(class_data)-1])  
        module = importlib.import_module(src_mod)
        class_ = getattr(module, class_str)
        return class_
    
    
        

class CsvSortError(Exception):
    pass    
   
def csvsort(input_filename, columns, output_filename=None, max_size=100, has_header=True, delimiter=',', quoting=csv.QUOTE_MINIMAL):
    """Sort the CSV file on disk rather than in memory
    The merge sort algorithm is used to break the file into smaller sub files and 

    input_filename: the CSV filename to sort
    columns: a list of column to sort on (can be 0 based indices or header keys)
    output_filename: optional filename for sorted file. If not given then input file will be overriden.
    max_size: the maximum size (in MB) of CSV file to load in memory at once
    has_header: whether the CSV contains a header to keep separated from sorting
    delimiter: character used to separate fields, default ','
    """
    if not os.path.exists(TMP_DIR):
        os.mkdir(TMP_DIR)
        
    reader = csv.reader(open(input_filename), delimiter=delimiter)
    if has_header:
        header = reader.next()
    else:
        header = None

    columns = parse_columns(columns, header)

    filenames = csvsplit(reader, max_size)
    print 'Merging %d splits' % len(filenames)
    for filename in filenames:
        memorysort(filename, columns)
    sorted_filename = mergesort(filenames, columns)

    # XXX make more efficient by passing quoting, delimiter, and moving result
    # generate the final output file
    writer = csv.writer(open(output_filename or input_filename, 'w'), delimiter=delimiter, quoting=quoting,lineterminator = '\n')
    if header:
        writer.writerow(header)
    for row in csv.reader(open(sorted_filename)):
        writer.writerow(row)
    os.remove(sorted_filename)
    try:
        os.rmdir(TMP_DIR)
    except OSError:
        pass


def parse_columns(columns, header):
    """check the provided column headers
    """
    for i, column in enumerate(columns):
        if isinstance(column, int):
            if header:
                if column >= len(header):
                    raise CsvSortError('Column index is out of range: "{}"'.format(column))
        else:
            # find index of column from header
            if header is None:
                raise CsvSortError('CSV needs a header to find index of this column name: "{}"'.format(column))
            else:
                if column in header:
                    columns[i] = header.index(column)
                else:
                    raise CsvSortError('Column name is not found in header: "{}"'.format(column))
    return columns


def csvsplit(reader, max_size):
    """Split into smaller CSV files of maximum size and return the list of filenames
    """
    max_size = max_size * 1024 * 1024 # convert to bytes
    writer = None
    current_size = 0
    split_filenames = []

    # break CSV file into smaller merge files
    for row in reader:
        if writer is None:
            filename = os.path.join(TMP_DIR, 'split%d.csv' % len(split_filenames))
            writer = csv.writer(open(filename, 'w'))
            split_filenames.append(filename)

        writer.writerow(row)
        current_size += sys.getsizeof(row)
        if current_size > max_size:
            writer = None
            current_size = 0
    return split_filenames


def memorysort(filename, columns):
    """Sort this CSV file in memory on the given columns
    """
    rows = [row for row in csv.reader(open(filename))]
    rows.sort(key=lambda row: get_key(row, columns))
    writer = csv.writer(open(filename, 'wb'))
    for row in rows:
        writer.writerow(row)


def get_key(row, columns):
    """Get sort key for this row
    """
    return [row[column] for column in columns]


def decorated_csv(filename, columns):
    """Iterator to sort CSV rows
    """
    for row in csv.reader(open(filename)):
        yield get_key(row, columns), row


def mergesort(sorted_filenames, columns, nway=2):
    """Merge these 2 sorted csv files into a single output file
    """
    merge_n = 0
    while len(sorted_filenames) > 1:
        merge_filenames, sorted_filenames = sorted_filenames[:nway], sorted_filenames[nway:]
        readers = map(open, merge_filenames)

        output_filename = os.path.join(TMP_DIR, 'merge%d.csv' % merge_n)
        writer = csv.writer(open(output_filename, 'w'))
        merge_n += 1

        for _, row in heapq.merge(*[decorated_csv(filename, columns) for filename in merge_filenames]):
            writer.writerow(row)
        
        sorted_filenames.append(output_filename)
        for filename in merge_filenames:
            for reader in readers:
                if reader.name == filename:
                    reader.close()
                    os.remove(filename)
    return sorted_filenames[0]


def main(argv):
    password = ""
    if len(argv) != 1:
        password = RawDataUtilities.encrypt_password(getpass.getpass('Please Enter a Password: '))
    else:
        password = RawDataUtilities.encrypt_password(sys.argv[1])

   
    print password       
            
if __name__ == "__main__":
    main(sys.argv[1:])
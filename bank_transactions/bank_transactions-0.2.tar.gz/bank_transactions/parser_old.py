import csv
import datetime
from decimal import Decimal


""" To do:
1. Remove redundancy in methods process_data()
2. Add functionality to support other file formats than csv
3. Add validation to check if the file matches the bank format
"""

    
class ReadFile(object):
    """ Takes bank transaction file and returns a two-dimensional 
    list of transactions
    """
    @staticmethod
    def csv_to_data(file):
        """ read from csv file """
        with open(file, 'rb') as f:
            reader = csv.reader(f, delimiter=';') # use delimiter bank config
            data = [row for row in reader]
            return data
    
    
class FileColumn(object):
    """ Contains column numbers for data objects in transaction file """
    def __init__(self, account, contra_account, transaction_date, amount, 
            currency, contra_account_name, description):        
        self.account = account
        self.contra_account = contra_account
        self.transaction_date = transaction_date
        self.amount = amount
        self.currency = currency
        self.contra_account_name = contra_account_name
        self.description = description

        
class Parse(object):
    """ Parses two-dimensional list with transaction data """    
    def remove_headers(self, data):
        """ Remove headers (if any) from transaction data """ 
        return data[self.header_rows:len(data)]    

    def date_to_datetime(self, data):
        """ Transform any date format to datetime format 
        Current date format is set in subclass 
        """    
        date_column = self.file_column.transaction_date
        for i in range(0, len(data)):            
            date = data[i][date_column]
            dtime = datetime.datetime.strptime(date, self.date_format).date()
            data[i][date_column] = dtime        
        return data      
        
    def data_row_to_transaction(self, row):
        """ Uses file_column settings from subclass to create transaction
        from data row
        """
        t = Transaction(
            row[self.file_column.account].replace(' ', ''),
            row[self.file_column.contra_account].replace(' ', ''),
            row[self.file_column.transaction_date],
            row[self.file_column.amount],
            row[self.file_column.currency],
            row[self.file_column.contra_account_name],
            row[self.file_column.description]
        )
        return t
    
    def create_transactions(self, data):
        trans = Transactions()
        for row in data:
            trans.add(self.data_row_to_transaction(row))
        return trans
    
    def process_data(self, file):
        """ Perform all steps to create Transactions from 
        transaction file
        """
        data = ReadFile.csv_to_data(file)
        data = self.remove_headers(data)
        data = self.date_to_datetime(data)
        trans = self.create_transactions(data)
        return trans
        
class ParseRabobank(Parse):
    """ Configuration for Rabobank transaction files """
    def __init__(self):
        self.file_column = FileColumn(2, 6, 10, 3, 4, 5, 8)
        self.header_rows = 1
        self.date_format = "%m/%d/%Y"

class ParseKnab(Parse):
    """ Configuration for Knab transaction files """    
    def __init__(self):
        self.file_column = FileColumn(0, 5, 7, 4, 2, 6, 9)
        self.header_rows = 2
        self.date_format = "%d-%m-%Y"
        self.debit_column = 3
    
    def amount(self, data):
        # dot instead of comma
        # fix credit/debit
        amount_column = self.file_column.amount
        for i in range(0, len(data)):
            amount = data[i][amount_column]
            amount = Decimal(amount.replace(',', '.'))
            if data[i][self.debit_column] == 'D':
                amount *= -1
            data[i][amount_column] = amount    
        return data
            
    def process_data(self, file):
        """ Override method from parent, additional operation amount()
        Rearrange methods to eliminate redundant methods
        """
        data = ReadFile.csv_to_data(file)
        data = self.remove_headers(data)
        data = self.date_to_datetime(data)
        data = self.amount(data) # additional operation
        trans = self.create_transactions(data)
        return trans
                
class Transaction(object):

    def __init__(self, account, contra_account, transaction_date, amount,
            currency, contra_account_name, description):        
        self.account = account
        self.contra_account = contra_account
        self.transaction_date = transaction_date
        self.amount = float(amount)
        self.currency = currency
        self.contra_account_name = contra_account_name
        self.description = description

        
class Transactions(object):
    """ Contains Transaction instances """
    def __init__(self):
        
        self.trans = [] 

    def add(self, t):
    
        self.trans.append(t)
     

""" Map bank keys to Parse()-classes of banks """        
banks = {
    'rabobank': ParseRabobank(),
    'knab': ParseKnab()
}        
    
def main(bank, file):
    
    b = banks[bank]
    trans = b.process_data(file)
    return trans
    

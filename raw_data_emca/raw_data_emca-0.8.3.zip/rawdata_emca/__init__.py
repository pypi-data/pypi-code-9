'''
Created on Mar 20, 2015

@author:  Jason Bowles
'''
import logging
import uuid
import datetime
import os


class Base_Type(object):
    """
    This base class is to setup all of the attributes needed to do correct logging on each step
    """
    log_uuid=None

    CONNECTOR = 'Connector'
    PROCESSOR = 'Processor'
    
    def __init__(self):
        """
        Constructor
        """
        self.log_type = None
        self.log_status = None
        self.log_step = None
        self.log_name = None
        self.log_level = logging.DEBUG    
        self.logger = logging.getLogger(type(self).__name__) 
        
    def set_uuid(self, uuid):
        self.log_uuid = uuid
    
    @staticmethod
    def get_today_date():
        return datetime.datetime.today()
        
    def setup_logging(self):
        self.log_uuid=uuid.uuid4()
        logging.basicConfig(filename=self.log_file,level=self.log_debug(),format=self.get_uuid()+',%(asctime)s,%(name)s,%(levelname)s,%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        
        
    def log_message(self, message, log_level=None,log_type=None, status=None, step=None, name=None):
        # some code
        
        if not name:
            name = self.log_name
        else:
            self.log_name = name
        
        if not log_level:
            log_level = self.log_level
        else:
            if not log_level == logging.ERROR:
                self.log_level = log_level
        
        if not log_type:
            log_type=self.log_type
        else:
            self.log_type=log_type
            
        if not status:
            status=self.log_status
        else:
            if not status == 'error':
                self.log_status=status
            
        if not step:
            step = self.log_step
        else:
            self.log_step = step
        
        log_msg = self.format_message(message, log_type, step, status,name)
        self.logger.log(log_level,log_msg)
        
    def format_message(self, message, log_type, step, status,name):
        msg = message.replace("\n"," ")
        return "{},{},{},{},{}".format(name,log_type, step, status, msg)
    
    def log_warn(self):
        return logging.WARNING
    
    def log_info(self):
        return logging.INFO
    
    def log_debug(self):
        return logging.DEBUG
    
    def log_error(self):
        return logging.ERROR
    
    def get_uuid(self):
        return str(self.log_uuid)
    
    def does_file_exist(self, filename,  working_directory, delete=False):
        """
        check if a file exists.. if it does the option argument determines if it should be deleted
        if it does exist and it was deleted it will still return true
        """
        path = os.path.join(working_directory,filename)
        exist = os.path.isfile(path) 
        if exist and delete:
            os.remove(path)
        return exist
'''
Created on Mar 27, 2015

@author:  Jason Bowles
'''
from rawdata_emca.processor import BaseProcessor
from rawdata_emca.connections import BaseConnector
from rawdata_emca import Base_Type


def create_entry(ent_name, _type):
    instance = None
    if _type == Base_Type.CONNECTOR:
        instance = create_connector(ent_name)
    else:
        instance = create_processor(ent_name)
    
    return instance({})

def create_processor(ent_name):
    class KickerProcessor(BaseProcessor):
        name = ent_name
        
        def execute_processor(self):
            """  just run something """
            print 'Kicking Off the Processors'
            return 0
            
    return KickerProcessor

def create_connector(ent_name):
    class KickerConnector(BaseConnector):
        name = ent_name
        
        def execute_connection(self):
            """
            This method should be overridden
            """
            print 'Kicking Off the Connectors'
            return 0
    return KickerConnector 
'''
Created on Sep 4, 2015

@author: andrei
'''

from kombu import Connection
import time
from Queue import Empty
import ConfigParser
import tools.auxiliary as auxiliary
import logging
import netifaces as ni

supported_apps = ['grok_hgs', 'enkf']

msg_args = {
                         'retrieve_cli_output': ['app_id'],
                         'update_output': ['app_id', 'output'],
                         'app_accepted': ['tmp_id', 'app_id'],
                         'update_app_status': ['app_id', 'status'],
                         'update_vm_spawning_time': ['app_id', 'time'],
                         
                         
                         'preprocess': ['input_id', 'input_file', 'group_id', 'input_param'],
                         'preprocessed': ['group_id', 'app_type', 'app_name', 'app_input_file', 'app_output_file', 'app_params'],
                         'preprocessing_completed': ['input_id', 'group_id'],
                         
                         'postprocess': ['group_id', 'apps_ids_list', 'outputs_list'],
                         'postprocessed': ['group_id', 'output', 'apps_ids_list'],
                         
                         'create_app': ['web_interface_id', 'app_type', 'app_params'],
                         'launch_app': ['app_manager_id'],
                         'const_output_update': ['app_manager_id', 'update_output'],
                         'delete_app': ['app_manager_id', 'web_interface_id'],
                         
                         'created_app': ['web_interface_id', 'app_manager_id'],
                         'expired_app': ['web_interface_id'],
                         'launched_app': ['web_interface_id'],
                         'update_info': ['web_interface_id', 'info_type', 'info'],
                         'app_output_file_ready': ['web_interface_id'],
                         'deleted_app': ['web_interface_id'],
}

#get IP address of the specified interface
def getIPAdreess(interface='eth0'):
    addr = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    return addr

#builds a RabbitMQ connection link 
def buildRabbitMQConnectionLink(address=getIPAdreess(), protocol='amqp', user='rabbitmq', password='rabbitmq', port='5672'):
    connection_link = protocol + '://' + user + ':' + password + '@' + address + ':' + port + '//'
    
    return connection_link

#TODO: add warnings about extra parameters
def createMessage(msg_type, return_queue=None, interface='eth0', **kwargs):
    try:
        args = msg_args[msg_type]   
    except KeyError:
        print 'Unexpected message type "%s". List of available types: %s' % (msg_type, msg_args.keys())
        raise KeyError
    
    try:
        for element in args:
            kwargs[element]
    except KeyError:
        print 'Missing "%s" element in kwargs' % element
        raise KeyError
    
    return_address = getIPAdreess(interface)
    
    message = {
               'msg_type': msg_type,
               'return_params': {
                                 'return_address': return_address, 
                                 'return_queue': return_queue
                                 },
               'kwargs': kwargs,
    }
    
    return message

def messageCheck(message):
    msg_type = message['msg_type']
    kwargs = message['kwargs']
    
    try:
        args = msg_args[msg_type]   
    except KeyError:
        print 'Unexpected message type "%s". List of available types: %s' % (msg_type, msg_args.keys())
        raise KeyError
    
    try:
        for element in args:
            kwargs[element]
    except KeyError:
        print 'Missing "%s" element in kwargs' % element
        raise KeyError
    
    return True

class MessageConsumer(object):
    def __init__(self, connection_link, queue, callback):
        self.queue = queue
        self.connection_link = connection_link
        self.callback = callback
        self.logger = auxiliary.getLogger()

        self.logger.info('Connection link: ' + connection_link)
    
    def consumeOneMsg(self):
        ret = True
        
        with Connection(self.connection_link) as conn:
            with conn.SimpleQueue(self.queue) as simple_queue:
                try:
                    message = simple_queue.get_nowait()
                    self.logger.info('Message received')
                    self.callback(message)
                    message.ack()
                except Empty:
                    ret = False
                
                simple_queue.close()
                    
        return ret
    
    def constantConsuming(self):
        self.logger.info('Starting constant consuming')
        
        while True:
            if not self.consumeOneMsg():
                time.sleep(1)
                
class MessageProducer(object):
    def __init__(self, connection_link, queue, logger=None):
        self.queue = queue
        self.connection_link = connection_link
        self.logger = logger
        #logger.info('Connection link: ' + connection_link)
        
    def publish(self, message):
        with Connection(self.connection_link) as conn:
            with conn.SimpleQueue(self.queue) as simple_queue:
                simple_queue.put(message)
                #self.logger.info('Message sent')
                simple_queue.close()
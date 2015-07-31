'''
Created on May 25, 2015

@author: andrei
'''

from kombu import Connection
import time
from Queue import Empty
import ConfigParser
import hgsTools.auxiliary as auxiliary
import logging
import netifaces as ni

supported_apps = ['grok_hgs', 'enkf']

mgs_types_dic = {
                         'create': 'create_app',
                         'created': 'created_app',
                         'launch': 'launch_app',
                         'launched': 'launched_app',
                         'delete': 'delete_app',
                         'retrieve': 'retrieve_cli_output',
                         'output': 'update_output',
                         'accepted': 'app_accepted',
                         'info': 'update_info',
                         'status': 'update_app_status',
                         'spawning': 'update_vm_spawning_time',
                         'preprocessing': 'preprocessing',
                         'preprocessed': 'preprocessed',
}

kwargs_dic = {
                         'create_app': [],
                         'created_app': ['app_id'],
                         'launch_app': ['app_id'],
                         'launched_app': ['app_id'],
                         'delete_app': ['app_id'],
                         'retrieve_cli_output': ['app_id'],
                         'update_output': ['app_id', 'output'],
                         'app_accepted': ['tmp_id', 'app_id'],
                         'update_info': ['app_id', 'info_type', 'info'],
                         'update_app_status': ['app_id', 'status'],
                         'update_vm_spawning_time': ['app_id', 'time'],
                         'preprocessing': ['input'],
                         'preprocessed': ['input'],
}

#get IP address of the specified interface
def getIPAdreess(interface='eth0'):
    addr = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
    return addr

#builds a RabbitMQ connection link 
def buildRabbitMQConnectionLink(address, protocol='amqp', user='rabbitmq', password='rabbitmq', port='5672'):
    connection_link = protocol + '://' + user + ':' + password + '@' + address + ':' + port + '//'
    
    return connection_link

def buildRabbitMQConnectionLinkWrapper(config, address):
    protocol = auxiliary.read_option(config, 'rabbit_mq', 'protocol')
    user = auxiliary.read_option(config, 'rabbit_mq', 'user')
    password = auxiliary.read_option(config, 'rabbit_mq', 'password')
    #address = getIPAdreess()
    port = auxiliary.read_option(config, 'rabbit_mq', 'port')
    connection_link = buildRabbitMQConnectionLink(address, protocol=protocol, user=user, password=password, port=port)
    
    return connection_link

#TODO: add warnings about extra parameters
def createMessage(m_type, return_queue=None, interface='eth0', **kwargs):
    if m_type in mgs_types_dic:
        msg_type = mgs_types_dic[m_type]
    else:
        print "Unexpected type: %s. List of available types: %s" % (m_type, mgs_types_dic.keys())
        raise BaseException
    
    if msg_type not in mgs_types_dic.values() or msg_type not in kwargs_dic:
        print 'Something is wrong with the library'
        raise BaseException
    
    args = kwargs_dic[msg_type]
    
    for element in args:
        if element not in kwargs.keys():
            print 'Missing %s element in kwargs' % element
            raise BaseException
    
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
    
    if msg_type not in mgs_types_dic.values() or msg_type not in kwargs_dic:
        print 'Something is wrong with the library'
        raise BaseException
    
    args = kwargs_dic[msg_type]
    
    for element in args:
        if element not in kwargs:
            print 'Missing %s element in kwargs' % element
            raise BaseException
    
    return True

class MessageConsumer(object):
    def __init__(self, connection_link, queue, callback, logger):
        self.queue = queue
        self.connection_link = connection_link
        self.callback = callback
        self.logger = logger

        logger.info('Connection link: ' + connection_link)
        
    def consumeOneMsg(self):
        ret = True
        
        with Connection(self.connection_link) as conn:
            with conn.SimpleQueue(self.queue) as queue:
                try:
                    message = queue.get_nowait()
                    self.logger.info('Message received')
                    self.callback(message, self.logger)
                    message.ack()
                except Empty:
                    ret = False
                    
        return ret
    
    def constantConsuming(self):
        self.logger.info('Starting constant consuming')
        while True:
            if not self.consumeOneMsg():
                time.sleep(1)
                
                
'''class MessageConsumerWrapper(object):
    def __init__(self, connection_link, queue, logger, callback):
        
        
        self.consumer = MessageConsumer(connection_link, queue, callback, logger)
        #self.consumer.constantConsuming()
        
    def consumeOneMsg(self):
        return self.consumer.consumeOneMsg()
    
    def constantConsuming(self):
        self.consumer.constantConsuming()'''


class MessageProducer(object):
    def __init__(self, connection_link, queue, logger=None):
        self.queue = queue
        self.connection_link = connection_link
        self.logger = logger
        
        #logger.info('Connection link: ' + connection_link)
        
    def publish(self, message):
        with Connection(self.connection_link) as conn:
            with conn.SimpleQueue(self.queue) as queue:
                queue.put(message)
                #self.logger.info('Message sent')
                

'''class MessageProducerWrapper(object):
    def __init__(self, config_file_path, queue, logger):
        config = auxiliary.readConfig(config_file_path)
        QUEUE = auxiliary.read_option(config, 'general', queue)
        
        protocol = auxiliary.read_option(config, 'rabbit_mq', 'protocol')
        user = auxiliary.read_option(config, 'rabbit_mq', 'user')
        password = auxiliary.read_option(config, 'rabbit_mq', 'password')
        address = getIPAdreess()
        port = auxiliary.read_option(config, 'rabbit_mq', 'port')
        CONNECTION_LINK = buildRabbitMQConnectionLink(address, protocol=protocol, user=user, password=password, port=port)
        
        
        
        self.producer = MessageProducer(CONNECTION_LINK, QUEUE, logger)
        
    def publish(self, message):
        self.producer.publish(message)'''
    
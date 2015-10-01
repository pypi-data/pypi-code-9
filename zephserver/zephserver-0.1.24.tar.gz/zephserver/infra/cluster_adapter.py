# -*- coding: utf-8 -*-
'''
Copyright 2015 
    Centre de données socio-politiques (CDSP)
    Fondation nationale des sciences politiques (FNSP)
    Centre national de la recherche scientifique (CNRS)
License
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

import socket, logging, json, uuid
from threading import Thread, Lock, Event
from zephserversettings import CLUSTER_SERVER_LIST

class ClusterAdapter(Thread):
    '''
        Singleton class managing the cluster communication. The message will be serialized
        in JSON and sended to the cluster via the network. 

        If the message is too long it will be slices in smaller messages by 
        sender and rebuilt by receiver (implemented but not used nor tested yet
        see _BigMessageHandler)

        If the CLUSTER_SERVER_LIST variable in the configuration file est shorter than two
        elements, the cluster will act like if there is an actual cluster of server but it 
        will do nothing. This behavior is made to permet all the aplication to work the same
        way with or without cluster
    '''

    _instance = None
    _instance_lock = Lock()
    _stop_event = Event()

    _host = socket.gethostname()
    _address = None
    _port = None
    _cluster = None
    _stop_service = False
    _main_listening_socket = None
    _answer_socket = None
    _suscribers = {}
    _big_message_handler = None

    def __init__(self):
        logging.info('starting cluster service')
        Thread.__init__(self)
        # trying to find where we are in the cluster
        if len(CLUSTER_SERVER_LIST) > 1:
            self._cluster = CLUSTER_SERVER_LIST
            self._big_message_handler = _BigMessageHandler(self)
            for server in self._cluster:
                if server.has_key('hostname'):
                    if server['hostname'] == self._host:
                        self._address = server['address']
                        self._port = server['port']
        logging.info('starting cluster service done')


    @classmethod
    def get_instance(cls):
        '''
            managing the singleton
        '''
        if not cls._instance:
            cls._instance_lock.acquire()
            try:
                if not cls._instance:
                    cls._instance = ClusterAdapter()
            finally:
                cls._instance_lock.release()
            return cls._instance
        else:
            return cls._instance


    def run(self):
        '''
            main thread function, will manage the listening on the socket
        '''
        logging.info('running cluster adapter')
        if len(CLUSTER_SERVER_LIST) > 1 :
            self._main_listening_socket = socket.socket(socket.AF_INET6)
            self._main_listening_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._main_listening_socket.bind(('',self._port))
            self._main_listening_socket.listen(1)
            while not self._stop_service:
                try:
                    self._answer_socket, addr = self._main_listening_socket.accept()
                    data = self._answer_socket.recv(4096)
                    logging.debug('recieived from cluster ||%s|| ', data)
                    self._execute(data)
                except:
                    logging.warning('error while receiving data from cluster')
                finally:
                    self._answer_socket.sendall('#!#end_communication#!#')
                    self._answer_socket.close()
                    self._answer_socket = None
                    
            self._main_listening_socket.close()
        else:
            self._stop_event.wait()
            self._stop_event.clear()
        logging.info('cluster_adapter stoped')


    def _execute(self, data):
        '''
            Method calling the surscribers to the event launched by an other 
            member of the cluster
        '''
        try:
            clear_data = json.loads(data)
            if clear_data.has_key('event'):
                event = clear_data['event']
                if self._suscribers.has_key(event):
                    for suscriber in self._suscribers[event]:
                        try:
                            suscriber(clear_data)
                        except Exception, e:
                            logging.warning('cannot execute suscriber error %s', str(e))

        except:
            logging.warning('execution failed data : %s', data)


    def suscribe(self, event, callback):
        '''
            Public method for a service (or wathever function) to suscribe to a 
            cluster event

            event : string : name of the event
            callback : function : function to call when receiving the event
            
            warning : there is no method to unsuscribe...yet
        '''
        if event != None and callback != None:
            if not self._suscribers.has_key(event):
                self._suscribers[event] = []
            self._suscribers[event].append(callback)
            return True
        else:
            return False


    def send(self, event, data):
        '''
            build the json and send it to the whole cluster

            event : string : name of the event to call
            data : dict : data to pass to the suscriber on the other servers. 
                          Must be json serializable
        '''
        if len(CLUSTER_SERVER_LIST) > 1:
            try:
                if event != None and data != None:
                    # creation of the real dict to send
                    local_dict = {
                        'event': event,
                        'source' : self._host,
                        'data' : data
                    }
                    json_dict = json.dumps(local_dict)
                    if len(json_dict) > 3500:
                        self._big_message_handler.send_message(json_dict)
                    else:
                    # sending data top all the servers on the cluster
                        for server in CLUSTER_SERVER_LIST:
                            try:
                                if server['hostname'] != self._host:
                                    s = socket.socket(socket.AF_INET)
                                    s.connect((server['address'], server['port']))
                                    try:
                                        s.sendall(json_dict)
                                        ready = True
                                        while(ready):
                                            data = s.recv(1024)
                                            if  data != None and data != '':
                                                if '#!#end_communication#!#' == str(data):
                                                    ready = False
                                                    break
                                    finally:
                                        s.close()
                            except Exception, e:
                                logging.warning('cluster communication with ' + server['hostname'] + 'failed %s', e)

            except Exception, e:
                logging.warning('cluster communication failed %s', e)
        else:
            pass

    def disable(self):
        '''
            shut down the cluster adapter
        '''
        logging.warn('shutdown cluster module asked')
        if len(CLUSTER_SERVER_LIST) > 1:
            try:
                self._stop_service =  True
                s = socket.socket(socket.AF_INET)
                s.connect((self._address, self._port))
                s.sendall('dummy')
                s.recv(1024)
                s.close()
            except Exception, e:
                logging.error('shutdown cluster module failed because : %s', e)
        else:
            self._stop_event.set()








class _BigMessageHandler(object):
    '''
        private class managing big message by slicing them in small chunks 
        (less than 3500 bytes) and rebuilding the whole json when receiving 
        sliced message

        warning not tested nor used
    '''
    _message_dict = {}
    _cluster_adapter = None

    def __init__(self, cluster_adapter):
        self._cluster_adapter = cluster_adapter
        self._cluster_adapter.suscribe('multipart', self.multipart_callback)

    def send_message(self, data):
        '''
            slice the message in 3500 bytes chunks and sending them as multipart message
        '''
        message_id = uuid.uuid1().hex
        chunk_length = 3500
        splidetd = [data[i:i + chunk_length] for i in range(0, len(data), chunk_length) ]
        sent_data = {
            'uuid' : message_id,
            'parts' : len(splidetd)
        }
        for i in range(len(splidetd)):
            sent_data['number'] = i
            sent_data['data'] = splidetd[i]
            self._cluster_adapter.send('multipart', sent_data)

    def multipart_callback(self, data):
        '''
            receiving multipart messages and rebuilding the original message before
            to execute them as if there was only one message
        '''
        message_data = data["data"]
        # creattion of the message if needed
        if not self._message_dict.has_key(message_data['uuid']):
            self._message_dict[message_data['uuid']] = {}
        # storing the chunk
        self._message_dict[message_data['uuid']][message_data['number']] = message_data['data']
        # if the message is complete rebuilding it
        if len(self._message_dict[message_data['uuid']]) == message_data['parts']:
            rebuilt = ''
            for i in range(message_data['parts']):
                rebuilt += self._message_dict[message_data['uuid']][i]
            # once the json is rebuit executing it
            self._cluster_adapter._execute(rebuilt)
            # forgetting message(destruction)
            del self._message_dict[message_data['uuid']]
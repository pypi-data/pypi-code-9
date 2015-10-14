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


import logging
import socket
import os
from threading import Thread, Event

from zephserversettings import CONFIGURATION_NETWORK_INTERFACE_SERVER

class ExternalControl(Thread):
    '''
        Class controlling the communication from the command script Actualy only used to 
        stop the server.

        this class is a sigleton.

        Warning : this class use a UNIX socket and is not compatible with Windows
    '''

    _bootstrap = None
    _stop_server = False
    _answer_socket = None
    _speaking_event = Event()
    _main_socket = None

    def __init__(self, bootstrap):
        Thread.__init__(self)
        self._bootstrap = bootstrap
        logging.info('creating admin_interface')
        
    

    def run(self):
        # Trying to remove the old socket file after a nasty stop
        try:
            os.remove(CONFIGURATION_NETWORK_INTERFACE_SERVER)
        except:
            pass
        self._main_socket = socket.socket(socket.AF_UNIX)
        self._main_socket.bind(CONFIGURATION_NETWORK_INTERFACE_SERVER)
        self._main_socket.listen(1)
        while not self._stop_server:
            try:
                self._answer_socket, addr = self._main_socket.accept()
                data = self._answer_socket.recv(1024)
                logging.info('recieived commande ||%s|| ', data)
                self._execute(data)# executing command

                self._speaking_event.wait() # waiting for the command to end
                self._speaking_event.clear()
            except Exception, e:
                logging.error('%s', e)
            finally:
                self._answer_socket.sendall('#!#end_communication#!#')
                self._answer_socket.close()
                self._answer_socket = None
        try:
            self._main_socket.close()
            os.remove(CONFIGURATION_NETWORK_INTERFACE_SERVER)
        except : 
            pass
        logging.info('external config closed')

    def _execute(self, data):
        '''
            private method executing commands
        '''
        try:
            argv = data.split(' ')
            command = argv[0]
            if command == 'stop':
                self._bootstrap.command_stop()
            else:
                self.say('unknow command')
        except Exception, e:
            logging.warning('%s', str(e))
        finally:
            self._speaking_event.set()
            


    def halt_external_control(self):
        logging.warning('halt external control asked')
        self._stop_server = True
        self._speaking_event.set()
        if self._main_socket != None:
            try:
                s = socket.socket(socket.AF_UNIX)
                s.connect(CONFIGURATION_NETWORK_INTERFACE_SERVER)
                s.sendall('dummy')
                s.recv(1024)
                s.close()
            except:
                pass

    def stop(self):
        '''
            Executing 'stop' command
        '''
        logging.warning("stoping server asked")
        self._bootstrap.command_stop()

    def say(self, data):
        '''
            public method to print somthing on the command shell(if a command script in connected)
        '''
        if self._answer_socket != None:
            self._answer_socket.sendall(data + '\n')


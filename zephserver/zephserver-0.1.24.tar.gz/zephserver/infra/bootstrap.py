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

import logging, os.path, os
from threading import Event

from zephserver.infra.service_manager import ServiceManager
from zephserversettings import LOG_LEVEL, LOG_PATH, LOCK_FILE
from zephserver.infra.external_control import ExternalControl
from zephserver.infra.cluster_adapter import ClusterAdapter

class Bootstrap:
    '''
        class managing the launch and stop sequences
    '''


    _stop_event = Event()
    _external_control = None
    _is_testing = False  # variabel changeant legerement la cinematique du bootstrap pour faire passer les TU


    def __init__(self, argv=None):
        self._argv = argv

    def start_server(self):
        '''
            launch the true starting sequence for the server
        '''
        self._set_logger()
        if self._is_server_started():
            print('\nserver alrady started if not remove the lock(if you are running the test this message is normal)')
            logging.error('server alrady started if not remove the lock')
            return 1
        else:
            self._lock_instance()
            logging.info('starting server')
            cluster_adapter = ClusterAdapter.get_instance()
            cluster_adapter.start()
            service_manager = ServiceManager.get_instance()
            service_manager.create_all_service(True)
            self._external_control = ExternalControl(self)
            self._external_control.start()
            logging.info('server started')
            if self._is_testing:
                pass
            else :
                # waiting for the stop order
                self._stop_event.wait()
                self.stop_server()
        return 0


    def command_stop(self):
        '''
            ask the server to stop
        '''
        self._stop_event.set()


    def stop_server(self):
        '''
            stoping sequence of the server
        '''
        logging.info('halting server requested')
        service_manager = ServiceManager.get_instance()
        service_manager.stop_service_manager()
        self._external_control.halt_external_control()
        self._external_control.join()
        cluster_adapter = ClusterAdapter.get_instance()
        cluster_adapter.disable()
        cluster_adapter.join()
        self._release_instace()
        logging.info('halting server done')



    def _set_logger(self, log_level=LOG_LEVEL, log_path=LOG_PATH):
        '''
            private method for handeling log level anf log path
            default log level is INFO
            default log path is ./logging.log
        '''
        level=None
        if log_level.upper() == 'DEBUG':
            level = logging.DEBUG
        elif log_level.upper() == 'INFO':
            level=logging.INFO
        elif log_level.upper() == 'WARNING':
            level=logging.WARNING
        elif log_level.upper() == 'ERROR':
            level=logging.ERROR
        elif log_level.upper() == 'CRITICAL':
            level=logging.CRITICAL
        else:
            level=logging.INFO

        if log_path == None or log_path == '':
            path = './logging.log'
        else:
            path = log_path

        logging.basicConfig(filename=path, level=level, format='%(asctime)s\t%(levelname)s\t%(module)s\t: %(message)s')

    def _is_server_started(self):
        '''
            return true if a server is started and false otherwise
            the other instance of the server is detected via a lock file
        '''
        return os.path.isfile(LOCK_FILE)


    def _lock_instance(self):
        '''
            create the lock file for blocking multiple instance of the server
        '''
        lock = open(LOCK_FILE, 'w+')
        lock.close()

    def _release_instace(self):
        '''
            destroy lock file.
            this method is the last thing done by the server at the end of stop sequence
        '''
        os.remove(LOCK_FILE)

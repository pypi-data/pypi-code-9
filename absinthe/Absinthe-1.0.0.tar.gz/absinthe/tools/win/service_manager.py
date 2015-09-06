
from os.path import splitext, abspath
from sys import modules

import win32serviceutil
import win32service
import win32api

class ServiceManager(object):

    def __init__(self, cls, name, display_name = None):
        '''
            cls : the class (derived from Service) that implement the Service
            name : Service name
            display_name : the name displayed in the service manager
        '''
        self.cls = cls
        cls._svc_name_ = name
        cls._svc_display_name_ = display_name or name

        try:
            module_path = modules[cls.__module__].__file__
        except AttributeError:
            # maybe py2exe went by
            from sys import executable
            module_path = executable

        module_file = splitext(abspath(module_path))[0]
        cls._svc_reg_class_ = '%s.%s' % (module_file, cls.__name__)

    def start(self):
        try:
            win32serviceutil.StartService(self.cls._svc_name_)
            return True
        except Exception as e:
            # the service is not installed
            if e[0] in [1060, 1056]:
                return False
            else:
                raise

    def stop(self):
        try:
            win32serviceutil.StopService(self.cls._svc_name_)
            return True
        except Exception as e:
            # the service is not running
            if e[0] in [1060, 1062]:
                return False
            else:
                raise

    def remove(self):
        self.stop()
        try:
            svc_mgr = win32service.OpenSCManager(None,None,win32service.SC_MANAGER_ALL_ACCESS)
            svc_handle = win32service.OpenService(svc_mgr, self.cls._svc_name_, win32service.SERVICE_ALL_ACCESS)
            win32service.DeleteService(svc_handle)
            return True
        except Exception as e:
            # the service is not installed
            if e[0] in [1060]:
                return False
            else:
                raise

    def install(self, stay_alive=True):
        '''
            stay_alive : Service will stop on logout if False
        '''
        if stay_alive: win32api.SetConsoleCtrlHandler(lambda x: True, True)
        try:
            win32serviceutil.InstallService(
                self.cls._svc_reg_class_,
                self.cls._svc_name_,
                self.cls._svc_display_name_,
                startType = win32service.SERVICE_AUTO_START
            )
            return True
        except Exception as e:
            # the service is already
            if e[0] in [1073]:
                return False
            else:
                raise

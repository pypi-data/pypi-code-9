#! /usr/bin/env python
#coding=utf-8

import win32serviceutil
import win32service
import subprocess

#daemon process command line
# this is modified from mointwisted.cmd
mointwisted = r'D:\Python26\python.exe "D:\Python26\Scripts\twistd.py" --python mointwisted.py'
#daemon process current dir
mointwisted_dir = r"E:\Moin\moin"


#py2.5 use TerminateProcess to kill service daemon
import ctypes

kernel32 = ctypes.windll.LoadLibrary('kernel32.dll')

def kill_process(pid):
    handle = kernel32.OpenProcess(1, False,pid)
    if handle:
        kernel32.TerminateProcess(handle,0)
    else:
        print 'can\'t open process %s' % pid

class servicerunner(win32serviceutil.ServiceFramework):
    _svc_name_ = "mointwisted"
    _svc_display_name_ = "mointwisted"
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        
        #init stop flag
        self.service_want_to_stop = False

    def SvcStop(self):
        # tell SCM I am stoping
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        
        #set stop flag
        self.service_want_to_stop = True
        
        #py2.6 use Popen.terminate() to kill service daemon process
        #self.p.terminate()
        
        #py2.5 use TerminateProcess() to kill service daemon process
        kill_process(self.p.pid)

    def SvcDoRun(self):
        #now I do not want to stop
        self.service_want_to_stop = False
        
        #this "while" is to make sure the daemon auto restarting when
        #ending with a error or crashing,when I do not want to stop
        while (self.service_want_to_stop == False):
            self.p = subprocess.Popen(mointwisted,cwd=mointwisted_dir)
            self.p.wait()

if __name__=='__main__':
    '''usage:
    u can use 'servicerunner.py install' to install service.
    'servicerunner.py will give the usage' '''
    win32serviceutil.HandleCommandLine(servicerunner)

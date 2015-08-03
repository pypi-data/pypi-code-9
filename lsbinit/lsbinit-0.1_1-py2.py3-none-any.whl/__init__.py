from sys import argv, exit
from subprocess import Popen
from os import kill, devnull, makedirs
from os.path import dirname, isdir

# Lense Libraries
from .common import _LSBCommon
from .pid import _LSBPIDHandler
from .lock import _LSBLockHandler

# Module version
__version__ = '0.1-1'

class LSBInit(_LSBCommon):
    def __init__(self, name, pid, lock, exe, output=None):
        super(LSBInit, self).__init__()
        
        # Lock / PID handler
        self.lock      = _LSBLockHandler(lock)
        self.pid       = _LSBPIDHandler(pid)
        
        # Service command / executable
        self.command   = argv[1]
        self.exe       = exe

        # Command output
        self.output    = output
            
    def is_running(self):
        """
        Check if the service is running.
        """
        try:
            kill(self.pid.get(), 0)
        
        # Process not running, remove PID/lock file if it exists
        except:
            self.pid.remove()
            self.lock.remove()
            
    def set_output(self):
        """
        Set the output for the service command.
        """
        if not self.output:
            return devnull
        
        # Get the output file path
        output_dir = dirname(self.output)
        
        # Make the path if it doesn't exist
        if not isdir(output_dir):
            try:
                makedirs(output_dir)
                return self.output
            except Exception as e:
                self.die('Failed to create output directory "{}": {}'.format(output_dir, str(e)))
            
    def do_start(self):
        if not self.is_running():
            try:
                output = self.set_output()
        
                # Generate the run command
                cmd  = ['nohup', self.exe] if isinstance(self.exe, str) else ['nohup'] + self.exe
            
                # Start the process and get the PID number
                proc = Popen(command, shell=False, stdout=output, stderr=output)
                pnum = str(proc.pid)
                
                # Generate the PID and lock files
                self.pid.make()
                self.lock.make()
                self.write_stdout('Service is running [PID {}]...'.format(pnum))
                
            # Failed to start process
            except Exception as e:
                self.die('Failed to start service: {}'.format(str(e)))
             
        # Service already running   
        else:
            self.write_stdout('Service already running [PID {}]...'.format(self.pid.get()))
    
    def do_stop(self):
        if self.is_running():
            self.pid.kill()
            self.lock.remove()
            
            # If the service failed to stop
            if self.is_running():
                self.die('Failed to stop service...')
            self.write_stdout('Service stopped...')
            
        # Service already stopped
        else:
            self.write_stdout('Service already stopped...')
    
    def do_status(self):
        """
        Get the status of the service.
        """
        pid    = self.pid.get()
        status = 'running [PID {}]'.format(pid) if pid else 'stopped'
        self.write_stdout('Service is {}...'.format(status))
            
    def do_systemd_start(self):
        self.do_start()
    
    def do_restart(self):
        self.do_stop()
        self.do_start()
            
    def interface(self):
        """
        Public method for handling service command argument.
        """
        
        # Possible control arguments
        controls = {
            'start': self.do_start,
            'stop': self.do_stop,
            'status': self.do_status,
            'systemd-start': self.do_systemd_start,
            'restart': self.do_restart,
            'force-reload': self.do_restart    
        }
        
        # Process the control argument
        try:
            controls[self.command]()
        except KeyError:
            self.write_stdout('Usage: {} {{start|stop|status|restart|force-reload|systemd-start}}'.format(self.name), 3)
        exit(0)
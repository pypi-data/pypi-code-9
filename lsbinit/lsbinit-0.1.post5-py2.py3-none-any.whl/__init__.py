from __future__ import print_function
from sys import argv, exit
from subprocess import Popen
from os import kill, devnull, makedirs, setpgrp, environ
from os.path import dirname, isdir

# Lense Libraries
from .common import _LSBCommon
from .pid import _LSBPIDHandler
from .lock import _LSBLockHandler

# Module version
__version__ = '0.1-5'

# Unicode characters
UNICODE = {
    'dot': u'\u2022'
}

def set_environ(inherit=True, append={}):
    """
    Helper method for passing environment variables to the subprocess.
    """
    _environ = {} if not inherit else environ
    for k,v in append.iteritems():
        _environ[k] = v
    return _environ 

class LSBInit(_LSBCommon):
    def __init__(self, name, pid, lock, exe, output=None, desc='', env=None, shell=False):
        super(LSBInit, self).__init__()
        
        # Service name / description
        self.name      = name
        self.desc      = desc
        
        # Lock / PID handler
        self.lock      = _LSBLockHandler(lock)
        self.pid       = _LSBPIDHandler(pid)
        
        # Service command / executable / environment / shell
        self.command   = argv[1]
        self.exe       = exe
        self.env       = env
        self.shell     = shell

        # Command output
        self.output    = output

    def _colorize(self, msg, color=None, encode=False):
        """
        Colorize a string.
        """
        
        # Valid colors
        colors = {
            'red':    '31',
            'green':  '32',
            'yellow': '33'
        }
        
        # No color specified or unsupported color
        if not color or not color in colors:
            return msg
        
        # The colorized string
        if encode:
            return u'\x1b[1;{}m{}\x1b[0m'.format(colors[color], msg)
        return '\x1b[1;{}m{}\x1b[0m'.format(colors[color], msg)
            
    def is_running(self):
        """
        Check if the service is running.
        """
        try:
            kill(int(self.pid.get()), 0)
            return True
        
        # Process not running, remove PID/lock file if it exists
        except:
            self.pid.remove()
            self.lock.remove()
            return False
            
    def set_output(self):
        """
        Set the output for the service command.
        """
        if not self.output:
            return devnull
        
        # Get the output file path
        output_dir = dirname(self.output)
        
        # Make the path exists
        if not isdir(output_dir):
            try:
                makedirs(output_dir)
            except Exception as e:
                self.die('Failed to create output directory "{}": {}'.format(output_dir, str(e)))
        return open(self.output, 'a')
            
    def do_start(self):
        if not self.is_running():
            try:
                output = self.set_output()
        
                # Generate the run command
                command = ['nohup', self.exe] if isinstance(self.exe, str) else ['nohup'] + self.exe
            
                # Start the process
                proc = Popen(command,  
                    stdout = output, 
                    stderr = output, 
                    shell  = self.shell,
                    env    = self.env
                )
                pnum = str(proc.pid)
                
                # Generate the PID and lock files
                self.pid.make(pnum)
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
        
        # Get the PID of the service
        pid    = self.pid.get()
        
        # Status color / attributes
        status_color  = 'green' if pid else 'red'
        status_dot    = self._colorize(UNICODE['dot'], status_color, encode=True)
        
        # Active text
        active_txt    = {
            'active':   '{} since {}'.format(self._colorize('active (running)', 'green'), self.pid.birthday()[1]),
            'inactive': 'inactive (dead)'
        }
        
        # Print the status message
        print(status_dot, end=' ')
        print('{}.service - LSB: {}'.format(self.name, self.desc))
        print('   Loaded: loaded (/etc/init.d/{})'.format(self.name))
        print('   Active: {}'.format(active_txt['active' if pid else 'inactive']))
        
        # Extra information if running
        if pid:
            ps = self.pid.ps()
            print('  Process: {}; [{}]'.format(pid, ps[0]))
            if ps[1]:
                for c in ps[1]:
                    print('    Child: {}'.format(c))
        print('')
            
    def do_reload(self):
        """
        There needs to be a customizable way for the developer to implement
        their own reload method depending on the needs of the application.
        """
        self.do_restart()
    
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
            'restart': self.do_restart,
            'reload': self.do_restart    
        }
        
        # Process the control argument
        try:
            controls[self.command]()
        except KeyError:
            self.write_stdout('Usage: {} {{start|stop|status|restart|reload}}'.format(self.name), 3)
        exit(0)
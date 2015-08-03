from os import makedirs, remove, kill
from os.path import dirname, isfile, isdir

# Lense Libraries
from .common import _LSBCommon

class _LSBPIDHandler(_LSBCommon):
    """
    Class wrapper for handling a service PID file.
    """
    def __init__(self, pid_file):
        super(_LSBPIDHandler, self).__init__()
        
        # PID file / directory
        self.pid_file = pid_file
        self.pid_dir  = dirname(pid_file)
        
    def get(self):
        """
        Retrieve the process ID from the PID file.
        """
        if isfile(self.pid_file):
            return open(self.pid_file, 'r').read()
        return None

    def make(self):
        """
        Make a PID file and populate with PID number.
        """
        try:
        
            # Make sure the PID directory exists
            if not isdir(self.pid_dir):
                makedirs(self.pid_dir, 0755)
                
            # Create the PID file
            pid_file = open(self.pid_file, 'w').write(self.get())
            pid_file.close()
        except Exception as e:
            self.die('Failed to generate PID file: {}'.format(str(e)))
    
    def remove(self):
        """
        Remove the PID file.
        """
        if isfile(self.pid_file):
            try:
                remove(self.pid_file)
            except Exception as e:
                self.die('Failed to remove PID file: {}'.format(str(e)))
        else:
            return True

    def kill(self):
        """
        Kill the running process and remove the PID/lock file.
        """
        try:
            kill(self.get(), 9)
            
        # Failed to kill the process
        except Exception as e:
            self.die('Failed to kill process: {}'.format(str(e)))
            
        # Remove the stale PID file
        self.remove()
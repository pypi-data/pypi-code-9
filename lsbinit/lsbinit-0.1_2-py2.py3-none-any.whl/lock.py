from os import remove, makedirs
from os.path import dirname, isfile, isdir

# Lense Libraries
from .common import _LSBCommon

class _LSBLockHandler(_LSBCommon):
    """
    Class wrapper for handling a service lock file.
    """
    def __init__(self, lock_file):
        super(_LSBLockHandler, self).__init__()
        
        # Lock file / directory
        self.lock_file = lock_file
        self.lock_dir  = dirname(lock_file)

    def exists(self):
        """
        Check if the lock file exists.
        """
        return exists(self.lock_file)

    def remove(self):
        """
        Remove the service lock file.
        """
        if isfile(self.lock_file):
            try:
                remove(self.lock_file)
            except Exception as e:
                self.die('Failed to remove lock file: {}'.format(str(e)))
        else:
            return True

    def make(self):
        """
        Make the lock file.
        """
        try:
        
            # Make sure the PID directory exists
            if not isdir(self.lock_dir):
                makedirs(self.lock_dir, 0755)
                
            # Create the lock file
            open(self.lock_file, 'w').close()
        except Exception as e:
            self.die('Failed to generate lock file: {}'.format(str(e)))
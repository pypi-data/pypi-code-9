from __future__ import division
from __future__ import unicode_literals
import re
from time import tzname, time
from datetime import datetime
from os import makedirs, remove, kill
from os.path import dirname, isfile, isdir, getmtime
from subprocess import Popen, PIPE

# Lense Libraries
from .common import _LSBCommon

# Weekday mapping
WEEKDAY = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

class _LSBPIDHandler(_LSBCommon):
    """
    Class wrapper for handling a service PID file.
    """
    def __init__(self, pid_file):
        super(_LSBPIDHandler, self).__init__()
        
        # PID file / directory
        self.pid_file = pid_file
        self.pid_dir  = self.mkdir(dirname(pid_file))
        
        # Regexes
        self.regex = {
            'pid': re.compile(r'^[^ ]*[ ]*([\d]+).*$'),
            'parent': re.compile(r'^[^ ]*[ ]*[\d]+[ ]+([\d]+).*$')
        }
        
    def _ps_extract_pid(self, line):
        """
        Extract PID and parent PID from an output line from the PS command
        """
        this_pid = self.regex['pid'].sub(r'\g<1>', line)
        this_parent = self.regex['parent'].sub(r'\g<1>', line)
        
        # Return the main / parent PIDs
        return this_pid, this_parent
        
    def ps(self):
        """
        Get the process information from the system PS command.
        """
        
        # Get the process ID
        pid = self.get()
        
        # Parent / child processes
        parent   = None
        children = []
        
        # If the process is running
        if pid:
            proc   = Popen(['ps', '-ef'], stdout=PIPE)
            for _line in proc.stdout.readlines():
                line = self.unicode(_line.rstrip())
                
                # Get the current PID / parent PID
                this_pid, this_parent = self._ps_extract_pid(line)
                try:
                    
                    # If scanning a child process
                    if int(pid) == int(this_parent):
                        children.append('{}; [{}]'.format(this_pid.rstrip(), re.sub(' +', ' ', line)))
                    
                    # If scanning the parent process
                    if int(pid) == int(this_pid):
                        parent = re.sub(' +', ' ', line)
                        
                # Ignore value errors
                except ValueError:
                    continue
                
        # Return the parent PID and any children processes
        return (parent, children)
        
    def created(self):
        """
        Get the creation date for the PID file.
        """
        return getmtime(self.pid_file)
        
    def age(self):
        """
        Get the age of the PID file.
        """
        
        # Created timestamp
        created = self.created()
        
        # Age in seconds / minutes / hours / days
        age_secs  = time() - created
        age_mins  = 0 if (age_secs < 60) else (age_secs / 60)
        age_hours = 0 if (age_secs < 3600) else (age_mins / 60)
        age_days  = 0 if (age_secs < 86400) else (age_hours / 24)
        
        # Return the age tuple
        return (
            int(age_secs), 
            int(age_mins), 
            int(age_hours), 
            int(age_days)
        )
        
    def birthday(self):
        """
        Return a string representing the age of the process.
        """
        if isfile(self.pid_file):
            
            # Timestamp / timezone string
            tstamp  = datetime.fromtimestamp(self.created())
            tzone   = tzname[0] 
            weekday = WEEKDAY[tstamp.isoweekday()]
            
            # PID file age / age string
            age     = self.age()
            age_str = '{}s ago'.format(age[0]) 
            
            # Birthday string
            bday   = '{} {} {}; {}'.format(weekday, tstamp, tzone, age_str)
            
            # Return timestamp / timestamp string
            return (self.created(), bday)
        return (None, None)
        
    def get(self):
        """
        Retrieve the process ID from the PID file.
        """
        if isfile(self.pid_file):
            return open(self.pid_file, 'r').read()
        return None

    def make(self, pnum):
        """
        Make a PID file and populate with PID number.
        """
        try:
                
            # Create the PID file
            self.mkfile(self.pid_file, pnum)
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
            kill(int(self.get()), 9)
            
        # Failed to kill the process
        except Exception as e:
            self.die('Failed to kill process: {}'.format(str(e)))
            
        # Remove the stale PID file
        self.remove()
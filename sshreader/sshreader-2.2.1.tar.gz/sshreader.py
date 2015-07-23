# coding=utf-8
"""A python module for multi-processing/threading ssh connections in order to make ssh operations
across multiple servers more parallel.  The module allows for timeouts for each ssh connection
as well as each command given to an ssh connection to run.  ServerJob objects allow for each server
to have multiple commands that should be run inside of that job.  The results
from each job will be returned as a list of tuples inside of each ServerJob object in the same order that the
command list is in.

SSHreader can also be used to create and call ssh connections without multiple processes/threads.

SSHreader can also run multi-processed/threaded shell commands on localhost and a serverJobList can contain both
serverJobs running on localhost as well as serverJobs running over ssh

When using pcount and tcount in conjunction tcount will equal the total number of threads each process is allowed to
spawn.  If the total jobs per process is less than tcount then the number of threads per process will equal the number
of jobs assigned to that process.  Thus, to find the total threads used across all processes use:
(pcount * tcount) = total_threads!

When using pcount, sshreader attempts to ensure that jobs are split evenly between the number of requested subprocesses.

The sshread method currently limits you to processing 1 million serverJobs at a time, per __jobHardLimit__ global.

The cpusoftlimit for a box is defined as (cpu_count - 1).  This means that sshreader will spawn a subprocess for all but
one cpu on a given box.

.. note::
    The cpuhardlimit is the maximum number of subprocesses that sshreader will spawn on a given box defined as:
    (cpuhardlimit * __cpuHardLimitFactor__).  This is so that you don't make a box unusable and was arrived at per my
    own testing.  Currently __cpuHardLimitFactor__ is set to 3.
    These numbers may increase in the future."""
# Copyright (C) 2015 Jesse Almanrode
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Lesser General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Lesser General Public License for more details.
#
#     You should have received a copy of the GNU Lesser General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
__version__ = '2.2.1'

# Include
import sys
import paramiko
import logging
from subprocess import Popen, PIPE, STDOUT
from os import getpid
from multiprocessing import Process, cpu_count
from multiprocessing import Queue as processQueue
from threading import Thread
from Queue import Queue as threadQueue
from types import FunctionType

# Globals
separator = "---------"
tqueue = None
tcounter = 0
pqueue = None
finqueue = None
__jobHardLimit__ = (10 ** 6)
__cpuHardLimitFactor__ = 3
__previouspercentage__ = -1


class InvalidHook(Exception):
    """A pre or post hook definition is invalid
    """
    pass


class ProcessesOrThreads(Exception):
    """You did not specify whether to use subprocessing or threading
    """
    pass


class ExceededJobLimit(Exception):
    """Your number of jobs exceeds the current limit
    """
    pass


class ExceededCPULimit(Exception):
    """You have asked for more sub processes than your CPU is allowed to handle
    """
    pass


def progress_bar(progress, total, longbar=False):
    """Prints a syled progress bar

    - **parameters** and **return types**::

        :param progress: Current item number being processed
        :param total: Total number of items being processed
        :param longbar: Use a longer style progress bar
        :return: None
    """
    global __previouspercentage__
    percent_float = float(progress) / float(total)
    percent = int(percent_float * 100)
    if __previouspercentage__ != percent:
        if longbar:
            hashes = "#" * percent
        else:
            hashes = "=" * int(percent/2)
            if percent % 2 != 0:
                hashes += "-"
        template = "[%s] %s%%" % (hashes, str(percent))
        if percent < 100:
            sys.stdout.write('\r' + template)
            sys.stdout.flush()
            __previouspercentage__ = percent
        else:
            __previouspercentage__ = -1
            print '\r' + template
    return None


def do_shell_script(command, combine=False):
    """Run a specified command in the shell on localhost and return the output

    - **parameters** and **return types**::

        :param command: String containing the shell script to run
        :param combine: Combine stderr and stdout in output
        :return: Tuple of (command,stdout,stderr) or (command,output)
    """
    if combine:
        pipeout = Popen(command, shell=True, stdout=PIPE, stderr=STDOUT).stdout
        stdout = pipeout.read()
        return command, stdout.strip()
    else:
        pipeout = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
        stdout, stderr = pipeout.communicate()
        return command, stdout.strip(), stderr.strip()


def tprint(message, stderr=False):
    """Attempt at a thread-safe print variation

    - **parameters** and **return types**::

        :param message: Message to output to stdout
        :param stderr: Message should go to stderr
        :return: None
    """
    if message.endswith('\n') is False:
        message += '\n'
    if stderr:
        sys.stderr.write(message)
        sys.stderr.flush()
    else:
        sys.stdout.write(message)
        sys.stdout.flush()
    return None


def _validate_hook_(hook):
    """Private method to take a pre or post hook and validate it!
    
    - **parameters** and **return types**::
    
        :param hook: Dictionary of {'func':<function>, 'args':[<args>], 'kwargs':{<dictionary>}}
        :return: Dictionary
    """
    if type(hook) is not dict:
        raise InvalidHook(str(hook) + " is not of type dict")
    hookkeys = hook.keys()
    if 'func' in hookkeys:
        if type(hook['func']) is not FunctionType:
            raise TypeError("'func' is not type FunctionType")
    if 'args' in hookkeys:
        if type(hook['args']) is list:
            pass
        elif type(hook['args']) is tuple:
            hook['args'] = list(hook['args'])
        else:
            hook['args'] = [hook['args']]
    else:
        hook['args'] = []
    if 'kwargs' in hookkeys:
        if type(hook['kwargs']) is not dict:
            raise TypeError("'kwargs' is not type dict")
    else:
        hook['kwargs'] = {}
    return hook


class ServerJob(object):
    """
    Custom class for holding all the info needed to run ssh commands or shell commands in subprocesses or threads

    - **parameters** and **return types**::

        :param fqdn: Fully qualified domain name or IP address
        :param cmds: List of commands to run (in the order you want them run)
        :param username: Username for SSH
        :param password: Password for SSH
        :param keyfile: Path to ssh key (can be used instead of password)
        :param debuglevel: 0 = off, 1 = some, 2 = more, 3 = all
        :param timeout: Timeout for entire job (30 seconds by default)
        :param cmdtimeout: Timeout for each command (30 seconds by default)
        :param runlocal: Run job on localhost (skips ssh to localhost)
        :param prehook: Dictionary of {'func':<function>, 'args':[<args>], 'kwargs':{<dictionary>}}
        :param posthook: Dictionary of {'func':<function>, 'args':[<args>], 'kwargs':{<dictionary>}}
        :return: serverJob Object

    - **properties**::
        :property cmdResults: List of results of each command in tuple form (cmd, stdout, stderr)
        :propery cmdStatus: List of states for each command ( None = initial state/cmd did not run, True = no stderr,
                            False = stderr)
        :property status: State of entire job (None = initial state/ssh failed, True = all cmd statuses is True,
                            False = one or more cmd statuses is False)
        :property prehook_return: Returned values from prehook method
        :property posthook_return: Returned values from posthook method
        :property combine_output: Combine stdout and stderr in cmdResults (default = False)
    """
    def __init__(self, fqdn, cmds, username=None, password=None, keyfile=None, debuglevel=0, timeout=30,
                 cmdtimeout=30, runlocal=False, prehook=None, posthook=None):
        if type(cmds) in (list, tuple):
            self.cmds = cmds
        else:
            self.cmds = [cmds]
        self.cmdResults = []
        self.cmdStatus = []
        self.username = username
        self.password = password
        self.key = keyfile
        self.status = None
        self.timeout = timeout
        self.cmdtimeout = cmdtimeout
        self.runlocal = runlocal
        self.name = fqdn
        self.prehook_return = None
        if prehook is not None:
            self.prehook = _validate_hook_(prehook)
        else:
            self.prehook = None
        self.posthook_return = None
        if posthook is not None:
            self.posthook = _validate_hook_(posthook)
        else:
            self.posthook = None
        self.combine_output = False
        try:
            if int(debuglevel) <= 3:
                self.debuglevel = debuglevel
            else:
                raise TypeError("Debug level must be an integer between 0 and 3")
        except Exception:
            raise TypeError("Debug level must be an integer between 0 and 3")
        if runlocal is False:
            self.ssh_con = None
            if keyfile is None:
                if username is None or password is None:
                    raise paramiko.SSHException("You must enter a username and password or supply an SSH key")
                else:
                    self.keyauth = False
            else:
                self.keyauth = True
        else:
            self.ssh_con = "localhost"

    def run(self):
        """Run a serverJob. SSH to server, run cmds, return result

        - **parameters** and **return types**::

            :return: serverJob.status
        """
        if self.debuglevel >= 1:
            print("Running serverJob: " + self.name)
        # Run prehook if it is defined
        if self.prehook is not None:
            if self.debuglevel >= 2:
                print("Running prehook")
            self.prehook['args'].append(self)
            self.prehook_return = self.prehook['func'](*self.prehook['args'], **self.prehook['kwargs'])
            self.prehook['args'].remove(self)
        # Establish SSH Connection if we are not working locally
        if self.runlocal is False:        
            try:
                if self.keyauth:
                    if self.username is None:
                        self.ssh_con = SSH(self.name, keyfile=self.key, timeout=self.timeout)
                    else:
                        self.ssh_con = SSH(self.name, username=self.username, keyfile=self.key, timeout=self.timeout)
                else:
                    self.ssh_con = SSH(self.name, username=self.username, password=self.password, timeout=self.timeout)
            except Exception, errorMsg:
                if self.debuglevel >= 2:
                    print(errorMsg)
                self.ssh_con = None
                if self.debuglevel >= 1:
                    print(self.name + ": Unable to establish ssh connection!")
        # This is a trick statement to allow ssh and local shell scripts to be run using similar output processing code
        if self.ssh_con is not None:
            for idX, thiscmd in enumerate(self.cmds):
                # Now running each command in turn
                self.cmdStatus.append(None)
                if self.debuglevel >= 3:
                    print(self.name + " running: " + thiscmd)
                if self.runlocal:
                    if self.combine_output:
                        result = do_shell_script(thiscmd, combine=True)
                    else:
                        result = do_shell_script(thiscmd)
                else:
                    if self.combine_output:
                        result = self.ssh_con.ssh_command(thiscmd, timeout=self.cmdtimeout, combine=True)
                    else:
                        result = self.ssh_con.ssh_command(thiscmd, timeout=self.cmdtimeout)
                self.cmdResults.append(result)
                if self.combine_output:
                    # We are combining stdout and stderr
                    self.cmdStatus[idX] = True
                else:
                    if len(result[2]) == 0:
                        # No stderr output
                        self.cmdStatus[idX] = True
                    else:
                        # Something was output to stdError
                        self.cmdStatus[idX] = False
                if self.debuglevel >= 3:
                    print(self.name + ": " + thiscmd + ": Finished")
            if False in self.cmdStatus or None in self.cmdStatus:
                self.status = False
            else:
                self.status = True
            # Close ssh connection if needed
            if self.runlocal is False:
                self.ssh_con.close()
            self.ssh_con = None
            # Run post hook before we are done with this job
        if self.posthook is not None:
            if self.debuglevel >= 2:
                print("Running posthook")
            self.posthook['args'].append(self)
            self.posthook_return = self.posthook['func'](*self.posthook['args'], **self.posthook['kwargs'])
            self.posthook['args'].remove(self)
        if self.debuglevel >= 1:
            print("Finished running serverJob: " + self.name)
        return self.status

    def print_results(self, printname=False):
        """Prints the command run and its output

        - **parameters** and **return types**::

            :param printname: Print the serverJob name
            :return: None
        """
        if printname:
            print "serverJob: " + self.name + "\n" + (separator*3)
        for idx, value in enumerate(self.cmds):
            print(value + ":\n" + ";".join(self.cmdResults[idx]) + "\n" + separator)
        return None

    def __str__(self):
        return str(self.__dict__)

    def __getitem__(self, item):
        return self.__dict__[item]

    def keys(self):
        """So you can work with the object in Dictionary form
        """
        return self.__dict__.keys()


class SSH(object):
    """SSH Session object

    - **parameters** and **return types**::

        :param fqdn: Fully qualified domain name or IP address
        :param username: SSH username
        :param password: SSH password
        :param keyfile: SSH keyfile (can be used instead of password)
        :param port: SSH port (default = 22)
        :param timeout: SSH connection timeout in seconds (default = 30)
        :return: SSH connection object
    """
    def __init__(self, fqdn, username=None, password=None, keyfile=None, port=22, timeout=30):
        self.__host__ = fqdn
        self.__username__ = username
        self.__password__ = password
        self.__keyfile__ = keyfile
        self.__port__ = port
        self.__timeout__ = timeout
        self.connection = paramiko.SSHClient()
        self.connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connect()

    def ssh_command(self, command, timeout=30, combine=False):
        """Run a command over an ssh connection

        - **parameters** and **return types**::

            :param command: The command to run
            :param timeout: Timeout for the command
            :param combine: Combine stderr and stdout
            :return: Tuple of (command, stdout, stderr) or (command, output)
        """
        if combine:
            stdin, stdout = self.connection.exec_command(command, timeout=timeout, get_pty=True)
            return command, stdout.read().strip()
        else:
            stdin, stdout, stderr = self.connection.exec_command(command, timeout=timeout)
            return command, stdout.read().strip(), stderr.read().strip()

    def close(self):
        """Closes an established ssh connection
        """
        self.connection.close()
        return None

    def is_alive(self):
        """Is an SSH connection alive
        """
        if self.connection._transport is None:
            return False
        else:
            return True
            
    def reconnect(self):
        """Alias to connect
        """
        self.connect()

    def connect(self):
        """Opens an SSH Connection
        """
        # http://stackoverflow.com/questions/26659772/silence-no-handlers-could-be-found-for-logger-paramiko-transport-message
        logging.basicConfig()
        if self.is_alive():
            raise paramiko.SSHException("Connection is already established")
        # Per http://stackoverflow.com/questions/19152578/no-handlers-could-be-found-for-logger-paramiko
        if self.__keyfile__ is not None:
            if self.__username__ is not None:  # Key file with a custom username!
                self.connection.connect(self.__host__, port=self.__port__, username=self.__username__,
                                        key_filename=self.__keyfile__, timeout=self.__timeout__, look_for_keys=False)
            else:
                self.connection.connect(self.__host__, port=self.__port__, key_filename=self.__keyfile__,
                                        timeout=self.__timeout__, look_for_keys=False)
        else:  # Username and password combo
            if self.__username__ is None or self.__password__ is None:
                raise paramiko.SSHException("You must enter a username and password or supply an SSH key")
            else:
                self.connection.connect(self.__host__, port=self.__port__, username=self.__username__,
                                        password=self.__password__, timeout=self.__timeout__, look_for_keys=False)
        # per https://github.com/paramiko/paramiko/issues/175
        self.connection.get_transport().window_size = 3 * 1024 * 1024


def sshread(serverjobs, debuglevel=0, pcount=None, tcount=None, progressbar=False, prehook=None, posthook=None):
    """Takes a list of serverJob objects and puts them into threads/subprocesses and runs them

    - **parameters** and **return types**::

        :param serverjobs: List of serverJob objects (A list of 1 job is acceptable)
        :param debuglevel: Debug level of all serverJobs (0 = off, 1 = some, 2 = more, 3 = all)
        :param pcount: Number of subprocesses to spawn (None = off, 0 = cpuSoftLimit, -1 = cpuHardLimit)
        :param tcount: Number of threads to spawn (None = off, 0 = adjusted length of serverJobList)
        :param progressbar: Print a progress bar
        :param prehook: Prehook for all serverJobs
        :param posthook: Posthook for all serverJobs
        :return: serverJobLst with completed serverJob objects (single object returned if single job passed)
    """
    if tcount is None and pcount is None:
        raise ProcessesOrThreads("You must specify a number for pcount or tcount!")
    if type(serverjobs) is not list:
        islist = False
        serverjobs = [serverjobs]
    else:
        islist = True
    totaljobs = len(serverjobs)

    # Per testing, don't allow more than 1 million jobs
    if totaljobs > __jobHardLimit__:
        print "The jobHardLimit for sshreader is: " + str(__jobHardLimit__)
        print "You are looking to process: " + str(totaljobs)
        raise ExceededJobLimit("Reached or exceeded jobHardLimit")

    # Figure out what globals we will need to apply to each serverJob object
    # before it is processed
    try:
        if int(debuglevel) <= 3:
            debuglevel = debuglevel
        else:
            raise TypeError("Debug level must be either 0, 1, 2, or 3")
    except:
        raise TypeError("Debug level must be an integer equal to 0, 1, 2, or 3")
    progressbar = progressbar
    if prehook is not None:
        prehook = _validate_hook_(prehook)
    if posthook is not None:
        posthook = _validate_hook_(posthook)

    if pcount is None:
        global tqueue, tcounter
        # Ensure the thread job counter is reset to 0
        tcounter = 0
        tqueue = threadQueue()
        # Fill up the Queue
        for thisJob in serverjobs:
            tqueue.put(thisJob)
        # Limit the number of threads to spawn
        if tcount == 0 or tcount > totaljobs:
            tcount = totaljobs

        # Start parent threads
        for pThread in xrange(tcount):
            if debuglevel >= 1:
                print "Spawning parent thread " + str(pThread)
            t = Thread(target=__tworker__, args=(debuglevel, prehook, posthook, progressbar, totaljobs))
            t.daemon = True
            t.start()

        # Wait for the queue to empty
        tqueue.join()

        if len(serverjobs) > 1 or islist:
            return serverjobs
        else:
            return serverjobs[0]
    else:
        global pqueue, finqueue
        pqueue = processQueue()
        finqueue = processQueue()
        # Load all but the current cpu on a box.
        cpusoftlimit = cpu_count() - 1
        # Imposing a hard limit for number of subprocesses so you don't make the system unusable
        cpuhardlimit = (cpusoftlimit * __cpuHardLimitFactor__)

        # Adjust number of subprocesses to spawn.
        if pcount == 0:
            pcount = cpusoftlimit
        elif pcount < 0:
            pcount = cpuhardlimit
        if pcount >= totaljobs:
            pcount = totaljobs

        if pcount > cpuhardlimit:
            print "The cpuHardLimit for your system is: " + str(cpuhardlimit)
            print "You asked for: " + str(pcount)
            raise ExceededCPULimit("Reached or exceeded cpuHardLimit")

        # Add each serverJob object to the queue
        if tcount is None:
            for thisJob in serverjobs:
                pqueue.put(thisJob)
            subqueue = None
        else:
            # Set the number of threads for each subprocess to use
            # This could end up being smaller than what is set here
            # due to the number of items in the sub queues we are
            # about to set up.
            if tcount == 0 or tcount > totaljobs:
                tcount = totaljobs
            # Build a "sub queue" for each process to use
            subqueue = []
            subqueueitems = int(totaljobs / pcount)
            # Balance the totaljobs into subQueues for each subprocess
            while subqueueitems * pcount < totaljobs:
                subqueueitems += 1
            for x in xrange(0, totaljobs, subqueueitems):
                subqueue.append(serverjobs[x: x + subqueueitems])
            # If the balanced sub queue requires fewer processes, make it so
            if len(subqueue) < pcount:
                pcount = len(subqueue)

        # Start Parent processes for processing the Queue
        plist = []
        if debuglevel >= 2:
            print "Spawning " + str(pcount) + " subprocesses"
        for pID in xrange(pcount):
            if subqueue is None:
                p = Process(target=__pworker__, args=(debuglevel, prehook, posthook))
            else:
                p = Process(target=__sprocess__, args=(debuglevel, prehook, posthook, tcount, subqueue[pID]))
            plist.append(p)
            p.start()

        # Get the results from the Queue
        returnlist = []
        returnlen = len(returnlist)
        while returnlen < totaljobs:
            if progressbar:
                progress_bar(returnlen, totaljobs)
            # I think there is a bug with the following line that randomly causes pickle errors.
            # Not sure how to fix it.
            returnlist.append(finqueue.get())
            returnlen = len(returnlist)
        # This ensures that we print a final 100% progress bar
        if progressbar:
            progress_bar(returnlen, totaljobs)

        # Ensure all processes are closed
        for p in plist:
            p.join()

        # If we were passed a list then we will return a list
        if len(returnlist) > 1 or islist:
            return returnlist
        else:  # If an object, return an object
            return returnlist[0]


def print_results(serverjobs):
    """Print the output of all serverJobs in as serverJobList by status

    - **parameters** and **return types**::

        :param serverjobs: A list of sshreaded serverJob objects
        :return: None
    """
    nonestatus = [x for x in serverjobs if x.status is None]
    completejobs = [x for x in serverjobs if x.status is True]
    errorjobs = [x for x in serverjobs if x.status is False]
    if len(completejobs) > 0:
        print "\nSUCCESSFUL SERVERJOBS\n"
        for x in completejobs:
            x.print_results(True)
    if len(errorjobs) > 0:
        print "\nERRORED SERVERJOBS\n"
        for x in errorjobs:
            x.print_results(True)
    if len(nonestatus) > 0:
        print "\nINCOMPLETE SERVERJOBS\n"
        for x in nonestatus:
            x.print_results(True)
    return None


def __pworker__(debuglevel, prehook, posthook):
    """This is a private method that is used by sshread to limit the number of processes sshreader spawns.

    DO NOT USE THIS METHOD! Use the sshread method instead!
    """
    global pqueue, finqueue
    pid = getpid()
    if debuglevel >= 1:
        print "Starting process: " + str(pid)
    while pqueue.empty() is False:
        thisjob = pqueue.get()
        thisjob.prehook = prehook
        thisjob.posthook = posthook
        thisjob.debuglevel = debuglevel
        thisjob.run()
        finqueue.put(thisjob)
    if debuglevel >= 1:
        print "Exiting process: " + str(pid)
    finqueue.close()
    return True


def __tworker__(debuglevel, prehook, posthook, progressbar, totaljobs):
    """This is a private method used to limit the number of threads that sshreader spawns.

    DO NOT USE THIS METHOD! Use the sshread method instead!
    """
    global tqueue, tcounter
    while True:
        thisjob = tqueue.get()
        thisjob.prehook = prehook
        thisjob.posthook = posthook
        thisjob.debuglevel = debuglevel
        cthread = Thread(target=thisjob.run)
        cthread.start()
        cthread.join()
        if progressbar:
            tcounter += 1
            progress_bar(tcounter, totaljobs)
        tqueue.task_done()


def __sprocess__(debuglevel, prehook, posthook, tcount, subqueue):
    """This is a private method used to have the multiprocessing and multithreading functionality combined.

    DO NOT USE THIS METHOD! Use the sshread method instead!
    """
    global finqueue, tqueue
    pid = getpid()
    if debuglevel >= 1:
        print "Starting process: " + str(pid)
    tqueue = threadQueue()
    for thisJob in subqueue:
        thisJob.prehook = prehook
        thisJob.posthook = posthook
        thisJob.debuglevel = debuglevel
        tqueue.put(thisJob)
    if tcount > len(subqueue):
        # Override the number of threads if it is greater than what we actually need
        tcount = len(subqueue)
    if debuglevel >= 2:
        print "Process " + str(pid) + " starting " + str(tcount) + " threads"
    for x in xrange(tcount):
        t = Thread(target=__sthread__)
        t.daemon = True
        t.start()
    tqueue.join()
    if debuglevel >= 1:
        print "Exiting process: " + str(pid)
    finqueue.close()
    return True


def __sthread__():
    """This is a private method used to have the multiprocessing and multithreading functionality combined.

    DO NOT USE THIS METHOD! Use the sshread method instead!
    """
    global tqueue, finqueue
    while tqueue.empty() is False:
        thisjob = tqueue.get()
        try:
            thisjob.run()
        except Exception as errMsg:
            print errMsg
        finqueue.put(thisjob)
        tqueue.task_done()
    return True

""" Worker (module)

This module contains a class that is designed to be spawned in
numbers as part of a queue of jobs to be completed. Each worker
carries out only one job, then dies.

The most common implementation of this module is to import it and
use inheritance to define how the worker should "work". The command
object it is passed is arbitrary, so the programmer is free to
define how each worker should interact with the object it is given.

The module has been structured to be used while threading, and
as a result contains a significant amount of threading logic
that remains application-agnostic, even as the definition of
"work" is altered for different workers.
"""

# imports for logging
import logging

# import pash from local library
import pash

# configures debug logging
logging.basicConfig(filename='/tmp/worker.log', level=logging.DEBUG,
    format='%(asctime)s (%(threadName)-2s) %(message)s',)


class Worker(object):
    """ Worker (class)

    A class object meant to be overriden to specify how work
    should be carried out.

    Implements:
        - 'logging' from Python standard library
        - Resource locking: The worker is passed an object which
           is expected have the attributes of a lock and a list.
        - Result passing: The worker adds an object to the lock
           before releasing it. This object represents the result
           of his work.

    Attributes:
        command (object): Some object which is to be worked on or
            otherwise processed.
        lock ('locked_queue'): An object that is expected to have
            the properties of a lock from the 'threading' module,
            as well as being capable of being appended to.

    """
    # setting the worker lock and the command to be carried out
    def __init__(self, lock, command):
        self.lock = lock
        self.command = command

    # container for the work being done, handles threading implementation, etc.
    def run(self):
        logging.debug('Starting a worker thread...')

        # acquire the lock
        self.lock.acquire()
        logging.debug('Got the lock.')

        # do work
        try:
            logging.debug("I am doing a thing: %s", self.command)
        except TypeError:
            logging.debug("I am doing something (that is not a string)")
        value = self.work(self.command)
        try:
            logging.debug("I did my thing: %s", self.command)
        except TypeError:
            logging.debug("I did something (that was not a string)")

        # add results to the worker lock, queen should pick these up
        self.lock.append(value)

        # release the lock
        logging.debug("Releasing the lock...")
        self.lock.release()

    # override this to define how work should be done;
    # this default implementation runs a bash command
    # and returns stdout
    def work(self, comm):
        """ Working

        This function should be overriden by the caller in order
        to provide the functionality of interest. The default
        implementation here uses 'pash' to run a command using
        Python's 'subprocess' module.

        This function is called during 'run', which is the intended
        target of any threading process. This function should
        never need to be called explicitly.

        Arguments:
            comm (string): A re-representation of 'command' from
                the 'run' function in this class

        Returns:
            proc.get_val('stdout') (string): The value of stdout
                returned for the command that was run
        """
        proc = pash.ShellProc()
        proc.run(comm)
        try:
       	    return proc.get_val('stdout').split('/n')
        except AttributeError:
            return None



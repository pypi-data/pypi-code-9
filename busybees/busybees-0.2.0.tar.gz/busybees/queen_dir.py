""" QueenDir (Queen Directory)

This module contains a nested dictionary data structure that is being
used to store objects representing threaded queue handlers.
"""

class QueenDir(object):
    """ Queen Directory

    This class is used as an interface for storing and managing
    objects of interest and their related attributes and components.
    An example present here is the storage of a queen who manages
    launching individual worker objects and is on a separate thread
    from MainThread. As such, the task of managing the queens is much
    simpler when the object representing the thread is able to be
    recalled by name, along with its related locks and other information.
    """

    def __init__(self):
        """ Initialization

        Attributes:
            lib [dict]: A simple hashmap used to store the queens
                alongside their other details
        """
        self.lib = {}

    def add_queen(self, name, queen, lock, sched):
        """ AddQueen (Adding a queen entry)

        This method is used to create a new entry for queen while adding
        the appropriate attributes to the dictionary under that index.
        A nested dictionary structure results, as the entries are
        organized into dictionaries.

        Args:
            name (string): A human-readable value to represent the entry
            queen (object): An instantiation of a threaded class
            lock (object): An instantiation of a threading lock
            sched (object): An instantiation of a task scheduler

        Attributes:
            lib[name]['stat'] (string): A value to represent other
                properties of interest, such as being gravebound
                (having received a kill command)
            lib[name]['result'] (object): Some object which the
                queen stores, typically containing useful information
                about the results of work done by her workers
        """
        self.lib[name] = {'queen':queen, 'lock':lock,
            'sched':sched, 'stat':None, 'result':None}

    def get_lock(self, name):
        """ getLock

        Returns the object indexed under lib[name]['lock']

        Args:
            name (string): The value representing the entry of interest

        Returns:
            lib[name]['lock'] (object): The object mapped to 'lock' for
                a given queen name
        """
        return self.lib[name]['lock']

    def get_queen(self, name):
        """ getQueen

        Returns the queen object indexed under lib[name]['queen'].

        Args:
            name (string): The value representing the entry of interest

        Returns:
            lib[name]['queen'] (object): The queen object belonging to
                a given queen name
        """
        return self.lib[name]['queen']

    def enum_queens(self):
        """ enumQueens (Enumerate queens)

        Returns a list of names of entries. Particularly useful for
        accessing all queens when performing operations like programmed
        controller death.

        Returns:
            lib.keys() (list of strings): A list that includes the name
                for each queen entry
        """
        return self.lib.keys()

    def set_stat(self, name, string):
        """ setStat

        Stores a string under the index lib[name]['stat'].

        Args:
            name (string): The value representing the entry of interest
            string (string): A string to be stored as the queen's status
        """
        self.lib[name]['stat'] = string

    def get_stat(self, name):
        """ getStat

        Returns the value for 'stat'.

        Args:
            name (string): The value representing the entry of interest

        Returns:
            lib[name]['stat'] (string): The status string belonging to
                a given queen name
        """
        return self.lib[name]['stat']

    def get_sched(self, name):
        """ getSched

        Returns the schedue object indexed under lib[name]['sched'].
        This method is currently unused, but is intended for use
        as part of an update to add transparency to job execution.

        Args:
            name (string): The value representing the entry of interest

        Returns:
            lib[name]['sched'] (object): The schedule object belonging to
                a given queen name
        """
        return self.lib[name]['sched']

    def get_result(self, name):
        """ getResult

        Returns the result object indexed under lib[name]['result'].

        Args:
            name (string): The value representing the entry of interest

        Returns:
            lib[name]['result'] (object): The queen object belonging to
                a given queen name
        """
        return self.lib[name]['result']

    def set_result(self, name, val):
        """ setResult

        Stores a result object under the index lib[name]['result'].

        Args:
            name (string): The value representing the entry of interest
            val (object): Some value to be stored as the result to be
                recalled later
        """
        self.lib[name]['result'] = val

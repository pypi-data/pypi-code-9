

"""
mbox_object
==========================================

Module that hold MboxObject class to interact with mbox files.

-----------------------
Current Status: alpha
-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""


# Import
# ------------------------------------------------------------------
# python
import sys
import os
import functools
import logging
import mailbox
import re


# logging basic configuration
logging.basicConfig()


# Import variable
do_reload = True


# mbox_globals
import mbox_globals as mbox_globals
if(do_reload):
    reload(mbox_globals)


# Globals
# ------------------------------------------------------------------
LOGGING_LEVEL = mbox_globals.LOGGING_LEVEL
DIVIDER = mbox_globals.DIVIDER


# MboxObject class
# ------------------------------------------------------------------
class MboxObject(object):
    """
    MboxObject class.
    """

    # Create and initialize
    # ------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        MboxObject instance factory.
        """

        # mbox_object_instance
        mbox_object_instance = super(MboxObject, cls).__new__(cls, args, kwargs)

        return mbox_object_instance

    def __init__(self, path=None, logging_level=LOGGING_LEVEL):
        """
        Customize instance.
        """

        # instance variables
        # ------------------------------------------------------------------
        # logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging_level)

        # _path
        self.set_path(path)

    # Special Methods
    # ------------------------------------------------------------------
    def __repr__(self):
        """String representation"""
        return self.path
    __str__ = __repr__

    # Methods
    # ------------------------------------------------------------------
    def get_path(self):
        """
        Return self._path.
        """

        return self._path

    def set_path(self, path):
        """
        Set self._path.
        """

        self._path = path

    # path
    path = property(get_path, set_path)
    """Access for _path"""

    def path_valid(self):
        """
        Return True or False based on wether or not
        self.path exists in the filesystem.
        """

        # check
        return True if os.path.isfile(self.path) else False

    def get_messages(self):
        """
        Get all messages from mbox file.
        Return list of type [mailbox.mboxMessage, mailbox.mboxMessage]
        """

        # check if self.path valid
        if not(self.path_valid()):
            # log
            logger.debug('Path {0} not valid. Return empty list'.format(self.path))
            return []

        # mbox
        mbox = mailbox.mbox(self.path)

        # message_list
        message_list = []
        # iterate
        for message in mbox:
            message_list.append(message)

        return message_list

    def get_senders(self):
        """
        Return list of all sender addresses.
        """

        # message_list
        message_list = self.get_messages()
        # empty
        if not(message_list):
            # log
            logger.debug('Message list empty. Mbox file {0} contains no emails'.format(self.path))
            return []

        # sender_list
        sender_list = [message['From'].split()[-1] for
                        message in
                        message_list]

        return sender_list

    def get_sender_domains(self):
        """
        Return list of all domains from all senders.
        """

        # sender_list
        sender_list = self.get_senders()
        # empty
        if not(sender_list):
            # log
            logger.debug('Sender list empty. Mbox file {0} contains no emails'.format(self.path))
            return []

        # domain_list
        domain_list = [address.split('@')[-1] for
                        address in
                        sender_list]

        # clean domain list
        domain_list = [domain.replace('>','') for
                        domain in
                        domain_list]

        return domain_list

    def print_domains_stats(self):
        """
        Print domain statistics.
        """

        # domain_list
        domain_list = self.get_sender_domains()
        # empty
        if not(domain_list):
            # log
            logger.debug('Domain list empty. Mbox file {0} contains no emails'.format(self.path))
            return []

        # domain_count_dict
        domain_count_dict = {}
        for domain in domain_list:

            # key exists
            if (domain_count_dict.has_key(domain)):

                # ++
                count = domain_count_dict[domain]
                domain_count_dict[domain] = count + 1

            # else
            else:

                domain_count_dict[domain] = 1

        # domain_count_complete
        domain_count_complete = len(domain_list)

        # print
        print('\nDomain Count Statistics (Domain - Count - Percent) \n{0}'.format(DIVIDER))
        for domain, count in domain_count_dict.iteritems():
            print('{0} - {1} - {2}%'.format(domain, count, float(count)/float(domain_count_complete)*100.0))



# Run
# ------------------------------------------------------------------
if(__name__ == '__main__'):

    # mbox_object_instance
    mbox_object_instance = MboxObject()

    # test_method
    print(mbox_object_instance)

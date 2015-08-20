"""this module implement the time tracer for transaction
"""

import time
import logging


_logger = logging.getLogger(__name__)


class TimeTrace(object):
    """
    """
    node = None

    def __init__(self, transaction):
        self.transaction = transaction
        self.children = []
        self.start_time = 0.0
        self.end_time = 0.0
        self.duration = 0.0
        self.exclusive = 0.0
        
    def __enter__(self):
        """
        """
        if not self.transaction:
            _logger.debug("transaction is %s.return now.", self.transaction)
            return self

        # check the base node is set or not
        parent_node = self.transaction.current_node()
        if not parent_node or parent_node.terminal_node():
            self.transaction = None
            return parent_node

        self.start_time = time.time()
        self.transaction.push_node(self)
        
        return self
        
    def __exit__(self, exc, value, tb):
        """
        """
        if not self.transaction:
            return self.transaction

        self.end_time = time.time()
        if self.end_time < self.start_time:
            self.end_time = self.start_time
            _logger.warn("end time is less than start time.")

        self.duration = int((self.end_time - self.start_time) * 1000)
        self.exclusive += self.duration
        
        # pop the self and return parent node
        parent_node = self.transaction.pop_node(self)

        self.finalize_data()
        current_node = self.create_node()
        
        if current_node:
            self.transaction.process_database_node(current_node)
            parent_node.process_child(current_node)
            
        self.transaction = None
        
    def create_node(self):
        if self.node:
            return self.node(**dict((k, self.__dict__[k]) for k in self.node._fields))

        return self

    def finalize_data(self):
        pass
    
    def process_child(self, node):
        self.children.append(node)
        self.exclusive -= node.duration
        
    def terminal_node(self):
        return False

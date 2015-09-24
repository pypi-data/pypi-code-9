import uuid

class GenericFlow(object):
    """
    This class represents a generic Flow (not related to ODL).
    In the context of this library, this is a flow before be installed on ODL.
    So first you should create object of this class and after that send to ODL.
    """

    def __init__(self, name, table):
        self.id = "%s" % uuid.uuid1()
        self.name = name
        self.table = table
        self.hard_timeout = 0
        self.idle_timeout = 0
        self.cookie = 10
        self.priority = 100

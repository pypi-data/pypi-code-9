
from abc import abstractmethod

class RemoteProcessBase(object):

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def start_command_server(self):
        pass

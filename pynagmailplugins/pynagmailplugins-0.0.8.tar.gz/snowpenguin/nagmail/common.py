from abc import ABCMeta, abstractmethod

class MailQueueDataFetchError(Exception):
    def __init__(self, msg):
        super(MailQueueDataFetchError, self).__init__(msg)

class MailQueueInterface(metaclass=ABCMeta):

    def __init__(self, data_generator):
        self.data_generator = data_generator

    @abstractmethod
    def has_deferred_counter(self):
        pass

    @abstractmethod
    def get_deferred_counter(self):
        pass

    @abstractmethod
    def has_active_counter(self):
        pass

    @abstractmethod
    def get_active_counter(self):
        pass

    @abstractmethod
    def has_total_counter(self):
        pass

    @abstractmethod
    def get_total_counter(self):
        pass

    @abstractmethod
    def update(self):
        pass

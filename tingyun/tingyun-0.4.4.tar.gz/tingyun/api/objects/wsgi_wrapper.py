"""this module is implement the data input read for wsgi

"""
import sys
from tingyun.api.tracert.function_trace import FunctionTrace


class WSGIInputWrapper(object):

    def __init__(self, transaction, wsgi_input):
        self.__transaction = transaction
        self.__input = wsgi_input

    def __getattr__(self, name):
        return getattr(self.__input, name)

    def close(self):
        if hasattr(self.__input, 'close'):
            self.__input.close()

    def read(self, *args, **kwargs):
        data = self.__input.read(*args, **kwargs)
        return data

    def readline(self, *args, **kwargs):
        line = self.__input.readline(*args, **kwargs)
        return line

    def readlines(self, *args, **kwargs):
        lines = self.__input.readlines(*args, **kwargs)
        return lines


class WSGIApplicationIterable(object):

    def __init__(self, transaction, generator):
        self.transaction = transaction
        self.generator = generator

    def __iter__(self):

        try:
            with FunctionTrace(self.transaction, name='Response', group='Python.WSGI'):
                for item in self.generator:
                    yield item
        except GeneratorExit:
            raise
        except:  # Catch all
            self.transaction.record_exception(*sys.exc_info())
            raise

    def close(self):

        try:
            if hasattr(self.generator, 'close'):
                self.generator.close()
        except:  # Catch all
            self.transaction.__exit__(*sys.exc_info())
            raise
        else:
            self.transaction.__exit__(None, None, None)
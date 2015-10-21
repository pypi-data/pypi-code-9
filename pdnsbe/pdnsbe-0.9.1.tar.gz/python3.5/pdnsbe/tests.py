import asyncio.queues as queues
import logging
import click
import pdnsbe.backend as backend
import pdnsbe.core as core


class MockRequest(object):

    def __init__(self, helo_line, iterations):
        self.__helo_line = helo_line
        self.__counter = 0
        self.__iterations = iterations
        self.__mode = None

    def makefile(self, mode=None):
        self.__mode = mode
        return self

    def readline(self):
        if self.__counter == 0:
            self.__counter += 1
            return self.__helo_line
        if self.__counter == self.__iterations:
            return ""
        self.__counter += 1
        return "Q\twww.booking.com\tIN\tA\t-1\t8.8.8.8"

    def write(self, line):
        pass

    def flush(self):
        pass


class MockServer(object):

    def get_loglevel(self):
        return logging.DEBUG

    def lookup_query(self, query: core.PDNSQuery):
        pass


def test_handler():
    handler = backend.PDNSBackendHandler(MockRequest("HELO\t1", 1), "8.8.8.8",
                                         MockServer())
    handler.handle()


def test_handler_handshake():
    try:
        handler = backend.PDNSBackendHandler(MockRequest("LOLZ 1", 1), "8.8.8.8",
                                             MockServer())
        handler.handle()
    except core.PDNSHandshakeException:
        # this is what we want
        return
    raise Exception("test failed, expected exception")


@click.command()
def run_tests():
    test_handler()
    test_handler_handshake()

@click.command()
def profile():
    pass

if __name__ == "__main__":
    run_tests()

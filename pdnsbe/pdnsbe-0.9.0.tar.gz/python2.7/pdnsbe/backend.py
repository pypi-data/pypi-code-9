#!/usr/bin/python

"""
Socket based back-end server for PowerDNS with pluggable query resolution.
"""


import re
import SocketServer
import pdnsbe.core as core
import logging
import logging.handlers


END_RESPONSE = "END"
HANDSHAKE_PATTERN = "^HELO\t([1-3])$"
DATA_RESPONSE_PREFIX = "DATA"


class AbstractPDNSResolver(object):

    """ Implement this class with your own resolver logic """

    def lookup_query(self, query):
        """
            This method will be called by the server. The query argument will
            be a PDNSQuery object, the method should return a list of
            PDNSRecord objects.
         """
        raise NotImplementedError("Not implemented, extend this class please.")


class PDNSBackendServer(SocketServer.UnixStreamServer):

    """
        This class is basically a UnixStreamServer that parses PDNS queries, and
        send the queries into a pluggable resolver. This allows the user to add
        resolver logic at runtime.
    """

    def __init__(self, socket):
        self.__resolver = None
        self.__banner = None
        self.__loglevel = logging.WARNING
        SocketServer.UnixStreamServer.__init__(self, socket, PDNSHandler)

    def set_query_resolver(self, resolver):
        """ Set the query resolver, this is where you plug your custom code """
        self.__resolver = resolver

    def set_loglevel(self, loglevel):
        """ set the desired log level """
        self.__loglevel = loglevel

    def get_loglevel(self):
        return self.__loglevel

    def set_banner(self, banner):
        """ Set the custom HELO banner for your backend """
        self.__banner = banner

    def get_banner(self):
        return self.__banner if self.__banner else "DEFAULT_BACKEND"

    def lookup_query(self, query):
        if not self.__resolver:
            raise Exception("This server has no resolver set.")
        return self.__resolver.lookup_query(query)


class PDNSHandler(SocketServer.BaseRequestHandler):

    """ This is the generic handler for a connected socket from pdns """

    def __init__(self, request, client_address, server):
        self.__logger = logging.getLogger()
        self.__logger.addHandler(logging.StreamHandler())
        self.__logger.setLevel(server.get_loglevel())
        SocketServer.BaseRequestHandler.__init__(self, request, client_address,
                                                 server)

    def handle(self):
        """
            this method is specified by BaseRequestHandler API. The name may
            be misleading; a request in this case is a 'session'/connection from
            PowerDNS.
        """
        self.__logger.info("Got connection from PowerDNS, this is a new fork")
        self.__f = self.request.makefile()
        try:
            self.__version = self.__handshake()
        except Exception as exception:
            # make sure the error is reported back, and PowerDNS knows we're
            # done with this query
            self.__error_out(exception)
            raise
        line = self.__f.readline().strip()
        while line:
            if line == "":
                self.__logger.info("Got (sort of) EOF, stopping listener.")
                break
            try:
                result = self.__lookup_query(line)
            except Exception as exception:
                self.__error_out(exception)
                # Re-raise the same exception
                raise
            self.__send_response(result)
            line = self.__f.readline().strip()
        self.__logger.info("Exiting thread, bye...")

    def __write_line_sync(self, line):
        """ The PowerDNS pipe backend protocol spec is line based, so we want
            synchronous writes with line atomicity """
        self.__f.write(line if line.endswith("\n") else "%s\n" % line)
        self.__f.flush()

    def __error_out(self, exception):
        """ report the error to PowerDNS """
        # maybe report errors? self.__write_line_sync("LOG\t%r" % e)
        self.__logger.exception(exception)
        self.__write_line_sync("FAIL")
        self.__write_line_sync("END")
        self.__f.close()
        self.request.close()

    def __parse_query(self, request_line):
        """ Parse the query according to the version of pipe backend session """
        args = request_line.split("\t")
        expected_args = {1: 6, 2: 7, 3: 8}
        if expected_args[self.__version] != len(args):
            raise core.PDNSInvalidQueryException("Invalid query: %s" %
                                                 request_line)
        return core.PDNSQuery(*args)

    def __handshake(self):
        """ Attempt to handshake with PowerDNS, return backend version """
        line = self.__f.readline().strip()
        matcher = re.match(HANDSHAKE_PATTERN, line)
        if matcher:
            self.__write_line_sync("OK\t%s" % self.server.get_banner())
            return int(matcher.group(1))
        raise core.PDNSHandShakeException("handshake failed: '%s'" % line)

    def __lookup_query(self, request_line):
        self.__logger.debug("got query %s", request_line)
        return self.server.lookup_query(self.__parse_query(request_line))

    def __send_response(self, result):
        """
            Write the response to a succesful query to the client. This takes
            PDNSRecord objects or objects that fill the same contract.
        """
        for record in result:
            self.__write_line_sync("%s\t%s" % (DATA_RESPONSE_PREFIX,
                                               record.to_response_line()))
        self.__write_line_sync(END_RESPONSE)


class ForkingPDNSBackendServer(SocketServer.ForkingMixIn, PDNSBackendServer):

    """ Add ForkingMixIn """
    pass


class ThreadingPDNSBackendServer(SocketServer.ThreadingMixIn,
                                 PDNSBackendServer):

    """ Add ThreadingMixin """
    pass

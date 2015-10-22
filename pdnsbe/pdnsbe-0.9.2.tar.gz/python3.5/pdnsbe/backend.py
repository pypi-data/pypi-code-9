
""" Python Generic Backend for PowerDNS """

import socketserver
import socket
import logging
import pdnsbe.core as core
import threading


LOGFORMAT = """%(process)d %(module)s thr:%(thread)d %(processName)s\
%(threadName)s %(levelname)s %(message)s"""

logger = logging.getLogger()


class PDNSResolver(object):

    """
    Abstract class to implement with custom resolver logic, plug your extended
    class into the PDNSBackendServer.
    """

    def lookup_query(self, query: core.PDNSQuery) -> list:
        """
        This method should be implemented when extending this resolver class.
        """
        raise Exception("Not implemented.")


class PDNSBackendServer(socketserver.UnixStreamServer):

    """
    Server listening for connections on a socket, splitting off handlers for
    each connection.
    """

    def __init__(self, socket_path):
        self.__handlers = []
        self.__resolver = None
        logger.info("Init server...")
        socketserver.UnixStreamServer.__init__(self, socket_path,
                                               PDNSBackendHandler)

    def set_resolver(self, resolver: PDNSResolver):
        """
        Set resolver which provides the actual logic for lookups.
        """
        logger.info("Setting resolver: %r" % resolver)
        self.__resolver = resolver

    def lookup_query(self, query: core.PDNSQuery) -> list:
        """
        Lookup a query. This method only works when the resolver is set.
        """
        if self.__resolver is None:
            raise Exception("This backend server has no resolver set!")
        return self.__resolver.lookup_query(query)

    def register_handler(self, handler):
        """
        This registers handlers that are running for this server. We need this
        so we can shut them down when we are told to stop.
        """
        logger.debug("Registering handler %r" % handler)
        self.__handlers.append(handler)

    def unregister_handler(self, handler):
        """
        Un-registers handlers after they are stopped or finished running.
        """
        logger.info("Un-registering handler %r" % handler)
        self.__handlers.remove(handler)

    def stop(self):
        """
        Stop the server and its handlers that may still be running
        """
        logger.info("Shutting down registered handlers (%d)"
                    % (len(self.__handlers)))
        for handler in self.__handlers:
            handler.stop()
        logger.debug("Closing server socket...")
        threading.Thread(target=self.socket.close).start()
        logger.info("Shutting down server...")
        threading.Thread(target=self.shutdown).start()
        logger.info("Server has been shut down")


class ForkingPDNSBackendServer(socketserver.ForkingMixIn, PDNSBackendServer):
    pass


class ThreadingPDNSBackendServer(socketserver.ThreadingMixIn,
                                 PDNSBackendServer):
    pass


class PDNSBackendHandler(socketserver.BaseRequestHandler):

    """
    This class handles a request(connection) from a client.
    """

    def __init__(self, request: socket.socket, client_address: str,
                 server: PDNSBackendServer):
        self.__server = server
        self.__request = request
        self.__shutdown = False
        self.__version = None
        self.__f = None
        server.register_handler(self)
        socketserver.BaseRequestHandler.__init__(self, request, client_address,
                                                 server)

    def handle(self):
        """
        This method handles a connection from a client.
        """
        self.__f = self.__request.makefile(mode="rw")
        self.__version = self.__handshake()
        logger.info("Start handling")
        try:
            self.__tight_loop()
        except Exception as e:
            self.__error_out(e)
            raise

    def __tight_loop(self):
        line = self.__readline()
        while line:
            if line is None or line == "":
                # We're done, exit loop
                break
            self.__handle_line(line)
            line = self.__readline()
        logger.info("Done with session, exiting...")

    def __handle_line(self, line: str):
        """
        Process one line received from client.
        """
        query = self.__parse_query(line)
        results = self.__server.lookup_query(query)
        if results is None:
            self.__write_line_sync("END")
            return
        self.__write_response(results)

    def __readline(self):
        """
        Blocking call to read a line from the client/socket. When shutting down
        this will throw an error, which is why we must handle shutdown here.
        """
        try:
            return self.__f.readline().strip()
        except (ValueError, OSError):
            if self.__shutdown:
                # Shutdown was requested, don't complain about closed handle
                return None
            raise

    def __write_line_sync(self, line: str):
        """
        The PowerDNS pipe backend protocol is line delimited so we want to
        write with line atomicity.
        """
        self.__f.write(line if line.endswith("\n") else "%s\n" % line)
        self.__f.flush()

    def __error_out(self, exception: Exception):
        """
        Log error and report failure to client.
        """
        logger.error(exception)
        self.__write_line_sync("FAIL")

    def __handshake(self) ->int:
        """
        Attempt to handshake with client, returns backend abi version
        """
        line = self.__readline()
        if line is None:
            return
        matcher = core.HELO_REGEX.match(line)
        if matcher is None:
            raise core.PDNSHandshakeException("Handshake failed: %s" % line)
        _ = matcher.group(1)
        version = int(matcher.group(2))
        if version not in range(1, 4):
            raise core.PDNSHandshakeException("Handshake failed: %s" % line)
        self.__write_line_sync("HELO\tdefault backend")
        return version

    def __parse_query(self, line: str) -> core.PDNSQuery:
        """
        Parse a line received from client into a query according to abi version
        """
        parts = line.split(core.Q_SEPARATOR)
        if self.__version == 1 and not len(parts) == 6:
                raise core.QueryParseException("Malformed query: %s version %d"
                                               % (line, self.__version))
        if self.__version == 2 and not len(parts) == 7:
                raise core.QueryParseException("Malformed query: %s version %d"
                                   % (line, self.__version))
        if self.__version == 3 and not len(parts) == 8:
                raise core.QueryParseException("Malformed query: %s version %d"
                                   % (line, self.__version))
        return core.PDNSQuery(self.__version, *parts)

    def __write_response(self, results: list):
        """
        Write a list of results back to the client.
        """
        for result in results:
            self.__write_line_sync(self.__to_response_line(result))
        self.__write_line_sync("END")

    def stop(self):
        """
        Stop this handler. We need this for cleanup and to prevent hanging
        threads blocking forever on readline when we want to shutdown.
        """
        self.__write_line_sync("")
        self.__shutdown = True
        logger.debug("Shutting down this handler")
        self.__request.close()
        if type(self.server) == ThreadingPDNSBackendServer:
            self.__f.close()
        logger.debug("Handler shut down")
        self.__server.unregister_handler(self)

    def __to_response_line(self, result: core.PDNSRecord):
        """
        Convert response into a PDNS pipe backend compliant string
        """
        return "%s\t%s\t%s\t%s\t%s\t%s\t%s" % ("DATA", result.get_name(),
                                               result.get_type(),
                                               result.get_class(),
                                               result.get_ttl(),
                                               result.get_id(),
                                               result.get_content())

#! /usr/bin/python
import sys
import socket
# Python 2 thread
try:
    import thread
# Python 3 thread
except:
    import _thread as thread

# For constant variables such as the port
import constants

class server(object):
    """
    Sends everything that gets passed to write
    to all connected clients
    """
    def __init__(self):
        """
        Sets up the variables used by client
        """
        super(server, self).__init__()
        # Should logs be writen to stdout
        self.silly_logging = constants.LOGGING
        # The connection to the server
        self.silly_socket = False
        # If we are recveing data from the server
        self.silly_running = False
        # The connected sockets
        self.silly_conns = []

    def log(self, *args):
        """
        Logs messages if self.silly_logging is True
        """
        if self.silly_logging:
            for string in args:
                sys.stdout.write(str(string) + " ")
            sys.stdout.write("\n")

    def write(self, *args):
        """
        Sends a message to all clients
        """
        try:
            # Send message to all clients
            for client in range(0, len(self.silly_conns)):
                # Start a new thread to send so we can move on
                thread.start_new_thread(self.silly_send_client, \
                    (client, args))
        # Array size might change if client is deleted
        except RuntimeError as error:
            pass

    def silly_send_client(self, client, args):
        """
        Sends a message to a client given its index in self.silly_conns
        """
        # Make agrs a list so we can modify the elements
        args = list(args)
        # Loop through all that needs to be sent
        for i in range(0, len(args)):
            # Try to send it
            try:
                # Dump objects to strings if possible
                try:
                    args[i] = str(args[i])
                # If you can't ascci encode thats ok
                except Exception as error:
                    pass
                args[i] = args[i].encode(constants.ENCODEING)
                # Send the message to the client
                self.silly_conns[client].sendall(args[i])
            # Client disconnected so call self.silly_close_conn
            # except BrokenPipeError:
            # Some other error happened, log it
            except Exception as error:
                self.silly_close_conn(client)
                self.log(error)

    def silly_close_conn(self, client):
        """
        Handle a connection that needs to be discarded
        """
        # Try to close the connection
        try:
            self.silly_conns[client].close()
        except Exception as error:
            self.log(error)
        # Try to delete the connection from the list
        try:
            del self.silly_conns[client]
        # Another thread may have already deleted it
        except IndexError as error:
            pass

    def bind(self, address, port):
        """
        Creates the servers silly_socket and binds it to the
        address and port given
        """
        # Create the socker
        self.silly_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # So that we don't get socket error 98 when the server restarts
        self.silly_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Bind to the address and port
        self.log("Binding to {}:{}".format(address, port))
        self.silly_socket.bind((address, port))
        return self.silly_socket

    def start(self, address=constants.ADDRESS, port=constants.PORT):
        """
        Starts the server and binds to the address and port
        """
        # Create the socket and bind it
        self.bind(address, port)
        # Listen to incoming connections
        self.silly_socket.listen(constants.LISTEN)
        # Say that the server is running
        self.silly_running = True
        while self.silly_running:
            # Accept connections
            conn, addr = self.silly_socket.accept()
            # Add connections to the list of connected clients
            self.silly_conns.append(conn)

    def start_thread(self, *args):
        """
        Calls start in a thread
        """
        thread.start_new_thread(self.start, tuple(args))

def main():
    """
    Creates a server and sends all inputs to connected clients
    """
    # Create the server object
    test = server()
    # Start the server in a thread
    test.start_thread()
    # In python 2x you need to send a ctrl-d to flush the buffer
    # and send everything you have typed and hit enter on
    for send in sys.stdin:
        # Python 2x reads in unicode weird
        if (sys.version_info < (3, 0)):
            send = send.decode(constants.ENCODEING)
        # Send any input
        test.write(send)

if __name__ == '__main__':
    main()

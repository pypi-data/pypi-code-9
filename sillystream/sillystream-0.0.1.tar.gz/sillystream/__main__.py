"""
sillystream

Stream content to all clients
"""
import sys
import argparse

import constants
import server as sillystream_server
import client as sillystream_client

def server(args):
    """
    Creates a server and sends all inputs to connected clients
    """
    # Create the server object
    test = sillystream_server.server()
    # Start the server in a thread
    test.start_thread(**args)
    # In python 2x you need to send a ctrl-d to flush the buffer
    # and send everything you have typed and hit enter on
    for send in sys.stdin:
        # Python 2x reads in unicode weird
        if (sys.version_info < (3, 0)):
            send = send.decode(constants.ENCODEING)
        # Send any input
        test.write(send)

def client(args):
    """
    Connects and sends input to server ctrl-d to stop
    """
    # Create the client
    test = sillystream_client.client()
    # Connect the client, default host is localhost
    test.connect(**args)
    # In python 2x you need to send a ctrl-d to flush the buffer
    # and send everything you have typed and hit enter on
    for send in sys.stdin:
        # Python 2x reads in unicode weird
        if (sys.version_info < (3, 0)):
            send = send.decode(constants.ENCODEING)
        # Send any input
        test.write(send)
    # Close connection
    test.close()

def arg_setup():
    arg_parser = argparse.ArgumentParser(description=constants.__description__)
    arg_parser.add_argument("action", type=unicode, \
        help="Start server or connect to server (server, client)")
    arg_parser.add_argument("--address", type=unicode, \
        help="Address to host on")
    arg_parser.add_argument("--host", type=unicode, \
        help="Address of host server")
    arg_parser.add_argument("--port", type=int, \
        help="Port of sillystream server")
    arg_parser.add_argument("--version", "-v", action="version", \
        version=u"sillystream " + unicode(constants.__version__) )
    initial = vars(arg_parser.parse_args())
    args = {}
    for arg in initial:
        if initial[arg]:
            args[arg] = initial[arg]
    return args

def main():
    args = arg_setup()
    # Get the action
    action = getattr(sys.modules[__name__], args["action"])
    del args["action"]
    action(args)

if __name__ == '__main__':
    main()

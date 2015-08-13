#! /usr/bin/python
import json
import SocketServer
import BaseHTTPServer

PORT = 0
ADDRESS = "0.0.0.0"

class ThreadedHTTPServer(SocketServer.ThreadingMixIn, BaseHTTPServer.HTTPServer):
    """Handle requests in a separate thread."""
    def __init__(self, *args, **kwargs):
        BaseHTTPServer.HTTPServer.__init__(self, *args, **kwargs)
        self.database = {}

    def send_headers(self, client):
        client.send_header("Access-Control-Allow-Origin", "*")
        client.send_header("Content-Type", "application/json")

    def port(self):
        return self.socket.getsockname()[1]

    def got_request(self, data, client_socket):
        """
        Receivces jsons from handlers and deals with them
        """
        response = None
        # Make sure there is a key
        if "key" in data:
            key = data["key"]
            # If there is a value then update the key
            if "value" in data:
                self.database[key] = data["value"]
            # Make sure there is a key to send back, else send nothing
            if key in self.database:
                # Send the value of the key back to the client
                response = {
                    "key": key,
                    "value": self.database[key],
                }
        # Dump the json into the client socket
        if response is not None:
            json.dump(response, client_socket)

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):
    """
    Handles post requests
    """
    def log_message(self, *args):
        return

    def do_POST(self):
        """
        Sends a 200 to the client and starts a new thread to
        execute the proper hook function
        """
        try:
            # Get the length of the post data
            content_len = int(self.headers.getheader("content-length", 0))
            # Read the post data
            post_body = self.rfile.read(content_len)
            # Load the post data from its json form to a dict
            post_body = json.loads(post_body)
            # Send the client a success reponse
            self.send_response(200)
            self.server.send_headers(self)
            self.end_headers()
            # Deal with the recived json
            self.server.got_request(post_body, self.wfile)
        except Exception as error:
            self.send_response(501)
            self.server.send_headers(self)
            self.end_headers()
            self.wfile.write(str(error) + "\n")
        return

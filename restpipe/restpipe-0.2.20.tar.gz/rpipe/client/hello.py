import json

import rpipe.client.utility
import rpipe.event


class ClientHello(object):
    """Send a hello message from client to server."""

    def send(self, connection):
        """Send welcome message and any information that we might need to 
        share, and use their response for the same purpose.
        """

        # Get the events that we want to hear about.
        eh = rpipe.client.utility.get_client_event_handler()
        event_couplets = eh.get_event_couplets_to_receive()

        data = {
            'remote_handled_event_couplets': event_couplets,
        }

        data_encoded = json.dumps(data)

        verb = 'post'
        noun = 'hello'
        mimetype = 'application/json'

        r = rpipe.event.send_message_to_remote(
                connection, 
                verb, 
                noun, 
                data_encoded, 
                mimetype)

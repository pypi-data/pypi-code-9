import json
import mock

from unittest import TestCase
from zymbit.messenger.server import ConsoleMessengerServer


class ConsoleMessengerServerTestCase(TestCase):
    @mock.patch('zymbit.messenger.server.get_connector')
    @mock.patch('zymbit.messenger.server.socket')
    def test_int_json(self, socket_mock, get_connector_mock):
        client = mock.Mock()

        server = ConsoleMessengerServer()
        server.connect((client, ('host', 12345)))

        server.handle_message(client, '3\n')

        send = get_connector_mock.return_value.send
        self.assertEqual(1, send.call_count)

        envelope = send.call_args[0][0]
        data = json.loads(envelope)

        self.assertEqual({'key': 'sensor', 'value': 3}, data['params'])

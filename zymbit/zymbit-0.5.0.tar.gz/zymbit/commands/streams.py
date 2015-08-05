import logging

from tabulate import tabulate

from zymbit.commands import Command

from zymbit.util import ZymbitApi


class StreamsCommand(Command):
    command_name = 'streams'
    datasets_endpoint = '/datasets'
    devices_endpoint = '/zymbots'

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def run(self):
        api = ZymbitApi()

        # get devices
        response = api.request('get', self.devices_endpoint)

        devices_data = response.json()
        devices_by_uuid = dict([(x['uuid'], x) for x in devices_data['results']])

        response = api.request('get', self.datasets_endpoint)

        data = response.json()

        headers = ['zymbot', 'routing_key']
        table = [[devices_by_uuid.get(x['zymbot']).get('hostname'), x['path']]
                 for x in data['results']]

        print tabulate(table, headers=headers)

import logging

from tabulate import tabulate

from zymbit.commands import Command

from zymbit.util import ZymbitApi


class DevicesCommand(Command):
    command_name = 'devices'
    api_endpoint = '/zymbots'

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def run(self):
        api = ZymbitApi()
        response = api.request('get', self.api_endpoint)

        data = response.json()

        headers = ['hostname', 'client_id', 'uuid']
        table = [[x['hostname'], x['client_id'], x['uuid']] for x in data['results']]

        print tabulate(table, headers=headers)

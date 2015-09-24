import logging
import sys

import requests

from zymbit.commands import Command
from zymbit.common.config import get_config, save_config

API_PREFIX = '/api/v1'
WEBSOCKET_URL = '/websocket_url'


class CloudCommand(Command):
    command_name = 'cloud'

    @property
    def logger(self):
        return logging.getLogger(__name__)

    @classmethod
    def setup_parser(cls, parser):
        command_parser = super(CloudCommand, cls).setup_parser(parser)

        command_parser.add_argument('--insecure', action='store_true')
        command_parser.add_argument('api_uri')

        return command_parser

    def run(self):
        api_uri = self.args.api_uri
        verify = not self.args.insecure

        self.logger.debug('api_uri={}, verify={}'.format(api_uri, verify))

        session = requests.Session()

        api_url = '{}{}'.format(api_uri, API_PREFIX)
        websocket_url_endpoint = '{}{}'.format(api_url, WEBSOCKET_URL)

        response = session.get(websocket_url_endpoint, verify=verify)
        try:
            response.raise_for_status()
        except requests.HTTPError, exc:
            status_code = response.status_code
            sys.exit('got status_code={} when getting websocket URL'.format(status_code))

        websocket_url = response.json()
        
        config = get_config()
        cloud_config = config.get('cloud', {})
        cloud_config.update({
            'check_hostname': verify,
            'api_url': api_url,
            'websocket_url': websocket_url,
        })

        config['cloud'] = cloud_config
        save_config(config)

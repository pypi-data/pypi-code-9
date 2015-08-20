__author__ = 'Sinisa'

import json
import inject
import requests
from six.moves.urllib.parse import urlparse, urljoin
from sbg_cli.config import Config
from sbg_cli.command import Command
from sbg_cli.sbg_docker.docker_client.utils import get_session
from sbg_cli.sbg_docker.docker_client.client import Docker


class Appget(Command):

    cmd = 'app-get'
    args = '<url> [--output=<output>]'
    order = 6

    def __init__(self):
        self.docker = inject.instance(Docker)
        self.cfg = inject.instance(Config)

    def __call__(self, *args, **kwargs):
        url = kwargs.get('<url>')
        output = kwargs.get('--output')
        app_url, sbg = url_resolver(url, self.cfg)
        session_id = get_session(self.cfg.docker_registry)
        file_name = output or app_name(app_url, sbg=sbg)
        app = get_app(app_url, session_id, sbg=sbg)
        if app:
            with open(file_name, 'w') as f:
                json.dump(app, f)
            print('App written to file: %s' % file_name)


def get_app(url, session, sbg=False):
    if sbg:
        headers = {'session-id': session, 'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()['message']
        else:
            print('App not found.')
    else:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print('App not found.')
    return None


def url_resolver(url, config):
    '''
    :param url: App url
    :param config: Config with app_registry and platform url. Resolve is the authentication needed
    :return: App url, and sbg flag if app is sbg hosted
    >>> url_resolver('https://igor.sbgenomics.com/u/sinisa/rabix-test/apps/#bwa-index/0', Config({"app_registry": "brood.sbgenomics.com", 'platform_url': ("www.sbgenomics.com", 'igor.sbgenomics.com')}))
    ('https://brood.sbgenomics.com/v1/apps/sinisa/rabix-test/bwa-index/0', True)
    >>> url_resolver('https://igor.sbgenomics.com/u/sinisa/rabix-test/apps/#bwa-index/', Config({"app_registry": "brood.sbgenomics.com", 'platform_url': ("www.sbgenomics.com", 'igor.sbgenomics.com')}))
    ('https://brood.sbgenomics.com/v1/apps/sinisa/rabix-test/bwa-index', True)
    >>> url_resolver('https://igor.sbgenomics.com/u/sinisa/rabix-test/apps/bwa-index/edit/?type=tool', Config({"app_registry": "brood.sbgenomics.com", 'platform_url': ("www.sbgenomics.com", 'igor.sbgenomics.com')}))
    ('https://brood.sbgenomics.com/v1/apps/sinisa/rabix-test/bwa-index', True)
    >>> url_resolver('https://www.rabix.org:3333/tool/552277439b80b4927ee6d5d6', Config({"app_registry": "brood.sbgenomics.com", 'platform_url': ("www.sbgenomics.com", 'igor.sbgenomics.com')}))
    ('https://www.rabix.org:3333/tool/552277439b80b4927ee6d5d6', False)
    '''
    p = urlparse(url)
    netloc = p.netloc
    path = [part for part in p.path.split('/') if part][1:-1]
    fragment = p.fragment
    if netloc in config.platform_url:
        if fragment:
            # App page - remove
            fragment = [part for part in fragment.split('/') if part]
            app_url = urljoin('https://' + config.app_registry,
                              '/'.join(['v1', 'apps'] + path + fragment))
        else:
            # Edit page
            path.pop(2)
            app_url = urljoin('https://' + config.app_registry,
                              '/'.join(['v1', 'apps'] + path))
        sbg = True
    elif netloc in config.app_registry:
        app_url = url
        sbg = True
    else:
        app_url = url
        sbg = False
    return app_url, sbg


def app_name(url, sbg=False):
    '''
    :param url: App url
    :param sbg: Flag if app is sbg hosted
    :return: Name of the output file
    >>> app_name('https://brood.sbgenomics.com/v1/apps/sinisa/rabix-test/bwa-index/0', sbg=True)
    'bwa-index.json'
    >>> app_name('https://brood.sbgenomics.com/v1/apps/sinisa/rabix-test/bwa-index', sbg=True)
    'bwa-index.json'
    >>> app_name('https://www.rabix.org:3333/tool/552277439b80b4927ee6d5d6', sbg=False)
    '552277439b80b4927ee6d5d6.json'
    '''
    path = [part for part in urlparse(url).path.split('/') if part][1:]
    if sbg:
        if len(path) == 4:
            name = '%s.json' % path[-1]
        else:
            name = '%s.json' % path[-2]
        return name
    else:
        return path[-1] if path[-1].endswith('.json') else '%s.json' % path[-1]


if __name__ == "__main__":
    import doctest
    doctest.testmod()
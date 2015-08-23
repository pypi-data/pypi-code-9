import logging
import os
import shutil

from zymbit.compat import config, provision, util

SCRIPT_DIR = os.path.dirname(__file__)


class Provision(object):
    def __init__(self, token, api_url=None, websocket_url=None, check_hostname=None, config_only=False, clean=False):
        self.token = token
        self.api_url = api_url
        self.websocket_url = websocket_url
        self.check_hostname = check_hostname
        self.config_only = config_only
        self.clean = clean
        self.ssh_pubkey = None

    @property
    def logger(self):
        return logging.getLogger(__name__)

    def copy_files(self):
        distro = util.get_distro()
        system = util.get_system()

        files_root = None
        _path = SCRIPT_DIR
        while _path != '/':
            system_files_path = os.path.join(_path, 'files', system)
            if os.path.exists(system_files_path):
                files_root = os.path.dirname(system_files_path)
                break

            _path = os.path.dirname(_path)

        if not files_root:
            self.logger.warning('files_root not found, skipping copy_files')
            return

        for tree in (system, '{}-{}'.format(system, distro)):
            tree_root = os.path.join(files_root, tree)

            if not os.path.exists(tree_root):
                self.logger.warning('tree_root={} does not exist'.format(tree_root))
                continue

            self.logger.info('copying files from tree_root={} to /'.format(tree_root))

            try:
                _makedirs = shutil.os.makedirs
                shutil.os.makedirs = lambda *args, **kwargs: None
                shutil.copytree(tree_root, '/')
            finally:
                shutil.os.makedirs = _makedirs

    def run(self):
        self.write_config()

        if self.config_only:
            return

        self.copy_files()

        system = util.get_system()

        try:
            status = provision.enable_init_script()
        except AttributeError:
            self.logger.warning('enable_init_script not found for system={}'.format(system))
        else:
            if status != 0:
                self.logger.warning('enable_init_script exited with status={}'.format(status))

        try:
            status = provision.start_service()
        except AttributeError:
            self.logger.warning('start_service not found for system={}'.format(system))
        else:
            if status != 0:
                self.logger.warning('start_service exited with status={}'.format(status))

        try:
            status = provision.setup_metrics()
        except AttributeError:
            self.logger.warning('setup_metrics not found for system={}'.format(system))
        else:
            if status != 0:
                self.logger.warning('setup_metrics exited with status={}'.format(status))

        try:
            status = provision.start_metrics()
        except AttributeError:
            self.logger.warning('start_metrics not found for system={}'.format(system))
        else:
            if status != 0:
                self.logger.warning('start_metrics exited with status={}'.format(status))

    def write_config(self):
        if self.clean and os.path.exists(config.CONFIG_PATH):
            os.remove(config.CONFIG_PATH)

        _config = config.get_config()

        if self.websocket_url:
            _config.setdefault('cloud', {})['websocket_url'] = self.websocket_url

        if self.api_url:
            _config.setdefault('cloud', {})['api_url'] = self.api_url

        _config.setdefault('cloud', {})['check_hostname'] = self.check_hostname

        _config.setdefault('auth', {})['provisioning_token'] = self.token

        config.save_config(_config)

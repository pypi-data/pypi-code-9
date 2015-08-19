'''
Created on April 21, 2015

@author: martin.melchior
'''
from remoot.starter import LocalStarter, SSHStarter

from euclidwf.framework.configuration import DRM_PROTOCOL, DRM_HOSTNAME,\
    DRM_USERNAME, DRM_PASSWORD, LOCALCACHE
from euclidwf.utilities.config_loader import load_from_config
from euclidwf.utilities.error_handling import ConfigurationError


def _resolve_status(data):
    pass

PROTOCOL_SSH="ssh"
PROTOCOL_LOCAL="local"

def create(config):
    protocol=load_from_config(config, DRM_PROTOCOL)
    if protocol==PROTOCOL_SSH:
        return SSHCmdExecutor(config)
    elif protocol==PROTOCOL_LOCAL:
        return LocalCmdExecutor(config)
    else:
        raise ConfigurationError("Protocol %s for accessing DRM not supported."%protocol)
    

class AbstractCmdExecutor(object):

    def execute(self, command):
        raise NotImplementedError()


class LocalCmdExecutor(AbstractCmdExecutor):

    def __init__(self, config):
        cachedir=load_from_config(config, LOCALCACHE, False)
        self.starter=LocalStarter(cachedir)

    def execute(self, command):
        return self.starter.start(command)
    


class SSHCmdExecutor(AbstractCmdExecutor):
    
    def __init__(self, config):
        self.hostname=load_from_config(config, DRM_HOSTNAME)
        self.username=load_from_config(config, DRM_USERNAME)
        self.password=load_from_config(config, DRM_PASSWORD)
        cachedir=load_from_config(config, LOCALCACHE, False)
        self.starter=SSHStarter(hostname=self.hostname, username=self.username, password=self.password, tmp_dir=cachedir)

    def execute(self, command):
        return self.starter.start(command)

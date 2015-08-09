from weaver.exceptions import InvalidConfigurationException
from weaver.utils import _
from weaver import helpers
from fabric.api import env

import collections
import logging

SERVICE_ENV_DEFAULTS = {
        'user':'ec2-user',
        'key_filename':'~/Dropbox/Tunnel/.ssh/awspdxlinkeviadmin.pem'
        }

SERVICE_REGISTRY = None
VALID_STAGES = ['Desktop', 'Alpha', 'Beta', 'Gamma', 'Prod']

DEFAULT_META = {
        'domains':{
            'stage':{
                'valid_keys': VALID_STAGES,
                }
            }
        }

class ServiceRegistry(object):
    """
    Holds service entries

        env.service_registry to get a list of services
    """

    def __init__(self, env, logger):
        self.service_dict = {}

        self._thread_config = None
        self._env_conf = None
        self._service = None
        self.logger = logger

        env.domain = {}
        env.service_registry = self

    def _is_initialized(self, service):
        """
        Has config been initialized yet?
        """
        if (self._service != service) or (self._thread_config is None):
            return False
        else:
            return True

    def _get_domain_node(self, conf_node, domain_key, domain_value,
            domain_meta):
        """
        Traverse down config tree and get next node for domain. If domain
        missing or invalid, raise InvalidDomainException
        """
        try:
            next_node = conf_node[domain_value]
        except KeyError:
            #FIXME: techinically, valid keys should be checked before this
            # point, we can get invalid keys that happen to exist in the
            # conf_node
            keys_valid = domain_meta[domain_key]['valid_keys']
            keys_node = conf_node.keys()
            # this is an invalid domain key
            if domain_value not in keys_valid:
                msg = _("""No entry for
            {self.service}/{domain_value} in valid keys. valid keys for
            {domain_key}(s): {keys_valid}""",['oneline'])
            else:
                # this is a valid domain key but not present in the config
                msg = _("""No entry for
            {self.service}/{domain_value} in node keys. node keys for
            {domain_value}(s): {keys_node}""",['oneline'])
            raise InvalidConfigurationException(msg)
        return next_node

    def _initialize_meta(self, meta, service):
        _meta = dict(DEFAULT_META)
        _meta.update(meta)
        self.service_dict[service]['meta'] = _meta

    def _initialize_service(self, service, env, stage, region):
        """
        Setup any bootstrapping needed by service stage
        Set env.service = service
        Updates env with service keys, overriding any previous service keys
        """
        # NOTE: important that this is the first line
        # other functions below depend on the service being set
        self.initialize_service(service)

        meta = self.meta
        conf_node = self.config
        domains = meta['domains']
        self.logger.debug(_("""initializing {service} w/meta:{meta} and
            conf_node{conf_node}""", ['oneline']))

        key = "stage"
        conf_node = self._get_domain_node(conf_node, key, stage,
                domains)

        key = "region"
        if domains.has_key(key):
            conf_node = self._get_domain_node(conf_node, key, region,
                    domains)

        self.logger.info(_("final conf: {conf_node}"))
        env_vars = conf_node.get('env', {})
        env.update(env_vars)
        thread_vars = conf_node.get('thread', {})
        self._thread_config = thread_vars
        return self

    def register(self, service, conf, meta = {}):
        """
        Args:
            service String: service name
            conf Hash:
                prototype:
                    {
                        'meta': {},
                        'config':{}
                    }
        Return updated conf
        """
        self.service_dict[service] = {'config':{}, 'meta':{}}
        self.service_dict[service]['config'] = conf
        self._initialize_meta(meta, service)
        return self

    def initialize_service(self, service):
        self._service = service

    def validate_conf(self, weaver_conf, metadata):
        """
        """
        #TODO
        pass

    @property
    def config(self):
        return self.service_dict[self.service]['config']

    @property
    def meta(self):
        return self.service_dict[self.service]['meta']

    @property
    def service(self):
        """
        Current service name
        """
        return self._service

    def get_thread_config(self, service, stage, region = None):
        """
        Get configuration for given service/domain(s)
        """
        global env
        if not self._is_initialized(service):
            self._initialize_service(service, env, stage, region)
        return self._thread_config

    @staticmethod
    def delete_service(self, service):
        """
        Delete service from Weaver runtime. Implies `reset_service`
        """
        ServiceRegistry.reset_service(service)
        #TODO
        pass

    @staticmethod
    def reset_service(self, service):
        """
        Revert environmental changes initialized in
        the ServiceRegistry of a service
        """
        #TODO
        pass

    @staticmethod
    def get_service_registry(reset=False):
        """
        Get singleton service registry object.
        Wrapper around global env object
        """
        global SERVICE_REGISTRY
        if not SERVICE_REGISTRY or reset:

            logger = logging.getLogger()
            #FIXME: make logging configurable
            logger.setLevel(logging.DEBUG)
            logger.addHandler(logging.StreamHandler())

            SERVICE_REGISTRY = ServiceRegistry(env, logger)
        return SERVICE_REGISTRY


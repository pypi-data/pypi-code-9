from collections import defaultdict, namedtuple
import logging

_logger = logging.getLogger()


class Registry:

    """
        self._repository.register_service(service)
        self._client_protocols[params['node_id']] = registry_protocol
        self._connect_to_service(params['host'], params['port'], params['node_id'], params['type'])
        self._handle_pending_registrations()
        self._inform_consumers(service)

    """

    def __init__(self, repository=None):
        self._repository = repository or Repository()

    def receive(self, packet: dict, protocol, transport):
        """
        bluntly assumes the availability of a parameter called node_id inside
        packet
        """

        request_type = packet['type']
        if request_type == 'register':
            service = ServiceInstance(protocol=protocol, **packet)
            self.register_service(service)

            # self.register_service(packet, protocol)
        elif request_type == 'get_instances':
            self.get_service_instances(packet, protocol)
        elif request_type == 'xsubscribe':
            self._xsubscribe(packet)
        elif request_type == 'get_subscribers':
            self.get_subscribers(packet, protocol)
        elif request_type == 'pong':
            self._ping(packet)
        elif request_type == 'ping':
            self._pong(packet, protocol)
        elif request_type == 'uptime_report':
            self._get_uptime_report(packet, protocol)

    def register_service(self, service):
        """
            - is the service registering for the first time?
        """

        self._repository.upsert_service(service)


class Repository:

    """
    should be able to reload itself by reading a file.

    services_dictionary schema:
    (name, version):
        type tcp/http:
            is_available: True/False
            host, port: 
                node_id:
                registered_at:
                last_pinged_at:


    """

    def __init__(self,):
        self._services = defaultdict()
        self._nodes = {}
        self._dependency_adjlist = {}
        self._subscription_adjlist = {}

    def upsert_service(self, service):
        """
        """
        self._nodes[service.node_id] = service

        try:
            record = self._services[service.service_tuple()][service.host_tuple()]
        except KeyError as e:
            # the instance is coming up for the first time.


class ServiceInstance:

    def __init__(self, name, version, host, port, node_id, _type, protocol, dependencies, registry):
        self.name = name
        self.version = version
        self.host = host
        self.port = port
        self.node_id = node_id
        self.type = _type
        self.protocol = protocol
        self.dependencies = dependencies

        self._registry = registry

        self._service_tuple = (self.name, self.version)
        self._host_tuple = (self.host, self.port)

    @property
    def service_tuple(self):
        return self._service_tuple

    @property
    def host_tuple(self):
        return self._host_tuple

    def __unicode__(self):
        return "{}/{}-{}:{}-{}".format(self.name, self.version, self.host, self.port, self.node_id)


def registry_record():
    return {
        'registered_at': None,
        'last_ponged_at': None,
        'node_id': None,
        'is_pending': True,
        'is_registered': False
    }


class Registry:

    """
    maintains a services dictionary.
    key service_name, service_version tuple.
    values are dictionaries containing instances.:
        instances = {(host, port): node_id}

    node_map = 
        node_id -> (service, version, host, port)


    {
        (name, version): {
            (host, port): {
                    registered_at: timestamp
                    last_ponged_at: timestamp.
                    node_id: "hex"
                    is_pending:
                    is_registered:

                }
    }

    dependency_adj_list:
        (service_name, service_version): [(service, version), ...]

    subscription_adj_list:
        publisher -> subscribers
        (service_name, service_version): [subscriber, entity, strategy etc]


    """
    services = defaultdict()

    def register_service(self, service):
        service_name_version = (service.name, service.version)
        service_host_port = (service.host, service.port)

        try:
            record = self.services[service_name_version][service_host_port]
        except KeyError:
            record = registry_record()

        record['node_id'] = service.node_id

    def deregister_service(self, service):
        pass

    def get_instances(self, service, version):
        pass

    def get_subscribers(self, service):
        pass

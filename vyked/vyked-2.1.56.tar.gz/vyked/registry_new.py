from collections import defaultdict, namedtuple
import logging

_logger = logging.getLogger()

class Registry:

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
            service.register()

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


class Repository:
    """
    (name, version):
        type tcp/http:
            is_available: True/False
            host, port: 
                node_id:
                registered_at:
                last_pinged_at:


    """

    def __init__(self,):
        self._services = {}
        self._nodes = {}
        self._dependency_adjlist = {}
        self._subscription_adjlist = {}


    def register_service(self, service):
        """
        """
        service_tuple = (service.name, service.version)
        host_tuple = (service.host, service.port)
        service_record = {
            'node_id': service.node_id,
            'registered_at': time.time(),
            'last_pinged_at': 0,
            ''

        }
        try:
            record = self._services[service_tuple]
        except KeyError as e:



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

    def service_tuple(self):
        return (self.name, self.version)

    def host_tuple(self):
        return(self.host, self.port)

    def registry_record(self):
        return {
            'node_id': service.node_id,
            'registered_at': time.time(),
            'last_pinged_at': 0,
        }


    def register(self,):
        pass

    def _deregister(self,):
        pass

    def subscribe(self,):
        pass

    def get_subscribers(self,):
        pass

    def get_instances(self,):
        pass

    # dependencies
    # subscriptions


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

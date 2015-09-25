from collections import defaultdict
import logging
import time

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
            # service = ServiceInstance(protocol=protocol, **packet)
            self.register_service(packet=packet, protocol=protocol)

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

    def register_service(self, packet, protocol):
        """
            - is the service registering for the first time?
        """
        service = self._repository.get_service(
            service_name=packet['name'], service_version=packet['version'], dependencies=packet['dependencies'],
            repository=self._repository)

        service_instance = ServiceInstance(service=service, host=packet['host'], port=packet['port'],
                                           node_id=packet['node_id'], _type=packet['type'], protocol=protocol)
        service_instance.register()

        self._repository.register_service(service_instance)
        self._repository.update_status()


class Service:

    def __init__(self, name, version, dependencies, repository):
        self.name = name
        self.version = version
        self._repository = repository

        self.instances = dict()
        self.dependencies = dependencies

        self._dependents = set()

        self.subscriptions = []
        self.subscribers = []

        self.status = None

    def upsert_instance(self, instance):
        self.instances[instance.host_tuple] = instance

    def remove_instance(self, instance):
        self.instances.pop(instance.host_tuple)

    def add_subscribers(self, *subscribers):
        pass

    def add_dependents(self, *dependents):
        """
        assumes dependent is a tuple of (service, version)
        """
        self._dependents = set.union(self._dependents, set(dependents))

    @property
    def dependents(self):
        return self._dependents

    @property
    def is_available(self):
        """
        check if at least one live instance is serving over tcp
        """
        for host_tuple, instance in self.instances.items():
            if instance.type == 'tcp' and instance.is_up:
                return True
        return False


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
                last_ponged_at:


    (name, version):
        working?
        stats?
        dependents: [(name,version) ... ],
        instances: {(host,port): node_id, type, registered, last_ponged_at etc}
        subscribers:


    """

    def __init__(self,):
        def default_instance_record():
            return dict({
                'node_id': None,
                'registered_at': time.time(),
                'last_ponged_at': 0,
                'is_available': True
            })

        def default_service_record():
            return dict({
                'is_available': False,
                'is_pending': True,
                'dependents': set(),
                'instances': defaultdict(default_instance_record),
                'subscribers': dict()
            })
        self._services = dict()
        self._nodes = dict()

    def get_service(self, service_name, service_version):
        try:
            service = self.services[(service_name, service_version)]
        except:
            service = Service(service_name, service_version)
            self.services[(service_name, service_version)] = service
        return service

    def register_service(self, instance):
        self._nodes[instance.node_id] = instance
        for service_name, service_version in instance.service.dependencies:
            service = self.get_service(service_name, service_name_version)
            service.add_dependents()

    def register_service(self, service):
        self._nodes[service.node_id] = service

        for service_tuple in service.dependencies:
            self._services[service.service_tuple]['dependents'].add(service_tuple)

        self._services[service.service_tuple]['instances'][service.host_tuple].update({
            'node_id': service.node_id,
            'type': service.type
        })

        self._services[service.service_tuple]['is_available'] = True

    def update_status(self):
        # available_services = filter(lambda x: self._services[x]['is_available'], self._services)
        available_services = set([x for x, y in self._services.items() if y['is_available']])
        for service_tuple in available_services:
            dependencies = self._services[service_tuple]['dependencies']
            self._services[service_tuple]['is_pending'] = dependencies.issubset(available_services)

    def deregister_service(self, service):
        "deregister service instance"
        self._service[service.service_tuple]['instance'][service.host_tuple]['is_available'] = False


class ServiceInstance:

    def __init__(self, host, port, node_id, _type, protocol, service):
        self.service = service
        self.host = host
        self.port = port
        self.node_id = node_id
        self.type = _type
        self.protocol = protocol

        self._host_tuple = (self.host, self.port)

    @property
    def service_tuple(self):
        return self._service_tuple

    @property
    def host_tuple(self):
        return self._host_tuple

    def __unicode__(self):
        return "{}/{}-{}:{}-{}".format(self.name, self.version, self.host, self.port, self.node_id)

    def register(self):
        self.service.upsert_instance(self)
        # self.service.update()


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

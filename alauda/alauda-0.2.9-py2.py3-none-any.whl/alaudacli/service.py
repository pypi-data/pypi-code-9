import json
import requests
import time

import auth
import util
from instance import Instance
from exceptions import AlaudaServerError

MAX_RETRY_NUM = 10
INSTANCE_SIZES = ['XXS', 'XS', 'S', 'M', 'L', 'XL']


class Service(object):

    def __init__(self, name, image_name, image_tag, target_num_instances=1, instance_size='XS', run_command='',
                 instance_ports=[], instance_envvars={}, volumes=[], links=[], details='', namespace=None,
                 scaling_mode='MANUAL', autoscaling_config={}, custom_domain_name='', region_name=None):
        self.name = name
        self.image_name = image_name
        self.image_tag = image_tag
        self.target_num_instances = target_num_instances

        self.instance_size = instance_size
        if instance_size not in INSTANCE_SIZES:
            raise AlaudaServerError(400, 'instance_size must be one of {}'.format(INSTANCE_SIZES))
        self.run_command = run_command
        self.instance_envvars = instance_envvars
        self.instance_ports = instance_ports
        self.volumes = volumes
        self.links = links
        self.details = details
        self.custom_domain_name = custom_domain_name

        self.api_endpoint, self.token, self.username = auth.load_token()
        self.headers = auth.build_headers(self.token)
        self.namespace = namespace or self.username
        self.scaling_mode = scaling_mode
        self.autoscaling_config = autoscaling_config
        self.region_name = region_name

    def _update_envvars_with_links(self, instance_envvars, links, namespace=None):
        linked_to = {}
        if links is not None:
            for link in links:
                service_name = link[0]
                alias = link[1]
                linked_to[service_name] = alias
                retry_num = 0
                while retry_num < MAX_RETRY_NUM:
                    linked_service = Service.fetch(service_name, namespace)
                    linked_service_data = json.loads(linked_service.details)
                    linked_service_ports = linked_service_data['instance_ports']
                    if len(linked_service_ports) == 0:
                        break
#                     linked_service_envvars = json.loads(linked_service_data['instance_envvars'])
#                     linked_service_addr = linked_service_envvars['__DEFAULT_DOMAIN_NAME__']
                    key = '{0}_PORT'.format(alias).upper()
                    for port in linked_service_ports:
                        service_port = port.get('service_port')
                        if service_port is None:
                            retry_num = retry_num + 1
                            time.sleep(1)
                            break
                        retry_num = MAX_RETRY_NUM + 1
                        url = '{0}://{1}:{2}'.format(port['protocol'], port['default_domain'], service_port)
                        if key not in instance_envvars.keys():
                            instance_envvars[key] = url
                        pattern = '{0}_PORT_{1}_{2}'.format(alias, port['container_port'], port['protocol']).upper()
                        instance_envvars[pattern] = url
                        instance_envvars[pattern + '_ADDR'] = port['default_domain']
                        instance_envvars[pattern + '_PORT'] = str(service_port)
                        instance_envvars[pattern + '_PROTO'] = port['protocol']
                if retry_num == MAX_RETRY_NUM:
                    raise AlaudaServerError(500, 'Timed out waiting for {} to acquire service port'.format(service_name))
        return linked_to

    def _create_remote(self, target_state):
        linked_to = self._update_envvars_with_links(self.instance_envvars, self.links, self.namespace)
        util.expand_environment(self.instance_envvars)
        url = self.api_endpoint + 'services/{}/'.format(self.namespace)
        payload = {
            "app_name": self.name,
            "target_num_instances": self.target_num_instances,
            "image_name": self.image_name,
            "image_tag": self.image_tag,
            "instance_size": self.instance_size,
            "scaling_mode": "MANUAL",
            "target_state": target_state,
            "run_command": self.run_command,
            "instance_envvars": self.instance_envvars,
            "instance_ports": self.instance_ports,
            'linked_to_apps': linked_to,
            "volumes": self.volumes,
            'scaling_mode': self.scaling_mode,
            'autoscaling_config': self.autoscaling_config,
            'custom_domain_name': self.custom_domain_name
        }
        if self.region_name:
            payload['region_name'] = self.region_name
        r = requests.post(url, headers=self.headers, data=json.dumps(payload))
        util.check_response(r)

    @classmethod
    def fetch(cls, name, namespace=None):
        api_endpoint, token, username = auth.load_token()
        url = api_endpoint + 'services/{}/'.format(namespace or username) + name
        headers = auth.build_headers(token)
        r = requests.get(url, headers=headers)
        util.check_response(r)
        data = json.loads(r.text)
        service = cls(name=data['service_name'],
                      image_name=data['image_name'],
                      image_tag=data['image_tag'],
                      target_num_instances=data['target_num_instances'],
                      instance_size=data['instance_size'],
                      details=r.text,
                      namespace=data['namespace'])
        return service

    @classmethod
    def list(cls, namespace, page):
        api_endpoint, token, username = auth.load_token()
        url = api_endpoint + 'services/{}/?page={}'.format(namespace or username, page)
        headers = auth.build_headers(token)
        r = requests.get(url, headers=headers)
        util.check_response(r)
        service_list = []
        services = json.loads(r.text)
        services = services.get('results', [])
        for data in services:
            try:
                service = Service.fetch(data['service_name'], namespace)
                service_list.append(service)
            except AlaudaServerError:
                continue
        return service_list

    @classmethod
    def remove(cls, name, namespace=None):
        print '[alauda] Removing service "{}"'.format(name)
        api_endpoint, token, username = auth.load_token()
        url = api_endpoint + 'services/{}/'.format(namespace or username) + name
        headers = auth.build_headers(token)
        try:
            r = requests.delete(url, headers=headers)
            util.check_response(r)
        except AlaudaServerError as ex:
            if ex.status_code == 404:
                print '[alauda] Service "{}" does not exist'.format(name)
            else:
                raise ex

    def create(self):
        print '[alauda] Creating service "{}"'.format(self.name)
        self._create_remote('STOPPED')

    def run(self):
        print '[alauda] Creating and starting service "{}"'.format(self.name)
        self._create_remote('STARTED')

    def inspect(self):
        if not self.details:
            url = self.api_endpoint + 'services/{}/'.format(self.namespace) + self.name
            r = requests.get(url, headers=self.headers)
            util.check_response(r)
            self.details = r.text
        return self.details

    def start(self):
        print '[alauda] Starting service "{}"'.format(self.name)
        self.target_state = 'STARTED'
        url = self.api_endpoint + 'services/{}/'.format(self.namespace) + self.name + '/start/'
        r = requests.put(url, headers=self.headers)
        util.check_response(r)

    def stop(self):
        print '[alauda] Stopping service "{}"'.format(self.name)
        self.target_state = 'STOPPED'
        url = self.api_endpoint + 'services/{}/'.format(self.namespace) + self.name + '/stop/'
        r = requests.put(url, headers=self.headers)
        util.check_response(r)

    def scale(self, target_num_instances):
        self.target_num_instances = target_num_instances
        print '[alauda] Scaling service: {0} -> {1}'.format(self.name, self.target_num_instances)
        url = self.api_endpoint + 'services/{}/'.format(self.namespace) + self.name
        payload = {
            "app_name": self.name,
            "target_num_instances": self.target_num_instances,
        }
        r = requests.put(url, headers=self.headers, data=json.dumps(payload))
        util.check_response(r)

    def enable_autoscaling(self, autoscaling_config):
        print '[alauda] Enabling auto-scaling for {0}'.format(self.name)
        url = self.api_endpoint + 'services/{}/'.format(self.namespace) + self.name
        payload = {
            "scaling_mode": 'AUTO',
            "autoscaling_config": autoscaling_config,
            'app_name': self.name
        }
        r = requests.put(url, headers=self.headers, data=json.dumps(payload))
        util.check_response(r)

    def disable_autoscaling(self, target_num_instances):
        if target_num_instances is not None:
            self.target_num_instances = target_num_instances
        print '[alauda] Disabling auto-scaling for {0}. Target number of instances: {1}'.format(self.name, self.target_num_instances)
        url = self.api_endpoint + 'services/{}/'.format(self.namespace) + self.name
        payload = {
            "app_name": self.name,
            "target_num_instances": self.target_num_instances,
            'scaling_mode': 'MANUAL'
        }
        r = requests.put(url, headers=self.headers, data=json.dumps(payload))
        util.check_response(r)

    def logs(self, start_time, end_time):
        start, end = util.parse_time(start_time, end_time)
        url = self.api_endpoint + 'services/{0}/{1}/logs?start_time={2}&end_time={3}'.format(self.namespace, self.name, start, end)
        r = requests.get(url, headers=self.headers)
        util.check_response(r)
        return r.text

    def get_region_info(self):
        data = json.loads(self.details)
        region_info = data['region']
        return region_info['IaaS'], region_info['name']

    def get_run_command(self):
        data = json.loads(self.details)
        run_command = data['run_command']
        if not run_command:
            run_command = ' '
        return run_command

    def get_state(self):
        data = json.loads(self.details)
        return data.get('current_status')

    def get_ports(self):
        ports = ''
        data = json.loads(self.details)
        if not data['instance_ports']:
            return ' '
        for port in data['instance_ports']:
            instance_envvars = json.loads(data['instance_envvars'])
            ports = ports + '{0}:{1}->{2}/{3}, '.format(instance_envvars['__DEFAULT_DOMAIN_NAME__'],
                                                        port.get('service_port', ''),
                                                        port['container_port'],
                                                        port['protocol'])
        return ports[:len(ports) - 2]

    def get_instance(self, id):
        url = self.api_endpoint + 'services/{0}/{1}/instances/{2}'.format(self.namespace, self.name, id)
        r = requests.get(url, headers=self.headers)
        util.check_response(r)
        data = json.loads(r.text)
        instance = Instance(service=self, uuid=data['uuid'], details=r.text)
        return instance

    def list_instances(self):
        url = self.api_endpoint + 'services/{0}/{1}/instances/'.format(self.namespace, self.name)
        r = requests.get(url, headers=self.headers)
        util.check_response(r)
        data = json.loads(r.text)
        instance_list = []
        for instance in data:
            instance = Instance(service=self, uuid=instance['uuid'], details=json.dumps(instance))
            instance_list.append(instance)
        return instance_list

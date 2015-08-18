import requests
import json
import os.path
from device import Device


class Lov2pi:

    def __init__(self, apikey, name):
        self.apikey = apikey
        self.config_path = os.path.expanduser("~") + '/.lov2pi'
        self.url = 'http://localhost:8080'
        self.device = Device()
        self.uuid = self.device.uuid
        self.name = name
        self.devices = None
        self.counters = None
        self.config = {'name': self.name, 'appkey': self.apikey, 'uuid': self.uuid}
        json.dump(self.config, open(self.config_path, 'w'))

    def register(self):
        data = self.get_config()
        data['type'] = self.device.type
        data['cpu'] = self.device.cpu
        data['memory'] = self.device.memory
        data['network'] = self.device.network
        data['disk'] = self.device.disks
        path = '/api/v1/devices'
        res = self.make_post(path, data)
        if res['status'] is 'ok':
            print 'registered ok'
        else:
            raise ValueError('appkey or user not found')

    def sync_counter(self):
        path = '/api/v1/metrics'
        data = {'device_uuid': self.uuid}
        self.device.update_counters()
        data['counters'] = self.device.counters
        res = self.make_post(path, data)
        if res['status'] is 'ok':
            return res['data']
        else:
            raise ValueError('counter sync failed')

    def get_config(self):
        if os.path.isfile(self.config_path):
            return json.load(open(self.config_path))
        else:
            return 'not_found'

    def get_devices(self):
        path = '/api/v1/user/%s/devices' % self.apikey
        res = self.make_get(path)
        if res['status'] == 'ok':
            self.devices = res['data']
            return res['data']
        else:
            return res

    def stream_events(self, name, data):
        pass

    def get_event(self, name, device=None):
        if device is None:
            device = self.uuid
        path = '/api/v1/device/' + device + '/feed/' + name
        res = self.make_get(path)
        if res['status'] is 'ok':
            if len(res['data']['feed']) is 0:
                return 'no feeds found'
            else:
                return res['data']['feed'][0]

    def log_event(self, name, value, feed_type='sensor'):
        path = '/api/v1/feed/' + self.apikey + '/' + self.uuid
        data = {'name': name, 'value': value, 'type': feed_type}
        res = self.make_post(path, data)
        if res['status'] is 'ok':
            return res['data']
        else:
            return res

    def make_post(self, path, payload, headers={'content-type': 'application/json'}):
        try:
            r = requests.post(self.url + path, headers=headers, data=json.dumps(payload))
            if r.status_code < 300:
                return {'status': 'ok', 'data': r.json()}
            else:
                return {'status': 'error'}
        except Exception as e:
            print e.message
            return {'status': 'error', 'message': e.message}

    def make_get(self, path, headers={'content-type': 'application/json'}):
        try:
            r = requests.get(self.url + path, headers=headers)
            if r.status_code < 300:
                return {'status': 'ok', 'data': r.json()}
            else:
                return {'status': 'error'}
        except Exception as e:
            print e.message
            return {'status': 'error', 'message': e.message}

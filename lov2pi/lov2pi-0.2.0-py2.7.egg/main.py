import requests
import json
import os.path
from device import Device
from connections import LoveMe


class Lov2pi:
    def __init__(self, apikey, name):
        self.apikey = apikey
        self.config_path = os.path.expanduser("~") + '/.lov2pi'
        #self.url = 'http://localhost:8080'
        self.url = 'http://dev.lov2pi.com'
        self.device = Device()
        self.device_id = self.device.uuid
        self.name = name
        self.devices = None
        self.counters = None
        self.ws = None
        self.config = {'name': self.name, 'appkey': self.apikey, 'device_id': self.device_id}
        json.dump(self.config, open(self.config_path, 'w'))

    def start_ws(self):
        self.ws = LoveMe(self.apikey, self.device_id)
        self.ws.deamonize()

    def register(self):
        data = self.get_config()
        data['type'] = self.device.type
        data['cpu'] = self.device.cpu
        data['memory'] = self.device.memory
        data['network'] = self.device.network
        data['disk'] = self.device.disks
        path = '/api/v1/device'
        res = self.make_post(path, data)
        if res['status'] is 'ok':
            print 'registered ok'
        else:
            raise ValueError('appkey or user not found')

    def sync_counter(self):
        path = '/api/v1/metric'
        data = {'device_id': self.device_id}
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
            device = self.device_id
        path = '/api/v1/device/' + device + '/feed/' + name
        res = self.make_get(path)
        if res['status'] is 'ok':
            if len(res['data']['feed']) is 0:
                return 'no feeds found'
            else:
                return res['data']['feed'][0]

    def get_events(self, device=None):
        if device is None:
            device = self.device_id
        path = '/api/v1/device/' + device + '/feeds'
        res = self.make_get(path)
        if res['status'] is 'ok':
            if len(res['data']['feeds']) is 0:
                return 'no feeds founded'
            else:
                return res['data']['feeds']

    def log_event(self, name, value, value_type='not_set', feed_type='sensor'):
        path = '/api/v1/feed'
        data = {'name': name,
                'value': value,
                'type': feed_type,
                'appkey': self.apikey,
                'value_type': value_type,
                'device_id': self.device_id}
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

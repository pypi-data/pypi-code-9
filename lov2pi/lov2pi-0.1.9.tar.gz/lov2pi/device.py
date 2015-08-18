import requests
import json
import psutil
import platform
import os
import netifaces
import crypt
from uuid import getnode as get_mac


class Device:
    def __init__(self):
        self.hostname = platform.node()
        self.architecture = platform.machine()
        self.platform = self.check_platform()
        self.counters = {'bytes_sent': 0, 'bytes_recv': 0, 'cpu_load': 0, 'per_cpu_load': []}
        self.disks = {}
        self.network = {'interfaces': {}}
        self.cpu = {}
        self.uuid = crypt.crypt(str(get_mac()), str(get_mac()))
        self.memory = {}
        self.type = os.uname()[4]
        self.get_cpu_info()
        self.get_memory_info()
        self.get_disk_info()
        self.get_network_info()

    def update_counters(self):
        self.counters['cpu_load'] = psutil.cpu_percent(interval=None)
        self.counters['per_cpu_load'] = psutil.cpu_percent(interval=None, percpu=True)
        #self.counters['cpu_temp'] = os.popen('vcgencmd measure_temp').readline().replace("temp=", "").replace("'C\n","")
        net_counters = psutil.net_io_counters()
        self.counters['bytes_sent'] = net_counters.bytes_sent - self.counters['bytes_sent']
        self.counters['bytes_recv'] = net_counters.bytes_recv - self.counters['bytes_recv']

    def get_network_info(self):
        net_if = netifaces.interfaces()
        gws = netifaces.gateways()
        gw_ip, default_intf_name = gws['default'][netifaces.AF_INET]
        self.network['gateway_ip'] = gw_ip
        self.network['default_interface'] = default_intf_name
        for net_dev in net_if:
            info = netifaces.ifaddresses(net_dev)
            if info:
                self.network['interfaces'].update({net_dev:  {'ip': info.get(netifaces.AF_INET, ['not set'])[0],
                                                   'mac': info.get(netifaces.AF_LINK, ['not set'])[0]}})

        return self.network

    def check_platform(self):
        # check if you are in arm platform
        if os.uname()[4][:3] == 'arm':
            return 'rpi'
        else:
            return os.uname()[0]

    def get_memory_info(self):
        mem = psutil.virtual_memory()
        self.memory['total_memory'] = mem.total
        self.memory['available_memory'] = mem.available
        self.memory['free_memory_available'] = mem.free
        # percent: the percentage usage calculated as (total - available) / total * 100.
        self.memory['free_memory_usage_percent'] = mem.percent
        return self.memory

    def get_cpu_info(self):
        self.cpu['cpu_cores_nun'] = psutil.cpu_count()
        self.cpu['type'] = platform.processor()
        return self.cpu

    def get_disk_info(self):
        p = psutil.disk_partitions()
        for device in p:
            usage = psutil.disk_usage(device.mountpoint)
            self.disks[device.mountpoint] = {'name': device.device,
                                             'fstype': device.fstype,
                                             'percent': usage.percent,
                                             'total': usage.total,
                                             'used': usage.used,
                                             'free': usage.free}
        return self.disks

    def getserial(self):
        cpuserial = "0000000000000000"
        try:
            f = open('/proc/cpuinfo', 'r')
            for line in f:
                if line[0:6] == 'Serial':
                    cpuserial = line[10:26]

            f.close()
        except Exception as e:
            return e
        return  cpuserial

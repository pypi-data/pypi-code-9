from time import sleep
from lov2pi import Lov2pi
from daemons.prefab import run
import os.path
import json


class Counters(run.RunDaemon):

    def run(self):
        config_path = os.path.expanduser("~") + '/.lov2pi'
        if os.path.isfile(config_path):
            config = json.load(open(self.config_path))
            print config
            client = Lov2pi(config['appkey'], config['name'])
            while True:
                client.sync_counter()
                sleep(1)
        else:
            raise ValueError('config not_found, you should register your lov2pi first')


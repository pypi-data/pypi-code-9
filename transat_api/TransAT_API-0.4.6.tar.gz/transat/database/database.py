import datetime
from tinydb import TinyDB, where
from transat.config import user_setup as usetup
import os

"""
.. module:: Database
   :platform: Unix, Windows
   :synopsis: Provides simple database interface

"""


class Database(object):
    def __init__(self, name="maApp", filename=None):

        env = usetup.load()
        folder = os.path.dirname(filename)
        if folder is not "" and not os.path.exists(folder):
            os.makedirs(folder)
            file = open(filename, 'w+')
        self.db = TinyDB(filename).table('simulations')
        self.simulation = {'application': name, 'created': str(datetime.datetime.now())}
        self.id = self.db.insert(self.simulation)

    def store_inputs(self, inputs):
        self.simulation['inputs'] = inputs
        self.db.update(self.simulation, eids=[self.id])

    def store_tags(self, tags):
        self.simulation['tags'] = tags
        self.db.update(self.simulation, eids=[self.id])

    def store_path(self, key, path):
        if 'path' not in self.simulation.keys():
            self.simulation['path'] = {}
        self.simulation['path'][key] = path
        return True
        # self.db.update(self.simulation, eids=[self.id])

    def load_path(self, key):
        if 'path' in self.simulation.keys() and key in self.simulation['path'].keys():
            return self.simulation['path'][key]
        else:
            raise KeyError()

    def store(self, key, data):
        self.simulation[key] = data
        # self.db.update(self.simulation, eids=[self.id])

    def load(self, key):
        if key in self.simulation.keys():
            return self.simulation[key]
        else:
            raise KeyError()

    def delete(self, key):
        print "Deleting data in database on key: " + key


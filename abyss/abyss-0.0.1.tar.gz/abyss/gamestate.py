#!/usr/bin/env python
''' abyss.server.gamestate
Holds, loads and dumps the gamestate
'''
import json
from abyss.server.mapstate import MapState

class GameState(object):
    
    def __init__(self, path):
        self.path = path
        self.map = MapState()

    def load(self):
        with open(self.path) as f:
            data = json.load(f)
        self.deserialize(data)

    def new(self):
        self.generate_new()
        self.dump(self.path)

    def deserialize(self, data):
        self.map.deserialize(data['map'])

    def serialize(self):
        return {'map': self.map.serialize()}

    def generate_new(self, **kwargs):
        self.map.generate_new(**kwargs)

    def dump(self, path):
        data = self.serialize()
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

#!/usr/bin/env python
''' abyss.server.mapstate '''
import json
from random import uniform
from abyss.entity import Manapool

class MapState(object):

    def __init__(self):
        pass

    def deserialize(self, data):
        self.map = data['map']
        self.height = data['height']
        self.width = data['width']

    def serialize(self):
        return {'map': self.map, 'height': self.height, 'width': self.width}

    def generate_new(self, width=100, height=100, **kwargs):
        self.map = [[None]*width for h in range(height)]
        self.width = width
        self.height = height
        self.spawn_manapools()

    def spawn_manapools(self, num=10):
        for i in range(num):
            x = int(uniform(0, self.width))
            y = int(uniform(0, self.height))
            self.map[y][x] = Manapool()

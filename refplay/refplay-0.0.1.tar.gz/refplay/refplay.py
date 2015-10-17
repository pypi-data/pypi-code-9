"""
Reflex Demo Parser
"""

import struct, mmap

class StructLoader(object):
    @classmethod
    def from_file(cls, f):
        data = list(struct.unpack(cls.STRUCT, f.read(struct.calcsize(cls.STRUCT))))

        # Cleanup null-terminated strings
        for index, char in enumerate([i for i in cls.STRUCT if not i.isdigit()]):
            if char == 's':
                data[index] = data[index].split('\x00')[0]

        return cls(f, *data)

class PlayerHeader(StructLoader):
    STRUCT = '32sii'

    def __init__(self, f, name, score, team):
        self.name = name
        self.score = score
        self.team = team

class DemoHeader(StructLoader):
    STRUCT = 'IIII64s256s256s'

    def __init__(self, f, tag, version, players, markers, gamemode, mapname, hostname):
        self.tag = tag
        self.version = version
        self.markers = markers
        self.gamemode = gamemode
        self.mapname = mapname
        self.hostname = hostname
        self.players = [PlayerHeader.from_file(f) for _ in range(players)]

def load_demo(name):
    with open(name, "r") as f:
        return DemoHeader.from_file(f)


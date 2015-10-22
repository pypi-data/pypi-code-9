import os
import random
import json
import re


def read_resource(filename):
    try:
        with open(filename) as f:
            ret = json.load(f)
            if isinstance(ret, dict):
                return ret
    except:
        pass
    return {}


def save_resource(rc, filename):
    with open(filename, 'w') as f:
        json.dump(rc, f)


def generate_port(rc):
    possible = set(range(1025, 65535)) - set(rc.values())
    if possible:
        return random.choice(list(possible))


def get_or_create_port(rc, name):
    if name not in rc:
        rc[name] = generate_port(rc)
        if rc[name] is None:
            raise RuntimeError('all ports are miraculously taken')
    return rc[name]

import os
import random
import re


def read_stripped_lines(filename):
    try:
        with open(filename) as f:
            for line in f:
                yield line.strip()
    except IOError:
        pass


def read_resource(filename):
    def read():
        for line in read_stripped_lines(filename):
            match = re.findall(r'export PLUT_([A-Z]+)=([0-9]+)', line)
            if match:
                service, port = match[0]
                yield service.lower(), int(port)

    return dict(read())


def save_resource(rc, filename):
    with open(filename, 'w') as f:
        for k, v in rc.iteritems():
            if k and v:
                f.write('export PLUT_%s=%d\n' % (k.upper(), int(v)))


def generate_port(rc):
    possible = set(range(1025, 65535)) - set(rc.values())
    if possible:
        return random.choice(list(possible))


def check_name(name):
    return all(ch.isalpha() for ch in name)


def get_or_create_port(rc, name):
    if name not in rc:
        rc[name] = generate_port(rc)
        if rc[name] is None:
            raise RuntimeError('all ports are miraculously taken')
    return rc[name]

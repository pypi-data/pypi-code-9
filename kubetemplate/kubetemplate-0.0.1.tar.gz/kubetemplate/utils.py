import os

import os
import yaml, json

class KubetemplateNotFound(Exception):
    pass
def root_path(p):
    d = os.getcwd()
    while True:
        if '.kubetemplate' in os.listdir(d):
            break
        elif os.path.realpath(d) == '/':
            raise KubetemplateNotFound('.kubetemplate file not found')
        d = os.path.dirname(d)

    return os.path.abspath(os.path.join(d, p))


def props():
    with open(root_path('.kubetemplate')) as f:
        return yaml.load(f)



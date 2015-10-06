from __future__ import absolute_import
from __future__ import unicode_literals
from future.standard_library import install_aliases
install_aliases()
import json
import os
import pypilist

def list():
    json_path = os.path.join(pypilist.__path__[0], 'packages.json')
    with open(json_path) as f:
        data = json.load(f)
    return data

def show():
    json_path = os.path.join(pypilist.__path__[0], 'packages.json')
    with open(json_path) as f:
        data = json.load(f)
    for i in data :
        print(i)

# template rendering helpers

import yaml
from base64 import b64encode
import subprocess, json

from kubetemplate import utils

def kube_secret(name, secrets):
    ob = \
    {
        "kind": "Secret",
        "apiVersion": "v1",
        "metadata": {
            "name": name
        },
        "data": {k: b64encode(v.encode('ascii')).decode('ascii') for k, v in secrets.items()}
    }
    return yaml.dump(ob)

def read_file(f):
    with open(utils.root_path(f)) as f:
        return f.read()

class KubeIPNotFound(Exception):
    pass
def kube_apiserver_ip():
    if props.get()['provider'] == 'vagrant':
        return '127.0.0.1:8080'
    elif props.get()['provider'] == 'gce':
        instances = subprocess.check_output('gcloud compute instances list --format json', shell=True)
        instances = json.loads(instances.decode('utf-8'))

        for i in instances:
            if i['name'] == props.get()['gce']['instance_name']:
                return i['networkInterfaces'][0]['accessConfigs'][0]['natIP'] + ':8080'

        raise KubeIPNotFound('GCE instance {} not found'.format(props.get()['gce']['instance_name']))

helpers = {}
for f in [utils.root_path, kube_secret, read_file, kube_apiserver_ip]:
    helpers[f.__name__] = f

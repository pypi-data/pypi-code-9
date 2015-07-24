import time, json
from common import api_get, api_post, api_delete
from ssh_key import list_all as list_ssh_keys


# list all droplets
def list_all():
    r = api_get('droplets?per_page=1000000', status_code = 200)
    return r.json()


# get droplet by name
def get_by_name(name):
    for droplet in list_all()['droplets']:
        if droplet['name'] == name:
            return droplet
    return None


# delete droplet by name
def delete_by_name(name):
    if name[:5] != 'temp.':
        return
    droplet = get_by_name(name)
    if not droplet:
        return
    api_delete('droplets/{0}'.format(droplet['id']), status_code = 204)


# get droplet by id
def get_by_id(droplet_id):
    r = api_get('droplets/{0}'.format(droplet_id), status_code = 200)
    return r.json()


# get a droplet's attribute
def get_attribute(id, attribute_str):
    droplet = get_by_id(id)
    dct = droplet['droplet']
    for token in attribute_str.split('.'):
        dct = dct[token]
    return dct


# create a new droplet
def create(name, region = 'nyc3'):
    payload = {
        "name":"temp.{0}".format(name),
        "region":region,
        "size":"512mb",
        "image":"docker",
        "ssh_keys": list_ssh_keys(),
        "backups": False,
        "ipv6": False,
        "user_data": None,
        "private_networking": None
    }
    r = api_post('droplets', data = json.dumps(payload), status_code = 202)
    droplet_id = r.json()['droplet']['id']
    status = 'new'
    while status != 'active':
        status = get_attribute(droplet_id, 'status')
        time.sleep(60)
    network = get_attribute(droplet_id, 'networks.v4')[0]
    ip_address = network['ip_address']
    return droplet_id, ip_address

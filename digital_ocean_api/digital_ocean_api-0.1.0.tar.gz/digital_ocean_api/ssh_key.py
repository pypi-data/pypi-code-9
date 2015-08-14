from common import api_get


# return all ssh key ids
def list_all():
    r = api_get('account/keys', status_code = 200)
    return [key['id'] for key in r.json()['ssh_keys']]

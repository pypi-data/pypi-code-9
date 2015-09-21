import requests


class PropertyDBClient(object):
    __INSERT_PROPERTY_GROUP_URL = '/%s/%s/property-group/'

    def __init__(self, property_db_url):
        self.property_db_url = property_db_url

    def insert_property_group(self, provenance, property_group_type, body):
        url = self.property_db_url + self.__INSERT_PROPERTY_GROUP_URL % (provenance, property_group_type)
        return self.__post_request(url, body)

    @staticmethod
    def __post_request(url, payload):
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, json=payload, headers=headers)
        return r.json()

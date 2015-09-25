import requests


class PropertyDBClient(object):
    __INSERT_PROPERTY_GROUP_URL = '/%s/%s/property-group/'
    __INSERT_PROPERTY_URL = '/property/'
    __INSERT_PROVENANCE_URL = '/provenance/'
    __INSERT_PROPERTY_GROUP_TYPE_URL = '/%s/property-group-type/'
    __INSERT_LINK_URL = '/link/'
    __DELETE_PROPERTY_GROUP_URL = '/%s/%s/property-group/%s'
    __QUERY_PROPERTY_GROUPS = '/query/%s/%s/%s'

    def __init__(self, property_db_url):
        self.property_db_url = property_db_url

    # -- query --
    def query(self, provenance, property_group_type, sirql_arguments=''):
        if sirql_arguments != '':
            sirql_arguments = '?' + sirql_arguments

        url = self.property_db_url + self.__QUERY_PROPERTY_GROUPS % (
            provenance,
            property_group_type,
            sirql_arguments)

        return self.__get_request(url)

    # -- delete --

    def delete_property_group(self, provenance, property_group_type,
                              sirql_arguments=''):
        if sirql_arguments != '':
            sirql_arguments = '?' + sirql_arguments

        url = self.property_db_url + self.__DELETE_PROPERTY_GROUP_URL % (
            provenance,
            property_group_type,
            sirql_arguments)
        return self.__delete_request(url)

    # -- inserts --

    def insert_property_groups(self, provenance, property_group_type,
                               property_groups):
        url = self.property_db_url + self.__INSERT_PROPERTY_GROUP_URL % (
            provenance, property_group_type)
        return self.__post_request(url, property_groups)

    def insert_properties(self, properties):
        url = self.property_db_url + self.__INSERT_PROPERTY_URL
        return self.__post_request(url, properties)

    def insert_provenances(self, provenance_list):
        url = self.property_db_url + self.__INSERT_PROVENANCE_URL
        return self.__post_request(url, provenance_list)

    def insert_property_group_types(self, provenance,
                                    property_group_type_list):
        url = self.property_db_url +\
              self.__INSERT_PROPERTY_GROUP_TYPE_URL % provenance
        return self.__post_request(url, property_group_type_list)

    def insert_links(self, link_list):
        url = self.property_db_url + self.__INSERT_LINK_URL
        return self.__post_request(url, link_list)

    # -- add --

    def add_provenance(self, name):
        return self.insert_provenances([name])

    def add_property_group_type(self, provenance_name, name):
        return self.insert_property_group_types(provenance_name, [name])

    def add_link(self, source, target, link_type, description):
        link = {'source': source,
                'target': target,
                'type': link_type,
                'description': description}
        return self.insert_links([link])

    @staticmethod
    def __post_request(url, payload):
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url, json=payload, headers=headers)
        return r.json()

    @staticmethod
    def __delete_request(url):
        r = requests.delete(url)
        return r.text

    @staticmethod
    def __get_request(url):
        r = requests.get(url)
        return r.json()

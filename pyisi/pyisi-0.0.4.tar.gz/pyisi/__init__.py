__author__ = 'jkingsbury'
import requests
import json

requests.packages.urllib3.disable_warnings()


class AuthenticationError(Exception):
    pass

class IsilonInterface:
    """
    Python interface for the Isilon API

    IsilonInterface.endpoints provides common URLs for different API endpoints

    """
    def __init__(self, hostname, username, password, port=8080, services=('platform', 'namespace'), https=True):
        self.username = username
        self.password = password
        self.services = services
        if https:
            method = 'https'
        else:
            method = 'http'

        self.ssl_verify = False

        self.url = "%s://%s:%s" % (method, hostname, port)

        self.headers = {"Content-Type": "application/json"}

    class endpoints:
        """
        Common endpoints for the API
        """
        session = '/session/1/session'
        nfs = '/platform/1/protocols/nfs/exports'
        smb = '/platform/1/protocols/smb/shares'
        namespace = '/namespace/'

    def session(self):
        """
        Get a session from the Isilon API
        The first return parameter is the session
        The second is the Response object from the auth request
        :return requests.Session
        :return requests.Response
        """

        s = requests.Session()

        r = s.post(url=self.url + self.endpoints.session,
                   headers=self.headers,
                   data=json.dumps({"username" : self.username,
                                    "password" : self.password,
                                    "services" : self.services}),
                   verify=self.ssl_verify)

        if r.status_code == 401:
            raise AuthenticationError("Not authorised")

        return s, r

    def get(self, endpoint, params={}):
        s, _ = self.session()
        r = s.get(url=self.url + endpoint, headers=self.headers, params=params, verify=self.ssl_verify)

        return r

    def head(self, endpoint, params={}):
        s, _ = self.session()
        r = s.head(url=self.url + endpoint, headers=self.headers, params=params, verify=self.ssl_verify)
        return r

    def put(self, endpoint, params={}):
        s, _ = self.session()
        r = s.put(url=self.url + endpoint, headers=self.headers, params=params, verify=self.ssl_verify)
        return r

    def post(self, endpoint, data={}):
        s, _ = self.session()
        r = s.post(url=self.url + endpoint, headers=self.headers, data=data, verify=self.ssl_verify)
        return r




class IsilonFileSystem:
    """
    This class provides an interface to the Isilon filesystem
    Requires an initialised object of an IsilonInterface type
    """
    def __init__(self, interface):
        self.interface = interface

    class acl_attributes:
        """
        Common attributes assigned to certain ACL types
        """
        read = ('dir_gen_read', 'dir_gen_execute')
        write = ('dir_gen_read', 'dir_gen_write', 'dir_gen_execute')
        all = ('dir_gen_all',)

    def listdir(self, directory):
        """
        List a given directory and return all children
        :param directory: Container on the Isilon filesystem
        :return: name of child
        """
        for c in self.interface.get(self.interface.endpoints.namespace + directory).get('children', []):
            yield c['name']

    def namespace(self, directory, params=''):
        return self.interface.get(self.interface.endpoints.namespace + directory + params)

    def metadata(self, directory):
        return self.namespace(directory, '?metadata')

    def acl(self, directory):
        return self.namespace(directory, '?acl')




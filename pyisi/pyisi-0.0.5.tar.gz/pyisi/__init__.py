import exceptions
import filesystem
from endpoint import endpoint
from request import APIRequest


class OneFS:
    """
    Isilon FileSystem API

    Requires a user with at least read abilities to the 'namespace' services
    """
    def __init__(self,
                 hostname,
                 username,
                 password,
                 port=8080,
                 services=('platform', 'namespace'),
                 https=True,
                 verify_ssl=False
                 ):
        """
        :param services: Tuple of platform, namespace or both
        :param https: Use https
        :param verify_ssl: Ignore SSL warnings
        """

        if https:
            method = 'https'
        else:
            method = 'http'
        url = "{}://{}:{}".format(method, hostname, port)
        self.request = APIRequest(base_url=url, verify_ssl=verify_ssl)
        self.request.create_session(username=username, password=password, services=services)

    def node(self, path):
        node_type = self.get_type(path)
        if node_type == 'container':
            return filesystem.FileSystemContainer(self.request, path)
        elif node_type == 'object':
            return filesystem.FileSystemObject(self.request, path)

    def create(self, path, f, overwrite=False, chmod=0600):
        """
        Create or overwrite an object on the filesystem
        :param path: path on filesystem
        :param f: file like object
        """
        self.request.put(uri=endpoint('namespace') + path,
                         params={"overwrite": overwrite},
                         data=f,
                         headers={'x-isi-ifs-target-type': 'object', 'x-isi-ifs-access-control': chmod})
        return filesystem.FileSystemObject(self.request, path)

    def get_type(self, path):
        return filesystem.FileSystemNode(self.request, path).type()
#
# class Permission:
#     def __init__(self, obj):
#         self.type = obj['permission_type']
#         self.permission = obj['permission']
#         self.trustee =
# class Share:
#     def __init__(self, obj):
#         self.path = FileSystemContainer(obj['path'])
#         self.permissions = [Permission(p) for p in obj['permissions']]
#

# class Platform:
#     def __init__(self, interface):
#         self.interface = interface
#
#     def get_quotas(self):
#         return self.interface.get(endpoint('quota')).json()['quotas']
#
#     def smb(self, name=None):
#         """
#         If name is not None then return a single shares, if not return a list of all shares.
#         :param name: share name
#         :return: list of shares
#         """
#         if name is not None:
#             return self.interface.get(endpoint('smb') + '/' + name).json()['shares'][0]
#         return self.interface.get(endpoint('smb')).json()['shares']
#
#     def nfs(self, id=None):
#         """
#         If id is not None then return a single export, if not return a list of all exports.
#         :param id: export id
#         :return: list of exports
#         """
#         if id is not None:
#             return self.interface.get(endpoint('nfs') + '/' + str(id)).json()['shares'][0]
#
#         return self.interface.get(endpoint('nfs')).json()['exports']

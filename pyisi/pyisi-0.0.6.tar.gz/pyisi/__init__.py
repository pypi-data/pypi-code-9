import exceptions
import filesystem
from endpoint import endpoint
from request import APIRequest
import exports


class OneFS:
    """
    The Isilon API for Python
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
        :param hostname
        :param username
        :param password
        :param port
        :param services: Tuple of platform, namespace or both
        :param https: Use https if true
        :param verify_ssl: Ignore SSL warnings if false
        """

        method = 'https' if https else 'http'

        url = "{}://{}:{}".format(method, hostname, port)
        self.request = APIRequest(base_url=url,
                                  username=username,
                                  password=password,
                                  services=services,
                                  verify_ssl=verify_ssl)

    def node(self, path):
        node_type = filesystem.FileSystemNode(self.request, path).type()
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

    def _network_export(self, capsule, api_endpoint, data_type, ne_id=None):
        """
        :param capsule: The Object to encapsulate each export
        :param api_endpoint: API endpoint for data_type
        :param data_type: Root key in API response
        :param ne_id: Export id or name
        :return:
        """
        if ne_id is not None:
            e = self.request.get(api_endpoint + '/' + ne_id).json()[data_type]
            if len(e) == 0:
                raise exceptions.AEC_NOT_FOUND('Network export type {}: {} not found'.format(data_type, e))
            return capsule(self.request, data=e[0])
        else:
            e = self.request.get(api_endpoint).json()[data_type]
            return [capsule(self.request, data=s) for s in e]

    def quota(self, quota_id=None):
        return self._network_export(exports.Quota, endpoint('quota'), 'quotas', quota_id)

    def smb(self, share_name=None):
        return self._network_export(exports.Share, endpoint('smb'), 'shares', share_name)

    def nfs(self, export_id=None):
        return self._network_export(exports.Export, endpoint('nfs'), 'exports', export_id)



from endpoint import endpoint
import exceptions


class FileSystemNode(object):
    def __init__(self, request, path=None):
        """
        :type request: pyisi.request.APIRequest
        :type path: str
        """
        self.path = path
        self.namespace_uri = self._get_namespace_uri(path)
        self.request = request

    def __str__(self):
        return self.path

    def _resp(self, mode='', params=[], stream=False):
        """
        GET a requests.Response object for the node
        :param mode:
        :param params:
        :param stream:
        :return: requests.Response
        """
        return self.request.get('{}?{}'.format(self.namespace_uri, mode), params=params, stream=stream)

    @staticmethod
    def _get_namespace_uri(path):
            if path.endswith('/'):
                path = path[:-1]
            return endpoint('namespace') + path

    def attributes(self):
        """
        Make a HEAD request for this node and return the HTTP headers
        The Isilon API uses HTTP headers to display attributes of a node
        They are in the format of:
            x-isi-ifs-*

        This requires read access to the directory

        :return: requests.Response.headers
        """
        return self.request.head(self.namespace_uri).headers

    def type(self):
        """
        Get the node type
        :return: 'container' | 'object'
        """
        return self.attributes().get('x-isi-ifs-target-type')

    def acl(self):
        return self._resp(mode='acl').json()

    def metadata(self):
        """
        Make a GET request for this node, return all metadata attributes
        Does not require read access like attributes() does.

        Note that this dict may not always have the same keys

        :return: dict of all metadata attributes
        """
        attrs = {}
        for attr in self._resp(mode='metadata').json().get('attrs', []):
            attrs.update({attr['name']: attr['value']})
        return attrs

    def size(self):
        return self.attributes().get('content-length')

    def raise_incorrect_type(self, exc_type):
        raise exceptions.INVALID_TYPE('{} is not a {}'.format(self.path, exc_type))


class FileSystemContainer(FileSystemNode):
    def __init__(self, request, path):
        FileSystemNode.__init__(self, request, path)

    def children(self):
        """
        Get all children for a container, return a generator of children
        If the child is an object then yield a FileSystemObject()
        If the child is a container then yield a FileSystemContainer()
        """
        for c in self._resp().json().get('children', []):
            path = '{}/{}'.format(self.path, c['name'])
            target_type = FileSystemNode(self.request, path).type()
            if target_type == 'container':
                    yield FileSystemContainer(self.request, path)
            elif target_type == 'object':
                yield FileSystemObject(self.request, path)

    def objects(self, recurse=False):
        for c in self.children():
            if type(c) is FileSystemObject:
                yield c
            elif type(c) is FileSystemContainer:
                if recurse:
                    for s_c in c.objects(True):
                        yield s_c

    def containers(self, recurse=False):
        for c in self.children():
            if type(c) is FileSystemContainer:
                yield c
                if recurse:
                    for s_c in c.containers(True):
                        yield s_c


class FileSystemObject(FileSystemNode):
    def __init__(self, request, path):
        FileSystemNode.__init__(self, request, path)

    def stream(self, f, chunk_size=1024):
        """
        Stream the resp of the object into a file object
        :param f: File object to write() to
        :param chunk_size: Size of chunk to write in bytes
        """
        resp = self._resp(stream=True)
        for c in resp.iter_content(chunk_size):
            if c:
                f.write(c)

    def content(self):
        """
        Similar to stream except the content is loaded into memory and returned as a string
        :return: content of object
        """
        return self._resp().content

    def delete(self):
        self.request.delete(self.namespace_uri)

import subprocess
from lxml import etree

from xpcs.exc import *


def to_object(thing, **kwargs):
    if thing.tag == 'resource':
        return Resource(thing, **kwargs)
    elif thing.tag == 'clone':
        return Clone(thing, **kwargs)
    elif thing.tag == 'group':
        return Group(thing, **kwargs)
    else:
        raise ValueError(thing.tag)


class BasicResource(dict):
    def __init__(self, ele, parent=None):
        self.parent = parent
        self.ele = ele
        self._nodes = ele.findall('node')
        super(BasicResource, self).__init__(ele.items())

    @property
    def nodes(self):
        return (Node(node) for node in self._nodes)


class ResourceContainer(BasicResource):
    def __init__(self, *args, **kwargs):
        super(ResourceContainer, self).__init__(*args, **kwargs)
        self._resources = self.ele.findall('resource')

    @property
    def resources(self):
        return (to_object(rsc, parent=self)
                for rsc in self._resources)

    def __iter__(self):
        return self.resources

    def get_active(self):
        return ('true' if not any(rsc['active'] != 'true'
                                  for rsc in self.resources)
                else 'false')

    def get_managed(self):
        return ('true' if not any(rsc['managed'] != 'true'
                                  for rsc in self.resources)
                else 'false')

    def get_started(self):
        return ('true' if not any(rsc['role'] != 'Started'
                                  for rsc in self.resources)
                else 'false')

    def get_stopped(self):
        return ('true' if not any(rsc['role'] != 'Stopped'
                                  for rsc in self.resources)
                else 'false')

    def get_failed(self):
        return ('true' if any(rsc['failed'] == 'true'
                              for rsc in self.resources)
                else 'false')

    def get_role(self):
        r = self.resources
        first = r.next()
        if all(first['role'] == rest['role'] for rest in r):
            return first['role']
        else:
            return 'Unknown'

    def __getitem__(self, k):
        try:
            return getattr(self, 'get_%s' % k)()
        except AttributeError:
            return super(ResourceContainer, self).__getitem__(k)


class Clone(ResourceContainer):
    pass


class Group(ResourceContainer):
    pass


class Resource(BasicResource):
    pass


class Node(dict):
    def __init__(self, node):
        super(Node, self).__init__(node.items())


class PCS(object):
    def __init__(self, statusfile=None):
        self._status = None
        self._status_file = None

        if statusfile is not None:
            if hasattr(statusfile, 'read'):
                self._status = statusfile.read()
            else:
                self._status_file = statusfile

    @property
    def status(self):
        if self._status:
            status = self._status
        elif self._status_file:
            with open(self._status_file) as fd:
                status = fd.read()
        else:
            status = subprocess.check_output(
                ['pcs', 'status', 'xml'])

        return etree.fromstring(status)

    @property
    def resources(self):
        return (to_object(x) for x in
                self.status.xpath('/crm_mon/resources/*'))

    @property
    def nodes(self):
        return (Node(x) for x in
                self.status.xpath('/crm_mon/nodes/node'))

    def resource(self, name):
        rsc = self.status.xpath(
            '/crm_mon/resources/*[@id="%s"]' % name)
        if not len(rsc):
            raise ResourceNotFound(name)

        return to_object(rsc[0])

    def node(self, name):
        node = self.status.xpath(
            '/crm_mon/nodes/node[@name="%s"]' % name)
        if not len(node):
            raise NodeNotFound(name)

        return Node(node[0])

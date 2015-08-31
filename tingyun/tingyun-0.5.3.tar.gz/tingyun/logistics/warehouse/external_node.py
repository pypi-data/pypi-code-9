
"""

"""

from collections import namedtuple
from tingyun.logistics.attribution import TimeMetric, node_start_time, node_end_time

_ExternalNode = namedtuple('_ExternalNode', ['library', 'url', 'children', 'start_time', 'end_time',
                                             'duration', 'exclusive'])


class ExternalNode(_ExternalNode):
    """

    """
    def time_metrics(self, root, parent):
        """
        :param root: the top node of the tracker
        :param parent: parent node.
        :return:
        """
        name = 'GENERAL/External/NULL/All'
        yield TimeMetric(name=name, scope=root.path, duration=self.duration, exclusive=self.exclusive)

        name = "GENERAL/External/NULL/AllWeb"
        yield TimeMetric(name=name, scope=root.path, duration=self.duration, exclusive=self.exclusive)

        name = 'External/%s/%s' % (self.url.replace("/", "%2F"), root.name)
        yield TimeMetric(name=name, scope=root.path, duration=self.duration, exclusive=self.exclusive)

        name = 'GENERAL/External/%s/%s' % (self.url.replace("/", "%2F"), root.name)
        yield TimeMetric(name=name, scope=root.path, duration=self.duration, exclusive=self.exclusive)

    def trace_node(self, root):
        """
        :param root: the root node of the tracker
        :return:
        """
        params = {}
        children = []
        call_count = 1
        class_name = ""
        method_name = root.name
        call_url = ""
        root.trace_node_count += 1
        start_time = node_start_time(root, self)
        end_time = node_end_time(root, self)
        metric_name = 'External/%s/%s' % (self.url.replace("/", "%2F"), root.name)

        return [start_time, end_time, metric_name, call_url, call_count, class_name, method_name, params, children]

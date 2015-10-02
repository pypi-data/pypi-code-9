# pylint: disable=E0611
""" Module for printout out linux device neighbors
"""
from netshow.linux.netjson_encoder import NetEncoder
from netshow.linux import print_iface
import netshowlib.linux.cache as linux_cache
from collections import OrderedDict
import json
from tabulate import tabulate
from netshow.linux.common import _, legend_wrapped_cli_output


class ShowNeighbors(object):
    """
    Class responsible for printing out basic linux device neighbor info
    """
    def __init__(self, cl):
        self.use_json = cl.get('--json') or cl.get('-j')
        self.ifacelist = OrderedDict()
        self.cache = linux_cache
        self.print_iface = print_iface
        self.show_legend = False
        if cl.get('-l') or cl.get('--legend'):
            self.show_legend = True

    def run(self):
        """
        :return: basic neighbor information based on data obtained on netshow-lib
        """
        feature_cache = self.cache.Cache()
        feature_cache.run()
        for _ifacename in sorted(feature_cache.lldp.keys()):
            self.ifacelist[_ifacename] = self.print_iface.iface(_ifacename, feature_cache)

        if self.use_json:
            return json.dumps(self.ifacelist,
                              cls=NetEncoder, indent=4)

        return self.print_neighbor_info()

    def print_neighbor_info(self):
        """
        :return: cli output of netshow neighbor
        """
        _header = [_('local'), _('speed'), _('mode'), '',
                   _('remote'), _('sw/hostname'), _('summary')]
        _table = []
        for _iface in self.ifacelist.values():
            _table.append([_iface.name, _iface.speed,
                           _iface.port_category,
                           '====',
                           _iface.iface.lldp[0].get('adj_port'),
                           _iface.iface.lldp[0].get('adj_hostname'),
                           ', '.join(_iface.summary)])
            del _iface.iface.lldp[0]
            if _iface.iface.lldp:
                for _entry in _iface.iface.lldp:
                    _table.append(['', '', '', '====',
                                   _entry.get('adj_port'),
                                   _entry.get('adj_hostname')])

        return legend_wrapped_cli_output(tabulate(_table, _header), self.show_legend)

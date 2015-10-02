""" Linux ip neighbor module.

IP neighbor relationships in IPv4 are handled by Address Resolution Protocol
In IPv6 this process is just known as IP neighbor discovery.

"""
import io
import netshowlib.linux.common as common


def cacheinfo():
    """
    :return hash of of :class:`IpNeighbor` info by parsing ``ip neighbor show`` output.
    """
    # return empty ip neighbor dict
    ip_dict = {}
    for _iptype in ['4', '6']:
        try:
            _table = common.exec_command("/sbin/ip -%s neighbor show" % (_iptype))
            parse_info(table=_table,
                       iptype="ipv%s" % (_iptype),
                       ip_neigh_dict=ip_dict)
        except common.ExecCommandException:
            continue
    return ip_dict


def parse_info(table, iptype, ip_neigh_dict):
    """
    parse ip neighbor information from either ipv4 or ipv6

    :params command: can be ``ip neigh show`` or ``ip -6 neigh show``
    :params iptype: can be ``ipv4`` or ``ipv6``
    :params ip_neigh_dict: dict to update neighbor table
    """
    fileio = io.StringIO(table)
    for line in fileio:
        if len(line.strip()) <= 0:
            continue
        ip_neigh_arr = line.split()
        if ip_neigh_arr[-1] == 'REACHABLE':
            _ip = ip_neigh_arr[0]
            ifacename = ip_neigh_arr[2]
            _mac = ip_neigh_arr[4]
            try:
                _instance = ip_neigh_dict[ifacename]
            except KeyError:
                _instance = {'ipv4': {},
                             'ipv6': {}}
                ip_neigh_dict[ifacename] = _instance

            _instance[iptype][_ip] = {'mac': _mac}


class IpNeighbor(object):
    """ Linux IP neighbor attributes

    * **name**: name of interface
    * **cache**: pointer to :class:`netshowlib.linux.cache.Cache` instance
    * **ipv4**: ipv4 neighbor entries
    * **ipv6**: ipv6 neighbor entries
    """
    def __init__(self, name, cache=None):
        if cache:
            self._cache = cache.ip_neighbor
        else:
            self._cache = None
        self.ipv4 = {}
        self.ipv6 = {}
        self._all_neighbors = {}
        self.name = name

    def run(self):
        """
        This function checks the cache for ip neighbor information
        If it is not there, it grabs this info from the
        system and populates the necessary attributes
        """
        if not self._cache:
            self._cache = cacheinfo()
        if self._cache.get(self.name):
            self.ipv4 = self._cache.get(self.name).get('ipv4')
            self.ipv6 = self._cache.get(self.name).get('ipv6')
            self._all_neighbors = self.ipv4.copy()
            self._all_neighbors.update(self.ipv6)

    @property
    def allentries(self):
        """
        :return: a list of all ip neighbors ipv4 + ipv6
        """
        if not self._all_neighbors:
            self.run()

        return self._all_neighbors

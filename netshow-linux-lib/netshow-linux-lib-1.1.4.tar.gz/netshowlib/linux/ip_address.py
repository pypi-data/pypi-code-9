# http://pylint-messages.wikidot.com/all-codes
# pylint: disable=R0903
"""
This module is responsible for getting IP address (ipv4 and ipv6) information
from a linux system. It currently has one provider, i.e information from the
`ip addr show` output
"""
import io
import netshowlib.linux.common as common
import re


def parse_ip_cache(fileio):
    """
    text scrapes  `ip addr show` info to get ipv4 and
    ipv6 info from each interface

    :return: has of ip addresses with iface names as keys
    """
    ip_cache = {}
    scope = None
    for line in fileio:
        if len(line.strip()) <= 0 or re.search(r'\s+mtu\s+', line):
            continue
        # determine interface name
        split_line = line.split()
        # account for interfaces that have '<X@Y' like subints
        foundname = split_line[1].split('@')[0]
        inet_type = split_line[2]
        ip_addr = split_line[3]
        for _pos in range(4, len(split_line)):
            if split_line[_pos] == 'scope':
                scope = split_line[_pos+1]
                break
        if foundname not in ip_cache.keys():
            ip_cache[foundname] = {'ipv4': [], 'ipv6': []}
        if scope == 'global' or scope == 'host':
            if inet_type == 'inet':
                ip_cache.get(foundname)['ipv4'].append(ip_addr)
            elif inet_type == 'inet6':
                ip_cache.get(foundname)['ipv6'].append(ip_addr)
    return ip_cache


def cacheinfo():
    """
    Cacheinfo function for IP addresses. Collects all IP addresses \
    from the system and in the return hash assigns IP addresses \
    to particular interfaces
    :return: hash of ip addresses with iface names as keys.
    """
    cmd = '/sbin/ip -o addr show'
    try:
        ipaddr_output = common.exec_command(cmd)
    except:
        return {}
    # stringIO in python3 returns byte string, to be python2.x compatible
    # with common.exec_command decode byte string to regular string
    _fileio = io.StringIO(ipaddr_output)

    return parse_ip_cache(_fileio)


class IpAddress(object):
    """ Ipaddr class attributes

    * **ipv4**: list of IPv4 addresses in CIDR format
    * **ipv6**: list of IPv6 addresses in CIDR format
    * **cache**: cache of all IP addresses
    * **all_ips**: Concatenation of ipv4 and ipv6 addresses

    """

    def __init__(self, name, cache=None):
        self.ipv4 = []
        """ list of IPv4 addresses in CIDR format """
        self.ipv6 = []
        """ list of IPv6 addresses in CIDR format """
        self.name = name
        if cache:
            self._cache = cache.ip_address
        else:
            self._cache = None

    @property
    def allentries(self):
        """
        :return: list of all IPs found both ipv6 and ipv4
        """
        self.run()
        return self.ipv4 + self.ipv6

    def run(self):
        """
        Run function for this feature. If cache is present, gets \
        IP info it. if, not will collect it individually
        """
        if not self._cache:
            self._cache = cacheinfo()

        ip_cache = self._cache.get(self.name)
        if ip_cache:
            self.ipv4 = ip_cache.get('ipv4')
            self.ipv6 = ip_cache.get('ipv6')

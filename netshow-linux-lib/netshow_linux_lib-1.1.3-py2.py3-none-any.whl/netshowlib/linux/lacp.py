"""
This module contains the Lacp Class responsible for methods
and attributes regarding Lacp support on Bond interfaces
"""

import netshowlib.linux.common as common


class Lacp(object):
    """ Lacp class attributes

    * **sys_priority**: LACP system priority. Used in conjunction with the \
        system mac of a bond to create a system Ia
    * **rate**: LACP rate/timeout.
    * **partner_mac**: LACP partner mac. Collected but not used. May be useful \
        in the future

    """
    def __init__(self, name):
        self.name = name
        self._sys_priority = None
        self._rate = None
        self._partner_mac = None
        self.common = common

    @property
    def rate(self):
        """
        :return: lacp rate/timeout. Can be slow(0) or fast(1)
        """
        self._rate = None
        fileoutput = self.common.read_from_sys(
            'bonding/lacp_rate', self.name)
        if fileoutput:
            self._rate = fileoutput.split()[1]
        return self._rate

    @property
    def sys_priority(self):
        """
        :return: lacp system priority
        """
        self._sys_priority = self.common.read_from_sys(
            'bonding/ad_sys_priority', self.name)
        return self._sys_priority

    @property
    def partner_mac(self):
        """
        :return:  bond partner mac
        """
        self._partner_mac = self.common.read_from_sys(
            'bonding/ad_partner_mac', self.name)
        return self._partner_mac

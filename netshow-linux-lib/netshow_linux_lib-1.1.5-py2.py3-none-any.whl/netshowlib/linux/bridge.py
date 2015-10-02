# pylint: disable=R0903
""" This module is responsible for finding properties
related to linux bridge and bridge member interfaces """
import netshowlib.linux.iface as linux_iface
import os
from collections import OrderedDict

# store cache of bridge instances
# used by KernelStpBridgeMember method.
BRIDGE_CACHE = {}


def update_stp_state(stp_hash, iface_to_add, iface_under_test):
    """
    Updates stp state dict from BridgeMember and Bridge
    """
    bridge_state = iface_under_test.stp_state()
    if bridge_state == '0':
        stp_hash.get('stp_disabled').append(iface_to_add)
        return

    iface_stp_state = iface_under_test.read_from_sys('brport/state')
    if iface_stp_state == '0':
        stp_hash.get('disabled').append(iface_to_add)
    elif iface_stp_state == '1' or iface_stp_state == '2':
        stp_hash.get('intransition').append(iface_to_add)
    elif iface_stp_state == '3':
        stp_hash.get('forwarding').append(iface_to_add)
    elif iface_stp_state == '4':
        stp_hash.get('blocking').append(iface_to_add)
    root_port_id = iface_under_test.read_from_sys(
        'brport/bridge/bridge/root_port')
    port_id = iface_under_test.read_from_sys('brport/port_id')
    if root_port_id == port_id and iface_stp_state != '0':
        stp_hash.get('root').append(iface_to_add)


# ======================================================================= #

class KernelStpBridge(object):
    """ Attributes for STP for a bridge

    * **bridge**: instance of :class:`Bridge`
    * **member_state**: return hash of basic stp attributes of \
    bridge members. Example

    .. code-block:: python

       iface = linux.bridge.Bridge('eth2')
       iface.stp.state
       >> { 'stp_disabled': [list of bridge member instances]
            'forwarding': [list of bridge member instances ]
            'blocking': [list of bridge member instances ]
            'intransition': [ list of bridge member instances ]
            'disabled': [list of bridge member instances]
            'root': [list of bridge member instances. should only be one]
          }

    * **root_priority**: root priority for the spanning tree domain
    * **bridge_priority**: bridge priority


    """

    def __init__(self, bridge):
        self.bridge = bridge
        self._root_priority = None
        self._bridge_priority = None
        self._initialize_state()

    def _initialize_state(self):
        """ initialize state """
        self._member_state = OrderedDict([
            ('root', []),
            ('forwarding', []),
            ('blocking', []),
            ('disabled', []),
            ('intransition', [])])

    def is_root(self):
        """
        :return: True if bridge is STP root.
        """
        _root_id = self.bridge.read_from_sys('bridge/root_id')
        _bridge_id = self.bridge.read_from_sys('bridge/bridge_id')
        if _root_id == _bridge_id:
            return True
        return False

    @property
    def root_priority(self):
        """
        :return: return root priority number
        """
        _priority = self.bridge.read_from_sys('bridge/root_id')
        if _priority:
            self._root_priority = str(int(_priority.split('.')[0], 16))
        return self._root_priority

    @property
    def bridge_priority(self):
        """
        :return: return bridge priority number
        """
        _priority = self.bridge.read_from_sys('bridge/bridge_id')
        if _priority:
            self._bridge_priority = str(int(_priority.split('.')[0], 16))

        return self._bridge_priority

    @property
    def member_state(self):
        """
        :return: dict of stp state of bridge members
        """
        self._initialize_state()
        # go through tagged members first
        for _ifacename, _iface in self.bridge.tagged_members.items():
            subiface = _iface.__class__(_ifacename)
            update_stp_state(self._member_state, _iface, subiface)

        for _ifacename, _iface in self.bridge.untagged_members.items():
            update_stp_state(self._member_state, _iface, _iface)

        return self._member_state

# ======================================================================= #


class KernelStpBridgeMember(object):
    """ Attributes for Bridgemems using the Kernel STP

    * **bridgemem**: instance of :class:`BridgeMember`
    * **state**: return hash of basic stp attributes of the port. Example

    .. code-block:: python

       iface = linux.bridge.BridgeMember('eth2')
       iface.stp.state
       >> { 'forwarding': [list of bridge instances ]
            'blocking': [list of bridge instances ]
            'intransition': [ list of bridge instances ]
            'disabled': [list of bridge instances]
            'root': [list of bridges instances with root ports ]
            'stp_disabled': [ list of bridge instances where stp is disabled]
          }

    * **cache**: feature cache that is used
    """

    def __init__(self, bridgemem, cache=None):
        self.bridgemem = bridgemem
        self._cache = cache
        self._initialize_state()

    def _initialize_state(self):
        """ initialize state """
        self._state = OrderedDict([
            ('root', []),
            ('forwarding', []),
            ('blocking', []),
            ('intransition', []),
            ('disabled', []),
            ('stp_disabled', [])])

    @property
    def state(self):
        """
        :return: dict of stp states with associated \
            :class:`linux.bridge<Bridge>` instances
        """
        self._initialize_state()
        # go through list of subints look for bridge members
        # understand stp config for that interface and update
        # _state dict.
        bridgename = self.bridgemem.read_symlink('brport/bridge')
        if bridgename:
            if BRIDGE_CACHE.get(bridgename):
                bridgeiface = BRIDGE_CACHE.get(bridgename)
            else:
                bridgeiface = Bridge(bridgename, cache=self._cache)
            update_stp_state(self._state, bridgeiface, self.bridgemem)

        for subintname in self.bridgemem.get_sub_interfaces():
            subiface = linux_iface.Iface(subintname)
            bridgename = subiface.read_symlink('brport/bridge')
            if bridgename:
                if BRIDGE_CACHE.get(bridgename):
                    bridgeiface = BRIDGE_CACHE.get(bridgename)
                else:
                    bridgeiface = Bridge(bridgename, cache=self._cache)
                update_stp_state(self._state, bridgeiface, subiface)
        return self._state

# ======================================================================= #


class BridgeMember(linux_iface.Iface):
    """ Linux Bridge Member attributes

    * **cache**: feature cache
    * **stp**: pointer to :class:`KernelStpBridgeMember` instance

    """
    def __init__(self, name, cache=None):
        linux_iface.Iface.__init__(self, name, cache)
        self._stp = None
        self._cache = cache
        self._bridge_masters = {}
        self.iface_mod = linux_iface
        self.bridge_class = Bridge

    @property
    def stp(self):
        """
        :return: instance of KernelStpBridgeMember
        """
        if not self._stp:
            self._stp = KernelStpBridgeMember(self, self._cache)
        return self._stp

    @property
    def bridge_masters(self):
        """
        :return: list of bridges associated with this port \
            and its subinterfaces.
        """
        self._bridge_masters = {}
        bridgename = self.read_symlink('brport/bridge')
        if bridgename:
            if BRIDGE_CACHE.get(bridgename):
                bridgeiface = BRIDGE_CACHE.get(bridgename)
            else:
                bridgeiface = self.bridge_class(bridgename, cache=self._cache)
            self._bridge_masters[bridgeiface.name] = bridgeiface

        for subintname in self.get_sub_interfaces():
            subiface = self.iface_mod.Iface(subintname)
            bridgename = subiface.read_symlink('brport/bridge')
            if bridgename:
                if BRIDGE_CACHE.get(bridgename):
                    bridgeiface = BRIDGE_CACHE.get(bridgename)
                else:
                    bridgeiface = self.bridge_class(bridgename, cache=self._cache)
                self._bridge_masters[bridgeiface.name] = bridgeiface

        return self._bridge_masters


# ======================================================================= #


class Bridge(linux_iface.Iface):
    """ Linux Bridge interface attributes

    * **tagged_members**: list of tagged bridge members *(part of a trunk)*
    * **untagged_members**: list of untagged bridge members *(access)*
    * **members**: all bridge members
    * **vlan_tag**: vlan ID tag if applicable. empty string means no tag.
    * **stp**: pointer to :class:`KernelStpBridge` instance.
    If set to ``None``, \
    then bridge has STP disabled.
    """

    def __init__(self, name, cache=None):
        linux_iface.Iface.__init__(self, name, cache)
        self._tagged_members = {}
        self._untagged_members = {}
        self._members = {}
        self._memberlist = {}
        self._vlan_tag = ''
        self._stp = None

    # -----------------
    def _memberlist_str(self):
        """
        :return: list of bridge member names. both tagged and untagged
        """
        dirlist = []
        try:
            dirlist = os.listdir(self.sys_path('brif'))
        except OSError:
            pass
        return dirlist

    def _get_members(self, bridgemem=BridgeMember):
        """
        :return: get the members of a bridge into the tagged ,
        untagged and total \
            member names and number structures
        """
        member_list_from_kernel = self._memberlist_str()
        if set(member_list_from_kernel) == set(self._memberlist):
            return

        self._memberlist = member_list_from_kernel

        self._members = {}
        self._tagged_members = {}
        self._untagged_members = {}

        for _name in self._memberlist:
            # take the name of the main physical or logical interface
            # not the subinterface
            membername_arr = _name.split('.')
            bdgmem = bridgemem(membername_arr[0],
                               cache=self._cache)
            if len(membername_arr) == 2:
                self._tagged_members[_name] = bdgmem
            else:
                self._untagged_members[_name] = bdgmem
            self._members[_name] = bdgmem

    # ---------------------------
    @property
    def stp(self):
        """
        :return: ``None`` if STP is disabled
        :return: :class:`KernelStpBridge` instance if STP is enabled
        """
        if self.read_from_sys('bridge/stp_state') == '0':
            return None
        else:
            if not self._stp:
                self._stp = KernelStpBridge(self)
            return self._stp

    @property
    def members(self):
        """
        :return: list of bridge port members
        """
        self._get_members(BridgeMember)
        return self._members

    @property
    def tagged_members(self):
        """
        *Works for default/classic linux bridge driver*

        :return: list of tagged bridge members.
        """
        self._get_members()
        return self._tagged_members

    @property
    def untagged_members(self):
        """
        *Works for default/classic linux bridge driver*

        :return: list of untagged bridge members
        """
        self._get_members()
        return self._untagged_members

    @property
    def vlan_tag(self):
        """
        For the classic/default bridge driver, if a tagged bridge member \
        is provided then the function will use the tag as the vlan id

        :return: vlan ID if applicable. If multiple tags found,
        possibly indicating \
            vlan translation, then all tags are printed as a list \
            Empty array means no tag
        """

        # this may print something like '100,400', meaning that this bridge
        # is doing vlan translation. If string is empty('') then no tag is found
        # ----------------------
        # the messy looking function below is doing the following:
        # take a list of members ['eth1.100', 'eth2', 'eth3.100'],
        # remove all untagged iface
        # take list of tagged members for example [ eth1.100', 'eth3.100']
        # strip off tag with list comprehension &
        # put in array so it is ['100',100']
        # apply set() to the array so it removes all non-unique values. becomes
        # set([100])
        # then convert back to a list
        # then sorts it, uses the sorted([list] key=int)
        # apply str.join function on list.
        # on an empty tagged_member output it will produce ''
        # -----------------------------------
        self._vlan_tag = sorted(list(set(
            [x.split('.')[1] for x in self._memberlist_str()
             if len(x.split('.')) > 1])), key=int)
        return self._vlan_tag

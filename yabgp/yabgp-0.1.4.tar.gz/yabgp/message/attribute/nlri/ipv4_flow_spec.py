# Copyright 2015 Cisco Systems, Inc.
# All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""IPv4 Flowspec NLRI
"""
import struct

from yabgp.common import constants as bgp_cons


class IPv4FlowSpec(object):

    @classmethod
    def parse(cls, value):
        """
        parse IPv4 flowspec NLRI
        :param value:
        :return:
        """
        # +------------------------------+
        # |    length (0xnn or 0xfn nn)  |
        # +------------------------------+
        # |    NLRI value  (variable)    |
        # +------------------------------+
        while value:
            offset = 0
            flowspec_type = struct.unpack('!B', value[0])[0]
            offset += 1
            # decode all kinds of flow spec
            if flowspec_type in [bgp_cons.BGPNLRI_FSPEC_DST_PFIX, bgp_cons.BGPNLRI_FSPEC_SRC_PFIX]:
                pass
                # prefix, offset_tmp = self.parse_prefix(nlri_data[1:])
                # offset += offset_tmp
                # nlri_list.append({flowspec_type: prefix})
                # nlri_data = nlri_data[offset:]
        pass

    @classmethod
    def construct(cls, value):
        pass

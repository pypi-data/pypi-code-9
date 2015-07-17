try:
    # python3
    from xmlrpc.client import DateTime
except ImportError:
    # python2
    from xmlrpclib import DateTime


def image_list(options):

    ret = [{'author_id': 248842,
            'datacenter_id': 3,
            'date_created': DateTime('20130902T15:04:18'),
            'date_updated': DateTime('20130903T12:14:30'),
            'disk_id': 527489,
            'id': 131,
            'kernel_version': '3.2-i386',
            'label': 'Fedora 17 32 bits',
            'os_arch': 'x86-32',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 3,
            'date_created': DateTime('20130902T15:04:18'),
            'date_updated': DateTime('20130903T12:14:30'),
            'disk_id': 527490,
            'id': 132,
            'kernel_version': '3.2-x86_64',
            'label': 'Fedora 17 64 bits',
            'os_arch': 'x86-64',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 3,
            'date_created': DateTime('20130902T15:04:18'),
            'date_updated': DateTime('20130903T12:14:30'),
            'disk_id': 527491,
            'id': 133,
            'kernel_version': '3.2-i386',
            'label': 'OpenSUSE 12.2 32 bits',
            'os_arch': 'x86-32',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 3,
            'date_created': DateTime('20130902T15:04:18'),
            'date_updated': DateTime('20130903T12:14:30'),
            'disk_id': 527494,
            'id': 134,
            'kernel_version': '3.2-x86_64',
            'label': 'OpenSUSE 12.2 64 bits',
            'os_arch': 'x86-64',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 3,
            'date_created': DateTime('20130902T15:04:18'),
            'date_updated': DateTime('20130903T12:14:30'),
            'disk_id': 726224,
            'id': 149,
            'kernel_version': '2.6.32',
            'label': 'CentOS 5 32 bits',
            'os_arch': 'x86-32',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 3,
            'date_created': DateTime('20130902T15:04:18'),
            'date_updated': DateTime('20130903T12:14:30'),
            'disk_id': 726225,
            'id': 150,
            'kernel_version': '2.6.32-x86_64',
            'label': 'CentOS 5 64 bits',
            'os_arch': 'x86-64',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 3,
            'date_created': DateTime('20130902T15:04:18'),
            'date_updated': DateTime('20130903T12:14:30'),
            'disk_id': 726230,
            'id': 151,
            'kernel_version': '3.2-i386',
            'label': 'ArchLinux 32 bits',
            'os_arch': 'x86-32',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 3,
            'date_created': DateTime('20130902T15:04:18'),
            'date_updated': DateTime('20130903T12:14:30'),
            'disk_id': 726233,
            'id': 152,
            'kernel_version': '3.2-x86_64',
            'label': 'ArchLinux 64 bits',
            'os_arch': 'x86-64',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 2,
            'date_created': DateTime('20140417T18:38:53'),
            'date_updated': DateTime('20141030T10:38:45'),
            'disk_id': 1401491,
            'id': 161,
            'kernel_version': '3.12-x86_64 (hvm)',
            'label': 'Debian 7 64 bits (HVM)',
            'os_arch': 'x86-64',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 1,
            'date_created': DateTime('20140417T18:38:53'),
            'date_updated': DateTime('20141030T18:06:44'),
            'disk_id': 1349810,
            'id': 162,
            'kernel_version': '3.12-x86_64 (hvm)',
            'label': 'Debian 7 64 bits (HVM)',
            'os_arch': 'x86-64',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 3,
            'date_created': DateTime('20140417T18:38:53'),
            'date_updated': DateTime('20141030T10:38:45'),
            'disk_id': 1401327,
            'id': 167,
            'kernel_version': '3.12-x86_64 (hvm)',
            'label': 'Debian 7 64 bits (HVM)',
            'os_arch': 'x86-64',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 1,
            'date_created': DateTime('20141203T14:15:28'),
            'date_updated': DateTime('20150116T11:24:56'),
            'disk_id': 3315704,
            'id': 172,
            'kernel_version': '3.12-x86_64 (hvm)',
            'label': 'Debian 8 (testing) 64 bits (HVM)',
            'os_arch': 'x86-64',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 2,
            'date_created': DateTime('20141203T14:15:28'),
            'date_updated': DateTime('20150116T11:24:56'),
            'disk_id': 3315992,
            'id': 176,
            'kernel_version': '3.12-x86_64 (hvm)',
            'label': 'Debian 8 (testing) 64 bits (HVM)',
            'os_arch': 'x86-64',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 3,
            'date_created': DateTime('20141203T14:15:28'),
            'date_updated': DateTime('20150116T11:24:56'),
            'disk_id': 3316076,
            'id': 180,
            'kernel_version': '3.12-x86_64 (hvm)',
            'label': 'Debian 8 (testing) 64 bits (HVM)',
            'os_arch': 'x86-64',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 1,
            'date_created': DateTime('20141203T14:15:28'),
            'date_updated': DateTime('20150116T11:24:56'),
            'disk_id': 3315748,
            'id': 184,
            'kernel_version': '3.12-x86_64 (hvm)',
            'label': 'Ubuntu 14.04 64 bits LTS (HVM)',
            'os_arch': 'x86-64',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 2,
            'date_created': DateTime('20141203T14:15:28'),
            'date_updated': DateTime('20150116T11:24:56'),
            'disk_id': 3316144,
            'id': 188,
            'kernel_version': '3.12-x86_64 (hvm)',
            'label': 'Ubuntu 14.04 64 bits LTS (HVM)',
            'os_arch': 'x86-64',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 3,
            'date_created': DateTime('20141203T14:15:28'),
            'date_updated': DateTime('20150116T11:24:56'),
            'disk_id': 3316160,
            'id': 192,
            'kernel_version': '3.12-x86_64 (hvm)',
            'label': 'Ubuntu 14.04 64 bits LTS (HVM)',
            'os_arch': 'x86-64',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 1,
            'date_created': None,
            'date_updated': DateTime('20150116T11:24:56'),
            'disk_id': 2876292,
            'id': 196,
            'kernel_version': '3.12-x86_64 (hvm)',
            'label': 'CentOS 7 64 bits (HVM)',
            'os_arch': 'x86-64',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 2,
            'date_created': None,
            'date_updated': DateTime('20150116T11:24:56'),
            'disk_id': 4744388,
            'id': 200,
            'kernel_version': '3.12-x86_64 (hvm)',
            'label': 'CentOS 7 64 bits (HVM)',
            'os_arch': 'x86-64',
            'size': 3072,
            'visibility': 'all'},
           {'author_id': 248842,
            'datacenter_id': 3,
            'date_created': None,
            'date_updated': DateTime('20150116T11:24:56'),
            'disk_id': 4744392,
            'id': 204,
            'kernel_version': '3.12-x86_64 (hvm)',
            'label': 'CentOS 7 64 bits (HVM)',
            'os_arch': 'x86-64',
            'size': 3072,
            'visibility': 'all'}]

    for fkey in options:
        ret = [dc for dc in ret if dc[fkey] == options[fkey]]
    return ret


def datacenter_list(options):

    ret = [{'iso': 'FR',
            'name': 'Equinix Paris',
            'id': 1,
            'country': 'France'},
           {'iso': 'US',
            'name': 'Level3 Baltimore',
            'id': 2,
            'country': 'United States of America'},
           {'iso': 'LU',
            'name': 'Bissen',
            'id': 3,
            'country': 'Luxembourg'}]

    for fkey in options:
        ret = [dc for dc in ret if dc[fkey] == options[fkey]]
    return ret


def disk_list(options):

    disks = [{'can_snapshot': True,
              'datacenter_id': 3,
              'date_created': DateTime('20150319T11:10:34'),
              'date_updated': DateTime('20150319T11:10:58'),
              'id': 4969232,
              'is_boot_disk': True,
              'kernel_version': '3.12-x86_64 (hvm)',
              'label': 'Debian 7 64 bits (HVM)',
              'name': 'sys_1426759833',
              'size': 3072,
              'snapshot_profile_id': None,
              'snapshots_id': [],
              'source': 1401327,
              'state': 'created',
              'total_size': 3072,
              'type': 'data',
              'visibility': 'private',
              'vms_id': [152966]},
             {'can_snapshot': True,
              'datacenter_id': 1,
              'date_created': DateTime('20150319T11:14:13'),
              'date_updated': DateTime('20150319T11:14:29'),
              'id': 4969249,
              'is_boot_disk': True,
              'kernel_version': '3.12-x86_64 (hvm)',
              'label': 'Debian 7 64 bits (HVM)',
              'name': 'sys_server01',
              'size': 3072,
              'snapshot_profile_id': None,
              'snapshots_id': [],
              'source': 1349810,
              'state': 'created',
              'total_size': 3072,
              'type': 'data',
              'visibility': 'private',
              'vms_id': [152967]},
             {'can_snapshot': True,
              'datacenter_id': 1,
              'date_created': DateTime('20150319T15:39:54'),
              'date_updated': DateTime('20150319T15:40:24'),
              'id': 4970079,
              'is_boot_disk': False,
              'kernel_version': None,
              'label': None,
              'name': 'data',
              'size': 3072,
              'snapshot_profile_id': 1,
              'snapshots_id': [663497],
              'source': None,
              'state': 'created',
              'total_size': 3072,
              'type': 'data',
              'visibility': 'private',
              'vms_id': [152967]},
             {'can_snapshot': False,
              'datacenter_id': 1,
              'date_created': DateTime('20140826T00:00:00'),
              'date_updated': DateTime('20140826T00:00:00'),
              'id': 663497,
              'is_boot_disk': False,
              'kernel_version': '3.2-x86_64',
              'label': 'Debian 7 64 bits',
              'name': 'snaptest',
              'size': 3072,
              'snapshot_profile_id': None,
              'snapshots_id': [],
              'source': 4970079,
              'state': 'created',
              'total_size': 3072,
              'type': 'snapshot',
              'visibility': 'private',
              'vms_id': []}]

    options.pop('items_per_page', None)

    for fkey in options:
        ret = []
        for disk in disks:
            if isinstance(options[fkey], list):
                if disk[fkey] in options[fkey]:
                    ret.append(disk)
            elif disk[fkey] == options[fkey]:
                ret.append(disk)
        disks = ret

    return disks


def disk_info(id):
    disks = disk_list({})
    disks = dict([(disk['id'], disk) for disk in disks])
    return disks[id]


def disk_update(disk_id, options):
    return {'id': 200, 'step': 'WAIT'}


def disk_delete(disk_id):
    return {'id': 200, 'step': 'WAIT'}


def disk_rollback_from(disk_id):
    return {'id': 200, 'step': 'WAIT'}


def disk_create_from(options, disk_id):
    return {'id': 200, 'step': 'WAIT'}


def disk_create(options):
    return {'id': 200, 'step': 'WAIT', 'disk_id': 9000}


def vm_list(options):

    ret = [{'ai_active': 0,
            'console': 0,
            'cores': 1,
            'datacenter_id': 3,
            'date_created': DateTime('20141008T16:13:59'),
            'date_updated': DateTime('20150319T11:11:31'),
            'description': None,
            'disks_id': [4969232],
            'flex_shares': 0,
            'hostname': 'vm1426759833',
            'id': 152966,
            'ifaces_id': [156572],
            'memory': 256,
            'state': 'running',
            'vm_max_memory': 2048},
           {'ai_active': 0,
            'console': 0,
            'cores': 1,
            'datacenter_id': 1,
            'date_created': DateTime('20150319T11:14:13'),
            'date_updated': DateTime('20150319T11:14:55'),
            'description': None,
            'disks_id': [4969249],
            'flex_shares': 0,
            'hostname': 'server01',
            'id': 152967,
            'ifaces_id': [156573],
            'memory': 256,
            'state': 'running',
            'vm_max_memory': 2048},
           {'ai_active': 0,
            'console': 0,
            'cores': 1,
            'datacenter_id': 1,
            'date_created': DateTime('20150319T11:14:13'),
            'date_updated': DateTime('20150319T11:14:55'),
            'description': None,
            'disks_id': [4969250],
            'flex_shares': 0,
            'hostname': 'server02',
            'id': 152968,
            'ifaces_id': [156574],
            'memory': 256,
            'state': 'halted',
            'vm_max_memory': 2048}]

    options.pop('items_per_page', None)

    for fkey in options:
        ret = [vm for vm in ret if vm[fkey] == options[fkey]]

    return ret


def vm_info(id):

    ret = [{'ai_active': 0,
            'console': 0,
            'console_url': 'console.gandi.net',
            'cores': 1,
            'datacenter_id': 3,
            'date_created': DateTime('20150319T11:10:34'),
            'date_updated': DateTime('20150319T11:11:31'),
            'description': None,
            'disks': [{'can_snapshot': True,
                       'datacenter_id': 3,
                       'date_created': DateTime('20150319T11:10:34'),
                       'date_updated': DateTime('20150319T11:10:58'),
                       'id': 4969232,
                       'is_boot_disk': True,
                       'kernel_cmdline': {'console': 'ttyS0',
                                          'nosep': True,
                                          'ro': True,
                                          'root': '/dev/sda'},
                       'kernel_version': '3.12-x86_64 (hvm)',
                       'label': 'Debian 7 64 bits (HVM)',
                       'name': 'sys_1426759833',
                       'size': 3072,
                       'snapshot_profile': None,
                       'snapshots_id': [],
                       'source': 1401327,
                       'state': 'created',
                       'total_size': 3072,
                       'type': 'data',
                       'visibility': 'private',
                       'vms_id': [152966]}],
            'disks_id': [4969232],
            'flex_shares': 0,
            'graph_urls': {'vcpu': [''], 'vdi': [''], 'vif': ['']},
            'hostname': 'vm1426759833',
            'id': 152966,
            'ifaces': [{'bandwidth': 102400.0,
                        'datacenter_id': 3,
                        'date_created': DateTime('20150319T11:10:34'),
                        'date_updated': DateTime('20150319T11:10:35'),
                        'id': 156572,
                        'ips': [{'datacenter_id': 3,
                                 'date_created': DateTime('20150319T11:10:34'),
                                 'date_updated': DateTime('20150319T11:10:36'),
                                 'id': 204557,
                                 'iface_id': 156572,
                                 'ip': '2001:4b98:dc2:43:216:3eff:fece:e25f',
                                 'num': 0,
                                 'reverse': 'xvm6-dc2-fece-e25f.ghst.net',
                                 'state': 'created',
                                 'version': 6}],
                        'ips_id': [204557],
                        'num': 0,
                        'state': 'used',
                        'type': 'public',
                        'vlan': None,
                        'vm_id': 152966}],
            'ifaces_id': [156572],
            'memory': 256,
            'probes': [],
            'state': 'running',
            'triggers': [],
            'vm_max_memory': 2048},
           {'ai_active': 0,
            'console': 0,
            'console_url': 'console.gandi.net',
            'cores': 1,
            'datacenter_id': 1,
            'date_created': DateTime('20150319T11:14:13'),
            'date_updated': DateTime('20150319T11:14:55'),
            'description': None,
            'disks': [{'can_snapshot': True,
                       'datacenter_id': 1,
                       'date_created': DateTime('20150319T11:14:13'),
                       'date_updated': DateTime('20150319T11:14:29'),
                       'id': 4969249,
                       'is_boot_disk': True,
                       'kernel_cmdline': {'console': 'ttyS0',
                                          'nosep': True,
                                          'ro': True,
                                          'root': '/dev/sda'},
                       'kernel_version': '3.12-x86_64 (hvm)',
                       'label': 'Debian 7 64 bits (HVM)',
                       'name': 'sys_server01',
                       'size': 3072,
                       'snapshot_profile': None,
                       'snapshots_id': [],
                       'source': 1349810,
                       'state': 'created',
                       'total_size': 3072,
                       'type': 'data',
                       'visibility': 'private',
                       'vms_id': [152967]}],
            'disks_id': [4969249],
            'flex_shares': 0,
            'graph_urls': {'vcpu': [''], 'vdi': [''], 'vif': ['']},
            'hostname': 'server01',
            'id': 152967,
            'ifaces': [{'bandwidth': 102400.0,
                        'datacenter_id': 1,
                        'date_created': DateTime('20150319T11:14:13'),
                        'date_updated': DateTime('20150319T11:14:16'),
                        'id': 156573,
                        'ips': [{'datacenter_id': 1,
                                 'date_created': DateTime('20150317T16:20:10'),
                                 'date_updated': DateTime('20150319T11:14:13'),
                                 'id': 203968,
                                 'iface_id': 156573,
                                 'ip': '95.142.160.181',
                                 'num': 0,
                                 'reverse': 'xvm-160-181.dc0.ghst.net',
                                 'state': 'created',
                                 'version': 4},
                                {'datacenter_id': 1,
                                 'date_created': DateTime('20150319T11:14:16'),
                                 'date_updated': DateTime('20150319T11:14:16'),
                                 'id': 204558,
                                 'iface_id': 156573,
                                 'ip': '2001:4b98:dc0:47:216:3eff:feb2:3862',
                                 'num': 1,
                                 'reverse': 'xvm6-dc0-feb2-3862.ghst.net',
                                 'state': 'created',
                                 'version': 6}],
                        'ips_id': [203968, 204558],
                        'num': 0,
                        'state': 'used',
                        'type': 'public',
                        'vlan': None,
                        'vm_id': 152967}],
            'ifaces_id': [156573],
            'memory': 256,
            'probes': [],
            'state': 'running',
            'triggers': [],
            'vm_max_memory': 2048}]

    vms = dict([(vm['id'], vm) for vm in ret])
    return vms[id]


def metric_query(query):

    vif_bytes_all = [
        {'direction': ['in'],
         'metric': 'vif.bytes',
         'points': [{'timestamp': '2015-03-18T10:00:00', 'value': 24420.0},
                    {'timestamp': '2015-03-18T11:00:00', 'value': 22370.0},
                    {'timestamp': '2015-03-18T12:00:00', 'value': 46680.0},
                    {'timestamp': '2015-03-18T13:00:00', 'value': 61664.0},
                    {'timestamp': '2015-03-18T14:00:00', 'value': 142789.0},
                    {'timestamp': '2015-03-18T15:00:00', 'value': 35633.0},
                    {'timestamp': '2015-03-18T16:00:00', 'value': 213987.0},
                    {'timestamp': '2015-03-18T17:00:00', 'value': 80055.0},
                    {'timestamp': '2015-03-18T18:00:00', 'value': 57690.0},
                    {'timestamp': '2015-03-18T19:00:00', 'value': 83508.0},
                    {'timestamp': '2015-03-18T20:00:00', 'value': 115038.0},
                    {'timestamp': '2015-03-18T21:00:00', 'value': 71923.0},
                    {'timestamp': '2015-03-18T22:00:00', 'value': 259466.0},
                    {'timestamp': '2015-03-18T23:00:00', 'value': 301198.0},
                    {'timestamp': '2015-03-19T00:00:00', 'value': 69579.0},
                    {'timestamp': '2015-03-19T01:00:00', 'value': 99998.0},
                    {'timestamp': '2015-03-19T02:00:00', 'value': 53706.0},
                    {'timestamp': '2015-03-19T03:00:00', 'value': 55539.0},
                    {'timestamp': '2015-03-19T04:00:00', 'value': 60018.0},
                    {'timestamp': '2015-03-19T05:00:00', 'value': 23000.0},
                    {'timestamp': '2015-03-19T06:00:00', 'value': 57812.0},
                    {'timestamp': '2015-03-19T07:00:00', 'value': 984992.0},
                    {'timestamp': '2015-03-19T08:00:00', 'value': 315608.0},
                    {'timestamp': '2015-03-19T09:00:00', 'value': 77852.0}],
         'resource_id': 152967,
         'resource_type': 'vm',
         'type': ['public']},
        {'direction': ['out'],
         'metric': 'vif.bytes',
         'points': [{'timestamp': '2015-03-18T10:00:00', 'value': 5335.0},
                    {'timestamp': '2015-03-18T11:00:00', 'value': 8763.0},
                    {'timestamp': '2015-03-18T12:00:00', 'value': 43790.0},
                    {'timestamp': '2015-03-18T13:00:00', 'value': 73345.0},
                    {'timestamp': '2015-03-18T14:00:00', 'value': 259536.0},
                    {'timestamp': '2015-03-18T15:00:00', 'value': 18595.0},
                    {'timestamp': '2015-03-18T16:00:00', 'value': 751379.0},
                    {'timestamp': '2015-03-18T17:00:00', 'value': 150840.0},
                    {'timestamp': '2015-03-18T18:00:00', 'value': 43115.0},
                    {'timestamp': '2015-03-18T19:00:00', 'value': 593737.0},
                    {'timestamp': '2015-03-18T20:00:00', 'value': 619675.0},
                    {'timestamp': '2015-03-18T21:00:00', 'value': 67605.0},
                    {'timestamp': '2015-03-18T22:00:00', 'value': 300711.0},
                    {'timestamp': '2015-03-18T23:00:00', 'value': 380400.0},
                    {'timestamp': '2015-03-19T00:00:00', 'value': 62705.0},
                    {'timestamp': '2015-03-19T01:00:00', 'value': 100512.0},
                    {'timestamp': '2015-03-19T02:00:00', 'value': 47963.0},
                    {'timestamp': '2015-03-19T03:00:00', 'value': 50301.0},
                    {'timestamp': '2015-03-19T04:00:00', 'value': 48572.0},
                    {'timestamp': '2015-03-19T05:00:00', 'value': 6263.0},
                    {'timestamp': '2015-03-19T06:00:00', 'value': 67014.0},
                    {'timestamp': '2015-03-19T07:00:00', 'value': 777215.0},
                    {'timestamp': '2015-03-19T08:00:00', 'value': 495497.0},
                    {'timestamp': '2015-03-19T09:00:00', 'value': 660825.0}],
         'resource_id': 152967,
         'resource_type': 'vm',
         'type': ['public']}]

    vbd_bytes_all = [
        {'direction': ['read'],
         'metric': 'vbd.bytes',
         'points': [{'timestamp': '2015-03-18T10:00:00', 'value': 13824000.0},
                    {'timestamp': '2015-03-18T11:00:00', 'value': 5644288.0},
                    {'timestamp': '2015-03-18T12:00:00', 'value': 0.0},
                    {'timestamp': '2015-03-18T13:00:00', 'value': 13516800.0},
                    {'timestamp': '2015-03-18T14:00:00', 'value': 27918336.0},
                    {'timestamp': '2015-03-18T15:00:00', 'value': 9150464.0},
                    {'timestamp': '2015-03-18T16:00:00', 'value': 64323584.0},
                    {'timestamp': '2015-03-18T17:00:00', 'value': 29974528.0},
                    {'timestamp': '2015-03-18T18:00:00', 'value': 761856.0},
                    {'timestamp': '2015-03-18T19:00:00', 'value': 41775104.0},
                    {'timestamp': '2015-03-18T20:00:00', 'value': 14286848.0},
                    {'timestamp': '2015-03-18T21:00:00', 'value': 1073152.0},
                    {'timestamp': '2015-03-18T22:00:00', 'value': 387248128.0},
                    {'timestamp': '2015-03-18T23:00:00', 'value': 13754368.0},
                    {'timestamp': '2015-03-19T00:00:00', 'value': 2056192.0},
                    {'timestamp': '2015-03-19T01:00:00', 'value': 9990144.0},
                    {'timestamp': '2015-03-19T02:00:00', 'value': 643072.0},
                    {'timestamp': '2015-03-19T03:00:00', 'value': 6148096.0},
                    {'timestamp': '2015-03-19T04:00:00', 'value': 8974336.0},
                    {'timestamp': '2015-03-19T05:00:00', 'value': 782336.0},
                    {'timestamp': '2015-03-19T06:00:00', 'value': 12214272.0},
                    {'timestamp': '2015-03-19T07:00:00', 'value': 29261824.0},
                    {'timestamp': '2015-03-19T08:00:00', 'value': 144080896.0},
                    {'timestamp': '2015-03-19T09:00:00', 'value': 39198720.0}],
         'resource_id': 152967,
         'resource_type': 'vm'},
        {'direction': ['write'],
         'metric': 'vbd.bytes',
         'points': [{'timestamp': '2015-03-18T10:00:00', 'value': 217088.0},
                    {'timestamp': '2015-03-18T11:00:00', 'value': 229376.0},
                    {'timestamp': '2015-03-18T12:00:00', 'value': 401408.0},
                    {'timestamp': '2015-03-18T13:00:00', 'value': 577536.0},
                    {'timestamp': '2015-03-18T14:00:00', 'value': 3862528.0},
                    {'timestamp': '2015-03-18T15:00:00', 'value': 217088.0},
                    {'timestamp': '2015-03-18T16:00:00', 'value': 2363392.0},
                    {'timestamp': '2015-03-18T17:00:00', 'value': 1773568.0},
                    {'timestamp': '2015-03-18T18:00:00', 'value': 217088.0},
                    {'timestamp': '2015-03-18T19:00:00', 'value': 3153920.0},
                    {'timestamp': '2015-03-18T20:00:00', 'value': 2039808.0},
                    {'timestamp': '2015-03-18T21:00:00', 'value': 606208.0},
                    {'timestamp': '2015-03-18T22:00:00', 'value': 12505088.0},
                    {'timestamp': '2015-03-18T23:00:00', 'value': 675840.0},
                    {'timestamp': '2015-03-19T00:00:00', 'value': 602112.0},
                    {'timestamp': '2015-03-19T01:00:00', 'value': 598016.0},
                    {'timestamp': '2015-03-19T02:00:00', 'value': 483328.0},
                    {'timestamp': '2015-03-19T03:00:00', 'value': 462848.0},
                    {'timestamp': '2015-03-19T04:00:00', 'value': 471040.0},
                    {'timestamp': '2015-03-19T05:00:00', 'value': 487424.0},
                    {'timestamp': '2015-03-19T06:00:00', 'value': 499712.0},
                    {'timestamp': '2015-03-19T07:00:00', 'value': 42958848.0},
                    {'timestamp': '2015-03-19T08:00:00', 'value': 6299648.0},
                    {'timestamp': '2015-03-19T09:00:00', 'value': 3862528.0}],
         'resource_id': 152967,
         'resource_type': 'vm'}]

    metrics = {'vif.bytes.all': vif_bytes_all,
               'vbd.bytes.all': vbd_bytes_all}

    metrics = [item for item in metrics[query['query']]
               if item['resource_id'] == query['resource_id'][0]]

    return metrics


def disk_list_kernels(dc_id):

    ret = {
        1: {'linux': ['2.6.18 (deprecated)',
                      '2.6.27-compat-sysfs (deprecated)',
                      '2.6.32',
                      '2.6.27 (deprecated)',
                      '2.6.32-x86_64',
                      '2.6.36 (deprecated)',
                      '2.6.32-x86_64-grsec',
                      '2.6.36-x86_64 (deprecated)',
                      '3.2-i386',
                      '3.2-x86_64',
                      '3.2-x86_64-grsec',
                      '3.10-x86_64',
                      '3.10-i386'],
            'linux-hvm': ['3.12-x86_64 (hvm)', 'grub', 'raw']},
        2: {'linux': ['2.6.18 (deprecated)',
                      '2.6.27-compat-sysfs (deprecated)',
                      '2.6.32',
                      '2.6.27 (deprecated)',
                      '2.6.32-x86_64',
                      '2.6.36 (deprecated)',
                      '2.6.32-x86_64-grsec',
                      '2.6.36-x86_64 (deprecated)',
                      '3.2-i386',
                      '3.2-x86_64',
                      '3.2-x86_64-grsec',
                      '3.10-x86_64',
                      '3.10-i386'],
            'linux-hvm': ['3.12-x86_64 (hvm)', 'grub', 'raw']},
        3: {'linux': ['2.6.32',
                      '2.6.27 (deprecated)',
                      '2.6.32-x86_64',
                      '2.6.32-x86_64-grsec',
                      '3.2-i386',
                      '3.2-x86_64',
                      '3.2-x86_64-grsec',
                      '3.10-x86_64',
                      '3.10-i386'],
            'linux-hvm': ['3.12-x86_64 (hvm)', 'grub', 'raw']}}

    return ret[dc_id]


def account_info():
    return {'average_credit_cost': 0.0,
            'credits': 2335360,
            'cycle_day': 23,
            'date_credits_expiration': DateTime('20160319T10:07:24'),
            'fullname': 'Peter Parker',
            'handle': 'PXP561-GANDI',
            'id': 2920674,
            'products': None,
            'rating_enabled': True,
            'resources': {'available': None,
                          'expired': None,
                          'granted': None,
                          'used': None},
            'share_definition': None}


def rating_list():
    return [{'bw_out': None,
             'cpu': {'default': 168},
             'disk_data': {'default': 135},
             'disk_snapshot': None,
             'disk_snapshot_auto': None,
             'instance': {'default': 0},
             'ip': {'v4_public': 210, 'v6': 0},
             'ram': {'default': 120},
             'rproxy': None,
             'rproxy_server': None,
             'rproxy_ssl': None,
             'timestamp': DateTime('20150319T15:07:24')}]


def vm_disk_detach(vm_id, disk_id):
    if vm_id == 152967 and disk_id == 4970079:
        return {'id': 200, 'step': 'WAIT'}


def vm_iface_detach(vm_id, iface_id):
    if vm_id == 152967 and iface_id == 156573:
        return {'id': 200, 'step': 'WAIT'}


def vm_iface_attach(vm_id, iface_id):
    if vm_id == 152966 and iface_id == 156573:
        return {'id': 200, 'step': 'WAIT'}

    if vm_id == 152967 and iface_id == 156575:
        return {'id': 200, 'step': 'WAIT'}


def vm_disk_attach(vm_id, disk_id, options):
    if vm_id == 152967 and disk_id == 663497:
        return {'id': 200, 'step': 'WAIT'}

    if vm_id == 152966 and disk_id == 4970079:
        return {'id': 200, 'step': 'WAIT'}

    if vm_id == 152967 and disk_id == 9000:
        return {'id': 200, 'step': 'WAIT'}


def vm_stop(vm_id):
    if vm_id in (152967, 152966):
        return {'id': 200, 'step': 'WAIT'}


def vm_start(vm_id):
    if vm_id in (152967, 152966):
        return {'id': 200, 'step': 'WAIT'}


def vm_reboot(vm_id):
    if vm_id in (152967, 152966):
        return {'id': 200, 'step': 'WAIT'}


def vm_delete(vm_id):
    if vm_id in (152968, 152967, 152966):
        return {'id': 200, 'step': 'WAIT'}


def vm_update(vm_id, options):
    if vm_id in (152967, 152966):
        return {'id': 200, 'step': 'WAIT'}


def vm_create_from(vm_spec, disk_spec, src_disk_id):
    return [{'id': 300, 'step': 'WAIT'}]


def vlan_list(options):
    return [{'datacenter_id': 1,
             'gateway': None,
             'id': 123,
             'name': 'vlantest',
             'state': 'created',
             'subnet': None,
             'uuid': 321},
            {'datacenter_id': 1,
             'gateway': None,
             'id': 717,
             'name': 'pouet',
             'state': 'created',
             'subnet': None,
             'uuid': 720}]


def iface_create(options):
    return {'id': 200, 'step': 'WAIT', 'iface_id': 156575}


def iface_delete(ip_id):
    return {'id': 200, 'step': 'WAIT'}


def iface_list(options):

    ret = [{'bandwidth': 102400.0,
            'datacenter_id': 1,
            'date_created': DateTime('20140423T00:00:00'),
            'date_updated': DateTime('20140423T00:00:00'),
            'id': 156573,
            'ips_id': [203968, 204558],
            'ips': [{'datacenter_id': 1,
                     'date_created': DateTime('20150317T16:20:10'),
                     'date_updated': DateTime('20150319T11:14:13'),
                     'id': 203968,
                     'iface_id': 156573,
                     'ip': '95.142.160.181',
                     'num': 0,
                     'reverse': 'xvm-160-181.dc0.ghst.net',
                     'state': 'created',
                     'version': 4},
                    {'datacenter_id': 1,
                     'date_created': DateTime('20150319T11:14:16'),
                     'date_updated': DateTime('20150319T11:14:16'),
                     'id': 204558,
                     'iface_id': 156573,
                     'ip': '2001:4b98:dc0:47:216:3eff:feb2:3862',
                     'num': 1,
                     'reverse': 'xvm6-dc0-feb2-3862.ghst.net',
                     'state': 'created',
                     'version': 6}],
            'num': 0,
            'state': 'used',
            'type': 'public',
            'vlan': None,
            'vm_id': 152967},
           {'bandwidth': 102400.0,
            'datacenter_id': 1,
            'date_created': DateTime('20141009T00:00:00'),
            'date_updated': DateTime('20141105T00:00:00'),
            'id': 1416,
            'ips_id': [],
            'num': None,
            'state': 'free',
            'type': 'private',
            'vlan': {'id': 717, 'name': 'pouet'},
            'vm_id': None},
           {'bandwidth': 204800.0,
            'datacenter_id': 1,
            'date_created': DateTime('20150105T00:00:00'),
            'date_updated': DateTime('20150105T00:00:00'),
            'id': 1914,
            'ips_id': [2361],
            'num': None,
            'state': 'free',
            'type': 'private',
            'vlan': {'id': 717, 'name': 'pouet'},
            'vm_id': None},
           {'bandwidth': 204800.0,
            'datacenter_id': 1,
            'date_created': DateTime('20150105T00:00:00'),
            'date_updated': DateTime('20150105T00:00:00'),
            'id': 156572,
            'ips_id': [204557],
            'num': None,
            'state': 'free',
            'type': 'private',
            'vlan': {'id': 717, 'name': 'pouet'},
            'vm_id': None}]

    options.pop('items_per_page', None)

    for fkey in options:
        if fkey == 'vlan':
            ret_ = []
            for iface in ret:
                if iface['vlan'] and iface['vlan']['name'] == options['vlan']:
                    ret_.append(iface)
            ret = ret_
        else:
            ret = [iface for iface in ret if iface[fkey] == options[fkey]]

    return ret


def iface_info(iface_id):

    ifaces = iface_list({})
    ifaces = dict([(iface['id'], iface) for iface in ifaces])
    return ifaces[iface_id]


def ip_list(options):

    ips = [{'datacenter_id': 1,
            'date_created': DateTime('20150317T16:20:10'),
            'date_updated': DateTime('20150319T11:14:13'),
            'id': 203968,
            'iface_id': 156573,
            'ip': '95.142.160.181',
            'num': 0,
            'reverse': 'xvm-160-181.dc0.ghst.net',
            'state': 'created',
            'version': 4},
           {'datacenter_id': 3,
            'date_created': DateTime('20150319T11:10:34'),
            'date_updated': DateTime('20150319T11:10:36'),
            'id': 204557,
            'iface_id': 156572,
            'ip': '2001:4b98:dc2:43:216:3eff:fece:e25f',
            'num': 0,
            'reverse': 'xvm6-dc2-fece-e25f.ghst.net',
            'state': 'created',
            'version': 6},
           {'datacenter_id': 1,
            'date_created': DateTime('20150319T11:14:16'),
            'date_updated': DateTime('20150319T11:14:16'),
            'id': 204558,
            'iface_id': 156573,
            'ip': '2001:4b98:dc0:47:216:3eff:feb2:3862',
            'num': 1,
            'reverse': 'xvm6-dc0-feb2-3862.ghst.net',
            'state': 'created',
            'version': 6}]

    options.pop('items_per_page', None)

    for fkey in options:
        ret = []
        for ip in ips:
            if isinstance(options[fkey], list):
                if ip[fkey] in options[fkey]:
                    ret.append(ip)
            elif ip[fkey] == options[fkey]:
                ret.append(ip)
        ips = ret

    return ips


def ip_info(ip_id):

    ips = ip_list({})
    ips = dict([(ip['id'], ip) for ip in ips])
    return ips[ip_id]


def ip_update(ip_id, options):
    return {'id': 200, 'step': 'WAIT'}


def ssh_list(options):
    ret = [{'fingerprint': 'b3:11:67:10:2e:1b:a5:66:ed:16:24:98:3e:2e:ed:f5',
            'id': 134,
            'name': 'default'},
           {'fingerprint': '09:11:21:e3:90:3c:7d:d5:06:d9:6f:f9:36:e1:99:a6',
            'id': 141,
            'name': 'mysecretkey'}]

    options.pop('items_per_page', None)

    for fkey in options:
        ret = [vm for vm in ret if vm[fkey] == options[fkey]]

    return ret


def vlan_info(options):
    return {'datacenter': {'country': 'Luxembourg',
                           'id': 3,
                           'iso': 'LU',
                           'name': 'Bissen'},
            'gateway': None,
            'id': 123,
            'name': 'vlantest',
            'state': 'created',
            'subnet': '192.168.0.0/24',
            'uuid': 321}


def snapshotprofile_list(options):
    ret = [{'id': 1,
            'kept_total': 2,
            'name': 'minimal',
            'quota_factor': 1.2,
            'schedules': [{'kept_version': 2, 'name': 'daily'}]},
           {'id': 2,
            'kept_total': 7,
            'name': 'full_week',
            'quota_factor': 1.7,
            'schedules': [{'kept_version': 7, 'name': 'daily'}]},
           {'id': 3,
            'kept_total': 10,
            'name': 'security',
            'quota_factor': 2.0,
            'schedules': [{'kept_version': 3, 'name': 'hourly6'},
                          {'kept_version': 6, 'name': 'daily'},
                          {'kept_version': 1, 'name': 'weekly4'}]}]
    return ret

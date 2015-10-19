#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import logging
from pprint import pprint

import sxclient

COMMAND_STRINGS = [u'sxclient.listNodes(cluster, session)',
                   u'sxclient.getNodeStatus(cluster, session, node_address={node_address!r})',
                   u'sxclient.setClusterMetadata(cluster, session, {{u"key1": "616263", u"key2": "616263646566676869"}})',
                   u'sxclient.getClusterMetadata(cluster, session)',
                   u'sxclient.createUser(cluster, session, userName=u"testuser", userType=u"normal", userKey=u"990f1457813947856378465144be7052748c194c", desc=u"A test user.")',
                   u'sxclient.modifyUser(cluster, session, userName=u"testuser", userKey=u"afd412970decb3213128465144be70527addfc43", quota=10737418240, desc=u"A modified test user.")',
                   u'sxclient.listUsers(cluster, session)',
                   u'sxclient.createVolume(cluster, session, volume=u"testvol", volumeSize=1073741824, owner=u"admin", replicaCount=1, volumeMeta={{u"VolumeDescription": u"736861726564206f666669636520646f63756d656e7473", u"ApplicationID": u"ff03"}})',
                   u'sxclient.modifyVolume(cluster, session, volume=u"testvol", size=2147483648, owner=None, maxRevisions=2, customVolumeMeta={{u"some_custom_meta": u"60626466"}})',
                   u'sxclient.listVolumes(cluster, session, includeMeta=True, includeCustomMeta=True)',
                   u'sxclient.locateVolume(cluster, session, volume=u"testvol", size=u"12345", includeMeta=True, includeCustomMeta=True)',
                   u'sxclient.updateVolumeACL(cluster, session, volume=u"testvol", actions={{u"grant-read": [u"testuser"], u"grant-write": [u"testuser"]}})',
                   u'sxclient.getVolumeACL(cluster, session, volume=u"testvol")',
                   u'sxclient.setVolumeACL(cluster, session, volume=u"testvol", permissions={{u"testuser": [u"read", u"manager"]}})',
                   u'sxclient.getVolumeACL(cluster, session, volume=u"testvol")',
                   u'sxclient.deleteVolume(cluster, session, volume=u"testvol", force=True)',
                   u'sxclient.removeUser(cluster, session, userName=u"testuser")']

def parse_command_line():
    parser = argparse.ArgumentParser(description='Run all available operations.')
    parser.add_argument('-n',
                        '--name',
                        dest='cluster_name',
                        required=True,
                        help="name of the cluster")
    parser.add_argument('-a',
                        '--address',
                        dest='cluster_address',
                        default=None,
                        help="IP address at which SX cluster is reachable; "
                        "if given, will be used instead cluster name "
                        "to connect to the cluster; also used in absence "
                        "of --node-address as a node address for node "
                        "operations")
    parser.add_argument('--node-address',
                        dest='node_address',
                        default=None,
                        help="IP address of a node in the cluster; "
                        "used in node operation calls")
    parser.add_argument('-p',
                        '--port',
                        type=int,
                        default=None,
                        help="cluster destination port")
    parser.add_argument('-k',
                        '--key-path',
                        required=True,
                        dest='key_path',
                        help="path to the file with user's authentication key")
    parser.add_argument('--no-ssl',
                        dest='secure',
                        action='store_false',
                        default=True,
                        help="disable secure communication "
                        "(it is enabled by default)")
    parser.add_argument('--no-verify',
                        dest='verify',
                        action='store_false',
                        default=True,
                        help="don't verify the SSL certificate at all; "
                        "this option overrides \"--ca-cert\"")
    parser.add_argument('--ca-cert',
                        dest='ca_cert',
                        default=None,
                        help="path to trusted CA certificate or certificate "
                        "bundle")
    parser.add_argument('-D',
                        '--debug',
                        action='store_true',
                        default=False,
                        help="enable debug messages")
    args = parser.parse_args()
    if args.cluster_address is None and args.node_address is None:
        parser.error('at least one of -a/--address, --node-address is required')
    return args

def main():
    args = parse_command_line()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    node_address = args.node_address or args.cluster_address

    cluster = sxclient.Cluster(name=args.cluster_name,
                               ip_address=args.cluster_address,
                               is_secure=args.secure,
                               port=args.port)
    user_data = sxclient.UserData.from_key_path(args.key_path)
    if not args.verify:
        verify = False
    elif args.ca_cert:
        verify = args.ca_cert
    else:
        verify = True
    with sxclient.ClusterSession(cluster, user_data, verify=verify) as session:
        for cmd in COMMAND_STRINGS:
            cmd = cmd.format(node_address=node_address)
            print '>>> {}'.format(cmd.encode('utf-8'))
            result = eval(cmd)
            pprint(result)
            print

if __name__ == '__main__':
    main()

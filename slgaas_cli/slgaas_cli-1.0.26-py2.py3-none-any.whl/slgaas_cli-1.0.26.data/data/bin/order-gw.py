#!/usr/bin/env python

# Order a vyatta using the GaaS REST API.
# This script also serves as an example of how to use the GaaS REST API.
# An example of invoking this script is:
#   order-gw.py -v --domain foo.com --vlans 2536.bcr01a.sjc01 --size small --gaashost http://localhost v1
# You also need to set environment variables SLUSERNAME and SLAPIKEY.
# And when you *really* want to order the vyatta, i.e. spend money, include the --really-order on the command line.
# After the gw is ordered and provisioned by softlayer, you can configure it using config-gw.py

# import requests, json
import socket
import sys
import os
import pprint
import re
import argparse
import time

try:
    from slgaas_cli import cliutils         # this will work if the slgaas_cli pkg is installed
except ImportError as e:
    if 'No module named slgaas_cli' not in str(e):
        # it found the module, but there was an error in it
        print 'Error: can not load python module slgaas_cli.cliutils: '+str(e)
        sys.exit(2)
    # if we are here, the slgaas_cli pkg is not installed, maybe we are running from the git repo
    pkgpath = os.path.dirname(os.path.realpath(__file__))+'/..'
    # print 'Did not find/load the cliutils module installed ('+str(e)+'), checking in '+pkgpath
    sys.path.append(pkgpath)
    try:
        from slgaas_cli import cliutils
    except ImportError as e:
        print 'Error: can not find/load python module slgaas_cli.cliutils: '+str(e)
        sys.exit(2)

# parse cmd line args
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
    description='Order a vyatta gateway using the GaaS REST API.',
    epilog='''In addition to the options below, you also need to set environment variables
SLUSERNAME and SLAPIKEY, or have them in your ~/.softlayer file.

EXAMPLES:

# Order a small virtual server gateway, on specific VLANs, suitable for a POC
order-gw.py --vlan 1275.fcr01a.tor01,1327.bcr01a.tor01 --size vs-small --output ~/tmp/gaas/order.txt --really-order vv11.softlayer.com

# Order a medium virtual server gateway in the Toronto data center
order-gw.py --datacenter tor01 --size vs-medium --output ~/tmp/gaas/order.txt --really-order vv12.softlayer.com

# Get a quote (do not actually order) for a bare metal gateway appliance
order-gw.py --domain softlayer.com --vlan 1327.bcr01a.tor01 --size large --output ~/tmp/gaas/order.txt v13
''')
parser.add_argument('vyatta', metavar='gatewayname', nargs='?',
    help='The name of the gateway. Either include the domain name in this name or specify it with --domain')
parser.add_argument('--domain', metavar='domainname', required=False,
    help='the domain name for the gateway. Required if you do not include the domain in the gateway name.')
parser.add_argument('--datacenter', metavar='datacenter', required=False,
    help='the datacenter to create this gateway in. Only valid for gateway virtual servers. Use the short name of the datacenter, e.g. sjc01.')
parser.add_argument('--vlan', metavar='associatedvlan', required=False,
    help='one of the VLANs to be associated to the gateway appliance, specified as <vlanNum>.<routerHostname>. This ensures the gateway is provisioned in the same pod/router as the VLANs you want it to be the router for. This argument is optional for a gateway virtual server, and in that case means what vlans (can be a comma separated list of public and private) the virtual server should be placed on.')
parser.add_argument('--size', metavar='size', required=False,
    help='Specify small, medium, or large for a monthly bare metal gateway appliance, or specify vs-small or vs-medium for an hourly gateway virtual server.')
parser.add_argument('--ha-pair', action="store_true",
    help="you want to order 2 vyattas configured together as an HA pair")
parser.add_argument('--output', metavar='file',
    help="file name to put the order or quote output in, instead of displaying it to stdout. The order/quote data structure is very large, so you will probably want it in a file.")
parser.add_argument('--os-code', metavar='os',
    help="A specific operating system that should be put on the virtual server. If this is specified, it assumes you are not ordering a vyatta, and will not verify the VLANs are not associated to another gateway. If not specified, the vyatta community edition OS will be used.")
parser.add_argument('--really-order', action="store_true",
    help="really order the vyatta, otherwise just get a quote")
parser.add_argument('--models', action="store_true",
    help="Display the available gateway models (instead of ordering one). If using this flag, do not specify any of the flags above, except optionally --size.")
parser.add_argument('--package', action="store_true",
    help="Display the available categories and item choices for the SoftLayer package that is used for the gateway model size specified in --size. Only for advanced users. You can use this to find possible values for --os-code.")
parser.add_argument('--gaashost', metavar='url', required=False,
    help='the GaaS REST API server, i.e. the 1st part of the URL for the REST API calls, e.g. https://svr1 . If not specified, it will use the environment variable GAASHOST. If neither are specified, it will use the production GaaS server.')
parser.add_argument('-v', "--verbose", action="store_true",
    help="display verbose output")


# main

# Check input
args = parser.parse_args()
# pprint.pprint(args)
cliutils.getSlCredentials()      # this will save them for use, or exit with an error msg
# if 'SLUSERNAME' not in os.environ or 'SLAPIKEY' not in os.environ:
#     parser.print_help()
gaashost = cliutils.getGaasHost(args)
if args.verbose:  cliutils.setVerbose(True)
if args.models or args.package:
    if args.vyatta or args.domain or args.datacenter or args.vlan or args.ha_pair or args.output or args.os_code:       # size is allowed
        cliutils.error(2, 'When specifying --models or --package, can not specify: gateway name, --domain, --datacenter, --vlan, --ha-pair, --output, --os-code')
    if args.package and not args.size:  cliutils.error(2, 'must specify --size with --package')
else:
    # not --models, so need a gw name
    if not args.vyatta:  cliutils.error(2, 'must specify the gateway name')
    if args.vyatta.find('.') == -1:
        # no domain in the name, --domain required
        if not args.domain:  cliutils.error(2, 'must either include the domain in the gateway name or specify the --domain flag')
        gw = args.vyatta
        domain = args.domain
    else:
        # domain is in the name
        gw, domain = args.vyatta.split('.', 1)
        if args.domain and args.domain!=domain:  cliutils.error(2, 'specify the domain in either the gateway name or the --domain flag, but not both')
    if not args.size:  cliutils.error(2, 'must specify --size')
    if args.size.startswith('vs-'):
        appliance = False
        if args.ha_pair:  cliutils.error(2, 'can not specify --ha-pair for a gateway virtual server.')
        if not args.vlan and not args.datacenter:  cliutils.error(2, 'must specify either --datacenter or --vlan')
    else:
        appliance = True
        if args.datacenter:  cliutils.error(2, 'can not specify --datacenter for a gateway appliance.')
        if not args.vlan:  cliutils.error(2, 'must specify --vlan for a gateway appliance.')
        if args.os_code:  cliutils.error(2, 'can not specify --os-code for gateway appliance')


if args.models:
    params = {'detail':'1'}
    if args.size:  params['size'] = args.size
    models = cliutils.get(gaashost, '/gateways/hardware/models', params=params)
    pprint.pprint(models)
    sys.exit()


if args.package:
    pkg = cliutils.get(gaashost, '/account/orders/packages/'+args.size)
    pprint.pprint(pkg)
    sys.exit()


print 'Checking permissions...'
# make sure they have the SL permissions needed to complete the task.  This will also kick out
# if they do not have a valid SL username and api key.
# requiredPermissions = ['Manage Network Gateways', 'View Hardware', 'add server', 'IPSEC Network Tunnel', 'View CloudLayer Computing Instances', 'Access all hardware', 'Hardware Firewall']
requiredPermissions = []        # using an empty list tells GaaS to check for the minimum set of permissions needed for GaaS
response = cliutils.post(gaashost, '/user/permissions', requiredPermissions)
if 'unmet-permissions' in response:
    cliutils.error(2, 'you need the following SoftLayer permissions to configure the vyatta:'+', '.join(response['unmet-permissions']))


print 'Verifying the VLAN...'
# ensure the vlan exists, it is not a transit vlan, and it is not already associated with another vyatta
vlan = args.vlan
vlans = vlan.split(',')             # for virtual svr it can be a list of 2
if vlan and not args.os_code:
    response = cliutils.get(gaashost, '/account/vlans')        # the resulting dictionary will be keyed by vlan number
    for v in vlans:
        if v.find('.') == -1:  cliutils.error(2, 'VLAN '+v+' must have the router hostname appended to make it unique.')
        if v not in response:  cliutils.error(2, 'invalid VLAN number: '+v)
        if response[v]['isTransitVlan']:  cliutils.error(2, 'VLAN '+v+' is a transit VLAN, it can not be associated to a gateway.')
        if response[v]['isAssociatedVlan']:  cliutils.error(2, 'VLAN '+v+' is already associated to another gateway.')


if args.os_code:  instance = 'VSI'
else:  instance = 'Gateway'
if args.really_order:
    print 'Ordering '+instance+'...'
    reallyOrder = True
else:
    if appliance:  print 'Getting quote for '+instance+'...'
    else:  print 'Not actually ordering the '+instance+' because --really-order was not specified'
    reallyOrder = False

body = {"name":gw, "domain":domain, "really-order":reallyOrder, "size":args.size}
if appliance:
    body['associated-vlan'] = vlan
else:
    if vlan:  body['vlans'] = vlans
    else:  body['datacenter'] = args.datacenter
if args.ha_pair:
    body['ha-pair'] = True
    body['name2'] = gw+'b'
if args.os_code:
    body['osCode'] = args.os_code
response = cliutils.post(gaashost, '/gateways', body)
if args.output:
    f = open(args.output, 'w')
    # f.write(str(response))
    pprint.pprint(response, f)
    f.close()
else:
    pprint.pprint(response)


if args.really_order:
    print instance+' order completed successfully.'
else:
    print instance+' quote completed successfully.'
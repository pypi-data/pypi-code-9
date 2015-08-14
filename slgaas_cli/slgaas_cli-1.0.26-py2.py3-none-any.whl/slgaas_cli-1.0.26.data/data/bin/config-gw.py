#!/usr/bin/env python

# Configure an existing vyatta using the GaaS REST API.
# This performs all of the configuration necessary for a vyatta after it has been ordered. A gateway can be ordered using the command order-gw.py.
# This script also serves as an example of how to use the GaaS REST API. The GaaS REST API is documented at https://gateway-as-a-service.com/gaas/v1/spec.html#!/spec .
# For examples of invoking this script, see the help info below.

# import requests, json
import socket
import sys
import os
import json
import pprint
import re
import argparse
import time
import datetime

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
    description='''Configure an existing vyatta gateway, using the GaaS REST API, with default
firewall zone settings and optionally NAT and/or a tunnel.''',
    epilog='''In addition to the options below, you also need to set environment variables
SLUSERNAME and SLAPIKEY, or have them in your ~/.softlayer file.

EXAMPLES:

# Configure the firewall and an IPSec/GRE tunnel to 1.2.3.4
config-gw.py --vlans 2536.bcr01a.sjc01 --peer-gw-ip 1.2.3.4 --peer-subnets 10.200.0.0/16 --pre-shared-secret foobar --gre-ip 10.254.254.1/30 --byoip-subnets 2536.bcr01a.sjc01:10.201.0.0/24,4567:10.201.1.0/24 v1

# Add an additional GRE-only tunnel
config-gw.py --peer-gw-ip 1.2.3.4 --peer-subnets 10.200.0.0/16 --gre-ip 10.254.254.1/30 --add-tunnel v1

# Configure the firewall and set up NAT masquerade so the machines with only private NICs can access the internet
config-gw.py --vlans 2536.bcr01a.sjc01 --masquerade v1

# Configure the firewall and an IPSec-only tunnel on a virtual server gateway
config-gw.py --peer-gw-ip 1.2.3.4 --peer-subnets 10.200.0.0/16 --pre-shared-secret foobar v2.softlayer.com
''')
parser.add_argument('vyatta', metavar='gatewayname',
    help='The name of the gateway. If it is a gateway appliance, specify the short name.  If it is a gateway virtual server, specify the fully qualified domain name.')
parser.add_argument('--vlans', metavar='associatedvlans', required=False,
    help='A comma separated list of the VLANs to be associated to the gateway. These are the VLANs that this gateway is providing firewall and routing services for. Each VLAN must be specified like <vlanNum>.<routerHostname>, e.g. 785.bcr02a.hou02. This argument is required for a gateway appliance, but can not be specified for a gateway virtual server.')
parser.add_argument('--peer-gw-ip', metavar='ip', required=False,
    help='The IP of the other gateway that this gateway will be communicating with via a tunnel. Required when configuring a tunnel.')
parser.add_argument('--zone-vlans', metavar='zonevlans',
    help='Which VLANs you want in your APP and DMZ zones. The format of this option is: APP:vlanname,DMZ:vlanname, where vlanname is of the form <vlanNum>.<routerHostname>. Either zone or the whole option can be omitted. All associated vlans not specified will be put in the PRIV zone.')
parser.add_argument('--peer-subnets', metavar='subnets', required=False,
    help='(Required if configuring a tunnel.) A comma separated list of the subnets the gateway at the other end of the tunnel is a gateway for. A route will be created for each subnet to send traffic for it down this tunnel. If specifying --nat-byoip, each peer subnet entry must be 2 IP ranges separated by ":", indicating what the peer subnet should be NATed to.')
parser.add_argument('--pre-shared-secret', metavar='pw', required=False,
    help='Password the 2 gateways should use to establish the IPsec tunnel. If not specified, it will not create an IPSect tunnel (it will only create a GRE tunnel).')
parser.add_argument('--gre-ip', metavar='subnet',
    help='An IP address in a small subnet (/30) to use for the GRE endpoint of this gateway. You must append the network prefix length (/30) to the IP address. This assumes the GRE IP address of the other end of the tunnel is set to the only other usable address in the subnet. If not specified, it will not create a GRE tunnel.')
parser.add_argument('--byoip-subnets', metavar='subnets',
    help='The list of the private subnets you want to bring to SoftLayer. Which VLAN you want each subnet on must be specified, so the format of this option must be a comma separated list of vlan:subnet, where vlan is of the form <vlanNum>.<routerHostname>. If you want multiple subnets on the same vlan, repeat vlan:subnet. This flag will result in the gateway being configured to have the first IP address in each subnet, so it can route for each of those subnets.')
parser.add_argument("--pbr-nat", action="store_true",
    help="Configure the gateway with PBR and NAT for the traffic to the SoftLayer shared services. This allows the on-prem and BYO IPs to overlap with 10.0.0.0/14 without having to NAT the traffic through the tunnel between on-prem and the customer's SL machines.")
parser.add_argument("--nat-byoip", action="store_true",
    help="NAT the traffic through the tunnel so on-prem and BYO IPs can overlap with all of 10.0.0.0/8. When using this option, the NAT mapping is specified in the --peer-subnets and --byoip-subnets flags. See the description of those flags.")
parser.add_argument("--masquerade", action="store_true",
    help="Configure NAT masquerading of the customer's SL machine private IP addresses so they can access the internet without public NICs.")
parser.add_argument('--ipsec-encryption', metavar='encryption',
    help='IPsec tunnel encryption key type and size (for both IKE and ESP). Valid values: aes256 (default), aes128, 3des.')
parser.add_argument('--ipsec-hash', metavar='hash',
    help='IPsec tunnel hash method (for both IKE and ESP). Valid values: sha1 (default), md5.')
parser.add_argument('--ipsec-ike-lifetime', metavar='seconds',
    help='IPsec tunnel IKE lifetime in seconds. Default is 86400.')
parser.add_argument('--ipsec-esp-lifetime', metavar='seconds',
    help='IPsec tunnel ESP lifetime in seconds. Default is 3600.')
parser.add_argument('--diffie-hellman-group', metavar='num',
    help='IPsec tunnel IKE Diffie-Hellman group number. Valid values: 5 (default), 2.')
parser.add_argument("--add-tunnel", action="store_true",
    help="Add this tunnel, instead of replacing any existing tunnel. This option assumes you have run config-gw.py for this gateway before, so it will not associate the vlans and it will only add the new firewall zone configuration needed for this tunnel, not the entire default firewall configuration.")
parser.add_argument("--wait-for-gw", metavar='minutes',
    help="Wait up to this many minutes for the gateway to finish being provisioned. Use this flag if you want to run this command immediately after running order-gw.py, so that it will wait until the gateway has been provisioned by SoftLayer before starting the configuration of the gateway. Vyatta gateway appliances (bare metal) usually take about 2 hours to be provisioned, but sometimes take longer. Vyatta virtual servers usually take 5-10 minutes to be provisioned but sometimes take longer.")
parser.add_argument('--gaashost', metavar='url', required=False,
    help='The GaaS REST API server, i.e. the 1st part of the URL for the REST API calls, e.g. https://svr1 . If not specified, it will use the environment variable GAASHOST. If neither are specified, it will use the production GaaS server.')
parser.add_argument("--dryrun", action="store_true",
    help="Do not actually modify this gateway. For the REST API calls that normally make configuration changes on the gateway, display the commands that would be run instead.")
parser.add_argument('-v', "--verbose", action="store_true",
    help="display verbose output")

def waitForVlans(vlans, mode, pollInterval):
    '''Wait for the vlans to be associated to the gw in either bypassed or routed mode.
    Returns False if it times out before it finds the vlans in the correct state.'''
    # wait until the procedure is done and the vlans are associated
    for i in range(1,100):
        time.sleep(pollInterval)
        response = cliutils.get(gaashost, '/gateways/'+gw+'/detail')
        if response['status']['name'] != 'Active':
            sys.stdout.write('.')
            sys.stdout.flush()
            continue
        # gw is active, check that the vlans are associated, to make sure we did not catch it before it started
        insideVlans = {}        # put the gw's vlans in this dict to make it easier to check that they are all there
        for iv in response['insideVlans']:  insideVlans[str(iv['networkVlan']['vlanNumber'])] = iv['bypassFlag']
        notFound = False
        for v in vlans:
            if v not in insideVlans:
                notFound = True
                break
            elif mode=='routed' and insideVlans[v]==True:       # we wanted it routed but bypassFlag was true
                notFound = True
                break
            # else if the mode wanted is bypassed, we do not care if it is already routed
        if notFound:  continue
        # if we got this far the gw was active and all the vlans were associated
        print ''        # print a newline after all the dots
        return True
    print ''        # print a newline after all the dots
    return False


# main

# Check input
args = parser.parse_args()
# pprint.pprint(args)
cliutils.getSlCredentials()      # this will save them for use, or exit with an error msg
# if 'SLUSERNAME' not in os.environ or 'SLAPIKEY' not in os.environ:
#     parser.print_help()
# do not think we need test mode, now that we have the dryrun flag
# if 'GAAS_REST_TEST_MODE' in os.environ:
#     testMode = True
#     print 'Note:  running in test mode, the gateway will not be modified.'
# else:  testMode = False

if args.verbose:  cliutils.setVerbose(True)
if args.dryrun:  dryrunParams = {'dryrun':1}
else:  dryrunParams = None
gw = args.vyatta
gaashost = cliutils.getGaasHost(args)
if gw.find('.') == -1:
    appliance = True
    if args.peer_subnets and not args.vlans:  cliutils.error(2, '--vlans must be specified for a gateway appliance if configuring a tunnel.')
else:
    appliance = False
    if args.vlans:  cliutils.error(2, '--vlans can not be specified for a gateway virtual server.')

# We now allow no tunnel, only firewall, and maybe masquerade. We also allow adding only a tunnel
if args.add_tunnel:
    if not args.peer_subnets:
        cliutils.error(2, 'Must specify --peer-subnets if specifying --add-tunnel')
    if args.vlans or args.zone_vlans:
        cliutils.error(2, 'Do not specify --vlans or --zone-vlans when specifying --add-tunnel')
if args.peer_gw_ip or args.peer_subnets:
    if not args.peer_gw_ip:
        cliutils.error(2, 'Must specify --peer-gw-ip when configuring a tunnel')
    if not args.peer_subnets:
        cliutils.error(2, 'Must specify --peer-subnets when configuring a tunnel')
    if not args.pre_shared_secret and not args.gre_ip:
        cliutils.error(2, 'Must specify --pre-shared-secret or --gre-ip when configuring a tunnel')
else:       # peer-subnets not specified
    if args.pre_shared_secret or args.gre_ip or args.byoip_subnets or args.pbr_nat or args.nat_byoip:
        cliutils.error(2, 'Must specify --peer-subnets when configuring a tunnel')
if not args.pre_shared_secret:
    if args.ipsec_encryption or args.ipsec_hash or args.ipsec_ike_lifetime or args.ipsec_esp_lifetime or args.diffie_hellman_group:
        cliutils.error(2, 'Must specify --pre-shared-secret when configuring an IPSec tunnel')
if args.byoip_subnets and not args.gre_ip:
    cliutils.error(2, 'If --byoip-subnets is specified, --gre-ip must also be specified')
if args.pbr_nat and not args.gre_ip:
    cliutils.error(2, 'If --pbr-nat is specified, --gre-ip must also be specified')
if args.pbr_nat and args.nat_byoip:
    cliutils.error(2, 'Can not specify both --pbr-nat and --nat-byoip')
if args.masquerade and args.pre_shared_secret and not args.gre_ip:
    cliutils.error(2, 'If --masquerade and --pre-shared-secret are specified, --gre-ip must also be specified')


print 'Checking permissions...'
# make sure they have the SL permissions needed to complete the task.  This will also kick out
# if they do not have a valid SL username and api key.
# requiredPermissions = ['Manage Network Gateways', 'View Hardware', 'add server', 'IPSEC Network Tunnel', 'View CloudLayer Computing Instances', 'Access all hardware', 'Hardware Firewall']
requiredPermissions = []        # using an empty list tells GaaS to check for the minimum set of permissions needed for GaaS
response = cliutils.post(gaashost, '/user/permissions', requiredPermissions)
if 'unmet-permissions' in response:
    cliutils.error(2, 'you need the following SoftLayer permissions to configure the vyatta:'+', '.join(response['unmet-permissions']))



# ensure the gateway exists and is not still in the process of being provisioned
if args.wait_for_gw:
    print 'Waiting for gateway to be provisioned (up to '+args.wait_for_gw+' minutes)...'
    numberOfChecks = 4 * int(args.wait_for_gw)           # we will check every 15 seconds
else:
    print 'Checking gateway...'
    numberOfChecks = 1
gwReady = False
for i in range(numberOfChecks):
    gwresponse = cliutils.get(gaashost, '/gateways/'+gw+'/detail', returnErrors=True)   # this returns its state, vlans, IPs, router, etc.
    if 'error-code' in gwresponse:
        if gwresponse['error-code']==405 and 'ateway not found' in gwresponse['error-msg']:
            if args.wait_for_gw:
                # maybe it does not exist yet because it has not been provisioned yet
                print 'Gateway does not exist yet, still waiting...'
                time.sleep(15)
                continue
            else:
                cliutils.error(2, 'gateway '+gw+' does not exist')
        else:
            # some unknown error
            cliutils.error(2, 'error from GET /gateways/'+gw+'/detail: '+str(gwresponse['error-code'])+', '+gwresponse['error-msg'])
    # if 'status' in gwresponse and gwresponse['status']['name'] == 'Active' and (appliance or not len(gwresponse['activeTransactions'])):
    if 'status' in gwresponse and gwresponse['status']['name'] == 'Active':
        # print 'app:', str(appliance), ' trans:', str(len(gwresponse['activeTransactions']))
        if appliance or (len(gwresponse['activeTransactions'])==0 and gwresponse['provisionDate']):      # sometimes we catch the activeTransactions before they have started, so also check provisionDate
            # pprint.pprint(gwresponse)
            print 'Gateway is ready, starting configuration...'
            gwReady = True
            break
        if not appliance:  print 'Gateway not ready yet, activeTransactions: '+str(gwresponse['activeTransactions'])+', provisionDate: '+gwresponse['provisionDate']
    else:
        print 'Gateway not ready yet, status: '+gwresponse['status']['name']
    # we get here if the gw is not ready yet
    if args.wait_for_gw:
        # print 'Gateway not ready yet, still waiting...'
        time.sleep(15)

if not gwReady:
    # status = 'status: '+gwresponse['status']['name']
    # if not appliance:  status += ', active transaction: '+','.join(gwresponse['activeTransactions'])
    cliutils.error(2, 'gateway '+gw+' is still in the process of being provisioned')



if appliance and args.vlans:
    print 'Verifying VLANs...'
    gwBackendRouter = gwresponse['privateVlan']['primaryRouter']['hostname']
    gwFrontendRouter = gwresponse['publicVlan']['primaryRouter']['hostname']
    # remember its associated vlans for the next step too
    insideVlans = []
    for iv in gwresponse['insideVlans']:  insideVlans.append(str(iv['networkVlan']['vlanNumber']))
    # ensure the vlans exist, they are not transit vlans, they are not already associated with another vyatta,
    # and they are on the same backend router as this vyatta
    vlans = args.vlans.split(',')       # this is also used in later steps
    acctVlans = cliutils.get(gaashost, '/account/vlans')        # the resulting dictionary will be keyed by vlan number. This is also used in later steps
    for v in vlans:
        if v.find('.') == -1:  cliutils.error(2, 'VLAN '+v+' must have the router hostname appended to make it unique.')
        if v not in acctVlans:  cliutils.error(2, 'invalid VLAN specified: '+v)
        if acctVlans[v]['isTransitVlan']:  cliutils.error(2, 'VLAN '+v+' is a transit VLAN, it can not be associated to a gateway.')
        if acctVlans[v]['isAssociatedVlan'] and v not in insideVlans:  cliutils.error(2, 'VLAN '+v+' is already associated to another gateway.')
        if acctVlans[v]['router'] != gwBackendRouter and acctVlans[v]['router'] != gwFrontendRouter:
            cliutils.error(2, 'VLAN '+v+' is not on the same backend or frontend router ('+acctVlans[v]['router']+') as gateway '+gw+' is ('+gwBackendRouter+', '+gwFrontendRouter+').')



if args.peer_subnets:
    print 'Checking reserved IP ranges...'
    if appliance:  gwDatacenter = gwresponse['members'][0]['hardware']['datacenter']['name']
    else:  gwDatacenter = gwresponse['datacenter']['name']
    # ensure the subnets they gave us do not overlap with the reserved ones
    if args.pbr_nat:  params = {'excludeSlRange':1}
    else:  params = None
    response = cliutils.get(gaashost, '/softlayer/datacenters/'+gwDatacenter+'/reservedipranges', params=params)      # response will be an array of subnet strings
    # check both peer-subnets and byoip-subnets
    #todo: steal code from dave to do real ip checking
    if args.nat_byoip:
        # entries for nat byoip are of the form subnet:tosubnet
        subnets = []
        for s in args.peer_subnets.split(','):
            parts = s.split(':')
            if len(parts) >= 2:  subnets.append(parts[1])  # only check the 2nd range they give us for each subnet
    else:
        subnets = args.peer_subnets.split(',')
    if args.byoip_subnets and not args.nat_byoip:
        for b in args.byoip_subnets.split(','):
            parts = b.split(':')        # each entry is the form vlan:subnet
            if len(parts) >= 2:  subnets.append(parts[1])
    for s in subnets:
        if s in response:
            # cliutils.error(2, 'specified subnet '+s+' is reserved by SoftLayer')
            print 'Warning: specified subnet '+s+' is reserved by SoftLayer'



if appliance and not args.add_tunnel and not args.dryrun:
    print 'Associating VLANs to gateway...'
    # build input body
    body = {}
    for v in vlans:  body[v] = 'bypassed'
    # associate the vlans in bypassed mode
    response = cliutils.put(gaashost, '/gateways/'+gw+'/vlans', data=body)

    pollInterval = 3
    print 'Waiting for VLANs to be associated (polling every '+str(pollInterval)+' seconds).',
    sys.stdout.flush()
    if not waitForVlans(vlans,'bypassed',pollInterval):  cliutils.error(2, 'timed out waiting for the VLANs to be associated')



print 'Enabling the vyatta REST API...'
response = cliutils.post(gaashost, '/gateways/'+gw+'/api', params=dryrunParams)
if args.dryrun:  pprint.pprint(response)



if not args.add_tunnel:
    print 'Configuring the firewall...'
    # build body input structure for the firewall zones
    body = {}
    if args.peer_gw_ip:  body["on-prem-gateway-ip"] = args.peer_gw_ip
    if args.zone_vlans:
        zvlans = {}
        for z in args.zone_vlans.split(','):
            parts = z.split(':')
            if len(parts) != 2:  cliutils.error(2, 'invalid format for zone-vlans option')
            zvlans[parts[0]] = [parts[1]]
        body['zone-vlans'] = zvlans
    response = cliutils.put(gaashost, '/gateways/'+gw+'/zones', body, params=dryrunParams)
    if args.dryrun:  pprint.pprint(response)



if appliance and not args.add_tunnel and not args.dryrun:
    print 'Changing VLANs to routed...'
    # build input body
    body = {}
    for v in vlans:  body[v] = 'routed'
    # associate the vlans in bypassed mode
    response = cliutils.put(gaashost, '/gateways/'+gw+'/vlans', data=body)

    pollInterval = 3
    print 'Waiting for VLANs to be routed (polling every '+str(pollInterval)+' seconds).',
    sys.stdout.flush()
    if not waitForVlans(vlans,'routed',pollInterval):  cliutils.error(2, 'timed out waiting for the VLANs to become routed')


if args.masquerade:
    print 'Configuring NAT masquerading...'
    if args.byoip_subnets:
        # build the byoip subnet list
        byoipList = []
        for b in args.byoip_subnets.split(','):
            parts = b.split(':')        # separate the vlan and subnet
            if len(parts) != 2:  cliutils.error(2, 'invalid format for --byoip-subnets')
            byoipList.append(parts[1])
        # now add it to the body
        body["byoip-subnets"] = byoipList
    else:
        body = None
    response = cliutils.put(gaashost, '/gateways/'+gw+'/masquerade', body, params=dryrunParams)
    if args.dryrun:  pprint.pprint(response)


if args.peer_gw_ip and args.peer_subnets:
    if args.pbr_nat:  print 'Configuring the IPSec and GRE tunnels with PBR/NAT...'
    elif args.nat_byoip:  print 'Configuring the IPSec and GRE tunnels with NAT BYOIP...'
    elif args.gre_ip and args.pre_shared_secret:  print 'Configuring the IPSec and GRE tunnels...'
    elif args.pre_shared_secret:  print 'Configuring the IPSec tunnel...'
    elif args.gre_ip:  print 'Configuring the GRE tunnel...'
    body = {
        "peer-gateway-ip":args.peer_gw_ip,
    }
    if args.nat_byoip:
        # build the correct 2 dimensional list of the subnets. peer-subnets is like "sub1a:sub1b,sub2a:sub2b"
        peerSubnets = []
        for s in args.peer_subnets.split(','):
            peerSubnets.append((s.split(':')))
        body['peer-subnets'] = peerSubnets
    else:
        body['peer-subnets'] = args.peer_subnets.split(',')
    if args.gre_ip: body["gre-ip"] = args.gre_ip
    if args.pbr_nat: body["use-pbr-nat2"] = 1           # eventually change this back to use-pbr-nat
    if args.nat_byoip: body["use-nat-byoip"] = 1
    if args.pre_shared_secret:
        body['pre-shared-secret'] = args.pre_shared_secret
        if args.ipsec_encryption: body["ipsec-encryption"] = args.ipsec_encryption
        if args.ipsec_hash: body["ipsec-hash"] = args.ipsec_hash
        if args.ipsec_ike_lifetime: body["ipsec-ike-lifetime"] = args.ipsec_ike_lifetime
        if args.ipsec_esp_lifetime: body["ipsec-esp-lifetime"] = args.ipsec_esp_lifetime
        if args.diffie_hellman_group: body["ike-diffie-hellman-group"] = args.diffie_hellman_group

    if args.byoip_subnets:
        # 1st build the byoip structure like:  {"2536.bcr01a.sjc01":["10.230.230.0/24"]}
        byoip = {}          # this is also used in a later step
        for b in args.byoip_subnets.split(','):
            parts = b.split(':')        # separate the vlan and subnet
            if len(parts) != 2:  cliutils.error(2, 'invalid format for --byoip-subnets')
            vlan, subnet = parts
            if vlan not in byoip:  byoip[vlan] = []
            byoip[vlan].append(subnet)
        # now add it to the body
        body["byoip-subnets"] = byoip
    else:
        byoip = None

    if args.add_tunnel:  response = cliutils.put(gaashost, '/gateways/'+gw+'/tunnels/'+args.peer_gw_ip, body, params=dryrunParams)
    else:  response = cliutils.put(gaashost, '/gateways/'+gw+'/tunnels', body, params=dryrunParams)
    if args.dryrun:  pprint.pprint(response)



filename = '/tmp/config.boot.'+datetime.datetime.today().strftime('%Y-%m-%d--%H-%M-%S')
print 'Getting gateway configuration file and saving it to '+filename+'...'
config = cliutils.get(gaashost, '/gateways/'+gw+'/configfile')
f = open(filename, 'w')
f.write(config)
f.close()


if args.peer_gw_ip and args.peer_subnets:
    print 'Getting the settings to be used for configuring the peer gateway...'
    settings = cliutils.get(gaashost, '/gateways/'+gw+'/settings', params={'peer-gateway-ip':args.peer_gw_ip})   # this returns a dict with the settings they should use in the peer gw

    print 'The SoftLayer gateway '+gw+' is now ready. Configure your corresponding peer gateway with these parameters:'
    # print it in json format, so it is more standard, and also to get rid of the unicode 'u' prefixes
    print json.dumps(settings, indent=4)


print 'Gateway configuration completed successfully.'
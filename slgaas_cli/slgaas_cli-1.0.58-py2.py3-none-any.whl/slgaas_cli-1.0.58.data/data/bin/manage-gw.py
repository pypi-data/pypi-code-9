#!/usr/bin/env python

# Run various GaaS REST API calls to manage the gateway.

import json
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
    description='''Run various operations to view or manage your gateway using the GaaS REST API.

Cmds supported:
  get-sl-detail - get information about this gateway from the SoftLayer API
  get-vlans - get information about the vlans associated with this gateway
  test-gw-api - see if the gateway API is set up and working
  init-gw-api - set up the gateway API
  get-zone-list - get the list of firewall zones defined on this gateway
  get-zone <zonename> - get details of this zone
  get-ruleset <rulesetname> - get details of this firewall rule set
  add-rules <rulesetname> "<rule>" "<rule>" - add/change rules to this rule set
  delete-rules <rulesetname> "<rule>" "<rule>" - remove rules to this rule set
  get-masquerade - get details about the NAT maquerade that is defined on this gateway
  get-tunnel-list - get a summary of each tunnel defined on the gateway
  get-tunnel <peer-ip> - get details of this tunnel
  get-tunnel-stats - get the byte transfer statistics for all the tunnels
  get-tunnel-settings <peer-ip> - get tunnel settings to use for configuring the other end of the tunnel
  get-configfile - get the content of the current gateway configuration file
  run-cmds "cmd1" "cmd2" - run non-configuration commands on the gateway
  commit-cmds "cmd1" "cmd2" - commit configuration commands on the gateway
  get-auditlog <begin-time> [<end-time>] - get the auditlog records for this user and gateway, where begin-time is like 2015-05-19.''',
    epilog='''In addition to the options below, you also need to set environment variables
SLUSERNAME and SLAPIKEY, or have them in your ~/.softlayer file.

EXAMPLES:

# Get the byte transfer statistics for all the tunnels on this gateway
manage-gw.py v1 get-tunnel-stats

# Run commands on this gateway
manage-gw.py v1 run-cmds "cmd1" "cmd2"
''')
parser.add_argument('gw', metavar='gatewayname', # nargs=1,
    help='The name of the gateway. Either include the domain name in this name or specify it with --domain')
parser.add_argument('cmd', metavar='cmd', # nargs=1,
    help='The operation to be run on this gateway')
parser.add_argument('params', metavar='parameters', nargs='*',
    help='Parameters specific to this operation')
parser.add_argument('--gaashost', metavar='url', required=False,
    help='the GaaS REST API server, i.e. the 1st part of the URL for the REST API calls, e.g. https://svr1 . If not specified, it will use the environment variable GAASHOST. If neither are specified, it will use the production GaaS server.')
parser.add_argument("--dryrun", action="store_true",
    help="Do not actually modify this gateway. For the REST API calls that normally make configuration changes on the gateway, display the commands that would be run instead.")
parser.add_argument('-v', "--verbose", action="store_true",
    help="display verbose output")


# main

# Check input
args = parser.parse_args()
# pprint.pprint(args)
username, apikey = cliutils.getSlCredentials()      # this will save them for use, or exit with an error msg
gaashost = cliutils.getGaasHost(args)
if args.verbose:  cliutils.setVerbose(True)
if args.dryrun:  dryrunParams = {'dryrun':1}
else:  dryrunParams = None


if args.cmd == 'get-sl-detail':
    response = cliutils.get(gaashost, '/gateways/'+args.gw+'/detail')
    # models = cliutils.get(gaashost, '/gateways/hardware/models', params=params)
    pprint.pprint(response)
    sys.exit()
elif args.cmd == 'get-vlans':
    response = cliutils.get(gaashost, '/gateways/'+args.gw+'/vlans')
    pprint.pprint(response)
    sys.exit()
elif args.cmd == 'test-gw-api':
    response = cliutils.get(gaashost, '/gateways/'+args.gw+'/api')
    pprint.pprint(response)
    sys.exit()
elif args.cmd == 'init-gw-api':
    response = cliutils.post(gaashost, '/gateways/'+args.gw+'/api', params=dryrunParams)
    pprint.pprint(response)
    sys.exit()
elif args.cmd == 'get-zone-list':
    response = cliutils.get(gaashost, '/gateways/'+args.gw+'/zones', params={'summary':'1'})
    pprint.pprint(response)
    sys.exit()
elif args.cmd == 'get-zone':
    if not args.params:  cliutils.error(2, 'zone name required as parameter')
    response = cliutils.get(gaashost, '/gateways/'+args.gw+'/zones/'+args.params[0])
    pprint.pprint(response)
    sys.exit()
elif args.cmd == 'get-ruleset':
    if not args.params:  cliutils.error(2, 'rule set name required as parameter')
    response = cliutils.get(gaashost, '/gateways/'+args.gw+'/ruleset/'+args.params[0])
    pprint.pprint(response)
    sys.exit()
elif args.cmd == 'add-rules':
    if not args.params or len(args.params)<2:  cliutils.error(2, 'rule set name and rules are required as parameters')
    rulesetName = args.params[0]
    rules = args.params[1:]
    # rules = ' '.join(args.params[1:])       # from the shell, each word is an element in the list. join them all, then split on comma
    # rules = rules.split(',')
    # pprint.pprint(rules)
    # sys.exit()
    # {"add-rules":["rule 25 action accept","rule 25 protocol tcp","rule 25 destination port 12345"]}
    body = {"add-rules": rules }
    response = cliutils.put(gaashost, '/gateways/'+args.gw+'/ruleset/'+rulesetName, body, params=dryrunParams)
    pprint.pprint(response)
    sys.exit()
elif args.cmd == 'delete-rules':
    if not args.params or len(args.params)<2:  cliutils.error(2, 'rule set name and rules are required as parameters')
    rulesetName = args.params[0]
    rules = args.params[1:]
    body = {"delete-rules": rules }
    response = cliutils.put(gaashost, '/gateways/'+args.gw+'/ruleset/'+rulesetName, body, params=dryrunParams)
    pprint.pprint(response)
    sys.exit()
elif args.cmd == 'get-masquerade':
    response = cliutils.get(gaashost, '/gateways/'+args.gw+'/masquerade')
    pprint.pprint(response)
    sys.exit()
elif args.cmd == 'get-tunnel-list':
    response = cliutils.get(gaashost, '/gateways/'+args.gw+'/tunnels', params={'list':'1'})
    pprint.pprint(response)
    sys.exit()
elif args.cmd == 'get-tunnel':
    if not args.params:  cliutils.error(2, 'tunnel peer IP required as parameter')
    response = cliutils.get(gaashost, '/gateways/'+args.gw+'/tunnels/'+args.params[0])
    pprint.pprint(response)
    sys.exit()
elif args.cmd == 'get-tunnel-stats':
    response = cliutils.get(gaashost, '/gateways/'+args.gw+'/tunnels/all/stats')
    pprint.pprint(response)
    sys.exit()
elif args.cmd == 'get-tunnel-settings':
    if not args.params:  cliutils.error(2, 'tunnel peer IP required as parameter')
    response = cliutils.get(gaashost, '/gateways/'+args.gw+'/settings', params={'peer-gateway-ip':args.params[0]})
    pprint.pprint(response)
    sys.exit()
elif args.cmd == 'get-configfile':
    response = cliutils.get(gaashost, '/gateways/'+args.gw+'/configfile')
    print response
    sys.exit()
elif args.cmd == 'run-cmds':
    if not args.params or len(args.params)<1:  cliutils.error(2, 'the commands to run are required as parameters')
    body = {"commands": args.params }
    response = cliutils.post(gaashost, '/gateways/'+args.gw+'/native', body, params=dryrunParams)
    pprint.pprint(response)
    sys.exit()
elif args.cmd == 'commit-cmds':
    if not args.params or len(args.params)<1:  cliutils.error(2, 'the commands to commit are required as parameters')
    body = {"commands": args.params }
    response = cliutils.put(gaashost, '/gateways/'+args.gw+'/native', body, params=dryrunParams)
    pprint.pprint(response)
    sys.exit()
elif args.cmd == 'get-auditlog':
    params = {'endtime':'END'}
    if not args.params or len(args.params)<1:  cliutils.error(2, 'at least the begin time must be specified as a parameter')
    params['begintime'] = args.params[0]
    if len(args.params) >= 2:
        params['endtime'] = args.params[1]
    response = cliutils.get(gaashost, '/gateways/'+args.gw+'/auditlog/'+username, params=params)
    pprint.pprint(response)
    sys.exit()
else:
    cliutils.error(2, 'cmd '+args.cmd+' unrecognized')

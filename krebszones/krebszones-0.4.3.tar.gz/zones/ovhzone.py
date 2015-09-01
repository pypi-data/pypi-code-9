#!/usr/bin/env python3
""" usage:
        ovh-zone [--config <file>] import <zonefile> [<zonename>]
        ovh-zone [--config <file>] export <zonename>
        ovh-zone [--config <file>] get-consumer-key

    --config <json-file>        points to a json file with the following
                                fields:

                                {   "APP_KEY": "x",
                                    "REGION": "ovh-eu",
                                    "APP_SECRET": "x",
                                    "CONSUMER_KEY":"x" }

                                REGION is optional and defaults to ovh-eu

    if --config is not given the script will fall back to environment variables
    with the same keys as the config file.

    if the zonefile basename is different from the zonename then an additional
    zonename can be provided as second parameter


    To create a new Application, go to https://eu.api.ovh.com/createApp/
    then configure either environment or configuration file with the app key
    and secret.

    after that run `ovh-zone get-consumer-key` to get a consumer key
"""

from functools import partial
import sys
log = partial(print,file=sys.stderr)

def testLogin(client):
    try:
        me= client.get('/me')
        log("Logged in as {} ({})".format(me['nichandle'],me['email']))
    except ovh.APIError as e:
        log("Failed to log in, bailing out: {}".format(e))
        sys.exit(1)
    except Exception as e:
        log("Failed to connect: {}".format(e))
        sys.exit(1)

def main():
    import os
    import ovh
    from docopt import docopt
    args=docopt(__doc__)
    zonefile = args['<zonefile>']
    cfgfile= args['--config']

    if not cfgfile:
        log("using environment vars")
        cfg = os.environ
    else:
        import json
        log("using config file")
        with open(cfgfile) as f:
            cfg = json.load(f)

    client = ovh.client.Client(
        cfg.get('REGION','ovh-eu'),
        cfg['APP_KEY'],
        cfg['APP_SECRET'],
        cfg.get('CONSUMER_KEY',None))

    if args['import']:
        import os.path
        testLogin(client)
        zn = args['<zonename>']
        zonename = zn if zn else os.path.basename(zonefile)
        log("beginning zone upload of {} with file {}".format(zonename,zonefile))
        with open(zonefile) as f:
            print(client.post('/domain/zone/{}/import'.format(zonename),zoneFile=f.read()))

    elif args['export']:
        testLogin(client)
        print(client.get('/domain/zone/{}/export'.format(args['<zonename>'])))

    elif args['get-consumer-key']:
        log('trying to request a consumer key ')
        rules = [ {'method': 'GET', 'path':'/me' },
                {'method': 'POST', 'path':'/domain/zone/*' },
                {'method': 'GET', 'path':'/domain/zone/*' } ]
        try:
            validation = client.request_consumerkey(rules)
        except ovh.APIError as e:
            log("Failed to request consumer key, bailing out: {}".format(e))
            sys.exit(1)

        log("Please visit {} to authenticate".format(
            validation['validationUrl']))
        log("\nAfter authentication you can use the following Consumer Key : {}".format(client._consumer_key))

if __name__ == '__main__':
    main()

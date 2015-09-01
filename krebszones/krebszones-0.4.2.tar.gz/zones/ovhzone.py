#!/usr/bin/env python3
""" usage:
        ovh-zone [--config <file>] import <zonefile> [<zonename>]
        ovh-zone [--config <file>] export <zonename>

    --config <json-file>        points to a json file with the following
                                fields:

                                {   "APP_KEY": "x",
                                    "REGION": "ovh-eu",
                                    "APP_SECRET": "x",
                                    "CONSUMER_KEY":"x" }

                                REGION is optional and defaults to ovh-eu
                                CONSUMER_KEY is optional and may be requested
                                if not given

    if --config is not given the script will fall back to environment variables
    with the same keys as the config file.

    if the zonefile basename is different from the zonename then an additional
    zonename can be provided as second parameter

    To create a new Application, go to https://eu.api.ovh.com/createApp/
"""

from functools import partial
import sys
log = partial(print,file=sys.stderr)

def main():
    import os
    import ovh
    from docopt import docopt
    args=docopt(__doc__)
    zonefile = args['<zonefile>']
    cfgfile= args['--config']
    if not cfgfile:
        log("using environment vars")
        env = os.environ
    else:
        import json
        log("using config file")
        with open(cfgfile) as f:
            env = json.load(f)

    client = ovh.client.Client(
        env.get('REGION','ovh-eu'),
        env['APP_KEY'],
        env['APP_SECRET'],
        env.get('CONSUMER_KEY',None))

    if not client._consumer_key:
        log('trying to retrieve the consumer key as none is given')
        rules = [
                {'method': 'GET', 'path':'/me' },
                {'method': 'POST', 'path':'/domain/zone/*' },
                {'method': 'GET', 'path':'/domain/zone/*' }
                ]
        validation = client.request_consumerkey(rules)
        log("Please visit {} to authenticate".format(
            validation['validationUrl']))
        raw_input("and press Enter to continue")
        log("The Consumer Key is {}".format(client._consumer_key))
    try:
        me= client.get('/me')
        log("Logged in as {} ({})".format(me['nichandle'],me['email']))
    except ovh.APIError as e:
        log("Failed to log in, bailing out: {}".format(e))
        sys.exit(1)
    except Exception as e:
        log("Failed to connect: {}".format(e))
        sys.exit(1)


    if args['import']:
        import os.path
        zn = args['<zonename>']
        zonename = zn if zn else os.path.basename(zonefile)
        log("beginning zone upload of {} with file {}".format(zonename,zonefile))
        with open(zonefile) as f:
            print(client.post('/domain/zone/{}/import'.format(zonename),zoneFile=f.read()))
    elif args['export']:
        print(client.get('/domain/zone/{}/export'.format(args['<zonename>'])))


if __name__ == '__main__':
    main()

import argparse
import sys

store_host_port = 'localhost:5000'
proxy_host_port = 'localhost:7010'
store_name = 'kvstore'


def add_runtime_params():
    parser = argparse.ArgumentParser()
    parser.add_argument('--storehostport',
                        help='specify the host and port of the store to use')
    parser.add_argument('--proxyhostport',
                        help='specify the host and port of the proxy to use')
    parser.add_argument('--storename',
                        help='specify the store name to use')
    args = parser.parse_args()
    global store_host_port
    global proxy_host_port
    global store_name
    if (args.storehostport is not None):
        store_host_port = args.storehostport
    if (args.proxyhostport is not None):
        proxy_host_port = args.proxyhostport
    if (args.storename is not None):
        store_name = args.storename
    del sys.argv[1:]
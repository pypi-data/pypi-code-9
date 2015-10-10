#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import logging
from .log import setup_logging

setup_logging()
logger = logging.getLogger('graphalviz')

from .settings import SERVER_HOST, SERVER_PORT
from . import get_version_str


def main():
    parser = argparse.ArgumentParser(description='Graph plot tool')
    ex_group = parser.add_mutually_exclusive_group()
    ex_group.add_argument(
        '-s', '--server', required=False, help='run graphalviz server',
        action='store_true'
    )
    ex_group.add_argument(
        '-c', '--client', required=False, help='run graphalviz clinet',
        action='store_true'
    )
    parser.add_argument(
        '-H', '--host', required=False, help='host address',
        default=SERVER_HOST
    )
    parser.add_argument(
        '-P', '--port', required=False, help='host port',
        default=SERVER_PORT
    )
    parser.add_argument(
        '-r', '--refresh-on-change', required=False,
        help='refresh plot on each update', action='store_true'
    )
    # TODO: implement direct load of file
    # parser.add_argument(
    #     '-f', '--file', type=file, required=False, help='load graph from file'
    # )
    parser.add_argument(
        '-l', '--loglevel', required=False, help='set log level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    )
    parser.add_argument(
        '--version', action='version',
        version='GraphAlViz version {}'.format(get_version_str())
    )

    args = parser.parse_args()

    if args.loglevel:
        logger.setLevel(args.loglevel)

    if args.server:
        from .server import main as server_main
        logger.debug('Running graphalviz as server')
        server_main(
            host=args.host,
            port=args.port,
            refresh_on_change=args.refresh_on_change
        )

    if args.client:
        # TODO: implement a client console
        print(
            'The client side is currently implemented as library '
            '(graphalviz.client) and not a stand alone app'
        )


if __name__ == '__main__':
    main()

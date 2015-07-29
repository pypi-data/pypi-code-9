#!/usr/bin/env python
import sys
import os
import argparse
import traceback
import signal
import time
import logging

from multiprocessing import Pool
from cPickle import load
import MySQLdb

logging.basicConfig()
log = logging.getLogger(__name__)


def load_inputs(output_dir):
    return ['%s/%s' % (output_dir, f) for f in os.listdir(output_dir) if f.endswith('.data')]

def make_client(args):
    return MySQLdb.connect(user=args.user, passwd=args.password,
                           host=args.host, port=args.port, connect_timeout=2)

def make_player(input_file):
    global args
    signal.signal(signal.SIGINT, sys.exit)
    player = LogPlayer(make_client(args), input_file)
    return player.start()


class LogPlayer:
    def __init__(self, client, input_file):
        self.file = open(input_file, 'r')
        self.client = client
        self.slower = 0
        self.faster = 0
        self.failed = 0

    def start(self):
        """
        Execute all queries in the input file until there are no more queries
        to execute in the file.
        """
        while 1:
            try:
                query = load(self.file)
                query_time = self.run_query(query)

                if query_time == False:
                    self.failed += 1
                    continue # query failed, continue with the next one

                if query_time > query['query_time']:
                    self.slower += 1
                else:
                    self.faster += 1
            except EOFError:
                break

        return {'faster': self.faster,
                'slower': self.slower,
                'failed': self.failed}

    def run_query(self, query):
        t = time.time()
        c = self.client.cursor()

        # some queries are composed of multiple operations, but connector does
        # not accept them, we need to iterate and run individually
        query_parts = query.query.split(';')

        # if first element in the list is an USE statement remove it
        if (query_parts[0].lower().startswith('use')):
            del(query_parts[0])

        # remove newlines and filter empty parts
        query_parts = [''.join(p.splitlines()) for p in query_parts if p]

        # force the USE statement, the log ommits it for consecutive queries to
        # the same database, but as we can skip block in the prepare script we
        # cannot trust it, fortunately we do have the actual db on the log metadata
        c.execute("USE `%s`" % query.database)
        for part in query_parts:
            try:
                c.execute(part)
                c.fetchall()
            except Exception, e:
                log.error("Query failed: [%s] %s" % e.args)
                return False

        return time.time() - t


def main():
    global args
    parser = argparse.ArgumentParser(
        prog="mysql-replay",
        description="""Execute prepared queries in parallel for benchmarking""")

    parser.add_argument('-u', '--user', help='mysql user', default='root')
    parser.add_argument('-p', '--password', help='mysql password', default='')
    parser.add_argument('-H', '--host', help='mysql host', default='localhost')
    parser.add_argument('-P', '--port', help='mysql port', default=3306)
    parser.add_argument('datadir', help='directory where prepared files are stored')
    args = parser.parse_args()

    inputs = load_inputs(args.datadir)
    p = Pool(len(inputs))
    try:
        results = p.map(make_player, inputs, chunksize=1)
        print results
    except KeyboardInterrupt:
        log.info("Caught SIGINT, exiting....")


if __name__ == "__main__":
    main()

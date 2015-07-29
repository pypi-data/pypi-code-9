#!/usr/bin/env python
import sys
import os
import argparse
import traceback
import signal
import time

from multiprocessing import Pool
from cPickle import load
import MySQLdb


def load_inputs(output_dir):
    return ['%s/%s' % (output_dir, f) for f in os.listdir(output_dir) if f.endswith('.data')]

def make_client(args):
    return MySQLdb.connect(user=args.user, passwd=args.password,
                           host=args.host, port=args.port, connect_timeout=2)

def make_player(input_file):
    global args
    signal.signal(signal.SIGINT, sys.exit)
    player = LogPlayer(make_client(args), input_file)
    player.start()


class LogPlayer:
    def __init__(self, client, input_file):
        self.file = open(input_file, 'r')
        self.client = client
        self.slower = 0
        self.faster = 0

    def start(self):
        """
        Execute all queries in the input file until there are no more queries
        to execute in the file.
        """
        while 1:
            try:
                query = load(self.file)
                query_time = self.run_query(query)
                if query_time > query['query_time']:
                    self.slower += 1
                else:
                    self.faster += 1
            except EOFError:
                break

        return "%s queries ran faster, %s queries ran slower" % (
                self.faster, self.slower)

    def run_query(self, query):
        t = time.time()
        c = self.client.cursor()

        # some queries are composed of multiple operations, but connector does
        # not accept them, we need to iterate and run individually
        query_parts = query.query.splitlines()

        # if first element in the list is an USE statement remove it
        if (query_parts[0].lower().startswith('use')):
            del(query_parts[0])

        # force the USE statement, the log ommits it for consecutive queries to
        # the same database, but as we can skip block in the prepare script we
        # cannot trust it, fortunately we do have te actual db on the log metadata
        c.execute("USE `%s`", (query.database,))
        for part in query_parts:
            c.execute(part)
            c.fetchall()

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
        print "Caught SIGINT, exiting...."


if __name__ == "__main__":
    main()

# Copyright 2012 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.jobrunner
#
# lazr.jobrunner is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.jobrunner is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.jobrunner. If not, see <http://www.gnu.org/licenses/>.


"""Inspect Celery result queues."""

__metaclass__ = type

from argparse import ArgumentParser
import os
import sys

import amqp


def show_queue_data(body, message):
    print '%s: %r' % (message.delivery_info['routing_key'], body)


def clear_queues(args):
    parser = ArgumentParser(description=__doc__, prog=args[0])
    parser.add_argument(
        '-c', '--config', dest='config', required=True,
        help='The name of the Celery config module')
    parser.add_argument(
        'queues', nargs='+', metavar='queue',
        help='The names of RabbitMQ queues that hold results of Celery tasks')
    args = parser.parse_args(args[1:])
    os.environ["CELERY_CONFIG_MODULE"] = args.config
    # Late import because Celery modules are imported by celerytask,
    # and these modules need to know where to find the configuration.
    from lazr.jobrunner.celerytask import drain_queues, RunJob

    # In theory, drain_queues() can be called with more than one queue
    # name in the second argument. But the callback is only called for
    # the first queue...
    for queue in args.queues:
        try:
            drain_queues(
                RunJob.app, [queue], callbacks=[show_queue_data],
                retain=True, passive_queues=True)
        except amqp.exceptions.NotFound as exc:
            print >>sys.stderr, exc.reply_text


def main():
    clear_queues(sys.argv)

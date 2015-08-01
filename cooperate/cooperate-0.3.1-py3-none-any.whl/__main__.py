import argparse
import asyncio
import asyncio.subprocess
import functools
import os.path
import signal
import sys
from .concurrency import Concurrency
from .modes import *
from .nodes import *
from .renderers import *
from aioutils import Group, Pool

here = os.path.dirname(os.path.abspath(__file__))


def node_factory(type):
    def wrap(obj):
        if type == 'local':
            return LocalNode()
        if type == 'lxc':
            return LxcNode(obj)
        if type == 'docker':
            return DockerNode(obj)
        if type == 'ssh':
            return SSHNode(obj)
        raise argparse.ArgumentTypeError('Bad type %r for %r' % (type, obj))
    return wrap


def mode_factory(type):
    if type == 'all':
        return AllMode
    elif type == 'distribute':
        return DistibuteMode
    else:
        raise argparse.ArgumentTypeError('Bad mode %r' % type)


def batch_factory(value):
    try:
        value = int(value, 10)
        return Concurrency(size=value)
    except ValueError:
        pass
    if value.endswith('%'):
        try:
            value = int(value[:-1], 10)
            if (0 < value) and (value < 100):
                return Concurrency(part=value)
        except ValueError:
            pass
    raise argparse.ArgumentTypeError('Bad value %r' % value)


def get_parser(args=None):

    ns = argparse.Namespace()

    args = args or sys.argv[1:]
    if '--' in args:
        # every nodes must exec this only command
        pos = args.index('--')
        args, command = args[:pos], args[pos + 1:]
        setattr(ns, 'commands', [command])
        setattr(ns, 'mode', AllMode)

    parser = argparse.ArgumentParser(description='execute commands in a cooperative manner, by distributing them to many nodes',  # noqa
                                     fromfile_prefix_chars='@')
    group = parser.add_argument_group('nodes',
                                      description='distribute commands to these nodes. repeatable. one required')  # noqa
    group.add_argument('--local',
                       action='store_true',
                       dest='local',
                       help='execute locally')
    group.add_argument('--docker',
                       action='append',
                       type=node_factory('docker'),
                       metavar='CONTAINER',
                       dest='nodes',
                       help='execute in a local container')
    group.add_argument('--lxc',
                       action='append',
                       type=node_factory('lxc'),
                       metavar='CONTAINER',
                       dest='nodes',
                       help='execute in a local container')
    group.add_argument('--ssh',
                       action='append',
                       type=node_factory('ssh'),
                       metavar='ACCESS',
                       dest='nodes',
                       help='execute in a remote server via ssh')
    if not hasattr(ns, 'execute'):
        parser.add_argument('-c', '--command',
                            action='append',
                            metavar='COMMAND',
                            dest='commands',
                            help='command to execute. repeatable. one required')  # noqa
    if not hasattr(ns, 'mode'):
        parser.add_argument('-m', '--mode',
                            type=mode_factory,
                            default='all',
                            help='select a mode (all, distribute)')
    parser.add_argument('-b', '--batch',
                        type=batch_factory,
                        metavar='SIZE',
                        help='how many jobs must be executed concurrently')
    parser.add_argument('-t', '--timeout',
                        type=int,
                        metavar='SECONDS',
                        help='restrict the whole execution time')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s 0.1')

    return parser, ns, args


def broadcast(args):
    loop = asyncio.get_event_loop()
    for signame in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, signame),
                                functools.partial(ask_exit, loop, signame))

    renderer = StatusRenderer()

    nodes = args.nodes or []
    if args.local:
        nodes.insert(0, LocalNode())

    jobs = args.mode(nodes, args.commands)
    if args.batch:
        pooler = Pool(args.batch.batch(jobs))
    else:
        pooler = Group()

    for node, command in jobs:
        task = pooler.spawn(node.run(command))
        render = functools.partial(renderer.render, node=node, command=command)
        task.add_done_callback(render)
    pooler.join()

    loop.close()


def ask_exit(loop, signame):
    print("# got signal %s: exit" % signame)
    loop.stop()


def main():
    parser, ns, remains = get_parser()
    args = parser.parse_args(remains, namespace=ns)
    broadcast(args)


if __name__ == '__main__':
    main()

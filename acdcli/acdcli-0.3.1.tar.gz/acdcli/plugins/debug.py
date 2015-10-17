from . import *


def create_file(args: argparse.Namespace):
    import uuid
    name = args.name if args.name else str(uuid.uuid4())

    return args.acd_client().create_file(name)


def sql_busy_timeout(args: argparse.Namespace):
    r = args.cache().engine.engine.execute('PRAGMA busy_timeout;')
    print(r.first()[0])
    r.close()


class TestPlugin(Plugin):
    MIN_VERSION = '0.3.0a6'

    @classmethod
    def attach(cls, subparsers: argparse.ArgumentParser, log: list, **kwargs):
        """ Attaches this plugin to the argparse action subparser group
        :param subparsers the action subparser group
        :param log a list to put initialization log messages in
         """
        p = subparsers.add_parser('debug', add_help=False)
        p.set_defaults(func=None)
        sp = p.add_subparsers()

        cr_p = sp.add_parser('create', aliases=['cr'])
        cr_p.add_argument('name', nargs='?', help='')
        cr_p.set_defaults(func=create_file)

        to_p = sp.add_parser('sql_timeout')
        to_p.set_defaults(func=sql_busy_timeout)

        log.append(str(cls) + ' attached.')

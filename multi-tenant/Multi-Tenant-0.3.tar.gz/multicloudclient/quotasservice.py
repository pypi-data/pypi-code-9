
from __future__ import print_function

import argparse

from cliff import lister
from cliff import show
import command
import quotasupdate
import pdb

class QuotaSet(command.OpenStackCommand):
    """Creating tenants 

    """
    #api = 'network'
    resource = "tenants"

    def get_parser(self, prog_name):
    
        parser = super(QuotaSet, self).get_parser(prog_name)
        parser.add_argument(
        '-D', '--show-details',
        help=('Show detailed information.'),
        action='store_true',
        default=False, )
        parser.add_argument(
        'tenant',
        metavar='<tenant-id>',
        help=('ID of tenant to set the quotas for.'))
        parser.add_argument(
        '--user',
        metavar='<user-id>',
        default=None,
        help=('ID of user to set the quotas for.'))
        parser.add_argument(
        '--instances',
        metavar='<instances>',
        type=int, default=None,
        help=('New value for the "instances" quota.'))
        parser.add_argument(
        '--cores',
        metavar='<cores>',
        type=int, default=None,
        help=('New value for the "cores" quota.'))
        parser.add_argument(
        '--ram',
        metavar='<ram>',
        type=int, default=None,
        help=('New value for the "ram" quota.'))
        parser.add_argument(
        '--floating-ips',
        metavar='<floating-ips>',
        type=int,
        default=None,
        help=('New value for the "floating-ips" quota.'))
        parser.add_argument(
        '--floating_ips',
        type=int,
        help=argparse.SUPPRESS)
        parser.add_argument(
        '--fixed-ips',
        metavar='<fixed-ips>',
        type=int,
        default=None,
        help=('New value for the "fixed-ips" quota.'))
        parser.add_argument(
        '--metadata-items',
        metavar='<metadata-items>',
        type=int,
        default=None,
        help=('New value for the "metadata-items" quota.'))
        parser.add_argument(
        '--metadata_items',
        type=int,
        help=argparse.SUPPRESS)
        parser.add_argument(
        '--injected-files',
        metavar='<injected-files>',
        type=int,
        default=None,
        help=('New value for the "injected-files" quota.'))
        parser.add_argument(
        '--injected_files',
        type=int,
        help=argparse.SUPPRESS)
        parser.add_argument(
        '--injected-file-content-bytes',
        metavar='<injected-file-content-bytes>',
        type=int,
        default=None,
        help=('New value for the "injected-file-content-bytes" quota.'))
        parser.add_argument(
        '--injected_file_content_bytes',
        type=int,
        help=argparse.SUPPRESS)
        parser.add_argument(
        '--injected-file-path-bytes',
        metavar='<injected-file-path-bytes>',
        type=int,
        default=None,
        help=('New value for the "injected-file-path-bytes" quota.'))
        parser.add_argument(
        '--key-pairs',
        metavar='<key-pairs>',
        type=int,
        default=None,
        help=('New value for the "key-pairs" quota.'))
        parser.add_argument(
        '--security-groups',
        metavar='<security-groups>',
        type=int,
        default=None,
        help=('New value for the "security-groups" quota.'))
        parser.add_argument(
        '--security-group-rules',
        metavar='<security-group-rules>',
        type=int,
        default=None,
        help=('New value for the "security-group-rules" quota.'))
        parser.add_argument(
        '--server-groups',
        metavar='<server-groups>',
        type=int,
        default=None,
        help=('New value for the "server-groups" quota.'))
        parser.add_argument(
        '--server-group-members',
        metavar='<server-group-members>',
        type=int,
        default=None,
        help=('New value for the "server-group-members" quota.'))
        parser.add_argument(
            '--regions', metavar='regions',required=True,
            help=('The owner regions'))
        return parser
        
    def run(self, parsed_args):
        quotasupdate.mainmethod(parsed_args)
        

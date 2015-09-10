"""Gets information on the CloudFormation stacks based on the given config."""

from os.path import expanduser, isdir

from argparse import ArgumentTypeError

from .base import BaseCommand
from ...actions import dump


def valid_directory(dir_string):
    expanded = expanduser(dir_string)
    if not isdir(expanded):
        raise ArgumentTypeError("Directory %s does not exist.", expanded)
    return expanded


class Dump(BaseCommand):

    name = 'dump'
    description = __doc__

    def add_arguments(self, parser):
        super(Dump, self).add_arguments(parser)
        parser.add_argument("--output", default=".",
                            metavar="DIR", type=valid_directory,
                            help="The directory to dump the templates into. "
                                 "Default: %(default)s")
        parser.add_argument("--stacks", action="append",
                            metavar="STACKNAME", type=str,
                            help="Only work on the stacks given. Can be "
                                 "specified more than once. If not specified "
                                 "then stacker will work on all stacks in the "
                                 "config file.")

    def run(self, options, **kwargs):
        super(Dump, self).run(options, **kwargs)
        action = dump.Action(options.context, provider=options.provider)
        action.execute()

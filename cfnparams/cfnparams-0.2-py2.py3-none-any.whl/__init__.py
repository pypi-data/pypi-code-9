import argparse
import logging

import boto.cloudformation

from cfnparams.params import ParamsFactory, JSONParams
from cfnparams.stack import Resolver, Stack

FILE_PREFIX = 'file://'

logging.basicConfig(level=logging.INFO)

epilog = """
The --parameters argument can be specified multiple times, and can take
multiple forms:

    1) Key/Value pair supplied directly:

        --parameters ParameterKey=string,ParameterValue=string

    2) A reference to a file containing parameters:

        --parameters file://path/to/file.{py,json}
"""


def main():
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(
        prog="cfn-params",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="A CloudFormation stack parameter munging utility.",
        epilog=epilog
    )
    parser.add_argument('--region', required=True, help="AWS region")
    parser.add_argument('--output',
                        required=True,
                        help="Filename to write the JSON parameters to")
    parser.add_argument('--parameters',
                        action='append',
                        required=True,
                        metavar="PARAMS",
                        help="A parameter source")
    parser.add_argument('--use-previous-value',
                        action='store_true',
                        default=False,
                        help="Set if UsePreviousValue should be true in the "
                        "output, defaults to false if not supplied.")
    args = parser.parse_args()

    sources = []
    for p in args.parameters:
        src = ParamsFactory.new(p)
        sources.append(src)

    dependent_stacks = set()
    for src in sources:
        deps = src.dependencies()
        dependent_stacks.update(deps)

    stack_outputs = {}
    if dependent_stacks:
        cfn = boto.cloudformation.connect_to_region(args.region)
        for name in dependent_stacks:
            stack = Stack(name)
            outputs = stack.outputs(cfn)
            stack_outputs.update({name: outputs})
    resolver = Resolver(stack_outputs)

    params = {}
    for src in sources:
        params.update(src.parse(resolver))

    output = JSONParams(None)
    outputs.params = params
    with open(args.output, 'wb') as f:
        f.write(output.write(args.use_previous_value))

if __name__ == '__main__':
    main()

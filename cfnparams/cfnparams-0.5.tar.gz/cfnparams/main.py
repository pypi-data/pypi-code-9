import argparse
import logging

import boto.cloudformation

from cfnparams import __version__
import cfnparams.arguments
import cfnparams.params
from cfnparams.resolution import Resolver, ResolveByName, ResolveByTag
import cfnparams.template

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
    parser = argparse.ArgumentParser(
        prog="cfn-params",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="A CloudFormation stack parameter munging utility.",
        epilog=epilog
    )
    parser.add_argument('--region', required=True, help="AWS region")
    parser.add_argument('--template',
                        required=False,
                        type=cfnparams.arguments.file_arg,
                        help="JSON template to which the parameters will "
                        "(potentially) supplied to. If provided, any "
                        "parameters not declared in the template will be "
                        "excluded from the output")
    parser.add_argument('--output',
                        metavar="FILENAME",
                        default="params.json",
                        required=True,
                        help="Filename to write the JSON parameters to")
    parser.add_argument('--parameters',
                        action='append',
                        required=True,
                        metavar="PARAMS",
                        type=cfnparams.arguments.parameter_arg,
                        help="A parameter source")
    parser.add_argument('--use-previous-value',
                        action='store_true',
                        default=False,
                        help="Set if UsePreviousValue should be true in the "
                        "output, defaults to false if not supplied.")
    parser.add_argument('--filter-tag',
                        metavar="KEYVALUE",
                        action='append',
                        help="A tag Key/Value pair which will limit the stack "
                        "resolution results.",
                        type=cfnparams.arguments.filter_tag)
    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s ' + __version__)

    resolve_by = parser.add_mutually_exclusive_group()
    resolve_by.add_argument('--resolve-by-name',
                            action='store_true',
                            default=True,
                            help="Set by default, and will attempt to resolve "
                            "dependent stacks by the stack name or ID")
    resolve_by.add_argument('--resolve-by-tag',
                            metavar="TAG",
                            action='store',
                            help="Overrides --resolve-by-name, and will "
                            "instead use the provided tag name to resolve "
                            "dependent stacks")

    args = parser.parse_args()

    sources = []
    for p in args.parameters:
        try:
            src = cfnparams.params.ParamsFactory.new(p)
        except Exception as e:
            logging.info('Skipping: {}'.format(e))
        sources.append(src)

    if args.resolve_by_tag:
        strategy = ResolveByTag(args.resolve_by_tag)
    else:
        strategy = ResolveByName
    cfn = boto.cloudformation.connect_to_region(args.region)
    resolver = Resolver(cfn, strategy, dict(args.filter_tag))

    params = {}
    for src in sources:
        params.update(src.parse(resolver))

    if args.template:
        tmpl = cfnparams.template.Template(args.template)
        declared_params = tmpl.params()
        unused = {p for p in params.keys() if p not in declared_params}
        logging.info('Dropping: Unused parameters: {}'.format(unused))
        params = {k: v for k, v in params.items() if k in tmpl.params()}

    output = cfnparams.params.JSONParams('{}')
    output.params = params
    with open(args.output, 'wb') as f:
        f.write(output.write(args.use_previous_value))


if __name__ == '__main__':
    main()

import docopt
import logging
import yaml

from os.path import isfile

from rabix import __version__ as version
from rabix.common.errors import RabixError
from rabix.common.ref_resolver import Loader
from rabix.common.util import log_level
from rabix.tools.build import run_steps
from rabix.tools.fmt import format_tool


log = logging.getLogger(__name__)


USAGE = """
Usage:
  rabix-tools fmt [-uiejy] <tool>
  rabix-tools build [-v...] [--config=<cfg_path>]
  rabix-tools checksum [--method=(md5|sha1)] <jsonptr>
  rabix-tools -h | --help
  rabix-tools --version

Commands:
  fmt                       Format tool according to options
  build                     Execute steps for app building, wrapping and
                            deployment.
  checksum                  Calculate and print the checksum of json document
                            (or fragment) pointed by <jsonptr>

Options:
  -c --config=<cfg_path>    Specify path to config file [default: .rabix.yml]
  -h --help                 Display this message.
  -m --method (md5|sha1)    Checksum type [default: sha1]
  --version                 Print version to standard output and quit.
  -v --verbose              Verbosity. More Vs more output.
  -u --keep-unknown-fields  Don't remove unknown fields from tool
  -i --keep-id              Don't remove tool ID
  -e --extract-tools        Extract tools from workflow into separate files
  -y --yaml                 Output YAML (default)
  -j --json                 Output JSON
"""


def checksum(jsonptr, method='sha1'):
    loader = Loader()
    obj = loader.load(jsonptr)
    print(method + '$' + loader.checksum(obj, method))


def build(path='.rabix.yml'):
    if not isfile(path):
        raise RabixError('Config file %s not found!' % path)
    with open(path) as cfg:
        config = yaml.load(cfg)
        run_steps(config)


def fmt(args):
    tool = args['tool']
    remove_unknown = '--keep-unknown-fields' not in args
    remove_id = '--keed-id' not in args
    format_tool(tool, args)


def main():
    logging.basicConfig(level=logging.WARN)

    args = docopt.docopt(USAGE, version=version)

    logging.root.setLevel(log_level(args['--verbose']))
    if args['checksum']:
        checksum(args['<jsonptr>'], args['--method'])
    elif args['build']:
        build(args.get('--config'))
    elif args['fmt']:
        fmt(args)

if __name__ == '__main__':
    main()

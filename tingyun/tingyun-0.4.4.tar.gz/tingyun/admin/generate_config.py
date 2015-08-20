from __future__ import print_function

import sys
import os


def generate_config(args):
    """generate default configuration to specified path.
    :param args:
    :return:
    """
    name = 'generate-config'
    options = '[license_key] output_file'
    description = "Generate the config file with license(optional) and output to specified path."

    if len(args) < 1:
        print('tingyun-admin generate-config %s' % options)
        sys.exit(1)

    from tingyun import __file__ as package_root

    package_root = os.path.dirname(package_root)
    config_file = os.path.join(package_root, 'tingyun.ini')
    default_config = open(config_file, 'r')
    content = default_config.read()

    if 2 == len(args):
        content = content.replace('** YOUR-LICENSE-KEY **', args[0])
        print("""
                    ================ Messages ==============
              You use license key: %s, to generate tingyun agent config file
              """ % args[0])

    if 2 == len(args):
        output_file = open(args[1], "w")
    else:
        output_file = open(args[0], "w")

    output_file.write(content)
    output_file.close()
    default_config.close()

import os
import sys
import yaml

from utils import print_err
from fs_commands import mkdirp
from jinja2 import Template, Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))


def get_config_vars(config):
    """\
    Fetches the config values from the yaml config and returns
    a dict.
    """
    stream = file(config, 'r')
    return yaml.load(stream)


def generate_config(template_name, config, outputfile, section="build-vars"):
    """\
    Generates a config from a template and with values from the yaml config.

    A section can optionally be passed if somthing else than 'build-vars' should be used. 
    """
    config_vars = get_config_vars(config)
    script_template = env.get_template(template_name)
    original_outputfile = outputfile
    try:
        outputfile = outputfile % config_vars[section]
    except KeyError:
        print_err("*" * 80)
        print_err("Error: You are using a variable that is not known in "
                  "%s:\n%s" % (section, original_outputfile, ))
        print_err("*" * 80)
        raise
    dirname = os.path.dirname(outputfile)
    if not os.path.exists(dirname):
        mkdirp(dirname)

    with open(outputfile, "wb") as fh:
        fh.write(script_template.render(config_vars[section]))

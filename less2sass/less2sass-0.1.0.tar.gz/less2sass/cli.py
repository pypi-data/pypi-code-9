#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
cookiecutter.cli
-----------------
Main `cookiecutter` CLI.
"""

from __future__ import unicode_literals

import os
import sys
import logging

import click

from less2sass import __version__
from .less2sass import convert

logger = logging.getLogger(__name__)

def version_msg():
    python_version = sys.version[:3]
    location = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    message = 'less2sass %(version)s from {} (Python {})'
    return message.format(location, python_version)


@click.command()
@click.version_option(__version__, '-V', '--version', message=version_msg())
@click.argument('in-file')
@click.option(
    '-i', '--in-file',
    help='Input less file that is *.less'
)
@click.option(
    '-o', '--out-file',
    help='The file that will be in sass'
)
@click.option(
    '-v', '--verbose',
    is_flag=True, help='Print debug information', default=False
)
def main(in_file, out_file, verbose):
    """Create a project from a Cookiecutter project template (TEMPLATE)."""
    if verbose:
        logging.basicConfig(
            format='%(levelname)s %(filename)s: %(message)s',
            level=logging.DEBUG
        )
    else:
        # Log info and above to console
        logging.basicConfig(
            format='%(levelname)s: %(message)s',
            level=logging.INFO
        )

    if not out_file:
        out_file = in_file.replace(".less", ".sass")

    if ".less" in out_file:
        out_file = in_file.replace(".less", ".sass")

    with open(in_file, 'r') as file_input:
        less_string = file_input.read()

    sass_string = convert(less_string)

    with open(out_file, 'w') as file_out:
        file_out.write(sass_string)

if __name__ == "__main__":
    main()

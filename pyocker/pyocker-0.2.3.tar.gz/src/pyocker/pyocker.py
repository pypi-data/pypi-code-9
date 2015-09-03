#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import click

import dep

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
CWD = os.getcwd()

@click.group(context_settings=CONTEXT_SETTINGS)
def pyocker():
    pass

@pyocker.command(context_settings=CONTEXT_SETTINGS)
@click.option('--file', default='docker-dependency.yml', type=str, help='Path to config file [default="docker-dependency.yml"]')
@click.option('--verbose/--quiet', default=True, help='Make lots of noise or not [default=verbose]')
@click.option('--dry-run', is_flag=True, default=False)
def build(file, verbose, dry_run):
    dep.main(CWD, file, verbose=verbose, dry=dry_run)

@pyocker.command(context_settings=CONTEXT_SETTINGS)
def compose():
    click.echo('[Upcoming Feature] Compose')

pyocker.add_command(build)
pyocker.add_command(compose)

def main():
    pyocker()

if __name__=="__main__":
    main()

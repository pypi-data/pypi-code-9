#!/usr/bin/env python
# encoding: utf-8
import os
import click
from ..main import main

@click.command()
def init():
    # init folders
    try:
        base_path = os.path.dirname(os.path.abspath('__file__'))
        os.makedirs(os.path.join(base_path, 'content'))
        os.makedirs(os.path.join(base_path, 'public'))
        click.echo('init success')
    except FileExistsError:
        click.echo('file already exists')


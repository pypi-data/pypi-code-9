#!/usr/bin/env python
# encoding: utf-8
import click
from ..main import main

@click.command()
def generate():
    main()


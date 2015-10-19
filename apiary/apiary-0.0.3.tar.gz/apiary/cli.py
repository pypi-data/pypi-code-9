# -*- coding: utf-8 -*-
import click
from apiary.command.preview import Preview

@click.command()
@click.option('--browser', help="Show API documentation in specified browser")
@click.option('--output', help="Write generated HTML into specified file")
@click.option('--path', default="apiary.apib", help="Specify path to blueprint file")
@click.option('--api_host', help="Specify apiary host")
@click.option('--server', help="Start standalone web server on port 8080")
@click.option('--port', help="Set port for server option")
def preview(**kwargs):
    cmd = Preview(**kwargs)
    cmd.execute()


@click.group()
def cli():
    pass

cli.add_command(preview)

if __name__ == '__main__':
    preview()
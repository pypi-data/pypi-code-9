import click
from pyramid_cli.cli import main
from montague import load_server

@click.command()
@click.pass_context
def serve(ctx):
    server = load_server(ctx.obj.config_file, name=ctx.obj.server_env)
    server(ctx.obj.app)

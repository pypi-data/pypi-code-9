import pkg_resources
import click
import os
import sys

from montague import load_app
from pyramid.scripting import prepare


def safe_load_app(config_file, name='main'):
    try:
        return load_app(config_file, name)
    except KeyError as e:
        key_missing = e.args[0]
        msg = 'Missing Key in section application#%s: %s' % (
            name,
            key_missing
        )
        click.echo(msg)
        sys.exit(1)


class Config(object):
    def __init__(self, config_file, env):
        self.config_file = config_file

        if not os.path.isfile(config_file):
            click.echo(
                "%s was not found, please create it or use -c" % config_file
            )
            sys.exit(1)
        self.env = env
        self.app = safe_load_app(config_file, name=env)
        self.pyramid_env = prepare()


@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.option(
    '--config', '-c',
    type=click.Path(resolve_path=True),
    default='app.yaml',
    help='The application configuration file, defaults to app.yaml'
)
@click.option(
    '--env', '-e',
    required=False,
    default='main',
    help='The configuration environment to load, defaults to main'
)
@click.version_option()
@click.pass_context
def cli(ctx, config, env):
    obj = Config(config, env)
    ctx.obj = obj


# Load any commands from the entrypoint `tomb.commands` and register
# them with our toplevel command.
for ep in pkg_resources.iter_entry_points('tomb.commands'):
    module = ep.load()
    cli.add_command(module)

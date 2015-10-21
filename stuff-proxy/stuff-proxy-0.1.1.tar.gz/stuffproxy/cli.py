import os
import socket
import sys

import click
import npyscreen
import yaml

from stuffproxy.config import settings
from stuffproxy.menu import ProjectSettingsForm
from stuffproxy.server import app
from stuffproxy.utils import generate_secret


def cli_binary(binary):
    cli_bin = os.path.join(os.path.dirname(sys.executable), binary)
    if not os.path.exists(cli_bin):
        click.secho('Not found %s binary at %s' % (binary, cli_bin), fg='red')

        raise click.Abort


def init_project():
    cfg = 'project.yml'
    if not os.path.isfile(cfg):
        click.secho('Not found %s in %s' % (cfg, os.path.abspath(os.path.curdir)))

        raise click.Abort()

    settings.configure(cfg)


@click.group()
def cli():
    pass


@cli.command(name='start-project')
@click.argument('name')
def start_project(name):
    if os.path.exists(name):
        click.secho('Path "%s" already exists' % name, fg='red')

        raise click.Abort()

    def check_domain_name(value):
        value = value.lstrip('w.')
        try:
            socket.gethostbyname(value)
        except Exception:
            if not click.confirm('Not found %s. Do you want to continue?' % value):
                raise click.UsageError('Bad domain name %s' % value)

        return value

    hostname = click.prompt('Please enter domain name for stuff-proxy', value_proc=check_domain_name)
    port = click.prompt('Please enter port (standard ports: HTTP is 80, HTTPS is 443)', default=80, type=click.INT)

    account = click.prompt('Please enter account name', default='default').lower()

    click.secho('Please check information:', fg='green')
    for v in ('hostname', 'port', 'account'):
        click.secho('  %s: %s' % (v.ljust(20).title(), locals()[v]))

    click.confirm('Is everything ok?', abort=True)

    os.makedirs(name, mode=0770)

    yaml.dump({
        'project': {
            'hostname': hostname,
            'port': port
        },
        'accounts': {
            account: generate_secret()
        }
    }, open(os.path.join(name, 'project.yml'), 'wb'), default_flow_style=False)
    click.secho('Project "%s" created succesfully' % name, fg='green')


@cli.command()
def build():
    init_project()

    if not hasattr(settings, 'accounts'):
        click.secho('Not found accounts in project.yml', fg='red')

        raise click.Abort

    dirs = ('tmp', 'logs', 'etc')
    click.secho('Checking project dirs: %s ...' % " ".join(dirs), fg='green')
    for d in dirs:
        if not os.path.isdir(d):
            os.makedirs(d)

    click.secho('Generating configuration ...', fg='green')
    etc = {
        'nginx.conf': ''
    }


@cli.command()
def menu():
    def show_menu(screen):
        npyscreen.setTheme(npyscreen.Themes.ElegantTheme)

        form = ProjectSettingsForm('Stuff-proxy project settings form')
        form.edit()

        file('test.log', 'w').write(form.nginxHostname.value)

    npyscreen.wrapper_basic(show_menu)


@cli.command()
def serve():
    init_project()

    app.run(**settings.serve)


if __name__ == '__main__':
    cli(obj={})

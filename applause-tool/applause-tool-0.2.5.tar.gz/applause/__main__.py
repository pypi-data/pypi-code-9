"""
Applause CLI Tool.
~~~~~~~~~~~~~~~~~~~
"""
import logging
import click
from . import settings
from .session import AuthSession
from .errors import InvalidLogin
from .utils import enable_debug_mode, requires_login
from .beta import ApplauseBETA
from .sdk import ApplauseSDK
from .param import PathString


# `prog` & `version` will be auto detected by clicked based on setup.py
VERSION_MESSAGE = '%(prog)s version %(version)s Applause Inc. 2015. All rights reserved'


@click.group(context_settings={"help_option_names": ['-h', '--help']})
@click.version_option(message=VERSION_MESSAGE)
@click.option('--debug', is_flag=True, help="Enable extended logging")
def main(debug):
    """
    Applause CLI tool, Applause Inc. All rights reserved.
    """
    if debug:
        enable_debug_mode()


@main.command()
@click.option('--username', '-u', help="Login")
@click.option('--password', '-p', help="Password")
def login(username=None, password=None):
    """
    Authenticate to the Applause CLI tool and persist your credentials file
    for later usage.
    """
    # Get user credentials
    username = username or click.prompt("Username")
    password = password or click.prompt("Password", hide_input=True)

    # Make sure they are valid & store data for later usage
    auth = AuthSession(client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET, load_cookie=False)

    try:
        click.echo("Logging in...")
        auth.login(username=username, password=password)
        click.echo("Success. Cookie stored at: {path}".format(path=auth.config_path))
    except InvalidLogin as e:
        logging.debug("Login error: {error}".format(error=e))
        click.echo("Invalid credentials")


@main.command()
def logout():
    """
    Revoke user access tokens & purge any session specific configuration files.
    """
    auth = AuthSession(client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET, load_cookie=False)
    click.echo("Logging out...")
    auth.logout()
    click.echo("Cookie removed.")


@main.command()
def account():
    """
    Print information about currently logged in user.
    """
    auth = AuthSession(client_id=settings.CLIENT_ID, client_secret=settings.CLIENT_SECRET)
    if auth.is_active():
        click.echo("Currently logged in user: {username}".format(username=auth.username))
    else:
        click.echo("No user session. Please login.")


@main.group()
def sdk():
    """
    Applause SDK product specific operations.
    """


@sdk.command(name='distribute')
@click.argument('company_id')
@click.argument('app_id')
@click.argument('path', type=click.Path(exists=True))
@click.option('--changelog', '-c', type=PathString(exists=True), help="Release notes file for the uploaded build")
@click.option(
    '--emails', '-e', type=PathString(exists=True), multiple=True,
    help="List of emails to distribute the build to. "
    "If path, each email should be on a new line.",
)
@requires_login
def distribute(session, company_id, app_id, path, changelog, emails):
    sdk = ApplauseSDK(session.get_session())
    sdk.distribute(company_id, app_id, path, changelog, emails)
    click.echo("Distributed.")


@sdk.command(name='upload')
@click.argument('company_id')
@click.argument('app_id')
@click.argument('path', type=click.Path(exists=True))
@click.option('--changelog', '-c', type=PathString(exists=True), help="Release notes file for the uploaded build")
@requires_login
def upload_to_sdk(session, company_id, app_id, path, changelog):
    # company_id is just for preserving cli usage
    sdk = ApplauseSDK(session.get_session())
    sdk.upload(app_id, path, changelog)
    click.echo("Uploaded.")


@main.group()
def beta():
    """
    Applause MBM product specific operations.
    """


@beta.command(name='upload')
@click.argument('company_id')
@click.argument('app_id')
@click.argument('path', type=click.Path(exists=True))
@click.option('--changelog', '-c', type=PathString(exists=True), help="Release notes file for the uploaded build")
@requires_login
def upload_to_beta(session, company_id, app_id, path, changelog):
    # company_id is just for preserving cli usage
    mbm = ApplauseBETA(session.get_session())
    mbm.upload(app_id, path, changelog)
    click.echo("Uploaded.")

if __name__ == '__main__':
    main()

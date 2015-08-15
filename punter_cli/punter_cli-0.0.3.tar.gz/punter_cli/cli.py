"""punter-cli - Simple CLI for the Email Hunter API.

The command line interface provides commands for initially setting and
updating the required API key and executing searches on either domains
or email addresses.

The API key can be set or retrieved depending on whether a key is
passed to the `key` command. Example usage is as follows:

    $ punter key d08d2ba22218d1b59df239d03fc5e66adfaec2b2
    $ punter key
    d08d2ba22218d1b59df239d03fc5e66adfaec2b2

Executing a domain search:

    $ punter search lamppostgroup.com
    {
    "status": "success",
    "pattern": "{first}.{last}",
    "results": 4,
    "webmail": false,
    "offset": 0,
    "emails": [{
        "sources": [
            {
                "domain": "chugalug.org",
                "extracted_on": "2015-01-25",
                "uri": "http://chugalug.org/widget/2550/who"
            },
        ...
    ...
    ]}

"""


import sys
import click
import json
import punter
import punter.exceptions as exceptions
from . import utils


@click.group()
def main():
    """A simple CLI for the Email Hunter API."""
    pass


@main.command()
@click.argument('query')
@click.option('--offset', help='Number of emails to skip.')
@click.option('--type', help='Email type (personal or generic).')
def search(query, offset, type):
    """Execute a search on a given domain/email.

    Provided the query is a valid domain or email address a search will
    be executed to find all available email addresses, if a domain is
    provided, or the domain associated with the provided email address.

    :param query: URL or email address on which to search.
    :param offset: Specifies the number of emails to skip.
    :param type: Specifies email type (i.e. generic or personal).

    """

    try:
        key = utils.get_api_key()
        result = punter.search(key, query)
        click.echo(json.dumps(result, indent=4))
    except exceptions.PunterException as e:
        click.secho('Search error: {0}'.format(e), fg='red')
        sys.exit(1)
    

@main.command()
@click.argument('api_key', required=False)
def key(api_key):
    """Set or retrieve the secret API key.

    A search can only be successfully executed if an API key is first
    set. This command will enable the key to be set or retrieved. At
    present time the API key is a 40 character string type.

    :param api_key: The secret API key.
    :type api_key: string

    """

    if not api_key or api_key is None:
        key = utils.get_api_key()
        click.echo(key if key else 'No API key set')
        sys.exit(1)

    try:
        utils.set_api_key(api_key)
        click.echo('Current API key: {0}'.format(api_key))
    except exception.PunterException as e:
        click.secho('Key error: {0}'.format(e), fg='red')
        sys.exit(1)

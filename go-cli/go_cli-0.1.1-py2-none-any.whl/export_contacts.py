""" Export contacts from the contacts API. """

import csv
import json

import click

from go_http.contacts import ContactsApiClient
from go_http.exceptions import PagedException


@click.option(
    '--token', '-t',
    help='Contacts API authentication token')
@click.option(
    '--resume',
    help='Resume failed contact download at the given cursor')
@click.option(
    '--csv', type=click.File('wb+'),
    help=('Export contacts to the named file in CSV format.'))
@click.option(
    '--json', type=click.File('wb+'),
    help=('Export contacts to the named file as new-line separated'
          ' JSON objects.'))
@click.pass_context
def export_contacts(ctx, token, resume, csv, json):
    """ Export contacts from the contacts API.
    """
    if not all((ctx.obj.account_key, token)):
        raise click.UsageError(
            "Please specify both the account key and the contacts API"
            " authentication token. See --help.")
    if not any((csv, json)) or all((csv, json)):
        raise click.UsageError(
            "Please specify either --csv or --json (but not both).")
    contacts_api = ContactsApiClient(token)
    if csv:
        write_contact = csv_contact_writer(csv, resumed=bool(resume))
    else:
        write_contact = json_contact_writer(json)
    try:
        for contact in contacts_api.contacts(start_cursor=resume):
            write_contact(contact)
    except PagedException as err:
        raise click.ClickException(
            "Error downloading contacts. Please re-run with --resume=%s to"
            " resume."
            % err.cursor)


def contact_to_csv_dict(contact):
    """ Convert a contact to a dictionary safe for CSV writing. """
    d = {}
    for k, v in contact.iteritems():
        if isinstance(v, unicode):
            v = v.encode("utf-8")
        elif not isinstance(v, str):
            v = json.dumps(v)
        d[k.encode("utf-8")] = v
    return d


def csv_contact_writer(csv_file, resumed):
    """ Return a function for writing contacts to the given CSV file. """
    closure = {'writer': None}

    def writer(contact):
        contact = contact_to_csv_dict(contact)
        dict_writer = closure['writer']
        if dict_writer is None:
            fields = sorted(contact.keys())
            dict_writer = closure['writer'] = csv.DictWriter(csv_file, fields)
            if not resumed:
                dict_writer.writerow(dict((k, k) for k in fields))
        dict_writer.writerow(contact)

    return writer


def json_contact_writer(json_file):
    """ Return a function for writing contacts to the given JSON file. """
    def writer(contact):
        json_file.write(json.dumps(contact))
        json_file.write("\n")
    return writer

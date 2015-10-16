""" Send messages via an HTTP API (nostream) conversation. """

import csv
import json

import click

from go_http.send import HttpApiSender


@click.option(
    '--conversation', '-c',
    help='HTTP API conversation key')
@click.option(
    '--token', '-t',
    help='HTTP API conversation token')
@click.option(
    '--csv', type=click.File('rb'),
    help=('CSV file with columns to_addr, content and, optionally,'
          'session_event.'))
@click.option(
    '--json', type=click.File('rb'),
    help=('JSON objects, one per line with fields to_addr, content and,'
          ' optionally, session_event'))
@click.pass_context
def send(ctx, conversation, token, csv, json):
    """ Send messages via an HTTP API (nostream) conversation.
    """
    if not all((ctx.obj.account_key, conversation, token)):
        raise click.UsageError(
            "Please specify all of the account key, conversation key"
            " and conversation authentication token. See --help.")
    if not any((csv, json)):
        raise click.UsageError("Please specify either --csv or --json.")
    http_api = HttpApiSender(ctx.obj.account_key, conversation, token)
    if csv:
        for msg in messages_from_csv(csv):
            click.echo("Sending message to %(to_addr)s." % msg)
            http_api.send_text(**msg)
    if json:
        for msg in messages_from_json(json):
            click.echo("Sending message to %(to_addr)s." % msg)
            http_api.send_text(**msg)


def messages_from_csv(csv_file):
    reader = csv.DictReader(csv_file)
    if not (set(["to_addr", "content"]) <= set(reader.fieldnames)):
        raise click.UsageError(
            "CSV file must contain to_addr and content column headers.")
    for data in reader:
        yield {
            "to_addr": data["to_addr"],
            "content": data["content"],
            "session_event": data.get("session_event")
        }


def messages_from_json(json_file):
    for line in json_file:
        data = json.loads(line.rstrip("\n"))
        if not isinstance(data, dict) or not (
                set(["to_addr", "content"]) <= set(data.keys())):
            raise click.UsageError(
                "JSON file lines must be objects containing to_addr and"
                " content keys.")
        yield {
            "to_addr": data["to_addr"],
            "content": data["content"],
            "session_event": data.get("session_event")
        }

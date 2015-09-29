from __future__ import print_function
from processors.kv import parse_kv
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('-r', '--record-delim', default='END\n', help='Delimiter separating records. Default: "END\\n".')
@click.option('-e', '--entry-delim', default='\n', help='Delimiter separating entries. Default: "\\n".')
@click.option('-f', '--field-delim', default=' ', help='Delimiter separating key-value fields. Default: " ".')
@click.argument('files', nargs=-1)
def fromkv(record_delim, entry_delim, field_delim, files):
    parse_kv(record_delim, entry_delim, field_delim, files)

if __name__ == '__main__':
    fromkv()

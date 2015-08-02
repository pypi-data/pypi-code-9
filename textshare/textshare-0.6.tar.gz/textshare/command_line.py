import click, sys, os
from textshare import SprungeSharer

@click.command()
@click.option('--input', '-i', help='uses stdin as input', is_flag=True, default=False)
@click.option('--map', help='returns output as a map of filepaths and url', is_flag=True, default=False)
@click.argument('filepaths', type=click.Path(exists=True), nargs=-1)
def cli(input, map, filepaths):
    textshare = SprungeSharer.SprungeSharer()
    if input:
        text = sys.stdin.readlines()
        click.echo(textshare.uploadtext(''.join(text)))
    else:
        if len(filepaths) != 0:
            for fpath in filepaths:
                map_fpath = " <- " + os.path.basename(fpath)
                if not map:
                    map_fpath = ""
                click.echo(textshare.uploadfile(click.format_filename(fpath)) + map_fpath)
        else:
            click.echo('pass atleast one filepath as argument or use -i/--input as an option')

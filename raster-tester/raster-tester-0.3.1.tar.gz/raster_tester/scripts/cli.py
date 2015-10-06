import click

import raster_tester

@click.group()
def cli():
    pass

@click.command("compare")
@click.argument("input_1", type=click.Path(exists=True))
@click.argument("input_2", type=click.Path(exists=True))
@click.option("--pixel-threshold", "-p", type=int, default=0,
    help='Threshold for pixel diffs [default=0]')
@click.option("--downsample", "-d", type=int, default=1,
    help='Downsample via decimated read for faster comparison, and to handle variation in compression artifacts [default=1]')
@click.option("--upsample", "-u", type=int, default=1,
    help='Upsample to handle variation in compression artifacts [default=1]')
@click.option("--compare-masked", is_flag=True,
    help='Only compare masks + unmasked areas of RGBA rasters')
@click.option("--no-error", is_flag=True,
    help='Compare in non stderr mode: echos "(OK|NOT OK) - <input_1> is (within|not within) <pixel-threshold> pixels of <input 2>"')
@click.option("--debug", is_flag=True,
    help='Print ascii preview of errors')
@click.option("--flex-mode", is_flag=True,
    help='Allow comparison of masked RGB + RGBA')
def compare(input_1, input_2, pixel_threshold, upsample, downsample, no_error, compare_masked, debug, flex_mode):
    raster_tester.compare(input_1, input_2, pixel_threshold, upsample, downsample, compare_masked, no_error, debug, flex_mode)

cli.add_command(compare)

if __name__ == "__main__":
    cli()
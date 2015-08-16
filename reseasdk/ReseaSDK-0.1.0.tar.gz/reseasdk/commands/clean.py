import shutil


SHORT_HELP = "remove generated files during builds"
LONG_HELP = """
Usage: reseasdk clean
"""


def clean():
    shutil.rmtree('build')


def main(args):
    clean()

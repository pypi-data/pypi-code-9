#! /usr/bin/env python3

from clize import run, parameters
from clean_directories import files

__prog__ = 'clean'
__version__ = 0.1

def version():
    """Print the version of the script"""
    return "{0} {1}".format(__prog__, __version__)


def _main(*directories, force:'f'=False,
        verbose:'v'=False, recursive:'r'=False,
        pattern:('p', parameters.multi())=None,
        configuration:('c', parameters.multi())=None):
    """

    force: Don't prompt user before removal

    verbose: Print what is being done

    recursive: Walk through directories recursively

    pattern: Use these patterns to match files

    configuration: Read patterns from given files
    """

    # default parameters
    if len(directories) == 0:
        directories = ('.',)
    if not pattern and not configuration:
        configuration = ['default']

    # Reading patterns from configuration files
    for config_file in configuration:
        pattern.extend(files.PatternFile(config_file))

    # Creating and processing the request
    request = files.CleaningRequest(pattern, directories, recursive)
    for file in request:
        files.CleaningFile(file, verbose, force).remove()

def main():
    run(_main, alt=[version])

if __name__ == '__main__':
    main()

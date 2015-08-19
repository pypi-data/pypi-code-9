"""
# handleget sourcecode -- please see handleget/readme.md
## src/output.py

The purpose of this file is to consolidate all output handling.
"""
import sys
import click

class OutputStrings(object):
    """
    Container for all the output messages
    """
    error   =   '\n! Critcal Error: '
    warning =   '\n! Warning: '
    info =      '\n! Info: '
    debug =     '\n! Debug: '

    # Service Loading Error
    service_load = error + "You're services folder does not exist, or "+ \
                   "your permissions are misconfigured. Please double check "+ \
                   "the configuration."

    config_path_warning = warning + "Invalid config file, using defaults."

    # Response Loading Error
    response_requst = warning +" The response to {0} failed. This could be "+\
                      "because you're internet is down, or because the"+\
                       "service is misconfigured."

    warn_invalid_service = warning + "Failed to load service {0}"

class ErrorHandler(object):
    """
    Important class that catches errors and handles them neatly..
    """

    def __init__(self, verbose=False):
        self.strings = OutputStrings()
        self.verbose = verbose

    def catch_invalid_service(self, e, service_name):
        if self.verbose:
            click.echo(e)
        click.echo(self.strings.warn_invalid_service.format(service_name))
        

terms= """\
  MiModD (Mutation Identification in Model Organism Genomes using Desktop PCs)
  Copyright (C) 2013, 2014, 2015  Wolfgang Maier

  Version: {0}

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
  
                               *****
"""

class Version (tuple):
    def __str__ (self):
        return '.'.join(str(d) for d in self)

__version__ = Version([0, 1, 7, 0])
terms = terms.format(__version__)

def catch_sigterm (signum, frame):
    """Define package-wide behavior on SIGTERM."""

    raise SystemExit ('Execution stopped by system.')


class MiModDError (Exception):
    """Base class for application-specific errors."""

    pass


class FileAccessError (MiModDError):
    """Base class for file system related errors."""

    pass


class ParseError (MiModDError):
    """Base class for input parsing errors."""

    def __init__ (self, message, *args):
        self.message = message
        self.args = args

    def __str__ (self):
        return str(self.message.format(*self.args))


class ConfigParseError (ParseError):
    """Exception class for errors during parsing of configuration settings."""

    pass


class ArgumentParseError (ParseError):
    """Exception class for errors during argument parsing."""

    pass


class ArgumentValidationError (ArgumentParseError):
    """Exception class for errors during argument validation."""
    
    pass


class FormatParseError (ParseError, RuntimeError):
    """Exception class for errors in parsing biosequence formats."""

    def __init__ (self, message, token = None, line_no = None,
                  help = None, context = None):
        self.message = message
        self.help = help
        self.token = token
        self.line_no = line_no
        self.context = context

    def __str__ (self):
        msg = self.message.format(token = self.token, line_no = self.line_no)
        if self.help:
            help = self.help.format(token = self.token, line_no = self.line_no)
            msg += '\n' + help
        return msg


class SamtoolsRuntimeError (MiModDError, RuntimeError):
    """Exception class for all errors encountered with internal calls to samtools."""

    def __init__ (self, message, call, error):
        self.message = message
        self.call = call.strip()
        self.error = error.strip()

    def __str__ (self):
        if self.error:
            msg_header = '"{0}" failed with:\n{1}\n\n'.format(
                self.call, self.error)
        else:
            msg_header = '{0} failed.\nNo further information about this error is available.\n\n'.format(
                self.call)
        return msg_header + self.message


class DependencyError (MiModDError):
    """Exception class to be used when package dependencies cannot be located."""

    pass

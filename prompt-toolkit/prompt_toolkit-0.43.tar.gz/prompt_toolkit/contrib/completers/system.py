from __future__ import unicode_literals

from prompt_toolkit.contrib.regular_languages.completion import GrammarCompleter
from prompt_toolkit.contrib.regular_languages.compiler import compile

import os

from .filesystem import PathCompleter

__all__ = (
    'SystemCompleter',
)


class SystemCompleter(GrammarCompleter):
    """
    Completer for system commands.
    """
    def __init__(self):
        # Compile grammar.
        g = compile(
            r"""
                # First we have an executable.
                (?P<executable>[^\s]+)

                # Ignore literals in between.
                (
                    \s+
                    ("[^"]*" | '[^']*' | [^'"]+ )
                )*

                \s+

                # Filename as parameters.
                (
                    (?P<filename>[^\s]+) |
                    "(?P<double_quoted_filename>[^\s]+)" |
                    '(?P<single_quoted_filename>[^\s]+)'
                )
            """,
            escape_funcs={
                'double_quoted_filename': (lambda string: string.replace('"', '\\"')),
                'single_quoted_filename': (lambda string: string.replace("'", "\\'")),
            },
            unescape_funcs={
                'double_quoted_filename': (lambda string: string.replace('\\"', '"')),  # XXX: not enterily correct.
                'single_quoted_filename': (lambda string: string.replace("\\'", "'")),
            })

        # Create GrammarCompleter
        super(SystemCompleter, self).__init__(
            g,
            {
                'executable': PathCompleter(only_directories=False,
                                            min_input_len=1,
                                            get_paths=lambda: os.environ.get('PATH', '').split(os.pathsep),
                                            file_filter=lambda name: os.access(name, os.X_OK),
                                            expanduser=True),
                'filename': PathCompleter(only_directories=False, expanduser=True),
                'double_quoted_filename': PathCompleter(only_directories=False, expanduser=True),
                'single_quoted_filename': PathCompleter(only_directories=False, expanduser=True),
            })

# /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        if 'formatter_class' not in kwargs:
            kwargs['formatter_class'] = HelpFormatter
        if 'usage' not in kwargs:
            kwargs['usage'] = '%(prog)s [command] [options]'

        super().__init__(*args, **kwargs)

    def _parse_known_args(self, arg_strings, namespace):
        if ['__options__'] == arg_strings:
            print('OPTIONS JSON')
            self.exit()
        else:
            return super()._parse_known_args(arg_strings, namespace)


class HelpFormatter(argparse.HelpFormatter):
    """Same as the original HelpFormatter, but only prints meta-vars once.

    Example:      -s, --long ARGS
    Instead of:   -s ARGS, --long ARGS
    """
    def _format_action_invocation(self, action):
        if not action.option_strings:
            default = self._get_default_metavar_for_positional(action)
            metavar, = self._metavar_formatter(action, default)(1)
            return metavar
        else:
            parts = []
            if action.nargs == 0:
                parts.extend(action.option_strings)
            else:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                parts.extend(action.option_strings)
                parts[-1] += ' ' + args_string
            return ', '.join(parts)

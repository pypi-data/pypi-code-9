# This code can be put in any Python module, it does not require IPython
# itself to be running already.  It only creates the magics subclass but
# doesn't instantiate it yet.
from __future__ import print_function
from datetime import datetime
import re
import logging
from itertools import chain
from threading import Thread
import shlex
from time import sleep
import os
import sys

from dateutil.parser import parse as parse_datetime
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
from IPython import get_ipython
from IPython.utils._process_common import arg_split
from IPython.lib.pretty import pprint
from iodine.salt_rest import RestClient
from docopt import docopt, DocoptExit
import yaml
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.lexers.data import YamlLexer
from pygments.lexers.markup import RstLexer
from pygments.formatters import Terminal256Formatter, NullFormatter
from pprint import pformat


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

CACHE_TIMEOUT = 3600
JOB_TIMEOUT = 60
formatter = NullFormatter() if 'win' in sys.platform else Terminal256Formatter()
yaml_lexer = YamlLexer()
python_lexer = PythonLexer()


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            doc = fn.__doc__
            res = docopt(doc, shlex.split(arg))
            opt = {}
            for key, val in res.items():
                if key.startswith('<'):
                    key = key[1:-1]
                opt[key] = val

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


# TODO https://docs.saltstack.com/en/latest/topics/netapi/writing.html#configuration
# The class MUST call this class decorator at creation time
@magics_class
class SaltMagics(Magics):
    def __init__(self, shell, no_cache=False, **opts):
        # You must call the parent constructor
        super(SaltMagics, self).__init__(shell)
        self.opts = opts
        self.client = RestClient(opts)
        self.client.login()
        self.result = None
        self.cache = {}
        if not no_cache:
            self._cache_minions()
            self.cache_thread = Thread(target=self._cache_run)
            self.cache_thread.start()

    def _set_result(self, result, name='salt_result'):
        self.shell.user_ns[name] = result
        self.result = result

    def _print_yaml(self, result, end='\n'):
        result = yaml.safe_dump(result, default_flow_style=False)
        print(highlight(
            result,
            yaml_lexer,
            formatter), end=end)

    def _print_python(self, result, end='\n'):
        print(highlight(
            pformat(result),
            python_lexer,
            formatter), end=end)


    _print = _print_yaml

    def _run(self, args):
        try:
            result = self.client.minions_run(**args)
            minions = result['return'][0].get('minions')
            if not minions:
                print("No minions matched.")
                return {}
            jid = result['return'][0]['jid']
            total_time = 0
            final_result = {}
            while True:
                result = self.client.jobs(jid)
                #pprint(result)
                _result = result['return'][0]
                new = set(_result.keys()) - set(final_result.keys())
                final_result.update(_result)
                new_results = {k: v for k, v in final_result.items() if k in new}
                if new_results:
                    self._print(new_results, end='')
                if len(_result) == len(minions):
                    break
                starttime = parse_datetime(result['info'][0]['StartTime'])
                total_time = (datetime.now()-starttime).total_seconds()
                if total_time > JOB_TIMEOUT:
                    break
                sleep(0.5)

            self._set_result(final_result)
            #self._print(result)
            print("Result in %s secs" % total_time)
            no_response = (set(minions) - set(final_result.keys()))
            if no_response:
                print("No return from: %s" % no_response)
            return result
        except KeyboardInterrupt as e:
            return {}


    @docopt_cmd
    @line_magic
    def salt(self, args):
        """Salt command

        Usage:
            salt [options] <tgt> <fun> [<arg>...]

        Options:
            -E, --pcre          Instead of using shell globs to evaluate the target
                                servers, use pcre regular expressions
            -L, --list          Instead of using shell globs to evaluate the target
                                servers, take a comma or space delimited list of
                                servers.
            -G, --grain         Instead of using shell globs to evaluate the target
                                use a grain value to identify targets, the syntax for
                                the target is the grain key followed by a
                                globexpression: "os:Arch*"
            -P, --grain-pcre    Instead of using shell globs to evaluate the target
                                use a grain value to identify targets, the syntax for
                                the target is the grain key followed by a pcre regular
                                expression: "os:Arch.*"
            -N, --nodegroup     Instead of using shell globs to evaluate the target
                                use one of the predefined nodegroups to identify a
                                list of targets.
            -R, --range         Instead of using shell globs to evaluate the target
                                use a range expression to identify targets. Range
                                expressions look like %cluster
            -C, --compound      The compound target option allows for multiple target
                                types to be evaluated, allowing for greater
                                granularity in target matching. The compound target is
                                space delimited, targets other than globs are preceded
                                with an identifier matching the specific targets
                                argument type: salt 'G@os:RedHat and webser* or
                                E@database.*'
            -I, --pillar        Instead of using shell globs to evaluate the target
                                use a pillar value to identify targets, the syntax for
                                the target is the pillar key followed by a glob
                                expression: "role:production*"
            -J, --pillar-pcre   Instead of using shell globs to evaluate the target
                                use a pillar value to identify targets, the syntax for
                                the target is the pillar key followed by a pcre
                                regular expression: "role:prod.*"
            -S, --ipcidr        Match based on Subnet (CIDR notation) or IP address.

        Variable salt_result is available with the last result of this command
        """
        for expr_form in ['grain', 'list', 'pcre', 'grain-pcre', 'pillar',
                          'pillar-pcre', 'nodegroup', 'compound', 'range']:
            if args.get('--%s' % expr_form):
                args['expr_form'] = expr_form.replace('-', '_')
        log.debug("run: %s", args)
        self._run(args)

    @docopt_cmd
    @line_magic
    def salt_runner(self, args):
        """Salt runner command

        Usage:
            salt_runner [options] <fun> [<arg>...]

        Variable salt_result is available with the last result of this command
        """
        args['client'] = 'runner'
        result = self.client.run(**args)
        self._print(result)
        self._set_result(result)

    @docopt_cmd
    @line_magic
    def salt_help(self, args):
        """Get doc string Salt modules and functions

        Usage:
            salt_help [options] <fun>

        """
        fun = args['fun']
        functions = self._cache_get('functions')
        for fs in functions.values():
            if fun in fs:
                self._print_plain(fs[fun])
                break
    @line_magic
    def print_python(self, args):
        self._print = self._print_python
    @line_magic
    def print_yaml(self, args):
        self._print = self._print_yaml

    def _cache_minions(self):
        result = self.client.minions_run(
            tgt='*', fun='test.ping')['return'][0]['minions']
        self.cache['minions'] = result

    def _cache_run(self):
        log.debug("Caching completions ...")
        result = self.cache['functions'] = self.client.run(
            tgt='*', fun='sys.doc')['return'][0]
        self.cache['functions'] = result
        self.cache['timestamp'] = datetime.now()
        log.debug("Done Caching completions ...")

    def _cache_get(self, key):
        if key not in self.cache or (
                'timeout' in self.cache and
                (datetime.now() - self.cache['timestamp']
                 ).total_seconds() > CACHE_TIMEOUT):
            self._cache_run()
        return self.cache[key]

    @line_magic
    def reset_cache(self, args):
        self.cache.clear()
        self._cache_run()

    def _salt_completer(self, shell, event):
        """Complete files that end in .py or .ipy or .ipynb for the %run command.
        """
        try:
            minions = self._cache_get('minions')
            luc = event.text_until_cursor
            luc = re.sub('-.{1} ', '', luc)
            luc = [x for x in re.split('( )', luc) if x]
            luclen = len(luc)
            if luclen == 2 or luclen == 3:
                return list(minions)
            elif luclen == 4 or luclen == 5:
                minion = luc[-1] if luclen == 4 else luc[-2]
                functions = self._cache_get('functions')
                functions = functions.get(minion, {}).keys() or set(
                    chain.from_iterable(
                        [m.keys() for m in functions.values()]))
                return functions
        except Exception as e:
            print(e)
        return []

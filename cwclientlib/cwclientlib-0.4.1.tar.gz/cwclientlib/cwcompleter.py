# -*- coding: utf-8 -*-
#
# copyright 2014-2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of cwclientlib.
#
# cwclientlib is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 2.1 of the License, or (at your
# option) any later version.
#
# cwclientlib is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with cwclientlib. If not, see <http://www.gnu.org/licenses/>.

"""provide RQL autocompletion for statements starting with::

   >>> whatever.execute('Any X WHERE X is
   >>> rql('Any X WHERE X is

"""
import re
import readline
from rlcompleter import Completer
import requests

from cwclientlib.cwproxy import build_request_headers


class AbstractMatcher(object):
    """Abstract class for CWShellCompleter's matchers.

    A matcher should implement a ``possible_matches`` method. This
    method has to return the list of possible completions for user's input.
    Because of the python / readline interaction, each completion should
    be a superset of the user's input.

    NOTE: readline tokenizes user's input and only passes last token to
    completers.
    """

    def possible_matches(self, text):
        """return possible completions for user's input.

        Parameters:
            text: the user's input

        Return:
            a list of completions. Each completion includes the original input.
        """
        raise NotImplementedError()


class RQLExecuteMatcher(AbstractMatcher):
    """Custom matcher for rql queries.

    If user's input starts with ``rql(`` or ``session.execute(`` and
    the corresponding rql query is incomplete, suggest some valid completions.
    """
    query_match_rgx = re.compile(
        r'(?P<func_prefix>\s*(?:rql)'  # match rql, possibly indented
        r'|'                           # or
        r'\s*(?:\w+\.execute))'        # match .execute, possibly indented
        # end of <func_prefix>
        r'\('                          # followed by a parenthesis
        r'(?P<quote_delim>["\'])'      # a quote or double quote
        r'(?P<parameters>.*)')         # and some content

    def __init__(self, client):
        self.client = client

    @staticmethod
    def match(text):
        """check if ``text`` looks like a call to ``rql`` or ``session.execute``

        Parameters:
            text: the user's input

        Returns:
            None if it doesn't match, the query structure otherwise.
        """
        query_match = RQLExecuteMatcher.query_match_rgx.match(text)
        if query_match is None:
            return None
        parameters_text = query_match.group('parameters')
        quote_delim = query_match.group('quote_delim')
        # first parameter is fully specified, no completion needed
        if re.match(r"(.*?)%s" % quote_delim, parameters_text) is not None:
            return None
        func_prefix = query_match.group('func_prefix')
        return {
            # user's input
            'text': text,
            # rql( or session.execute(
            'func_prefix': func_prefix,
            # offset of rql query
            'rql_offset': len(func_prefix) + 2,
            # incomplete rql query
            'rql_query': parameters_text,
            }

    def possible_matches(self, text):
        """call ``rql.suggestions`` component to complete user's input.
        """
        # readline will only send last token, but we need the entire
        # user's input
        user_input = readline.get_line_buffer()
        query_struct = self.match(user_input)
        if query_struct is None:
            return []
        else:
            # we must only send completions of the last token =>
            # compute where it starts relatively to the rql query
            # itself.
            compl_offset = readline.get_begidx() - query_struct['rql_offset']
            rql_query = query_struct['rql_query']
            return [suggestion[compl_offset:]
                    for suggestion in get_suggestions(self.client, rql_query)]


class DefaultMatcher(AbstractMatcher):
    """Default matcher: delegate to standard's `rlcompleter.Completer`` class
    """
    def __init__(self, namespace=None):
        self.completer = Completer(namespace)

    def possible_matches(self, text):
        if "." in text:
            return self.completer.attr_matches(text)
        else:
            return self.completer.global_matches(text)


class CWShellCompleter(object):
    """Custom auto-completion helper for cubicweb-ctl shell.

    ``CWShellCompleter`` provides a ``complete`` method suitable for
    ``readline.set_completer``.

    Attributes:
        matchers: the list of ``AbstractMatcher`` instances that will suggest
                  possible completions

    The completion process is the following:

    - readline calls the ``complete`` method with user's input,
    - the ``complete`` method asks for each known matchers if
      it can suggest completions for user's input.
    """

    def __init__(self, client, namespace=None):
        # list of matchers to ask for possible matches on completion
        self.matchers = [DefaultMatcher(namespace)]
        self.matchers.insert(0, RQLExecuteMatcher(client))

    def complete(self, text, state):
        """readline's completer method

        see:
          http://docs.python.org/2/library/readline.html#readline.set_completer
        for more details.

        Implementation inspired by `rlcompleter.Completer`
        """
        if state == 0:
            # reset self.matches
            self.matches = []
            for matcher in self.matchers:
                matches = matcher.possible_matches(text)
                if matches:
                    self.matches = matches
                    break
            else:
                return None  # no matcher able to handle `text`
        try:
            return self.matches[state]
        except IndexError:
            return None


def get_suggestions(client, user_input):
    try:
        data = {'fname': 'rql_suggest',
                'term': user_input,
                }
        sugg = requests.post(url=client.build_url('/json'),
                             headers=build_request_headers(),
                             verify=client._ssl_verify,
                             auth=client.auth,
                             data=data).json()
    except Exception as exc:
        print ("Failed to fetch suggestions: {0}".format(exc))
    return sugg


def setup_autocompleter(client, namespace=None):
    import readline
    from .cwcompleter import CWShellCompleter
    completer = CWShellCompleter(client, namespace)
    readline.set_completer(completer.complete)
    readline.parse_and_bind('tab: complete')

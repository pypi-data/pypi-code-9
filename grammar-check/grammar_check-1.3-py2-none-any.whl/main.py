# -*- coding: utf-8 -*-
u"""LanguageTool command line."""

from __future__ import with_statement
from __future__ import absolute_import
import argparse
import locale
import re
import sys

from . import __version__
from . import get_build_date
from . import get_version
from . import Error
from . import LanguageTool
from io import open


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__.strip(),
                                     prog=u'grammar-check')
    parser.add_argument(u'files', nargs=u'+',
                        help=u'plain text file or "-" for stdin')
    parser.add_argument(u'-c', u'--encoding',
                        help=u'input encoding')
    parser.add_argument(u'-l', u'--language', metavar=u'CODE',
                        help=u'language code of the input or "auto"')
    parser.add_argument(u'-m', u'--mother-tongue', metavar=u'CODE',
                        help=u'language code of your first language')
    parser.add_argument(u'-d', u'--disable', metavar=u'RULES', type=get_rules,
                        action=RulesAction, default=set(),
                        help=u'list of rule IDs to be disabled')
    parser.add_argument(u'-e', u'--enable', metavar=u'RULES', type=get_rules,
                        action=RulesAction, default=set(),
                        help=u'list of rule IDs to be enabled')
    parser.add_argument(u'--api', action=u'store_true',
                        help=u'print results as XML')
    parser.add_argument(
        u'--version', action=u'version',
        version=u'%(prog)s {} (LanguageTool {} ({}))'.format(
            __version__,
            get_version(),
            get_build_date()),
        help=u'show version')
    parser.add_argument(u'-a', u'--apply', action=u'store_true',
                        help=u'automatically apply suggestions if available')
    parser.add_argument(u'-s', u'--spell-check-off', dest=u'spell_check',
                        action=u'store_false',
                        help=u'disable spell-checking rules')
    parser.add_argument(u'--ignore-lines',
                        help=u'ignore lines that match this regular expression')
    return parser.parse_args()


class RulesAction(argparse.Action):

    def __call__(self, parser, namespace, values, option_string=None):
        getattr(namespace, self.dest).update(values)


def get_rules(rules):
    return set(rule.upper() for rule in re.findall(ur"[\w\-]+", rules))


def get_text(filename, encoding, ignore):
    with open(filename, encoding=encoding) as f:
        text = u''.join(u'\n' if (ignore and re.match(ignore, line)) else line
                       for line in f.readlines())
    return text


def print_unicode(text):
    u"""Print in a portable manner."""
    if sys.version_info[0] < 3:
        text = text.encode(u'utf-8')

    print text


def main():
    args = parse_args()

    status = 0

    for filename in args.files:
        if len(args.files) > 1:
            print >>sys.stderr, filename

        if filename == u'-':
            filename = sys.stdin.fileno()
            encoding = args.encoding or (
                sys.stdin.encoding if sys.stdin.isatty()
                else locale.getpreferredencoding()
            )
        else:
            encoding = args.encoding or u'utf-8'

        lang_tool = LanguageTool(
            motherTongue=args.mother_tongue)
        guess_language = None

        try:
            text = get_text(filename, encoding, ignore=args.ignore_lines)
        except UnicodeError, exception:
            print >>sys.stderr, u'{}: {}'.format(filename, exception)
            continue

        if args.language:
            if args.language.lower() == u'auto':
                try:
                    from guess_language import guess_language
                except ImportError:
                    print >>sys.stderr, u'guess_language is unavailable.'
                    return 1
                else:
                    language = guess_language(text)
                    if not args.api:
                        print >>sys.stderr, u'Detected language: {}'.format(language)
                    if not language:
                        return 1
                    lang_tool.language = language
            else:
                lang_tool.language = args.language

        if not args.spell_check:
            lang_tool.disable_spellchecking()

        lang_tool.disabled.update(args.disable)
        lang_tool.enabled.update(args.enable)

        try:
            if args.api:
                print_unicode(lang_tool._check_api(text).decode())
            elif args.apply:
                print_unicode(lang_tool.correct(text))
            else:
                for match in lang_tool.check(text):
                    rule_id = match.ruleId
                    if match.subId is not None:
                        rule_id += u'[{}]'.format(match.subId)

                    replacement_text = u', '.join(
                        u"'{}'".format(word)
                        for word in match.replacements).strip()

                    message = match.msg

                    # Messages that end with punctuation already include the
                    # suggestion.
                    if replacement_text and not message.endswith((u'.', u'?')):
                        message += u'; suggestions: ' + replacement_text

                    print_unicode(u'{}:{}:{}: {}: {}'.format(
                        filename,
                        match.fromy + 1,
                        match.fromx + 1,
                        rule_id,
                        message))

                    status = 2
        except Error, exception:
            print >>sys.stderr, u'{}: {}'.format(filename, exception)
            continue

    return status

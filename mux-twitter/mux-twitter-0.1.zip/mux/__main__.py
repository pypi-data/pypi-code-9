#!/usr/bin/env python
"""cmdline: utility for interacting with the main game daemon"""

from .credentials import OAUTH_TOKEN, OAUTH_TOKEN_SECRET
from .credentials import APP_KEY, APP_SECRET
from .credentials import save_oauth_tokens
from .utils import get_twitter, scoped_unlink, err_print
from .utils import get_editor, get_terminal_width
from . import __version__, program_name, TWITTER_MAX_LEN, auth_file

from argparse import ArgumentParser, ONE_OR_MORE
from blessed import Terminal
from subprocess import call
from appdirs import AppDirs
from twython import Twython
from enum import IntEnum
from pathlib import Path

import webbrowser
import tempfile
import textwrap
import shlex
import sys
import os


class EXIT(IntEnum):
    TOO_LONG = 2
    NO_MSG = 3

def write_template(file, width):
    lines, chars = divmod(TWITTER_MAX_LEN, width)
    lines = ["-" * width] * lines
    lines.append("-" * chars)
    
    footer = textwrap.wrap("Compose your tweet on an empty line "
                           "Whitespace will be stripped, as will "
                           "lines beginning with #",
                            width - 2)

    file.write('\n')
    file.write('\n')
    for line in lines:
        file.write("#{}\n".format(line[1:]))
    file.write('\n')
    for line in footer:
        file.write("# {}\n".format(line))
    
    file.flush()

def authorize():
    twitter = Twython(APP_KEY, APP_SECRET)

    auth = twitter.get_authentication_tokens()

    OAUTH_TOKEN = auth['oauth_token']
    OAUTH_TOKEN_SECRET = auth['oauth_token_secret']

    webbrowser.open(auth['auth_url'])
    print(auth['auth_url'])

    pin = input("Pin: ")

    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    final_step = twitter.get_authorized_tokens(pin)

    OAUTH_TOKEN = final_step['oauth_token']
    OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']

    print("OAUTH Token", OAUTH_TOKEN)
    print("OAUTH Token Secret", OAUTH_TOKEN_SECRET)

    return OAUTH_TOKEN, OAUTH_TOKEN_SECRET


def stream_main(argv=sys.argv[1:]):
    pass

def cli_main(argv=sys.argv[1:]):
    args = ArgumentParser()
    args.add_argument("--version", action='version', version='%(prog)s {}'.format(__version__),
        help="Display the client version")
    
    subs = args.add_subparsers(dest="command")
    
    auth = subs.add_parser("auth", help="Authorise this utility to access your twitter account")
    
    tweet = subs.add_parser("tweet", help="Send a message via twitter")
    tweet.add_argument("msg", nargs=ONE_OR_MORE, help="The message to tweet")
    tweet.add_argument("-r", "--reply", type=int, default=None,
        help="The ID of a tweet to reply to (Default: Send a normal tweet)")

    compose = subs.add_parser("compose", help="Launch a text editor to edit a message to send to twitter")
    compose.add_argument("-r", "--reply", type=int, default=None,
        help="The ID of a tweet to reply to (Default: Send a normal tweet)")
    compose.add_argument("-w", "--width", type=int, default=None,
        help="Word wrap the tweet template to the width of the terminal (Default: Auto detect width)")
    compose.add_argument("-e", "--editor",
        help="Text editor to invoke to edit the tweet (Default: Auto detect)")

    options = args.parse_args(argv)

    if not options.command:
        args.print_usage()
        sys.exit(os.EX_USAGE)

    if options.command == 'auth':
        token, secret = authorize()
        save_oauth_tokens(token, secret)

        sys.exit(os.EX_OK)

    elif options.command == 'tweet':
        options.msg = " ".join(options.msg)

        if len(options.msg) > 140:
            err_print("Output too long")
            sys.exit(EXIT.TOO_LONG)
        if len(output) == 0:
            err_print("Output too short")
            sys.exit(EXIT.NO_MSG)

        twitter = get_twitter()
        twitter.update_status(status=options.msg)

    elif options.command == 'compose':
        editor = options.editor or get_editor() or 'vi'
        width = options.width or get_terminal_width()
        template = tempfile.NamedTemporaryFile(mode='w+',
                                               prefix=program_name + '-', 
                                               delete=False,
                                               )

        cmd = "{} {}".format(editor, template.name)

        with scoped_unlink(template):
            write_template(template, width)
            template.seek(0)
    
            cmd_failed = call(cmd, shell=True)
            if cmd_failed:
                err_print("Error in text editor")
                sys.exit(cmd_failed)
    
        output = (line.strip() for line in template)
        output = (line for line in output if line)
        output = (line for line in output if not line.startswith("#"))
        output = "".join(output)

        # TODO: markdown like link intergration and shortening

        if len(output) > 140:
            err_print("Output too long")
            sys.exit(EXIT.TOO_LONG)
        if len(output) == 0:
            err_print("Output too short")
            sys.exit(EXIT.NO_MSG)
        print(">>> " + output)
        sys.exit(0)
        twitter = get_twitter()
        twitter.update_status(status=output)
        
    else:
        err_print("Unknown option")
        args.print_usage()
        sys.exit(os.EX_USAGE)

if __name__ == "__main__":
    sys.exit(main())

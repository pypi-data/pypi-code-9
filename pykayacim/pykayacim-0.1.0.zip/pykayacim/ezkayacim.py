#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This is a command-line tool for PyKayacIM.

Functions defined in this module should not be used directly.

"""

from __future__ import unicode_literals
from __future__ import absolute_import
import pykayacim.api
import pykayacim.exceptions
import argparse
import sys
import builtins
import logging
import atexit

_ez_logger = logging.getLogger("EzKayacIM")
api_logger = logging.getLogger(pykayacim.api.__name__)


@atexit.register
def finish():
    """Called when this command-line tool exits.

    """

    _ez_logger.info("EzKayacIM exits.")


def decode_params(params):
    """Decode values of the provided dictionary if necessary. 

    """

    decoded_params = dict()
    for k, v in params.items():
        if isinstance(v, builtins.bytes):
            decoded_params[k] = v.decode(sys.stdin.encoding)
        else:
            decoded_params[k] = v
    _ez_logger.debug("Decoded the provided parameters.")
    return decoded_params


def _send_notification(args):
    """Send a notification.

    """

    init_params = {"username": args.username, "method": args.method}
    send_params = {"message": args.message, "handler": args.scheme}
    if args.method == "password":
        init_params["key"] = args.pw
    elif args.method == "secret":
        init_params["key"] = args.key

    _ez_logger.debug("Initializing an KayacIMAPI instance.")
    api = pykayacim.api.KayacIMAPI(**decode_params(init_params))

    _ez_logger.debug("Sending a notification.")
    try:
        api.send(**decode_params(send_params))
    except pykayacim.exceptions.PyKayacIMError as err:
        _ez_logger.error("Failed to send a notification.")
        sys.exit(-1)
    else:
        _ez_logger.info("Successfully sent a notification.")


def main():
    """Used if this module is run as a script.

    """

    # Logging
    _ez_logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    formatter = logging.Formatter(
        "%(levelname)s: %(name)s - %(message)s")
    console_handler.setFormatter(formatter)
    _ez_logger.addHandler(console_handler)
    api_logger.addHandler(console_handler)
    _ez_logger.info("EzKayacIM started.")

    # Top-level
    parser = argparse.ArgumentParser(
        description="Send push notifications via im.kayac.com.",
        epilog="See '%(prog)s <method> --help' for details.")
    subparsers = parser.add_subparsers(
        help="Available authorization methods.",
        dest="method")

    # Subcommands
    parser_none = subparsers.add_parser("none",
                                        help="No authorization.")
    parser_none.set_defaults(func=_send_notification)

    parser_password = subparsers.add_parser("password",
                                            help="Use authorization with a password.")
    parser_password.set_defaults(func=_send_notification)

    parser_secret = subparsers.add_parser("secret",
                                          help="Use secret key cryptosystem.")
    parser_secret.set_defaults(func=_send_notification)

    # Common arguments
    for p in [parser_none, parser_password, parser_secret]:
        p.add_argument("username",
                       help="The username of your im.kayac.com account.")
        p.add_argument("message",
                       help="The message to be sent.")
        p.add_argument("-s", "--scheme",
                       help="The URI scheme for iPhone applications.")

    # Other arguments
    parser_password.add_argument("pw",
                                 help="The password for notifications, not for your account.")
    parser_secret.add_argument("key",
                               help="The secret key for sending notifications.")

    args = parser.parse_args()

    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

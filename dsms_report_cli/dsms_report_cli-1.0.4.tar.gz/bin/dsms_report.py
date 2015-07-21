#! /usr/bin/env python

"""
Usage:
    dsms_blacklist.py
    dsms_blacklist.py [--ignore_ssl_errs] [--query=profile:phishing] [--template=<s>] [--template_dir=mytemplates]
    dsms_blacklist.py --list_templates [--template_dir=/home/tom/mytemplates]

Options:
  --ignore_ssl_errs        Ignore errors with SSL certs (e.g. self signed)
  --query=<s>              DSMS search to run [default: age:7]
  --template=<s>           Output format of report [default: text_urls]
  --list_templates         List default templates available
  --template_dir=<s>       Path to a directory containing extra templates
"""

import sys
import dsms_cmd.dsms_cmd as dcmd

from docopt import docopt


def list_templates(args):
    """
    Print a text list of template names available to be passed into the
    --template parameter.
    """
    r = dcmd.DSMSReporter(do_auth=False)
    print "\n".join(
        sorted(
            r.list_templates(template_dir=args.get("--template_dir"))
        )
    )
    sys.exit()


def run_report(args):
    """
    Attempt to auth to DSMS, run a --query if provided or get everything,
    then try to render with --template in the default template path or a custom
    --template_dir.
    Print to stdout.
    """
    try:
        r = dcmd.DSMSReporter(ignore_ssl_errs=args.get("--ignore_ssl_errs"))

        data = r.query_data(args.get("--query"))
        print r.output(data, template=args.get("--template"),
                       template_dir=args.get("--template_dir"))
    except (RuntimeError, ValueError) as e:
        sys.exit(str(e))


def main():
    args = docopt(__doc__)

    if args.get("--list_templates"):
        list_templates(args)
    else:
        run_report(args)


if __name__ == "__main__":
    main()

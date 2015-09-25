#!/usr/bin/python2.7
"""Mailwatch - output the list of new mails in a Maildir hierarchy"""

import argparse
import codecs
import inspect
import locale
import mailbox
import os
import re
import sys

from collections import Counter
from email.header import decode_header


__version__ = "0.2"
__author__ = "Tobias Klausmann" 
__author_email__ = "klausman()schwarzvogel.de"

# This will optionally be replaced later
def eprint(_):
    """Empty hull, the default eprint()"""
    pass

def _eprint(msg):
    """The eprint replacement if debug is set"""
    prefix = " " * (len(inspect.stack())-3)
    sys.stderr.write(prefix+msg+"\n")


class OnlyNewMaildir(mailbox.Maildir):
    """Overload/Augment basic Maildir to just look at new mail"""
    def _refresh(self):
        """Update table of contents mapping."""
        self._toc = {}
        for subdir in ('new', ):
            subdir_path = os.path.join(self._path, subdir)
            for entry in os.listdir(subdir_path):
                path = os.path.join(subdir_path, entry)
                if os.path.isdir(path):
                    continue
                uniq = entry.split(self.colon)[0]
                self._toc[uniq] = os.path.join(subdir, entry)

def loadconfig(fname):
    """Load configuration from file named fname"""
    eprint("Trying to load config file")
    try:
        homedir = os.environ["HOME"]
    except KeyError:
        homedir = "."
    eprint("Looking in '%s'" % (homedir))
    # These are the hardcoded defaults
    configvalues = { "maildir": "%s/Mail" % (homedir),
                     "whitelist": "",
                     "blacklist": "",
                     "linelength": "75",
                     "maxsubjects": "20",
                     "showempty": "0",
                     "unprintables": "replace",
    }
    eprint("Defaults: %s" % (configvalues))
    # Valid values for the errors= var of codec.Streamwriter
    validoptunprint = ['strict', 'ignore', 'replace', 'xmlcharrefreplace', 
                       'backslashreplace']
    eprint("Trying to read from '%s'" % (fname))
    try:
        content = open(fname).read()
    except IOError:
        return configvalues

    for line in content.split("\n"):
        eprint("Saw line '%s'" % (repr(line)))
        line = line.lstrip()
        if not line or line.startswith("#"):
            eprint("Skipping line")
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        eprint("Adding '%s'='%s' to config" % (key, value))
        configvalues[key] = value

    for field in ['blacklist', 'whitelist']:
        eprint("Added %s as %s" % (field, set(configvalues[field].split())))
        configvalues[field] = set(configvalues[field].split())

    if configvalues["unprintables"] not in validoptunprint:
        sys.stderr.write("Invalid value for 'unprintables' in %s: '%s'\n" %
                          (fname, configvalues["unprintables"]))
        sys.stderr.write("Valid values are: %s\n" % 
                         (",".join(validoptunprint)))
        sys.exit(1)

    eprint("Config file loading complete.")
    return configvalues

def subj_simplify(subj, config):
    """Simplify subjects so threads have uniform subjects"""
    eprint("Simplifying subject '%s'" % (subj))
    if subj is None:
        return "(none)"

    subj = subj.replace("\n", "")
    subj = subj.replace("\r", "")
    subj = subj.strip()
    subj = re.sub("(\t| )(\t| )*", " ", subj)
    subj = re.sub(" *(Re:|AW:|Fwd:|RE:|FW:) *", "", subj)
    eprint("Simplified subject: '%s'" % (subj))

    if len(subj) > int(config["linelength"]):
        subj = subj[:int(config["linelength"])]
        eprint("Shortened subject: '%s'" % (subj))

    return subj

def getboxlist(config):
    """Create list of relevant mailboxes from config values"""
    try:
        boxes = set(os.listdir(config.get('maildir')))
    except OSError, msg:
        sys.stderr.write("Could not open your mail directory: %s\n" % (msg))
        sys.exit(2)
    eprint("Full list of boxes: %s" % (boxes))
    if config.get('whitelist'):
        boxes &= config.get('whitelist')
    eprint("List of boxes after whitelisting: %s" % (boxes))
    if config.get('blacklist'):
        boxes -= config.get('blacklist')
    eprint("List of boxes after blacklisting: %s" % (boxes))

    boxes = list(boxes)
    boxes.sort()

    eprint("Final sorted list of boxes: %s" %(boxes))
    return boxes

def printmails(config, boxes, output):
    """Read mails from boxes and output them on file/stream output"""
    eprint("Number of boxes to examine: %s" % (len(boxes)))
    for box in boxes:
        eprint("Looking at box '%s'" % (box))
        mbox = OnlyNewMaildir("%s/%s"% (config.get('maildir'), box),
                              factory=None)
        subjects = Counter()
        for msg in mbox:
            eprint("Examining message")
            raw_subj = msg.get("Subject")
            decoded_subj = []
            if not raw_subj:
                decoded_subj = ["(none)"]
            else:
                eprint("Assembling tokens")
                for (token, enc) in decode_header(raw_subj):
                    if enc:
                        try:
                            if enc != "unknown":
                                decoded_subj.append(unicode(token, enc))
                        except UnicodeDecodeError:
                            decoded_subj.append('[]')
                    else:
                        decoded_subj.append(token)
                    eprint("New token list: %s" % (decoded_subj))
            try:
                subj = u"%s" % ("".join(decoded_subj))
            except UnicodeDecodeError:
                # Ok, we give up now, this mail is a _mess_
                subj = "(malformed)"
            eprint("Final decoded subject: %s" % (subj))
            subj = u"%s" % (subj_simplify(subj, config))
            subjects[subj] += 1

        if (len(subjects) > 0 and 
            (len(subjects) < int(config.get("maxsubjects")) or
             int(config.get("maxsubjects")) == -1)):

            eprint("Mailbox is nonempty (%s subjects)" %(len(subjects)))
            output.write("%s:\n" % (box))

            for subj, count in sorted(subjects.items(),
                                      key=lambda(k, v): (v, k),
                                      reverse=True):
                output.write("%3s %s\n"% (count, subj))
            output.write("\n")

        elif len(subjects) > 0:
            eprint("Mailbox is nonempty but too big to print (%s>%s)" %
                    (len(subjects), config.get("maxsubjects")))
            output.write("%s: %s\n" % (box, len(subjects)))
        elif config.get("showempty") != "0":
            eprint("Mailbox is empty")
            output.write("%s: 0\n" % (box))

def main():
    """Main program function"""

    # While this duplicates our efforts, it makes for earlier debugging
    if "-d" in sys.argv or "--debug" in sys.argv:
        global eprint
        eprint = _eprint

    try:
        default_cfgfile = "%s/.mwrc" % (os.environ["HOME"])
    except KeyError:
        default_cfgfile = ".mwrc"

    argp = argparse.ArgumentParser()
    argp.add_argument("-v", "--version", action="store_true",
        help='Show version information')
    argp.add_argument("-c", "--configfile", 
        help='Config file to read (default: %(default)s)', 
        default=default_cfgfile)
    argp.add_argument("-d", "--debug", action='store_true',
        help='Enable printing of debug info to stderr.') 
    argp.add_argument('boxes', metavar='box', type=str, nargs='*',
        help='Mailboxes to examine, default: all configured')

    args = argp.parse_args()

    if args.version:
        print("mailwatch (mw), v%s" % (__version__))
        print("(C) Copyright 2011 %s <%s>" % (__author__, __author_email__))
        print("Licensed under the GPL v2, see COPYING for details")
        sys.exit(0)

    config = loadconfig(args.configfile)
    eprint("Config settings:")
    eprint(str(config))

    boxes = getboxlist(config)
    # The commandlines overrides the configured boxes
    if len(args.boxes) > 0:
        boxes = args.boxes

    # Set up stdout so it just it just replaces nonprintables
    sys.stdout = codecs.getwriter(locale.getpreferredencoding())(
        sys.stdout, errors=config["unprintables"])
    printmails(config, boxes, sys.stdout)

if __name__ == "__main__":
    main()

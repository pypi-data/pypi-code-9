# encoding: UTF-8
# Copyright (C) 2009-2010, Stefan Schwarzer
# see the file LICENSE for the license of this software

"""
Configure the application.

Configuration is done from the command line and/or from
environment variables. Of these, currently only the variable
`WSB_IGNORE` is supported.

This module also contains the manpage-style documentation for end
users of Websourcebrowser.
"""

import fnmatch
import sys


MAN_PAGE = """\
NAME

  Websourcebrowser - conveniently browse source code with a webbrowser

SYNOPSIS

  wsbrowser [options]

  The name of the executable is wsbrowser on Posix and wsbrowser.py on
  Windows.

DESCRIPTION

  Websourcebrowser starts an internal webserver and listens for HTTP
  requests for directories and files in a project's source code
  directory. The web interface allows to browse the source code with a
  left frame containing the directory tree and a right frame a
  selected file. The directory frame is always accessible.

  If Pygments (http://pygments.org) is installed, files may be
  displayed with syntax highlighting.

  To stop Websourcebrowser, type Ctrl-C (on Posix) or Ctrl-Break (on
  Windows).

WEB INTERFACE

  After invoking Websourcebrowser, it outputs the URL you should put
  in the address line of your webbrowser. After you've done this, you
  get a display with two frames: The left displays the directory
  specified by the --root option (or the default), the right shows a
  placeholder. If you click a link in the left frame denoting a file,
  it's shown in the right frame. If the file is a binary file for
  which Websourcebrowser doesn't know to render it, a hexdump is shown
  instead. At the moment, this happens even for popular formats as
  PDF, and that will change.

  The directory display on the left has several framed links which you
  can imagine as buttons. "Reset view" resets the display, this is as
  if you just entered the root URL which Websourcebrowser prints in
  the terminal upon start. The button "Homepage" opens a new window
  with the page identified with the command line option
  --project-homepage. Below the two already described buttons you can
  control the number of expanded directory levels. By definition, when
  the level is 1, just a linear list of the directories and files in
  the project root directory is shown. A level of 2 means that the
  contained directories and files are also displayed. This is easier
  to check out than to describe. Note that you won't see a difference
  after a click if the project directory structure is not that deep.
  By the way, clicking on a directory link will show a list of its
  contents if they're not already displayed. If, for your taste, too
  many levels are shown, you can reduce them with the buttons at the
  top of the frame.

OPTIONS

  -h, --help
        Show this help text and exit.

  -r ROOT, --root=ROOT
        Set the document root directory (default: current directory).
        For example, if --root=/my/greatproject is specified, the URL
        path / will correspond to the directory /my/greatproject.
        Directories or files "above" the root directory aren't
        accessible (probably, see section BUGS).

  -t PROJECT_TITLE, --project-title=PROJECT_TITLE
        Set the project title to display as the title of the frameset
        (default: capitalized base name of the root directory, so the
        above root option sets a project title "Greatproject").

  -i PATTERN, --ignore-pattern=PATTERN
        Ignore directories and files matching this pattern (default:
        nothing is ignored). To specify more than one pattern, repeat
        this option.

        For each pattern, the corresponding pattern plus "/*" is also
        used, so you don't have to specify two patterns to ignore a
        directory and everything under it.

        Example: To ignore all Mercurial and Subversion bookkeeping
        files, use --ignore-pattern="/*.svn" --ignore-pattern="/*.hg".

  -l, --line-numbers
        Prepend lines of text files with line numbers (default: no
        line numbers).

        This works only if Pygments is installed, otherwise this
        option is ignored.

  --http-host=HTTP_HOST
        Use the specified host name or IP for the local interface to
        listen on (default: localhost).

        With the defaults for --http-host and --http-port, the address
        line in the browser is http://localhost:8000/ .

  --http-port=HTTP_PORT
        Listen on this HTTP port (default: 8000).

        With the defaults for --http-host and --http-port, the address
        line in the browser is http://localhost:8000/ .

  -c CLIENT, --allowed-client=CLIENT
        Allow remote access from this host name or IP address
        (default: allow only access from localhost). The localhost
        address is always included. For multiple host names or IP
        addresses use the option several times. For example:

        wsbrowser -c my.host.com -c 199.243.19.27

        As a special case, specifying ALL as the options value accepts
        requests from all addresses and so effectively makes
        Websourcebrowser a web server on the public internet, unless
        prevented by a router or firewall.

  --logging
        Activate logging of HTTP accesses to standard output (default:
        no logging).

ENVIRONMENT

  WSB_IGNORE
        Set wildcard patterns to ignore. If multiple patterns are
        given, they must be separated by whitespace.

        A typical example for WSB_IGNORE might be
        *.pyc  *.pyo  */.svn  *.svn/*  */.hg  */.hg/*  *.swp

        If both this environment variable and one or more
        --ignore-pattern options are used, the patterns from the
        command line are added to those from the environment variable.

BUGS

  Probably there are some bugs as Websourcebrowser is still alpha
  software. Currently, I don't recommend to use Websourcebrowser for
  use on the public internet because it may contain significant
  vulnerabilities. (I indeed paid attention to security though I would
  welcome an experienced fellow to spot security problems.)

  Since the software is still in the alpha stage, it may still change
  significantly. This may include incompatible variations like
  removing command line options or changing their semantics.

AUTHOR

  The author of Websourcebrowser is
  Stefan Schwarzer <sschwarzer@sschwarzer.net>.

SEE ALSO

  The pydoc module in the Python distribution similarly acts as a
  webserver if it's invoked as a program with the option -p and a port
  number.
"""

import optparse
import os
import socket
import sys

# Websourcebrowser modules
import coding
import tools

#
# constants used in several places
#
# Websourcebrowser version
VERSION = "0.4 pre-alpha"
# special value to denote allowance of all clients
ALL_CLIENTS = "all_clients_allowed"

# The following paths are also used in the JavaScript code. So
#  if you change the constants here, you'll possibly also have
#  to change the JavaScript code.

# "subdirectory" for the project
#  this is hard-coded in `browser.Websourcebrowser`!
PROJECT_DIR = u"project"
# "subdirectory" for static files
STATIC_DIR = u"static"

#
# defaults, can be changed via command line
#

# project root directory
root = os.getcwd()
if not isinstance(root, unicode):
    #XXX default and fallback encoding in `coding` module _may_
    #  _both_ be wrong, that is, the file actually may have
    #  another encoding
    root = coding.decode(root)

# project title, included in HTML `title` and `h1` tags; if `None`,
#  use the basename of the root directory (see above), i. e. if the
#  root directory is "/some/project/path", the title becomes "Path"
project_title = None

# list of glob patterns for files/directories to ignore; for each
#  pattern "x", the pattern "x/*" is added implicitly, so you don't
#  need to do it
ignore_patterns = []

# if true, include line numbers in listings; works only if Pygments
#  is installed and used
line_numbers = False

# the local HTTP interface
http_host = 'localhost'

# the HTTP port to listen on
http_port = 8000

# clients which are allowed to access this server
allowed_clients = ['localhost']

# if true, log each GET request on stdout
logging = False


def ignore_path(path):
    """Return True if the path should be ignored according to formerly
    set ignore patterns.

    In addition to the values given on the command line and in the
    `WSB_IGNORE` environment variable, the test uses a pattern "x/*"
    for each pattern "x".
    """
    additional_ignore_patterns = [p + "/*" for p in ignore_patterns]
    for pattern in ignore_patterns + additional_ignore_patterns:
        if fnmatch.fnmatch(path, pattern):
            return True
    return False

def set_from_args(args=None):
    """(Re)set the configuration values in the module from the
    provided list of arguments `args`, similar to what
    `sys.argv[1:]` usually contains. If `args` is not set or None,
    use the defaults as set in this file.

    >>> import config
    >>> config.set_from_args(["-t", u"Cool project", '--ignore-pattern=*/.svn',
    ...                       '--ignore-pattern=*/.svn/*', '--http-port=8080',
    ...                       '--line-numbers'])
    >>> config.project_title
    u'Cool project'
    >>> config.ignore_patterns
    ['*/.svn', '*/.svn/*']
    >>> config.http_port   # the port value is an integer
    8080
    >>> config.line_numbers, config.logging
    (True, False)
    """
    if args is None:
        args = sys.argv[1:]
    # set up command line parser
    parser = optparse.OptionParser(add_help_option=False)
    parser.add_option("-h", "--help", action='store_true')
    parser.add_option("-r", "--root", help="document root [current directory]")
    parser.add_option("-t", "--project-title",
                      help="project title to use in HTML title "
                           "[last part of root dir]")
    parser.add_option("-i", "--ignore-pattern", metavar="PATTERN",
                      dest='ignore_patterns', action='append',
                      help='ignore dirs/files matching this pattern '
                           '(e. g. "*/.svn/*") [nothing ignored]')
    parser.add_option("-l", "--line-numbers", action='store_true',
                      help="prepend text lines with line numbers [no]")
    parser.add_option("--http-host", help="local HTTP interface [localhost]")
    parser.add_option("--http-port", type='int',
                      help="HTTP port to listen on [%default]")
    parser.add_option("-c", "--allowed-client", metavar="CLIENT",
                      dest='allowed_clients', action='append',
                      help="allow a remote client to connect [localhost]; "
                           "use ALL to run as a public server")
    parser.add_option("--logging", action='store_true',
                      help="log HTTP accesses to stdout [no]")
    parser.set_defaults(**globals())
    (options, args) = parser.parse_args(args)
    if options.help:
        print MAN_PAGE
        sys.exit()
    # from here on, `args` is the list of only the positional arguments!
    if args:
        parser.error("program doesn't take arguments")
    if not isinstance(options.root, unicode):
        #XXX default and fallback encoding in `coding` module _may_
        #  _both_ be wrong, in other words, the file may have yet
        #  another encoding
        options.root = coding.decode(options.root)
    # interpret tilde markup for a user's home directory, then normalize
    #  path by collapsing ".." sequences etc.
    options.root = tools.normalize_path(os.path.expanduser(options.root))
    if options.project_title is None:
        options.project_title = os.path.basename(options.root).capitalize()
    try:
        options.project_title = coding.decode(options.project_title)
    except coding.Error:
        pass
    # normalize allowed client addresses to IPs
    allowed_clients = set()
    dummy_port = 80
    global invalid_clients
    invalid_clients = []
    for client in options.allowed_clients:
        if client == "ALL":
            allowed_clients = ALL_CLIENTS
            break
        try:
            for addr_info in socket.getaddrinfo(client, dummy_port):
                # `addr_info[4]` is a host/port tuple
                allowed_clients.add(addr_info[4][0])
        except socket.gaierror:
            invalid_clients.append(client)
    options.allowed_clients = allowed_clients
    # copy changed configuration back to module namespace; do not use
    #  `globals().update()` because that may copy too much
    option_names = ['root', 'project_title', 'ignore_patterns',
                    'line_numbers', 'http_host', 'http_port',
                    'allowed_clients', 'logging']
    for name in option_names:
        globals()[name] = getattr(options, name)

def set_from_environment():
    """Inspect the environment to set some configuration parameters.

    Currently, only the ignore patterns are considered, via the
    environment variable `WSB_IGNORE`. Its value is a whitespace-
    separated string of patterns, for example "*.pyc  *.pyo  */.svn
    *.svn/*  */.hg  */.hg/*  *.swp".
    """
    global ignore_patterns
    environ = os.environ
    patterns = environ.get('WSB_IGNORE', "")
    for pattern in patterns.split():
        ignore_patterns.append(pattern)


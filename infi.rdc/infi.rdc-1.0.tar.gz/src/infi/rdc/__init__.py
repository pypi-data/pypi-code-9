"""rdc

Usage:
    rdc [options] <address> [<program> [<cmdline>]]

Options:
    --allow-desktop-composition         allow desktop composition
    --allow-font-smoothing              allow font smoothing
    --audio-mode=<audio-mode>           either local or remote [default: none]
    --authentication-level=<level>      either warn or fail or none [default: none]
    --bitdepth=<bitdepth>               either 8, 15, 16, 24 or 32 [default: 32]
    --console                           login to console
    --fullscreen                        full-screen display, not availalble for apps
    --disable-cursor-settings           disable cursor
    --disable-full-window-drag          disable full window drag
    --disable-menu-animations           disable menu animation
    --disable-themes                    disable theme
    --disable-wallpaper                 disable wallpaper
    --desktop-height=<height>           custom height
    --desktop-width=<width>             custom width
    --redirect-printers                 redirect printers
    --username=<username>
    --domain=<domain>

"""

__import__("pkg_resources").declare_namespace(__name__)

import sys


def _boolify(i):
    return 1 if i else 0


def _audiomode(i):
    return 0 if i == "local" else 1 if i == "remote" else 2


def _warninglevel(i):
    return 1 if i == "fail" else 2 if i == "warn" else 0


def _screenmode(i):
    return 2 if i else 1


def main(argv=sys.argv[1:]):
    # https://technet.microsoft.com/en-us/library/dn690096.aspx
    import docopt
    import os

    arguments = docopt.docopt(__doc__, argv=argv)
    url_parameters = []
    url_parameters.append("full address=s:{}".format(arguments['<address>']))
    url_parameters.append("allow desktop composition=i:{}".format(_boolify(arguments['--allow-desktop-composition'])))
    url_parameters.append("allow font smoothing=i:{}".format(_boolify(arguments['--allow-font-smoothing'])))
    url_parameters.append("audiomode=i{}".format(_audiomode(arguments['--audio-mode'])))
    url_parameters.append("authentication level=:{}".format(_warninglevel(arguments['--authentication-level'])))
    url_parameters.append("bpp=i:{}".format(arguments['--bitdepth']))
    url_parameters.append("connect to console=i:{}".format(_boolify(arguments['--console'])))
    url_parameters.append("disable cursor settings=i:{}".format(_boolify(not arguments['--disable-cursor-settings'])))
    url_parameters.append("disable menu anims=i:{}".format(_boolify(not arguments['--disable-menu-animations'])))
    url_parameters.append("disable themes=i:{}".format(_boolify(not arguments['--disable-themes'])))
    url_parameters.append("disable wallpaper=i:{}".format(_boolify(not arguments['--disable-wallpaper'])))

    if arguments['--desktop-height']:
        url_parameters.append("desktopheight=i:{}".format(arguments['--desktop-height']))
    if arguments['--desktop-width']:
        url_parameters.append("desktopwidth=i:{}".format(arguments['--desktop-width']))
    if arguments['<program>']:
        url_parameters.append("remoteapplicationmode=i:1")
        url_parameters.append("remoteapplicationprogram=s:{}".format(arguments['<program>']))
        if arguments['<cmdline>']:
            url_parameters.append("remoteapplicationcmdline=s:{}".format(arguments['<cmdline>']))

    if arguments['--username']:
        url_parameters.append("username=s:{}".format(arguments['--username']))
    if arguments['--domain']:
        url_parameters.append("domain=s:{}".format(arguments['--domain']))
    url_parameters.append("prompt for credentials on client=i:1")

    url_parameters.append("screen mode id=i:{}".format(_screenmode(arguments['--fullscreen'])))
    url = "rdp://{}".format("&".join(url_parameters)).replace(" ", "%20")
    os.execv("/usr/bin/open", ["open", url])

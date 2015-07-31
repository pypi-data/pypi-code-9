"""
"critbot" lib.
Sending critical errors to syslog, slack, email, {your_plugin}.

Docs:
https://github.com/denis-ryzhkov/critbot
https://pypi.python.org/pypi/critbot

critbot version 0.1.2
Copyright (C) 2015 by Denis Ryzhkov <denisr@denisr.com>
MIT License, see http://opensource.org/licenses/MIT
"""

### import

from adict import adict
import time
from traceback import format_exc
import sys

### crit_defaults

crit_defaults = adict(
    subject='CRIT', # '{service_name} {host}:{port} CRIT'
    plugins=[], # [critbot.plugins.syslog.plugin(), ...]
    crit_in_crit=sys.stderr.write, # your_logger.critical
)

### utf8

def utf8(value):
    return (
        value.encode('utf8') if isinstance(value, unicode) else
        value if isinstance(value, str) else
        str(value)
    )

### crit

def crit(only='', also='', subject='', plugins=None):
    """
    Sends critical error.

    @param str only - The only details of crit, don't include traceback.
    @param str also - Additional details of crit to add to traceback.
    @param str subject - Subject of this crit instead of "crit_defaults.subject".
    @param list plugins - Plugins to send this crit to instead of "crit_defaults.plugins".
    @return NoneType
    """

    try:

        ### text

        text = utf8(only) or '{} {}'.format(utf8(also), format_exc())

        ### plugins, seconds_per_notification

        now = time.time()
        for plugin in plugins or crit_defaults.plugins:
            if now - plugin.last_notification_timestamp < plugin.seconds_per_notification:
                continue
            plugin.last_notification_timestamp = now

            ### send

            try:
                plugin.send(subject or crit_defaults.subject, text)

            ### crit_in_crit

            except Exception:
                crit_defaults.crit_in_crit(format_exc())

    except Exception:
        crit_defaults.crit_in_crit(format_exc())

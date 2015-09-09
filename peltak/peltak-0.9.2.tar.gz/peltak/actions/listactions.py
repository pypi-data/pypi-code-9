# -*- coding: utf-8 -*-
import re
import textwrap
from peltak.actions import actions
from peltak.core import cstr


@actions.register(
    'list-actions',
    desc="Prints all available actions.",
    cmdline=[{
        'args':     ('--porcelain',),
        'action':   'store_true',
        'dest':     'porcelain',
        'help': ("Show output in a format friendly for scripts "
                 "instead of humans")
    }]
)
def list_actions(app):
    if app.cl.porcelain:
        print(' '.join(p.name for p in actions.iter()))
    else:
        maxlen  = max(len(p.name) for p in actions.iter())
        fmt     = "  ^32{{name:{}}}^0 -- {{desc}}".format(maxlen)
        indent  = '{}'.format(' ' * (maxlen + 6))
        plugins = sorted(actions.iter(), key=lambda x: x.name)
        print("\033[1mAvailable actions:\033[0m")
        for plugin in plugins:
            text = plugin.meta.get('desc', 'NO DESCRIPTION').strip()
            desc = cstr(fmt).format(
                name=plugin.name,
                desc=re.sub(r'\s+', ' ', text)
            )
            lines = textwrap.wrap(desc, 80, subsequent_indent=indent)
            print('\n'.join(lines))
            print('')


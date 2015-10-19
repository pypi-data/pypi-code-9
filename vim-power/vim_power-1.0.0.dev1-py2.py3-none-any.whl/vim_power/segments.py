# vim:fileencoding=utf-8:noet
from __future__ import (unicode_literals, division, absolute_import, print_function)

import os

from powerline.theme import requires_segment_info

@requires_segment_info
def in_vim_shell(pl, segment_info, text="vim"):
    vim_runtime = segment_info['environ'].get('VIMRUNTIME', '')
    return str(text) if vim_runtime else None

def prompt_text(pl, text=''):
    return str(text.encode('utf-8'))

# -*- coding: utf-8 -*-
from __future__ import absolute_import
import sys
import getpass
import os.path
from ..config import MR_TEMPLATE_PATH
from ..core import ensure_dirs
from ..common import prompt
from ..core.template import Template


def user_details():
    defuser = getpass.getuser()
    sys.stdout.write("User (default: {}): ".format(defuser))
    user = sys.stdin.readline().strip() or defuser
    password = getpass.getpass()
    return user, password


def login():
    user, pw = user_details()
    return user, pw, prompt.yesno("Keep logged in?", default=True)


def mr_description(mr, skip_context=False, force_update=[]):
    if not os.path.exists(MR_TEMPLATE_PATH):
        if 'description' in mr:
            return mr.description
        else:
            return prompt.ask("Description")

    ensure_dirs(MR_TEMPLATE_PATH)
    template = Template.load_from_file(MR_TEMPLATE_PATH)
    template.fill(mr)

    if not skip_context:
        skip = lambda k, v: v and k.lower() not in force_update
        filled = ((k, v) for k, v in template.context.items() if skip(k, v))
        missing = (k for k, v in template.context.items() if not skip(k, v))

        for key, value in filled:
            prompt.form_print(key, value)

        for key in missing:
            ans = prompt.ask(key, multiline=True)
            template.context[key] = ans
            if ans:
                mr[key] = ans

    missing = (k for k, v in template.checklist.items() if not v)
    for key in missing:
        ans = prompt.yesno(key, default=False)
        template.checklist[key] = ans
        if ans:
            mr[key] = ans

    return template.render()


# -*- coding: utf-8 -*-
from __future__ import absolute_import
import readline
import os.path
from six import PY2, PY3
from ..config import MR_TEMPLATE_PATH
from ..core import git, cstr
from ..core.template import Template
if PY2:
    from urlparse import urljoin
elif PY3:
    from urllib.parse import urljoin


class UserCompleter(object):
    def __init__(self, users):
        self.users = users

    def complete(self, text, state):
        response = None
        if state == 0:
            # This is the first time for this text, so build a match list.
            if text:
                self.matches = [u.username for u in self.users if all((
                    u.username.startswith(text),
                    u.state == 'active'
                ))]
            else:
                self.matches = self.options[:]

        # Return the state'th item from the match list,
        # if we have that many.
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response


def yesno(question, default=None):
    prompt = cstr('^1{question} {options} ^0 '.format(
        question = question,
        options = {
            True:   '[Y/n]',
            False:  '[y/N]'
        }.get(default, '[y/n]')
    ))
    while True:
        choice = raw_input(prompt).lower()
        if choice in set(('yes', 'y')):
            return True
        elif choice in set(('no', 'n')):
            return False
        elif default is not None and not choice.strip():
            return default
        else:
            print("Invalid response")


def ask(prompt, multiline=False):
    if not multiline:
        return raw_input(cstr('^1{}:^0 ').format(prompt))

    ret = []
    try:
        ret.append(raw_input(cstr('^1{} (^^D to finish):^0 ').format(prompt)))
        while True:
            ret.append(raw_input())
    except EOFError:
        print("")

    return '\n'.join(ret)


def autouser(gitlab, prompt):
    user = None
    users = gitlab.list_users()

    readline.set_completer(UserCompleter(users).complete)
    while user is None:
        username = ask(prompt)
        user = gitlab.find_user(username)
        if username == '':
            break
        elif username == 'list':
            for u in users:
                print(cstr('^33@{}^0 ({})'.format(
                    u.username, u.name.encode('utf-8')
                )))
        elif user is None:
            print(cstr("^31User not found:^0 {}".format(username)))

    readline.set_completer(None)
    return user


def print_mr(app, mr):
    author = '<current-user>'
    title = ''
    assignee = "<no-one>"
    description = ''
    url = ''

    if 'title' in mr:
        title = mr['title']
    if 'assignee' in mr:
        assignee = "\033[33m@{}\033[0m ({})".format(
            mr['assignee'].username, mr['assignee'].name
        )
    if 'author' in mr:
        author = "\033[33m@{}\033[0m ({})".format(
            mr['author'].username, mr['author'].name
        )
    if 'description' in mr:
        description = mr['description']
    elif os.path.exists(MR_TEMPLATE_PATH):
        description = Template.load_from_file(MR_TEMPLATE_PATH).render()

    if 'remote_cache' in mr:
        url = urljoin(app.conf.gitlab_url, '/{}/merge_requests/{}'.format(
            app.conf.project,
            mr.remote_cache.iid
        ))

    print('')
    print(cstr("^1{}^0").format('-' * 80))
    print(cstr("^1{0:-^80}^0").format('{ Merge request preview }'))
    print(cstr("^1{}^0").format('-' * 80))
    print(cstr("^1URL:^0         ^34{}^0").format(url))
    print(cstr("^1Title:^0       ^32{}^0").format(title))
    print(cstr("^1Branch:^0      {}^0").format(git.current_branch()))
    print(cstr("^1Author:^0      {}").format(author))
    print(cstr("^1Assigned To:^0 {}").format(assignee))
    print(cstr("^1{0:-^80}^0").format('{ Description }'))
    print(description)
    print(cstr("\033[1m{}^0").format('-' * 80))
    print('')


def form_print(name, value):
    print(cstr('^1{}:^0 {}').format(name, value))


# -*- coding: utf-8 -*-
"""
This is a super secure to-do list app

Definitely no security holes here
"""


from flask import Blueprint, abort, current_app, g, request, redirect, \
                  render_template, url_for
from werkzeug.security import safe_str_cmp
from .session import create_session, require_auth
import hashlib
import os


url_prefix = '/phase2-%s/' % os.environ.get('PHASE2_TOKEN')
phase2 = Blueprint('phase2', __name__, url_prefix=url_prefix)


def test_login(username, password):
    password = password.encode('utf-8')
    pw_hash = current_app.redis.get('user:%s:password' % username)
    if not pw_hash:
        return False
    if not safe_str_cmp(hashlib.sha1(password).hexdigest(), pw_hash):
        return False
    return True


@phase2.route('')
def home():
    """The login form"""
    return render_template('phase2/home.html')


@phase2.route('login/', methods=['POST'])
def login():
    """Submit a login attempt"""
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    if test_login(username, password):
        # Successful login
        resp = redirect(url_for('phase2.dashboard'), code=303)
        create_session(resp, username)
        return resp
    else:
        # Invalid login
        return redirect(url_for('phase2.home'), code=303)


@phase2.route('dashboard/')
@require_auth  # This sets global "g.username" to the session username
def dashboard():
    """Either display the to-do list, or the admin panel"""
    if g.username != 'admin':
        # Load the list of ids ids of to-do items for the curent user
        ids = current_app.redis.lrange('items:%s' % g.username, 0, -1)
        # For each item, load its message from the database
        items = {}
        for i in ids:
            i = i.decode('utf-8')
            message = current_app.redis.get('user:%s:%s' % (g.username, i))
            items[i] = message.decode('utf-8')
        return render_template('phase2/dashboard.html', items=items)
    else:
        return render_template('phase2/success.html')


@phase2.route('dashboard/<username>/<item_id>/')
@require_auth  # This sets global "g.username" to the session username
def todo_item(username, item_id):
    """View a the message of a single to-do item"""
    message = current_app.redis.get('user:%s:%s' % (username, item_id))
    if not message:
        abort(404)
    message = message.decode('utf-8')
    return render_template('phase2/item.html', item=item_id, message=message)

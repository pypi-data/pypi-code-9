# -*- coding: utf-8 -*-
"""
Rhizom - Relationship grapher

Copyright (C) 2015  Aurelien Bompard <aurelien@bompard.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import unicode_literals, print_function

import browserid
from flask import request, g, abort, redirect, url_for, flash
from flask.ext.login import login_user, logout_user, current_user
from flask.ext.babel import gettext

from .. import app
from ..models import User


__all__ = (
    "login",
    "logout",
    )


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if app.config['TESTING']:
            data = request.form # bypass browserid check
        else:
            # La requête doit avoir une assertion à vérifier
            if 'assertion' not in request.form:
                abort(400)
            data = browserid.verify(request.form['assertion'],
                                    app.config["BROWSERID_AUDIENCE"])
        user = g.db.query(User).get(data['email'])
        if user is None:
            user = User(email=data["email"],
                        name=data["email"].partition("@")[0])
            g.db.add(user)
            g.db.commit()
        login_user(user)
        flash(gettext("Hello %(name)s! :-)", name=user.name), "success")
        # no redirect here, the JS will follow it in the AJAX request and load
        # the page twice.
        return request.args.get("next") or url_for("index")
    if current_user.is_authenticated:
        print("Already authenticated as %s" % current_user.name)
    return redirect(request.args.get("next") or url_for("index"))


@app.route('/logout', methods=["GET", "POST"])
def logout():
    if current_user.is_authenticated:
        name = current_user.name
        logout_user()
        flash(gettext("Disconnect successful, see you soon %(name)s!", name=name), "success")
    # no redirect here, the JS will follow it in the AJAX request and load the
    # page twice.
    return url_for('index')

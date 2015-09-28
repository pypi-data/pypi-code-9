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

from flask import request, g, render_template, redirect, url_for, flash, jsonify
from flask.ext.login import current_user
from flask.ext.babel import gettext, get_locale, refresh as locale_refresh

from .. import app
from ..models import User
from ..forms import UserForm, UserProfileForm


__all__ = (
    "users",
    "profile",
    )


@app.route('/users', methods=["GET", "POST"])
def users():
    if not current_user.is_master:
        return render_template("error.html",
            code=403, message=gettext("Access unauthorized")), 403
    user_form = UserForm()
    context = dict(
        user_form = user_form,
        users = g.db.query(User).order_by(User.name).all(),
    )
    if request.method == "POST" and request.form.get("action") == "delete":
        user = g.db.query(User).get(request.form["email"])
        g.db.delete(user)
        g.db.commit()
        #flash("Utilisateur supprimé", "success")
        return jsonify({"status": "OK"})
        #return redirect(url_for("users"))
    return render_template("users.html", **context)


@app.route('/profile', methods=["GET", "POST"])
def profile():
    if not current_user.is_authenticated:
        return render_template("error.html",
            code=403, message=gettext("Access unauthorized")), 403
    form = UserProfileForm(obj=current_user)
    if current_user.locale is None:
        form.locale.data = get_locale().language
    if form.validate_on_submit():
        form.populate_obj(current_user)
        g.db.commit()
        locale_refresh()
        flash(gettext("Profile modified."), "success")
        return redirect(url_for("profile"))
    return render_template("profile.html", user_profile_form=form)

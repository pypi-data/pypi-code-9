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

from flask import request, g, render_template, redirect, url_for, flash
from flask.ext.login import current_user
from flask.ext.babel import gettext

from .. import app
from ..models import Graph, Permission, PermissionLevel
from ..forms import NewGraph, CopyGraph


__all__ = (
    "index",
    )


@app.route('/', methods=["GET", "POST"])
def index():
    if not current_user.is_authenticated:
        graphs = []
    else:
        if current_user.is_master:
            graphs = g.db.query(Graph).order_by(Graph.id).all()
        else:
            graphs = g.db.query(Graph).join(Permission).filter(
                Permission.user_email == current_user.email,
                Permission.level >= PermissionLevel.view.value
                ).order_by(Graph.id).all()
    new_form = NewGraph(prefix="newgraph")
    copy_form = CopyGraph(prefix="copygraph")
    copy_form.existing.choices = [ (str(graph.id), graph.name) for graph in graphs ]
    if request.method == "POST":
        if request.form.get("formname") == "new" and new_form.validate():
            graph = Graph(name=new_form.name.data)
            g.db.add(graph)
            g.db.flush() # otherwise graph.id is None
            g.db.add(Permission(graph_id=graph.id,
                                user_email=current_user.email,
                                level=PermissionLevel.admin.value))
            g.db.commit()
            flash(gettext("Graph created"), "success")
            return redirect(url_for("admin", graph_id=graph.id))
        if request.form.get("formname") == "copy" and copy_form.validate():
            existing = g.db.query(Graph).get(copy_form.existing.data)
            graph = Graph(name=gettext("Copy of %(name)s", name=existing.name))
            g.db.add(graph)
            g.db.flush() # otherwise graph.id is None
            graph.copy_from(existing)
            # The copying user is the admin of the new graph
            myperm = g.db.query(Permission).get((graph.id, current_user.email))
            myperm.level = PermissionLevel.admin.value
            g.db.commit()
            flash(gettext("Graph copied"), "success")
            return redirect(url_for("admin", graph_id=graph.id))
    return render_template("index.html",
        graphs=graphs, new_form=new_form, copy_form=copy_form)

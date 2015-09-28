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

import json

from flask import request, g, render_template, abort, redirect, url_for, flash, jsonify
from flask.ext.babel import gettext

from .. import app
from ..models import Graph, Person, User, Permission, PermissionLevel, RelationshipType
from ..lib import has_permission_level
from ..forms import NewAccess, RelationshipTypes, GraphProperties

__all__ = (
    "admin",
    )


@app.route('/graph/<int:graph_id>/admin', methods=["GET", "POST"])
def admin(graph_id):
    graph = g.db.query(Graph).get(graph_id)
    if not graph:
        abort(404)
    if not has_permission_level(graph_id, PermissionLevel.admin):
        return render_template("error.html", code=403, graph=graph,
                               message=gettext("Access unauthorized")), 403
    newaccess_form = NewAccess(prefix="newaccess")
    graphprops_form = GraphProperties(obj=graph, prefix="graphprops")
    graphprops_form.center_id.choices = [("0", gettext("(no one)"))] + [
        (str(p.id), p.name) for p in g.db.query(Person).filter_by(graph_id=graph_id
        ).order_by(Person.name) ]
    reltypes_form = RelationshipTypes(prefix="reltypes")
    perm_choices = [ (int(getattr(PermissionLevel, l)), n) for l, n in
                  ( ("view", gettext("View")), ("edit", gettext("Edit")),
                    ("admin", gettext("Admin")) ) ]
    newaccess_form.level.choices = perm_choices
    context = dict(
        graph = graph,
        graphprops_form = graphprops_form,
        reltypes_form = reltypes_form,
        newaccess_form = newaccess_form,
        permissions = g.db.query(Permission).join(User).filter(
            Permission.graph_id == graph_id).order_by(User.name).all(),
        rel_types = g.db.query(RelationshipType).filter_by(
            graph_id=graph_id).order_by(RelationshipType.name).all(),
        perm_choices = perm_choices,
    )
    if request.method == "POST":
        # Graph: properties edition
        if request.form.get("formname") == "graphprops":
            if not graphprops_form.validate():
                return render_template("admin.html", **context)
            graph.name = graphprops_form.name.data
            graph.center_id = int(graphprops_form.center_id.data)
            graph.anonymous = graphprops_form.anonymous.data
            g.db.commit()
            flash(gettext("Graph updated."), "success")
            return redirect(url_for("admin", graph_id=graph_id))
        # Graph: permissions
        elif request.form.get("formname") == "permissions":
            if request.form.get("action") == "add":
                if not newaccess_form.validate():
                    return render_template("admin.html", **context)
                user = g.db.query(User).get(newaccess_form.email.data)
                if user is None:
                    user = User(email=newaccess_form.email.data)
                    g.db.add(user)
                perm = Permission(graph_id=graph_id,
                                  user_email=newaccess_form.email.data,
                                  level=newaccess_form.level.data)
                g.db.add(perm)
                g.db.commit()
                flash(gettext("Access added."), "success")
                return redirect(url_for("admin", graph_id=graph_id))
            elif request.form.get("action") == "delete":
                perm = g.db.query(Permission).get((graph_id, request.form["email"]))
                if perm is None:
                    return jsonify({"status": "error",
                                    "message": gettext("Invalid permission")})
                user = perm.user
                g.db.delete(perm)
                g.db.flush() # flushing is required for the next step
                if len(user.permissions) == 0:
                    g.db.delete(user) # no permissions left
                g.db.commit()
                #flash("Accès supprimé", "success")
                return jsonify({"status": "OK"})
            elif request.form.get("action") == "edit":
                perm = g.db.query(Permission).get((graph_id, request.form["email"]))
                if perm is None:
                    return jsonify({"status": "error",
                                    "message": gettext("Invalid permission")})
                perm.level = request.form["level"]
                g.db.commit()
                flash(gettext("User modified."), "success")
                return jsonify({"status": "OK"})
        ## Graph: relationship types
        elif request.form.get("formname") == "reltypes":
            if request.form.get("action") == "add":
                if not reltypes_form.validate():
                    return render_template("admin.html", **context)
                reltype = RelationshipType(graph_id=graph_id,
                                           name=reltypes_form.name.data,
                                           color=reltypes_form.color.data)
                for existing_types in g.db.query(RelationshipType
                    ).filter_by(graph_id=graph_id):
                    if reltype.cssname == existing_types.cssname:
                        reltypes_form.name.errors.append(gettext("This name is already used."))
                        return render_template("admin.html", **context)
                g.db.add(reltype)
                g.db.commit()
                flash(gettext("Relationship type added."), "success")
                return redirect(url_for("admin", graph_id=graph_id))
            elif request.form.get("action") == "delete":
                reltype = g.db.query(RelationshipType).get(
                    (graph_id, request.form["origname"]))
                if reltype is None:
                    return jsonify({"status": "error",
                                    "message": gettext("Invalid relationship type")})
                g.db.delete(reltype)
                g.db.commit()
                #flash("Type de relation supprimé", "success")
                return jsonify({"status": "OK"})
            elif request.form.get("action") == "edit":
                reltype = g.db.query(RelationshipType).get(
                    (graph_id, request.form["origname"]))
                if reltype is None:
                    return jsonify({"status": "error",
                                    "message": gettext("Invalid relationship type")})
                reltype.name = request.form["name"]
                reltype.color = request.form["color"]
                g.db.commit()
                flash(gettext("Relationship type modified."), "success")
                return jsonify({"status": "OK"})
            else:
                flash(gettext("Invalid request"), "danger")
        # Graph: import
        elif request.form.get("formname") == "graphimport":
            if not request.files['import']:
                flash(gettext("No graph data."), "danger")
                return redirect(url_for("admin", graph_id=graph_id))
            try:
                data = json.load(request.files['import'])
            except ValueError as e:
                #log.warning("Failed to load the graph data for graph %s: %s", graph.id, e)
                flash(gettext("Invalid graph data."), "danger")
                return redirect(url_for("admin", graph_id=graph_id))
            graph.import_dict(data)
            g.db.commit()
            flash(gettext("Graph imported."), "success")
            return redirect(url_for("admin", graph_id=graph_id))
        # Graph: deletion
        elif request.form.get("formname") == "graphdel":
            g.db.delete(graph)
            g.db.commit()
            flash(gettext("Graph deleted."), "success")
            return redirect(url_for("index"))
    return render_template("admin.html", **context)

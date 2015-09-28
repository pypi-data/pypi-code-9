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

from flask import request, g, render_template, abort, redirect, url_for, flash, jsonify
from flask.ext.login import current_user
from flask.ext.babel import gettext
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound

from .. import app
from ..models import Graph, Person, Relationship, PermissionLevel, RelationshipType
from ..lib import has_permission_level
from ..forms import NewRelationship


__all__ = (
    "edit",
    )


@app.route('/graph/<int:graph_id>/edit', methods=["GET", "POST"])
def edit(graph_id):
    graph = g.db.query(Graph).get(graph_id)
    if not graph:
        abort(404)
    if not has_permission_level(graph_id, PermissionLevel.edit):
        return render_template("error.html", code=403, graph=graph,
                               message=gettext("Access unauthorized")), 403
    newrel_form = NewRelationship()
    rel_types = [ rt.name for rt in g.db.query(RelationshipType.name).filter_by(
        graph_id=graph_id).order_by(RelationshipType.name) ]
    newrel_form.rtype.choices = [ (rt, rt) for rt in rel_types ]
    context = dict(
        graph = graph,
        newrel_form = newrel_form,
        relationships = g.db.query(Relationship).filter_by(
                graph_id=graph_id
            ).order_by(
                Relationship.source_id, Relationship.target_id
            ).all(),
        rel_types = rel_types,
    )
    if request.method == "POST":
        if request.form.get("action") == "delete":
            sid = int(request.form["source-edit"])
            tid = int(request.form["target-edit"])
            ltype = request.form["origltype-edit"]
            link = g.db.query(Relationship).filter_by(
                source_id=sid, target_id=tid, type_name=ltype).one()
            g.db.delete(link)
            g.db.flush() # flushing is required for the next step
            # Cleanup orphans
            for pid in (sid, tid):
                if g.db.query(Relationship).filter(or_(
                    Relationship.source_id == pid,
                    Relationship.target_id == pid)).count() == 0:
                    g.db.delete(g.db.query(Person).get(pid))
            g.db.commit()
            #flash("Relation supprimée", "success")
            return jsonify({"status": "OK"})
            #return redirect(url_for("edit", graph_id=graph_id))
        elif request.form.get("action") == "edit":
            sid = int(request.form["source-edit"])
            tid = int(request.form["target-edit"])
            ltype = request.form["origltype-edit"]
            newltype = request.form["ltype-edit"]
            dotted = request.form["dotted-edit"] not in ("", "false")
            if ltype != newltype and g.db.query(Relationship).filter_by(
                source_id=sid, target_id=tid, type_name=newltype).count():
                return jsonify({
                        "status": "error",
                        "message": gettext("This relationship already exists.")})
            link = g.db.query(Relationship).filter_by(
                source_id=sid, target_id=tid, type_name=ltype).one()
            link.type_name = newltype
            link.dotted = dotted
            g.db.commit()
            flash(gettext("Relationship modified."), "success")
            return jsonify({"status": "OK"})
        elif request.form.get("action") == "add":
            if not newrel_form.validate():
                return render_template("edit.html", **context)
            try:
                source = g.db.query(Person).filter_by(
                    graph_id=graph_id, name=newrel_form.source.data).one()
            except NoResultFound:
                source = Person(graph_id=graph_id, name=newrel_form.source.data)
                g.db.add(source)
            try:
                target = g.db.query(Person).filter_by(
                    graph_id=graph_id, name=newrel_form.target.data).one()
            except NoResultFound:
                target = Person(graph_id=graph_id, name=newrel_form.target.data)
                g.db.add(target)
            g.db.flush() # flushing is required for the next step
            if source.id > target.id:
                source, target = target, source # the source is always the lowest id
            if g.db.query(Relationship).get(
                (source.id, target.id, newrel_form.rtype.data)) is not None:
                flash(gettext("This relationship already exists."), "warning")
                return render_template("edit.html", **context)
            newlink = Relationship(
                source_id=source.id, target_id=target.id,
                type_name=newrel_form.rtype.data, graph_id=graph.id,
                dotted=newrel_form.dotted.data)
            g.db.add(newlink)
            g.db.commit()
            flash(gettext("Relationship added."), "success")
            return redirect(url_for("edit", graph_id=graph_id))
    return render_template("edit.html", **context)

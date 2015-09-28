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

import os
import urllib
try:
    from lxml import etree as ET
except ImportError:
    from xml.etree import ElementTree as ET

from flask import request, g, abort, redirect, url_for, jsonify, Response

from .. import app
from ..models import Graph, PermissionLevel
from ..lib import has_permission_level


__all__ = (
    "export_graph",
    "import_graph",
    "to_svg",
    )


@app.route('/api/graph/<int:graph_id>/export/<name>.json')
def export_graph(graph_id, name):
    graph = g.db.query(Graph).get(graph_id)
    if not graph:
        abort(404)
    if not has_permission_level(graph_id, PermissionLevel.view):
        abort(403)
    with_perms = has_permission_level(graph_id, PermissionLevel.admin)
    data = graph.export_dict(with_perms=with_perms)
    data["version"] = 1
    response = jsonify(**data)
    user_agent = request.headers.get('USER_AGENT')
    if user_agent and 'WebKit' in user_agent:
        filename = "filename=%s.json" % graph.name.encode('utf-8')
    elif user_agent and 'MSIE' in user_agent:
        filename = '' # does not support internationalized filenames at all
    else:
        filename = "filename*=UTF-8''%s.json" % urllib.quote(
            graph.name.encode('utf-8'))
    response.headers["Content-Disposition"] = "attachment; %s" % filename
    return response


@app.route('/api/graph/<int:graph_id>/import', methods=["POST"])
def import_graph(graph_id):
    graph = g.db.query(Graph).get(graph_id)
    if not graph:
        abort(404)
    if not has_permission_level(graph_id, PermissionLevel.edit):
        abort(403)
    data = request.get_json()
    if "permissions" in data and not \
            has_permission_level(graph_id, PermissionLevel.admin):
        del data["permissions"]
    graph.import_dict(data)
    g.db.commit()
    return redirect(url_for('graph', graph_id=graph_id))


@app.route('/api/graph/<int:graph_id>/export/<name>.svg', methods=["POST"])
def to_svg(graph_id, name):
    graph = g.db.query(Graph).get(graph_id)
    if not graph:
        abort(404)
    if not has_permission_level(graph_id, PermissionLevel.view):
        abort(403)
    svg = ET.fromstring(request.form["svg"].strip().encode("utf-8"))
    # cleanups
    for attr in ("width", "height"):
        elems = svg.findall(".//*[@%s='100%%']" % attr) \
              + svg.findall(".[@%s='100%%']" % attr)
        for elem in elems:
            del elem.attrib[attr]
    for elem in svg.findall(".//*[@class='']"):
        del elem.attrib["class"]
    #ET.dump(svg)
    css = []
    with open(os.path.join(app.static_folder, "graph.css")) as fh:
        css.append(fh.read())
    for rtype in graph.relationship_types:
        css.append("path.link.%s { stroke: %s; }" % (
                   rtype.cssname, rtype.color))
    style = ET.Element("style")
    style.text = "\n".join(css)
    svg.insert(0, style)
    return Response(
        ET.tostring(svg, encoding="utf-8"),
        content_type="image/svg+xml; charset=utf-8")

# -*- coding: utf-8 -*-
# copyright 2013-2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.
"""cubicweb-relationwidget views/forms/actions/components for web ui"""

from cwtags.tag import div, p, a, span, h3, input, ul, li, label, button

from logilab.common.registry import Predicate
from logilab.mtconverter import xml_escape

from rql import nodes

from cubicweb.uilib import js
from cubicweb.predicates import empty_rset
from cubicweb.view import View, EntityStartupView
from cubicweb.web import formwidgets as fwdg
from cubicweb.web.views import tableview

_ = unicode

_('required_error')
_('no selected entities')

def _ensure_set(value):
    """Given None, a string or some kind of iterable of strings, ensure the value is a set
    of strings (empty in case of None).
    """
    if value is None:
        return frozenset()
    if isinstance(value, (set, frozenset)):
        return value
    if isinstance(value, basestring):
        return frozenset((value,))
    assert isinstance(value, (list, tuple)), 'unexpected type for %r' % value
    return frozenset(value)


class edited_relation(Predicate):
    """Predicate to be used to specialize 'search_related_entities' views
    (:cls:`SearchForRelatedEntitiesView` here) by specifying at least one of

    * `rtype`, the edited relation,
    * `tetype`, the target entity type,
    * `role`, the originating entity role in the relation.

    `rtype` or `tetype` may be given as a string value or as a (list/tuple/set) of string values.
    """
    def __init__(self, rtype=None, tetype=None, role=None):
        assert rtype or tetype or role
        self.rtypes = _ensure_set(rtype)
        self.tetypes = _ensure_set(tetype)
        assert role is None or role in ('subject', 'object'), role
        self.role = role

    def __call__(self, cls, _cw, **kwargs):
        if 'relation' not in _cw.form:
            return 0
        rtype, tetype, role = _cw.form['relation'].split(':')
        score = 0
        if rtype in self.rtypes:
            score += 1
        if tetype in self.tetypes:
            score += 1
        if role == self.role:
            score += 1
        return score


def _guess_multiple(form, field, targetetype):
    """guess cardinality of edited relation"""
    eschema = form._cw.vreg.schema[form.edited_entity.cw_etype]
    rschema = eschema.schema[field.name]
    rdef = eschema.rdef(rschema, role=field.role, targettype=targetetype)
    card = rdef.role_cardinality(field.role)
    return card in '*+'


def make_action(form, field, targetetype, widgetuid, dialog_options):
    multiple = _guess_multiple(form, field, targetetype)
    kwargs = {'vid': 'search_related_entities',
              '__modal': 1,
              'multiple': '1' if multiple else '',
              'relation': '%s:%s:%s' % (field.name, targetetype, field.role)}
    entity = form.edited_entity
    if not entity.has_eid():
        # entity is not created yet
        url = form._cw.build_url('ajax', fname='view', etype=entity.__regid__, **kwargs)
    else:
        # entity is edited, use its absolute url as base url
        url = form._cw.build_url('ajax', fname='view', eid=entity.eid, **kwargs)
    options = {
        'dialogOptions': dialog_options,
        'editOptions': {
            'required': int(field.required),
            'multiple': multiple,
            'searchurl': url,
        },
    }
    return str(js.jQuery('#' + widgetuid).relationwidget(options))


class RelationFacetWidget(fwdg.Select):
    """ Relation widget with facet selection, providing:

    * a list of checkbox-(de-)selectable related entities
    * a mecanism to trigger the display of a pop-up window for each possible
      target entity type of the relation
    * a pop-up window to search (using facets) entities to be linked to the
      edited entity, display (in a paginated table) and select them (using a
      checkbox on each line)

    Partitioning by target entity type provides:

    * potentially lighter result sets
    * pertinent facets (mixing everything would shut down all
      but the most generic ones)
    """
    needs_js = ('jquery.ui.js',
                'cubicweb.ajax.js',
                'cubicweb.widgets.js',
                'cubicweb.facets.js',
                'cubes.relationwidget.js')
    needs_css = ('jquery.ui.css',
                 'cubicweb.facets.css',
                 'cubes.relationwidget.css')

    def __init__(self, *args, **kwargs):
        """Overriden so that it is possible to configure window dialog options (height, width, etc.)
        """
        self._dialog_options = kwargs.pop('dialog_options', {})
        super(RelationFacetWidget, self).__init__(*args, **kwargs)

    def _render(self, form, field, renderer):
        _ = form._cw._
        form._cw.html_headers.define_var(
            'facetLoadingMsg', _('facet-loading-msg'))
        entity = form.edited_entity
        html = []
        w = html.append
        domid = ('widget-%s'
                 % field.input_name(form, self.suffix).replace(':', '-'))
        rtype = entity._cw.vreg.schema.rschema(field.name)
        # prepare to feed the edit controller
        related = self._compute_related(form, field)
        self._render_post(w, entity, rtype, field.role, related, domid)
        # compute the pop-up trigger action(s)
        self._render_triggers(w, domid, form, field, rtype)
        # this is an anchor for the modal dialog
        w(div(id=domid, style='display: none'))
        return u'\n'.join(unicode(node) for node in html)

    def _compute_related(self, form, field):
        """ For each already related entity, return a pair with its eid and its
        `incontext` html view """
        entity = form.edited_entity
        related = field.relvoc_linkedto(form)
        if entity.has_eid():
            rset = entity.related(field.name, field.role)
            related += [(e.view('incontext'), unicode(e.eid))
                        for e in rset.entities()]
        return related

    def _render_post(self, w, entity, rtype, role, related, domid):
        name = '%s-%s:%s' % (rtype, role, entity.eid)
        with div(w, id='inputs-for-' + domid,
                 Class='cw-relationwidget-list'):
            for html_label, eid in related:
                with div(w, Class='checkbox'):
                    with label(w, **{'for-name': name}):
                        w(input(name=name, type='checkbox',
                                checked='checked',
                                value=eid,
                                **{'data-html-label': xml_escape(html_label)}))
                        w(html_label)

    def _render_triggers(self, w, domid, form, field, rtype):
        """ According to the number of target entity types for the edited entity
        and considered relation, write the html for:

        * a user message indicating there is no entity that can be linked
        * a button-like link if there is a single possible target etype
        * a drop-down list of possible target etypes if there are more than 1

        In both later cases, actionning them will trigger the dedicated search
        and select pop-up window.
        """
        _ = form._cw._
        dialog_title = _('search entities to be linked to %(targetetype)s')
        actions = []
        target_etypes = rtype.targets(form.edited_entity.e_schema, field.role)
        for target_etype in target_etypes:
            if form.edited_entity.unrelated(
                    field.name, target_etype, field.role, limit=None,
                    lt_infos=form.linked_to):
                options = self._dialog_options.copy()
                if 'title' not in options:
                    options['title'] = dialog_title % {'targetetype': _(target_etype)}
                actions.append((target_etype, make_action(
                    form, field, target_etype, domid, options)))
        if not actions:
            w(div(xml_escape(_('no available "%s" to relate to')
                             % ', '.join("%s" % _(e) for e in target_etypes)),
                  **{'class': 'alert alert-warning'}))
        elif len(actions) == 1:
            # Just one: a direct link.
            target_etype, action = actions[0]
            link_title = xml_escape(_('link to %(targetetype)s')
                                    % {'targetetype': _(target_etype)})
            w(p(a(link_title, onclick=xml_escape(action),
                  href=xml_escape('javascript:$.noop()'),
                  Class='btn btn-default cw-relationwidget-single-link'),
                Class='form-control-static'))
        else:
            # Several possible target types, provide a combobox
            with div(w, Class='btn-group'):
                with button(w, type="button",
                            Class="btn btn-default dropdown-toggle",
                            **{'data-toggle': "dropdown"}):
                    w(_('link to ...') + ' ')
                    w(span(Class="caret"))
                with ul(w, Class='dropdown-menu'):
                    for target_etype, action in actions:
                        w(li(a(xml_escape(_(target_etype.type)),
                               Class="btn-link",
                               onclick=xml_escape(action))))


class SearchForRelatedEntitiesView(EntityStartupView):
    """view called by the edition view when the user asks to search
    for something to link to the edited eid
    """
    __regid__ = 'search_related_entities'
    title = _('Link/unlink entities')
    # do not add this modal view in the breadcrumbs history:
    add_to_breadcrumbs = False

    def call(self):
        _ = self._cw._
        w = self.w
        # refreshable part
        if self.title:
            w(h3(_(self.title)))
        with div(w, id='cw-relationwidget-table'):
            self.wview('select_related_entities_table', rset=self.linkable_rset())
        if self._cw.form.get('multiple'):
            w(h3(_('Selected items')))
        else:
            w(h3(_('Selected item')))
        # placeholder divs for deletions & additions
        w(div(**{'id': 'cw-relationwidget-alert',
                 'class': 'alert alert-danger hidden'}))
        # placeholder for linked entities summary
        w(ul(**{'id': 'cw-relationwidget-linked-summary',
                'class': 'cw-relationwidget-list'}))

    def linkable_rset(self):
        """Return rset of entities to be displayed as possible values for the edited relation. You may want
        to override this.
        """
        entity = self.compute_entity()
        rtype, tetype, role = self._cw.form['relation'].split(':')
        rql, args = entity.cw_linkable_rql(rtype, tetype, role,
                                           ordermethod='fetch_order',
                                           vocabconstraints=False)
        return self._cw.execute(rql, args)

    def compute_entity(self):
        if self.cw_rset:
            return self.cw_rset.get_entity(0, 0)
        else:
            etype = self._cw.form['etype']
            return self._cw.vreg['etypes'].etype_class(etype)(self._cw)


class SelectEntitiesTableLayout(tableview.TableLayout):
    __regid__ = 'select_related_entities_table_layout'
    display_filter = 'top'
    hide_filter = False


class SelectMainEntityColRenderer(tableview.MainEntityColRenderer):
    """Custom renderer of the main entity in the table of selectable entities
    that includes a DOM attribute to be used for selection on JS side.
    """
    attributes = {'data-label-cell': 'true'}


class SelectEntitiesColRenderer(tableview.RsetTableColRenderer):

    def render_header(self, w):
        # do not add headers
        w(u'')

    def render_cell(self, w, rownum):
        entity = self.cw_rset.get_entity(rownum, 0)
        w(input(type='checkbox', value=entity.eid))

    def sortvalue(self, rownum):
        return None


class SelectEntitiesTableView(tableview.EntityTableView):
    """Table view of the selectable entities in the relation widget

    Selection of columns (and respective renderer) can be overridden by
    updating `columns` and `column_renderers` class attributes.
    """
    __regid__ = 'select_related_entities_table'
    layout_id = 'select_related_entities_table_layout'
    columns = ['select', 'entity']
    column_renderers = {
        'select': SelectEntitiesColRenderer('one', sortable=False),
        'entity': SelectMainEntityColRenderer(),
    }

    def page_navigation_url(self, navcomp, _path, params):
        params['divid'] = self.domid
        params['vid'] = self.__regid__
        return navcomp.ajax_page_url(**params)


def rset_main_type(rset):
    """Try to get the type of the first variable of the result set. None if not found.
    """
    rqlst = rset.syntax_tree()
    if len(rqlst.children) > 1:
        return None
    select = rqlst.children[0]
    if not isinstance(select.selection[0], nodes.VariableRef):
        return None
    varname = select.selection[0].name
    etypes = set(sol[varname] for sol in select.solutions)
    if len(etypes) != 1:
        return None
    return etypes.pop()


class NoEntitiesToSelectView(View):
    """Fallback view to be used when there is no entity to relate
    """
    __regid__ = 'select_related_entities_table'
    __select__ = empty_rset()

    def call(self, **kwargs):
        self.w(u'<div class="searchMessage"><strong>%s</strong></div>\n'
               % self._cw._('No entity to put in relation'))
        etype = rset_main_type(self.cw_rset)
        if etype:
            eschema = self._cw.vreg.schema[etype]
            if not (eschema.final or eschema.is_subobject(strict=True)) \
               and eschema.has_perm(self._cw, 'add'):
                url = self._cw.vreg["etypes"].etype_class(etype).cw_create_url(self._cw)
                self.w(u'<div><a href="%s">%s</a></div>' % (
                    url, self._cw.__('New %s' % eschema).capitalize()))

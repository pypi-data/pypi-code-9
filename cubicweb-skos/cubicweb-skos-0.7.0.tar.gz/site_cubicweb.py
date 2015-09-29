# copyright 2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""cubicweb-skos site customizations"""

from copy import copy
from datetime import datetime
import inspect

from logilab.common.decorators import monkeypatch

from cubicweb.dataimport import MetaGenerator, NoHookRQLObjectStore


@monkeypatch(MetaGenerator)
def __init__(self, cnx, baseurl=None, source=None):
    self._cnx = cnx
    if baseurl is None:
        config = cnx.vreg.config
        baseurl = config['base-url'] or config.default_base_url()
    if not baseurl[-1] == '/':
        baseurl += '/'
    self.baseurl = baseurl
    if source is None:
        source = cnx.repo.system_source
    self.source = source
    self.create_eid = cnx.repo.system_source.create_eid
    self.time = datetime.now()
    # attributes/relations shared by all entities of the same type
    self.etype_attrs = []
    self.etype_rels = []
    # attributes/relations specific to each entity
    self.entity_attrs = ['cwuri']
    schema = cnx.vreg.schema
    rschema = schema.rschema
    for rtype in self.META_RELATIONS:
        # skip owned_by / created_by if user is the internal manager
        if cnx.user.eid == -1 and rtype in ('owned_by', 'created_by'):
            continue
        if rschema(rtype).final:
            self.etype_attrs.append(rtype)
        else:
            self.etype_rels.append(rtype)


@monkeypatch(MetaGenerator)
def init_entity(self, entity):
    entity.eid = self.create_eid(self._cnx)
    extid = entity.cw_edited.get('cwuri')
    for attr in self.entity_attrs:
        if attr in entity.cw_edited:
            # already set, skip this attribute
            continue
        genfunc = self.generate(attr)
        if genfunc:
            entity.cw_edited.edited_attribute(attr, genfunc(entity))
    if isinstance(extid, unicode):
        extid = extid.encode('utf-8')
    return self.source, extid


@monkeypatch(NoHookRQLObjectStore)
def create_entity(self, etype, **kwargs):
    for k, v in kwargs.iteritems():
        kwargs[k] = getattr(v, 'eid', v)
    entity, rels = self.metagen.base_etype_dicts(etype)
    # make a copy to keep cached entity pristine
    entity = copy(entity)
    entity.cw_edited = copy(entity.cw_edited)
    entity.cw_clear_relation_cache()
    entity.cw_edited.update(kwargs, skipsec=False)
    entity_source, extid = self.metagen.init_entity(entity)
    cnx = self._cnx
    self.source.add_info(cnx, entity, entity_source, extid)
    self.source.add_entity(cnx, entity)
    kwargs = dict()
    if inspect.getargspec(self.add_relation).keywords:
        kwargs['subjtype'] = entity.cw_etype
    for rtype, targeteids in rels.iteritems():
        # targeteids may be a single eid or a list of eids
        inlined = self.rschema(rtype).inlined
        try:
            for targeteid in targeteids:
                self.add_relation(cnx, entity.eid, rtype, targeteid,
                                  inlined, **kwargs)
        except TypeError:
            self.add_relation(cnx, entity.eid, rtype, targeteids,
                              inlined, **kwargs)
    self._nb_inserted_entities += 1
    return entity

try:
    from cubicweb.devtools.testlib import CubicWebTC
except ImportError:
    # devtools not available
    pass
else:
    # #4985805
    from cubicweb.web import eid_param

    @monkeypatch(CubicWebTC, methodname='fake_form')
    @staticmethod
    def fake_form(formid, field_dict=None, entity_field_dicts=()):
        """Build _cw.form dictionnary to fake posting of some standard cubicweb form

        * `formid`, the form id, usually form's __regid__

        * `field_dict`, dictionary of name:value for fields that are not tied to an entity

        * `entity_field_dicts`, list of (entity, dictionary) where dictionary contains name:value
          for fields that are not tied to the given entity
        """
        assert field_dict or entity_field_dicts, \
            'field_dict and entity_field_dicts arguments must not be both unspecified'
        if field_dict is None:
            field_dict = {}
        form = {'__form_id': formid}
        fields = []
        for field, value in field_dict.items():
            fields.append(field)
            form[field] = value

        def _add_entity_field(entity, field, value):
            entity_fields.append(field)
            form[eid_param(field, entity.eid)] = value

        for entity, field_dict in entity_field_dicts:
            if '__maineid' not in form:
                form['__maineid'] = entity.eid
            entity_fields = []
            form.setdefault('eid', []).append(entity.eid)
            _add_entity_field(entity, '__type', entity.cw_etype)
            for field, value in field_dict.items():
                _add_entity_field(entity, field, value)
            if entity_fields:
                form[eid_param('_cw_entity_fields', entity.eid)] = ','.join(entity_fields)
        if fields:
            form['_cw_fields'] = ','.join(fields)
        return form

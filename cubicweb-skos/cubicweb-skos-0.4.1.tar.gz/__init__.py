"""cubicweb-skos application package

"SKOS implementation for cubicweb"
"""

def to_unicode(obj):
    """Turn some object (usually an exception) to unicode"""
    try:
        # The exception message might already be a unicode string.
        return unicode(obj)
    except UnicodeDecodeError:
        return str(obj).decode(errors='ignore')

class ExtEntity(object):
    """Transitional representation of an entity for use in data importer"""

    def __init__(self, etype, extid, values=None):
        self.etype = etype
        self.extid = extid
        if values is None:
            values = {}
        self.values = values
        self._schema = None

    def __repr__(self):
        return '<%s %s %s>' % (self.etype, self.extid, self.values)

    def prepare(self, schema):
        """Prepare an external entity for later insertion:

        * ensure attributes and inlined relations have a single value
        * turn set([value]) into value and remove key associated to empty set
        * remove non inlined relations and return them as a [(e1key, relation, e2key)] list

        Return a list of non inlined relations that may be inserted later, each relations defined by
        a 3-tuple (subject extid, relation type, object extid).

        Take care the importer may call this method several times.
        """
        if self._schema is not None: # already prepared
            assert self._schema is schema
            return ()
        self._schema = schema
        eschema = schema.eschema(self.etype)
        deferred = []
        entity_dict = self.values
        for rtype in list(entity_dict):
            rschema = schema.rschema(rtype)
            if rschema.final or rschema.inlined:
                assert len(entity_dict[rtype]) <= 1, \
                    "more than one value for attribute %s: %s (%s)" % (rtype, entity_dict[rtype],
                                                                       self.extid)
                if entity_dict[rtype]:
                    entity_dict[rtype] = entity_dict[rtype].pop()
                    if (rschema.final and eschema.has_metadata(rtype, 'format')
                            and not rtype + '_format' in entity_dict):
                        entity_dict[rtype + '_format'] = u'text/plain'
                else:
                    del entity_dict[rtype]
            else:
                for target_extid in entity_dict[rtype]:
                    deferred.append((self.extid, rtype, target_extid))
                del entity_dict[rtype]
        return deferred

    def is_ready(self, extid2eid):
        """Return True if the ext entity is ready, i.e. has all the URIs used in inlined relations
        currently existing.
        """
        entity_dict = self.values
        assert self._schema, 'prepare() method should be called first'
        schema = self._schema
        for rtype in entity_dict:
            rschema = schema.rschema(rtype)
            if not rschema.final:
                # _prepare_extentity should drop other cases from the entity dict
                assert rschema.inlined
                if not entity_dict[rtype] in extid2eid:
                    return False
        # entity is ready, replace all relation's extid by eids
        for rtype in entity_dict:
            rschema = schema.rschema(rtype)
            if rschema.inlined:
                entity_dict[rtype] = extid2eid[entity_dict[rtype]]
        return True

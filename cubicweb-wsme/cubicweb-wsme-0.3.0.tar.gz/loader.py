""" Utilities to load ws types from the database
"""
import itertools
import re

import wsme.types

from rql import nodes

from rqlquery.filter import FilterParser
from rqlquery import query

from cubes.wsme.types import wsattr


def get_fetchable_attributes(user, eschema):
    relations = []
    for rschema in eschema.ordered_relations():
        if not rschema.final:
            continue
        if rschema.type in (
                'eid', 'has_text', 'cw_source', 'is'):
            continue
        if rschema.objects()[0].type in ('Password',):
            continue
        rdef = eschema.rdef(rschema)
        if not user.matching_groups(rdef.get_groups('read')):
            continue
        relations.append(rschema)
    return relations


def get_fetchable_unary_relations(user, eschema):
    relations = []
    for rschema in eschema.ordered_relations():
        card = eschema.rdef(rschema.type, takefirst=True).cardinality[0]
        if (card in ('*', '+')
                # cardinality '?' with polymorphic relations raises
                # https://www.cubicweb.org/ticket/4482382
                or card == '?' and len(rschema.objects(eschema)) > 1):
            continue

        if rschema.final:
            continue

        if rschema.type in (
                'eid', 'has_text', 'cw_source', 'is'):
            continue
        if any(
                not user.matching_groups(es.get_groups('read'))
                for es in rschema.objects(eschema)):
            continue
        relations.append(rschema)
    return relations


def get_unfetchable_unary_relations(user, eschema):
    relations = []

    for rschema in eschema.ordered_relations():
        card = eschema.rdef(rschema.type, takefirst=True).cardinality[0]
        if card == '?' and len(rschema.objects(eschema)) > 1:
            relations.append(rschema)

    return relations


def tree_touch_path(tree, path):
    node = tree
    for name in path:
        node = node.setdefault(name, {})


def to_fetchtree(fetchlist, keyonly=False):
    if fetchlist is None:
        if keyonly:
            return {}
        else:
            return {'': {}}

    fetchtree = {}

    for rel in fetchlist:
        tree_touch_path(fetchtree, rel.split('.'))

    return fetchtree


def get_columns(cnx, cwetype, fetchtree):
    """ Returns columns to query for filling cwetype

    Recursively calls itself for inlined relations

    Returns
    - a mapping for itself and the inlined relations (recursively)

    """
    mapping = {'eid': None}

    if fetchtree in (None, {}) or cwetype.__etype__ == 'Any':
        mapping['modification_date'] = None

    else:
        eschema = cnx.vreg.schema.eschema(cwetype.__etype__)

        for rtype in get_fetchable_attributes(cnx.user, eschema):
            mapping[rtype.type] = None

        for rtype in get_fetchable_unary_relations(cnx.user, eschema):
            if not hasattr(cwetype, rtype.type):
                continue

            tgt_cwetype = getattr(cwetype, rtype.type).datatype

            mapping[rtype.type] = get_columns(
                cnx, tgt_cwetype, fetchtree.get(rtype.type))

    return mapping


def add_columns(q, mapping, col_counter, prefix=()):
    """ Add columns of the mapping to the query

    Returns the updated query
    """
    mapping['eid'] = col_counter.next()

    for key in list(mapping):
        value = mapping[key]

        if value is None:
            q = q.add_column(prefix + (key,))
            mapping[key] = col_counter.next()

        elif isinstance(value, dict):
            q = q.add_column(prefix + (key,))

            q = add_columns(q, value, col_counter, prefix + (key,))

    return q

_rtype_re = re.compile(
    r'(?P<rev>\<)?(?P<rtype>[^.[]+)(\[(?P<etypes>[^\]]+)\])?')


def get_unloaded_relations(cnx, cwetype, mapping, fetchtree):
    # for each key in fetchtree not present in mapping, check the actual
    # relation type (final or not) and returns it.

    # for each key in both trees that is a dict with content
    # do a recursive call

    schema = cnx.vreg.schema

    relations = []

    if cwetype.__etype__ == 'Any':
        return ()

    eschema = schema.eschema(cwetype.__etype__)
    # automatically add the ?* relations because they are expected by the
    # clients but not automatically loaded (see get_fetchable_unary_relations)
    for rschema in get_unfetchable_unary_relations(cnx.user, eschema):
        # make sure the relation exists as an attribute:
        attr = filter(
            lambda a: (
                isinstance(a, wsattr)
                and a.rtype == rschema.type
                and a.role == 'subject'),
            cwetype._wsme_attributes)
        if attr:
            attr = attr[0]
            if attr.key not in fetchtree and attr.key not in mapping:
                relations.append(((attr.key,), attr, None))

    for key in fetchtree:
        if key in mapping and not(fetchtree[key]):
            continue

        if key in ('', '*'):
            continue

        m = _rtype_re.match(key)
        assert m is not None, (
            "A invalid key in fetchtree should never reach this code")

        name = (m.group('rev') or '') + m.group('rtype')

        attr = cwetype.attr_by_name(name)

        if not isinstance(attr, wsattr):
            continue

        rtype = attr.rtype

        rschema = schema.rschema(rtype)

        if rschema.final:
            # TODO handle fetching specific attributes
            # (not in this function obviously)
            continue

        if key not in mapping:
            relations.append(((key,), attr, fetchtree[key]))
        else:
            relations.extend((
                ((key,) + path, t, f)
                for path, t, f in get_unloaded_relations(
                    cnx,
                    attr.datatype.item_type
                    if wsme.types.isarray(attr.datatype)
                    else attr.datatype,
                    mapping[key],
                    fetchtree[key])
            ))

    return relations


def make_iter(obj_or_iter):
    if obj_or_iter in (None, wsme.types.Unset):
        return iter(())
    if isinstance(obj_or_iter, (list, dict, set, tuple)):
        return iter(obj_or_iter)
    return iter((obj_or_iter,))


def get_entities(roots, path):
    entities = roots

    for attrname in path:
        if not entities:
            break
        key = iter(entities).next().attr_by_name(attrname).key
        entities = set(itertools.chain(
            *[make_iter(getattr(o, key)) for o in entities]))

    return list(entities)


def load_entities(
        cnx, cwetype,
        orderby=None, query_filter=None, limit=None, offset=None,
        fetchtree=None):

    q = query.Query(cnx.vreg.schema, cwetype.__etype__)

    mapping = get_columns(cnx, cwetype, fetchtree)

    col_count = iter(xrange(999))

    q = add_columns(q, mapping, col_count)

    if orderby:
        q = q.orderby(*orderby)
    if query_filter:
        q = q.filter(FilterParser(
            cnx.vreg.schema, cwetype.__etype__, query_filter
        ).parse())
    if limit:
        q = q.limit(limit)
    if offset:
        q = q.offset(offset)

    rset = q.execute(cnx)

    entities = [
        cwetype.from_row(cnx, rset, row_i, row, mapping, fetchtree)
        for row_i, row in enumerate(rset)
    ]

    # nested relation loading
    # scan the mapping and get all unloaded relations that are in fetchtree.
    # Load them, complete the mapping (which is now only a tree of what was
    # loaded), and redo until every relation is loaded

    while True:
        relations = get_unloaded_relations(cnx, cwetype, mapping, fetchtree)

        if not relations:
            break

        for path, attr, sub_fetchtree in relations:
            sub_cwetype = attr.datatype
            isarray = wsme.types.isarray(sub_cwetype)

            if isarray:
                sub_cwetype = sub_cwetype.item_type

            col_count = iter(xrange(999))

            etype = sub_cwetype.__etype__
            etypes = None
            if etype == 'Any':
                m = _rtype_re.match(path[-1])
                if m.group('etypes'):
                    etypes = m.group('etypes').split(',')
                    if len(etypes) == 1:
                        etype = etypes[0]
                        etypes = None

            q = query.Query(cnx.vreg.schema, etype)

            if etypes:
                q = q.filter(query.Is(*etypes))

            sub_mapping = get_columns(cnx, sub_cwetype, sub_fetchtree)
            q = add_columns(q, sub_mapping, col_count)

            # Get all parent objects waiting for relation targets
            objs_by_eid = {}
            for entity in get_entities(entities, path[:-1]):
                objs_by_eid.setdefault(entity.eid, []).append(entity)

            if not objs_by_eid:
                m = mapping
                for key in path[:-1]:
                    m = m[key]
                m[path[-1]] = sub_mapping
                continue

            rql, kw = q.torql()

            rqlst = cnx.vreg.parse(cnx, rql, kw)

            select = rqlst.children[0]

            select.set_groupby(list(select.selection))

            mainvar = select.get_variable('X')
            srcvar = select.get_variable('Y')

            gr = nodes.Function('GROUP_CONCAT')
            gr.append(nodes.VariableRef(srcvar))

            select.add_selected(gr)

            if attr.role == 'subject':
                rel = nodes.make_relation(
                    srcvar, attr.rtype, (mainvar,), nodes.VariableRef)
            else:
                rel = nodes.make_relation(
                    mainvar, attr.rtype, (srcvar,), nodes.VariableRef)

            select.add_restriction(rel)

            select.add_restriction(
                nodes.make_constant_restriction(
                    srcvar, 'eid', objs_by_eid.keys(), 'Int'))

            rset = cnx.execute(select, kw)

            if isarray:
                for obj in itertools.chain(*objs_by_eid.values()):
                    setattr(obj, attr.key, [])
            for row_i, row in enumerate(rset):
                sub_entity = sub_cwetype.from_row(
                    cnx, rset, row_i, row, sub_mapping, sub_fetchtree)
                eids = [int(eid) for eid in row[-1].split(',')]

                for obj in itertools.chain(
                        *[objs_by_eid[eid] for eid in eids]):
                    if isarray:
                        getattr(obj, attr.key).append(sub_entity)
                    else:
                        setattr(obj, attr.key, sub_entity)

            m = mapping
            for key in path[:-1]:
                m = m[key]
            m[path[-1]] = sub_mapping

    return entities

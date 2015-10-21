"""cubicweb-datacat test utilities"""

from cubicweb import Binary


def same_entities(eids, expected, cnx):
    """Returns a 2-uple ``(bool, msg)`` depending on entities given by their eids.

    Returns ``(True, 'Same entities')`` if the entities match the given expected values.

    Returns ``(False, msg)`` in the other case.

    ``expected`` parameter is a dictionary with the following format.

    .. code-block:: python

        {<cwuri>:
            (<etype>,
            {<attr1>: set([<value1>]),
             <attr2>: set([<value2>]),
             <rel1>: set([<eid1>, <eid2>]),
            ...
            })
        }

    ``cnx`` is the connection object to CubicWeb used to get an entity from its eid.
    """
    i = 0
    for i, eid in enumerate(eids, 1):
        entity = cnx.entity_from_eid(eid)
        uri = entity.cwuri
        expected_type, expected_values = expected[uri]
        # Check type
        if entity.cw_etype != expected_type:
            return False, u"Not same type '{0}' & '{1}' for entity {2}".format(
                entity.cw_etype, expected_type, uri)
        # Check attributes and relations
        for attr, expected_value in expected_values.iteritems():
            value = getattr(entity, attr)
            if attr == 'geometry':
                value = set([value])
            elif isinstance(value, (list, tuple)):  # attr is a relation
                value = set([rel_entity.cwuri for rel_entity in value])
            else:
                value = set([value])
            if not value.issubset(expected_value):
                return False, (u"Not same value '{0}' & '{1}' for attribute "
                               U"'{2}' on entity {3}".format(
                                   value, expected_value, attr, uri))
    if i == len(expected):
        return True, u'Same entities'
    else:
        return False, u'There are not found expected entities.'


def create_file(cnx, data, data_name=None, **kwargs):
    """Create a File entity"""
    data_name = data_name or data.decode('utf-8')
    kwargs.setdefault('data_format', u'text/plain')
    return cnx.create_entity('File', data=Binary(data),
                             data_name=data_name,
                             **kwargs)


def produce_file(cnx, resourcefeed, inputfile):
    """Simulate the production of `inputfile` by resource feed `resourcefeed`"""
    # Build a transformation process "by hand".
    with cnx.security_enabled(write=False):
        process = cnx.create_entity('DataTransformationProcess',
                                    process_input_file=inputfile,
                                    process_script=resourcefeed.transformation_script)
        cnx.commit()
    iprocess = process.cw_adapt_to('IDataProcess')
    # Add `produced_by` relation.
    with cnx.security_enabled(write=False):
        outfile = iprocess.build_output(inputfile, 'plop')
        cnx.commit()
    return outfile

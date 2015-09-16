# -*- coding: utf-8 -*-


def parse_sort_string(sort):
    """
    Parse a sort string for use with elasticsearch

    :param: sort: the sort string
    """
    if sort is None:
        return ['_score']
    l = sort.rsplit(',')
    sortlist = []
    for se in l:
        se = se.strip()
        order = 'desc' if se[0:1] == '-' else 'asc'
        field = se[1:] if se[0:1] in ['-', '+'] else se
        field = field.strip()
        sortlist.append({field: {"order": order, "unmapped_type": "string", "missing": "_last"}})
    sortlist.append('_score')
    return sortlist

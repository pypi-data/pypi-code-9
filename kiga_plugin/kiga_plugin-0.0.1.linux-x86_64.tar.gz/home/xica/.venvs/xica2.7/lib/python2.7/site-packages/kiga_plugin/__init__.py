from pkg_resources import iter_entry_points


def load_entry_point(group, name):
    entry_point = next((x for x in iter_entry_points(group, name) if x.name == name), None)
    if entry_point is None:
        raise ValueError('entry point "{}.{}" not found.'.format(group, name))
    return entry_point.load()

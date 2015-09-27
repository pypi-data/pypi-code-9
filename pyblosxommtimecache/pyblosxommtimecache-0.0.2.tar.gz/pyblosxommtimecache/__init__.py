__author__      = "Sean Hammond pyblosxommtimecache at seanh dot cc"
__version__     = "0.1"
__url__         = "https://github.com/seanh/pyblosxommtimecache"
__description__ = ("A Pyblosxom filestat plugin caches the mtimes of your "
                   "entries in a .mtimes.yaml file.")


import datetime
import stat
import os.path


def _mtimes_path(args):
    """Return the absolute path to the .mtimes.yaml file."""
    return os.path.join(
        args['request'].get_configuration()['datadir'], '.mtimes.yaml')


def _mtimes_cache(args):
    """Return the mtimes_cache dict from the request data."""
    return args['request'].get_data()['mtimes_cache']


def _iso_8601_to_unix_time(s):
    """Return the given ISO 8601-formatted time string as a UNIX timestamp.

    Returns the time in number of seconds since the epoch, as a float.

    """
    return float(
        datetime.datetime.strptime(s, '%Y-%m-%dT%H:%M:%S').strftime('%s'))


def _unix_time_to_iso_8601(t):
    """Return the given UNIX timestamp as an ISO 8601-formatted string."""
    return datetime.datetime.fromtimestamp(t).isoformat()


def verify_installation(request):
    try:
        import yaml
        return True
    except ImportError:
        print "Couldn't import yaml, is PyYAML installed?"
        return False


def cb_start(args):
    """Add the mtimes_cache dict to the request data.

    Read the mtimes_cache dict from the .mtimes.yaml file, fall back to an
    empty dict if the file doesn't exist yet.

    """
    import yaml
    try:
        mtimes_cache = yaml.load(open(_mtimes_path(args), 'r').read())
    except IOError as err:
        if err.errno == 2:
            mtimes_cache = {}
        else:
            raise
    args['request'].add_data({'mtimes_cache': mtimes_cache})


def cb_filestat(args):
    """Override the entry's mtime with its cached mtime, if we have one."""
    mtime = _mtimes_cache(args).get(args['filename'])
    if mtime:
        mtime = _iso_8601_to_unix_time(mtime)
        stat_list = list(args['mtime'])
        stat_list[stat.ST_MTIME] = mtime
        args['mtime'] = tuple(stat_list)
    return args


def cb_story(args):
    """Cache the entry's mtime, if we haven't already."""
    mtimes_cache = _mtimes_cache(args)
    entry = args['entry']
    if entry['filename'] not in mtimes_cache:
        mtime = _unix_time_to_iso_8601(entry['mtime'])
        mtimes_cache[entry['filename']] = mtime
        args['request'].get_data()['mtimes_cache_modified'] = True
    return args


def cb_end(args):
    """Save the mtimes_cache if we've changed it."""
    import yaml
    if args['request'].get_data().get('mtimes_cache_modified'):
        open(_mtimes_path(args), 'w').write(
            yaml.dump(_mtimes_cache(args), default_flow_style=False))

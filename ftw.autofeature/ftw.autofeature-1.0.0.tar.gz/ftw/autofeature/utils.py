from itertools import permutations
from operator import attrgetter
from path import Path
from pkg_resources import DistributionNotFound
from pkg_resources import get_distribution


def find_package_by_module(module):
    egg_info = get_egg_info_path_by_module(module)
    if not egg_info:
        return None

    pkg_info = egg_info.joinpath('PKG-INFO')
    assert pkg_info.isfile(), '{0} is missing'.format(pkg_info)

    names = filter(lambda line: line.startswith('Name: '),
                   pkg_info.lines())
    assert names, 'No "Name: " in {0}'.format(pkg_info)
    return names[0].split(':')[1].strip()


def find_extras_by_package(packagename):
    dist = get_distribution(packagename)
    requires = set(map(attrgetter('project_name'), dist.requires()))
    result = {}

    for name in dist.extras:
        extras_requires = set(map(attrgetter('project_name'),
                                  dist.requires([name])))
        result[name] = sorted(extras_requires - requires)

    return result


def get_egg_info_path_by_module(module):
    path = Path(module.__file__)
    while path != '/':
        egg_info = get_egg_info_path_in_path(path)
        if egg_info:
            return egg_info

        path = path.parent

    return None


def get_egg_info_path_in_path(path):
    egg_infos = path.glob('*.egg-info') + path.glob('EGG-INFO')
    if not egg_infos:
        return None

    egg_info, = egg_infos
    pkg_info = egg_info.joinpath('PKG-INFO')
    if pkg_info.isfile():
        return egg_info
    else:
        return None


def all_packages_installed(packagenames):
    try:
        map(get_distribution, packagenames)
    except DistributionNotFound:
        return False
    else:
        return True


def combine_features(names):
    result = []
    for parts in range(1, len(names) + 1):
        result.extend(map(':'.join, permutations(names, parts)))
    return result

import os
from reseasdk.helpers import load_yaml
from reseasdk.validators import \
    validate_packages_yml, validate_package_yml, validate_build_yml, validate_global_yml
from reseasdk.helpers import error


def get_package_dir(package):
    cwd = os.getcwd()
    # look for packages.yml
    while True:
        os.chdir("..")
        if os.getcwd() == "/":
            error("packages.yml not found")
        if os.path.exists("packages.yml"):
            package_dir = os.getcwd()
            break

    yml = load_yaml('packages.yml', validator=validate_packages_yml)
    os.chdir(cwd)

    # get the path to the package
    try:
        path = os.path.join(package_dir, yml["packages"][package]["path"])
    except KeyError:
        error("package not found in packages.yml: '{}'".format(package))

    return path


def get_package(package):
    """ Prepare a package in 'packages' directory """

    if not os.path.exists('packages/' + package):
        os.makedirs('packages', exist_ok=True)
        os.chdir('packages')
        os.symlink(get_package_dir(package), package)
        os.chdir('..')


global_ymls = {} # cache
def load_global_yml(package):
    if package in global_ymls:
        return global_ymls[package]

    get_package(package)
    try:
        yml = load_yaml('packages/{}/global.yml'.format(package),
                        validator=validate_global_yml)
    except FileNotFoundError:
        yml = {}
    global_ymls[package] = yml
    return yml


build_ymls = {} # cache
def load_build_yml(package):
    if package in build_ymls:
        return build_ymls[package]

    get_package(package)
    try:
        yml = load_yaml('packages/{}/build.yml'.format(package),
                        validator=validate_build_yml)
    except FileNotFoundError:
        yml = {}
    build_ymls[package] = yml
    return yml


package_ymls = {} # cache
def load_package_yml(package):
    if package in package_ymls:
        return package_ymls[package]

    get_package(package)
    yml = load_yaml('packages/{}/package.yml'.format(package),
                    validator=validate_package_yml)
    package_ymls[package] = yml
    return yml


def resolve_package_dependency(_packages, all_in_one):
    """ Returns list of required packages. """
    packages = []
    follows = ['library']
    if all_in_one:
        follows.append('application')
    for package in _packages:
        yml = load_package_yml(package)
        packages += yml['implements']
        packages += yml['uses']
        for require in yml['requires']:
            if load_package_yml(require)['category'] in follows:
                packages += resolve_package_dependency([require], all_in_one)
            packages.append(require)
        packages.append(package)
    return list(set(packages))


def filter_package_by_category(categories, packages):
    matched = []
    for package in packages:
        if load_package_yml(package)['category'] in categories:
            matched.append(package)
    return matched


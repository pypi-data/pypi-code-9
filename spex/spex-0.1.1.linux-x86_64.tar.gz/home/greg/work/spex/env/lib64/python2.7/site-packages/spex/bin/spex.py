from __future__ import absolute_import, print_function

from contextlib import contextmanager

from .args import create_parser
from ..config import SpexConfig, SparkConfig
from ..utils import establish_spark_distro, uber_distro_location

import tempfile
import functools
import os
import shutil
import sys
import tarfile

import pkg_resources

from pex.archiver import Archiver
from pex.base import maybe_requirement
from pex.common import die, safe_delete, safe_mkdir, safe_mkdtemp
from pex.crawler import Crawler
from pex.fetcher import PyPIFetcher
from pex.http import Context
from pex.installer import EggInstaller
from pex.interpreter import PythonInterpreter
from pex.iterator import Iterator
from pex.package import EggPackage, SourcePackage
from pex.pex_builder import PEXBuilder
from pex.requirements import requirements_from_file
from pex.resolvable import Resolvable
from pex.resolver import CachingResolver, Resolver, Unsatisfiable
from pex.resolver_options import ResolverOptionsBuilder
from pex.tracer import TRACER
from pex.util import DistributionHelper
from pex.variables import ENV
from pex.version import SETUPTOOLS_REQUIREMENT, WHEEL_REQUIREMENT

CANNOT_DISTILL = 101
CANNOT_SETUP_INTERPRETER = 102
INVALID_OPTIONS = 103
INVALID_ENTRY_POINT = 104

_PREAMBLE = '''
import os
import sys
import zipfile
import contextlib

FULL_WORKING_DIR = os.path.abspath(os.path.realpath(os.getcwdu()))
PEX_ROOT = os.path.join(FULL_WORKING_DIR, 'pex_root')
try:
    os.makedirs(PEX_ROOT)
except OSError:
    pass
SPEX_FILE = os.path.abspath(os.path.realpath(sys.path[0]))
SPEX_CONF = os.path.join(PEX_ROOT, 'SPEX-INFO')
# Set this to avoid pex writing out to shared home directories
os.environ['PEX_ROOT'] = PEX_ROOT
# PEX cleans this up when it does its execvp, stash it because we know better
os.environ['SPEX_ROOT'] = PEX_ROOT
os.environ['SPEX_FILE'] = SPEX_FILE
os.environ['SPEX_CONF'] = SPEX_CONF

with contextlib.closing(zipfile.ZipFile(SPEX_FILE)) as zf:
    with open(SPEX_CONF, 'w') as spex_conf:
        spex_conf.write(zf.read('SPEX-INFO'))
'''


def log(msg, verbose=False):
    if verbose:
        print(msg, file=sys.stderr)


def _safe_link(src, dst):
    try:
        os.unlink(dst)
    except OSError:  # noqa
        pass
    os.symlink(src, dst)


def _resolve_and_link_interpreter(requirement, fetchers, target_link, installer_provider):
    # Short-circuit if there is a local copy
    if os.path.exists(target_link) and os.path.exists(os.path.realpath(target_link)):
        egg = EggPackage(os.path.realpath(target_link))
        if egg.satisfies(requirement):
            return egg

    context = Context.get()
    iterator = Iterator(fetchers=fetchers, crawler=Crawler(context))
    links = [link for link in iterator.iter(requirement) if isinstance(link, SourcePackage)]

    with TRACER.timed('Interpreter cache resolving %s' % requirement, V=2):
        for link in links:
            with TRACER.timed('Fetching %s' % link, V=3):
                sdist = context.fetch(link)

            with TRACER.timed('Installing %s' % link, V=3):
                installer = installer_provider(sdist)
                dist_location = installer.bdist()
                target_location = os.path.join(
                    os.path.dirname(target_link), os.path.basename(dist_location))
                shutil.move(dist_location, target_location)
                _safe_link(target_location, target_link)

            return EggPackage(target_location)


def resolve_interpreter(cache, fetchers, interpreter, requirement):
    requirement = maybe_requirement(requirement)

    # short circuit
    if interpreter.satisfies([requirement]):
        return interpreter

    def installer_provider(sdist):
        return EggInstaller(
            Archiver.unpack(sdist),
            strict=requirement.key != 'setuptools',
            interpreter=interpreter)

    interpreter_dir = os.path.join(cache, str(interpreter.identity))
    safe_mkdir(interpreter_dir)

    egg = _resolve_and_link_interpreter(
        requirement,
        fetchers,
        os.path.join(interpreter_dir, requirement.key),
        installer_provider)

    if egg:
        return interpreter.with_extra(egg.name, egg.raw_version, egg.path)


def _establish_interpreter(args):
    if args.python:
        if os.path.exists(args.python):
            interpreter = PythonInterpreter.from_binary(args.python)
        else:
            interpreter = PythonInterpreter.from_env(args.python)
        if interpreter is None:
            die('Failed to find interpreter: %s' % args.python)
    else:
        interpreter = PythonInterpreter.get()

    with TRACER.timed('Setting up interpreter %s' % interpreter.binary, V=2):
        resolve = functools.partial(resolve_interpreter, args.interpreter_cache_dir, args.repos)

        # resolve setuptools
        interpreter = resolve(interpreter, SETUPTOOLS_REQUIREMENT)

        # possibly resolve wheel
        if interpreter and args.use_wheel:
            interpreter = resolve(interpreter, WHEEL_REQUIREMENT)

        return interpreter


def _establish_resolver_options(args):
    resolver_options_builder = ResolverOptionsBuilder()

    if args.use_pypi:
        resolver_options_builder.add_index(PyPIFetcher.PYPI_BASE)

    for index in args.indicies:
        resolver_options_builder.add_index(index)

    for repo in args.repos:
        resolver_options_builder.add_repository(repo)

    if args.build_source:
        resolver_options_builder.allow_builds()
    else:
        resolver_options_builder.no_allow_builds()

    if args.use_wheel:
        resolver_options_builder.use_wheel()
    else:
        resolver_options_builder.no_use_wheel()

    return resolver_options_builder


def _add_spex_deps(resolvables, pex_builder, resolver_option_builder=None):
    spex = [pkg for pkg in pkg_resources.working_set if pkg.project_name == 'spex']
    assert len(spex) == 1, 'Too many spex distributions'
    spex = spex[0]
    spex_reqs = (Resolvable.get(str(req), resolver_option_builder) for req in spex.requires())
    resolvables.extend(spex_reqs)
    pex_builder.add_distribution(spex)
    pex_builder.add_requirement(spex.as_requirement())


def build_pex(args):
    with TRACER.timed('Resolving interpreter', V=2):
        interpreter = _establish_interpreter(args)

    if interpreter is None:
        die('Could not find compatible interpreter', CANNOT_SETUP_INTERPRETER)

    pex_builder = PEXBuilder(path=safe_mkdtemp(), interpreter=interpreter, preamble=_PREAMBLE)

    pex_info = pex_builder.info

    pex_info.zip_safe = False
    pex_info.always_write_cache = True
    pex_info.inherit_path = False

    resolver_option_builder = _establish_resolver_options(args)
    reqs = args.reqs
    resolvables = [Resolvable.get(req, resolver_option_builder) for req in reqs]

    for requirements_txt in args.requirement_files:
        resolvables.extend(requirements_from_file(requirements_txt, resolver_option_builder))

    resolver_kwargs = dict(interpreter=interpreter, platform=args.platform)
    _add_spex_deps(resolvables, pex_builder, resolver_option_builder=resolver_option_builder)

    if not args.disable_cache:
        resolver = CachingResolver(args.cache_dir, args.cache_ttl, **resolver_kwargs)
    else:
        resolver = Resolver(**resolver_kwargs)

    resolveds = []
    with TRACER.timed('Resolving distributions'):
        try:
            resolveds = resolver.resolve(resolvables)
        except Unsatisfiable as exception:
            die(exception)

    for dist in resolveds:
        log('  %s' % dist, verbose=args.verbosity)
        pex_builder.add_distribution(dist)
        pex_builder.add_requirement(dist.as_requirement())

    pex_builder.set_entry_point('spex:spex')

    if args.python_shebang:
        pex_builder.set_shebang(args.python_shebang)

    return pex_builder


@contextmanager
def dump_args_as_config(args):
    """Given the args and the parser that made them, dump the configuration out

    Parameters
    ----------
    args : dict-like
        The arguments to serialise to json
    """
    def _safe_dump(name, default=None):
        if hasattr(args, name):
            return getattr(args, name)
        else:
            return default

    spark_config = SparkConfig(**{k: _safe_dump(k) for k in SparkConfig._fields})  # noqa
    if args.build_distro:
        to_replace = {}
        for group in ('jars', 'py_files', 'files'):
            original_artifacts = getattr(spark_config, group, [])
            altered_artifacts = tuple(os.path.join(group, os.path.basename(art)) for art in original_artifacts)
            to_replace[group] = altered_artifacts

        spark_config = spark_config._replace(**to_replace)  # noqa

    to_dump = SpexConfig(
        spex_name=args.spex_name,
        spark_config=spark_config,
        spex_root=None,
        spex_conf=None,
        spex_file=None,
        spark_distro=None,
        entry_point=None,
    )

    _, name = tempfile.mkstemp(text=True)
    with open(name, 'w') as output:
        output.write(to_dump.dumps())
    yield name
    os.unlink(name)


def create_distro_tarball(spark_distro, spark_name, spex_file, spex_name, args):
    with tarfile.open(spex_name + '-distro.tar.bz2', 'w:bz2') as tarball:
        log('Including spex file [%s] in full distribution' % spex_file)
        tarball.add(spex_file, arcname=os.path.join(spex_name, spex_file))
        log('Including spark package [%s] in full distribution' % spark_distro)
        tarball.add(spark_distro, arcname=os.path.join(spex_name, spark_name + '.tar.bz2'))

        additional_artifacts = (
            ('files', args.files),
            ('py_files', args.py_files),
            ('jars', args.jars))

        log('Including additional artifacts in full distribution')
        for arcdir, artifacts in additional_artifacts:
            for artifact in (os.path.realpath(a) for a in artifacts):
                arcfile = os.path.basename(artifact)
                if os.path.exists(artifact):
                    arcname = os.path.join(os.path.join(spex_name, arcdir), arcfile)
                    log('Including ' + arcname)
                    tarball.add(artifact, arcname=arcname)
                else:
                    die('You asked me to include a %s that does not exist [%s]' % (arcdir, artifact))


def main(args=None):
    parser = create_parser()
    args = parser.parse_args(args)

    if args.build_distro:
        if not args.spark_home:
            die("No spark home given but building a distribution")

        spark_home = os.path.realpath(os.path.abspath(args.spark_home))
        if not os.path.exists(spark_home):
            die("No spark home given but building a distribution")
        spark_name = os.path.basename(spark_home)

        args.spark_home = spark_home
        args.spark_name = spark_name
    else:
        spark_home = None
        spark_name = None

    spex_name = args.spex_name
    spex_file = spex_name + '.spex'

    with ENV.patch(PEX_VERBOSE=str(args.verbosity)):
        with TRACER.timed('Building spex'):
            with TRACER.timed('Building pex'):
                pex_builder = build_pex(args)

                with dump_args_as_config(args) as cfg:
                    pex_builder.add_resource(cfg, 'SPEX-INFO')

                    log('Saving PEX file to %s' % spex_file, verbose=args.verbosity)
                    tmp_name = args.spex_name + '~'
                    safe_delete(tmp_name)
                    pex_builder.build(tmp_name)
                    os.rename(tmp_name, spex_file)

            if args.build_distro:
                with TRACER.timed('Building spark package'):
                    spark_distro = uber_distro_location(spark_name)
                    establish_spark_distro(spark_distro, spark_home, spark_name, spex_file, spex_name)
                log('Spark package built')

                with TRACER.timed('Building full distribution'):
                    create_distro_tarball(spark_distro, spark_name, spex_file, spex_name, args)
                log('Saved full distribution to %s' % spark_distro)

    return 0


if __name__ == '__main__':
    main()

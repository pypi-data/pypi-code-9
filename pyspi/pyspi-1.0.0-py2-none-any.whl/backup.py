import argparse
import functools
import hashlib
import logging
import os
import re
import subprocess
import sys

from github3 import GitHub

logging.captureWarnings(True)


def main():
    """
    # Preparing a github repository as a barrow repository:

        1. Create a github release
        2. Attach python wheels or eggs to the releases

    $ barrow build
    $ barrow host \
        [--repo REPO] [--rev COMMITTISH] [--tag TAG] [--title NAME] WHEEL

    To release wheels for all tags but those with 'rc' in the name:

    $ for tag in $(git tag --list | grep -v rc); do
        rm *.whl
        git checkout $tag
        barrow build
        barrow host --repo REPO --rev $(git rev-parse HEAD) --tag $tag *.whl
      done

    It makes sense that the version of the package declared in setup.py is used
    as the tag of the revision. This will be an easier convention to help with
    uploading; but is by no means a requirement when it comes to hosting them.

        ? Do we need to include the MD5 information here? YESSIR

    # Adding a python package to the package repository:

        1. Add the package name and a reference to its barrow repo in the
           package index located in the root of the repository.
        2. Create a link in simple/index.html to simple/$package/index.html.
        3. List all of the downloadable wheels, and eggs for each version of
           the repository in index.html.

    # Point pip at the repository. Job done.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--github', metavar='TOKEN', help='Github API Token',
                        type=lambda token: GitHub(token=token),
                        default='fb58af392e2793b31f1a8b4af8f513eabbd2c725')

    sub = parser.add_subparsers()

    build_parser = sub.add_parser('build')
    build_parser.add_argument('--root', default='.', help='Python pkg root')
    build_parser.set_defaults(_entry=main_build)

    host_parser = sub.add_parser('host')
    host_parser.add_argument('--repo', metavar='OWNER/REPO', type=github_repo,
                             help='Github repository', required=True)
    host_parser.add_argument('--rev', help='Revision', metavar='SHA')
    host_parser.add_argument('--tag', help='Tag for release', required=True)
    host_parser.add_argument('--title', help='Title for the release')
    host_parser.add_argument('assets', nargs='+',
                             help='Assets (wheels/eggs) to upload')
    host_parser.set_defaults(_entry=main_host)

    index_parser = sub.add_parser('index')
    index_parser.add_argument('--index', metavar='PATH', default='.')
    index_parser.add_argument('--add', nargs=3, action='append')
    index_parser.add_argument('packages', nargs='*', metavar='package')
    index_parser.set_defaults(_entry=main_index)

    args = parser.parse_args()
    return args._entry(args)


def main_build(args):
    subprocess.check_call(['pip', 'wheel', '--no-deps', '-w', '.', args.root])


def main_host(args):
    github = args.github

    # Get the repository.
    repo = github.repository(*args.repo)
    if not repo:
        return warn('Could not find repository %s' % '/'.join(args.repo))

    # Get the tag.
    tag_name = args.tag
    tag = repo.ref('tags/%s' % tag_name)
    if not tag:
        # Create the tag.
        if not args.rev:
            return warn('Revision required to create tag %s' % tag_name)
        warn('Creating tag ref %s at revision %s' % (tag_name, args.rev))
        tag = repo.create_ref('refs/tags/%s' % tag_name, args.rev)

    # Get the release.
    release = find_repo_release(repo, tag_name)
    if not release:
        # Create the release.
        warn('Creating release at tag %s' % tag_name)
        release = repo.create_release(
            tag_name=tag_name,
            name=args.title
        )

    # Refuse to override assets which already exist.
    assets = {
        os.path.basename(asset): asset
        for asset in args.assets
    }
    for release_asset in release.iter_assets():
        if release_asset.name in assets:
            warn('Cowardly refusing to upload %s. Attachment with that name '
                 'already exists.' % release_asset.name)
            del assets[release_asset.name]

    # Upload other assets
    for asset, path in assets.iteritems():
        print 'Uploading %s...' % asset
        with open(path, 'rb') as f:
            rass = release.upload_asset('application/octet-stream', asset, f)
        rass.edit(asset, label='%s (md5:%s)' % (asset, md5_file(path)))


def main_index(args):
    origins = {
        'github': functools.partial(github_assets, args.github),
    }

    # index_add-packages(args.index, args.packages)
    simple_build_list(args.index, lol_fuck_it_iter(args, origins))


def index_add_packages(root, packages):
    pass


def lol_fuck_it_iter(args, origins):
    packages = {pkg.lower() for pkg in args.packages}
    limit = len(packages) > 0

    for package, origin, ident in index_packages_iter(args.index):
        yield package, origin, ident
        if limit:
            if package.lower() not in packages:
                continue
            packages.remove(package.lower())

        print 'Rebuilding %s version list...' % package

        simple_build_package(args.index, package, (
            (url, md5) for (_, url, md5) in
            index_versions_iter(
                [(package, origin, ident)],
                origins=origins
            )
        ))
    if len(packages) > 0:
        warn('Some packages were not found: %s' % ', '.join(packages))


def index_packages_iter(root, packages=()):
    packages = {pkg.lower() for pkg in packages}
    visited = set()
    prev_package = None

    with open(os.path.join(root, 'index'), 'r') as f:
        for line in iter(f):
            line = line.strip()
            if line.startswith('#'):
                continue

            package, origin, ident = line.split()
            plower = package.lower()

            if plower == prev_package:
                raise ValueError('Duplicate package entry: %r' % package)
            elif plower < prev_package:
                raise ValueError('Packages out of order: expected %s before %s'
                                 % (package, prev_package))

            if packages:
                if plower in packages:
                    visited.add(plower)
                else:
                    continue

            prev_package = plower
            yield package, origin, ident

    unvisited = packages - visited
    if unvisited:
        warn('Some packages were not found in the index: %s'
             % ', '.join(unvisited))


def index_versions_iter(packages, origins):
    for package, origin, ident in packages:
        if origin not in origins:
            raise ValueError('Unrecognised origin: %r' % origin)
        for asset, md5 in origins[origin](ident):
            yield package, asset, md5


def simple_build_list(root, packages):
    with open(os.path.join(root, 'simple/index.html'), 'w') as out:
        out.write('<html><head></head><body>\n')
        for package, _, _ in packages:
            out.write('<a href="%s">%s</a><br />\n' % (
                package.lower(),
                package
            ))
        out.write('</body></html>\n')


def simple_build_package(root, package, assets):
    # Make the package listing directory.
    package_dir = os.path.join(root, 'simple', package.lower())
    try:
        os.makedirs(package_dir)
    except OSError:
        pass  # It's probably just that the folder already exists.

    # Write the assets into the file.
    with open(os.path.join(package_dir, 'index.html'), 'w') as out:
        out.write('<html><head></head><body>\n')
        out.write('<h1>%s</h1>\n' % package)
        for url, md5 in assets:
            out.write('<a href="%s">%s</a><br />\n' % (
                '%s#md5=%s' % (url, md5) if md5 else url,
                os.path.basename(url)
            ))
        out.write('</body></html>\n')


def github_assets(github, repo):
    for release in github.repository(*github_repo(repo)).iter_releases():
        for asset in release.iter_assets():
            if not asset.name[-4:].lower() in ('.whl', '.egg'):
                continue
            yield (
                asset._json_data['browser_download_url'],
                extract_md5(asset.label) if asset.label else None
            )


def extract_md5(label):
    match = re.search(r'\(md5:([0-9a-f]{32})\)', label, re.IGNORECASE)
    return match.group(1) if match else None


def md5_file(path):
    with open(path, 'rb') as f:
        h = hashlib.md5()
        for chunk in iter(lambda: f.read(4096), ''):
            h.update(chunk)
        return h.hexdigest()


def find_repo_release(repo, tag_name):
    for release in repo.iter_releases():
        if release.tag_name == tag_name:
            return release
    return None


def github_repo(repo):
    try:
        owner, repo = repo.strip().split('/')
        return owner, repo
    except ValueError:
        raise argparse.ArgumentTypeError('must be of the form "owner/repo"')


def warn(msg, exit_code=1):
    print >>sys.stderr, msg
    return exit_code


if __name__ == '__main__':
    sys.exit(main() or 0)

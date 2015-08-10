#!/usr/bin/env python

from __future__ import print_function

import io
import os.path

import click

version = __version__ = '0.1.0'


def envdir_to_dict(d):
    result = {}
    for fname in os.listdir(d):
        path = os.path.join(d, fname)
        with open(path) as c:
            result[fname] = c.read()
    return result


def dict_to_envdir(env_vars, dpath):
    if not os.path.exists(dpath):
        os.mkdir(dpath)
    for k, v in env_vars.items():
        with open(os.path.join(dpath, k), 'w') as f:
            f.write(v)


def parse_envfile_contents(contents):
    result = {}
    try:
        for line in contents.strip().splitlines():
            if line.strip() and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                result[k] = v
    except ValueError:
        raise IOError("Invalid env file format: {0}".format(line))
    return result


def envfile_to_dict(fpath, encoding='utf-8'):
    with io.open(fpath, encoding=encoding) as f:
        return parse_envfile_contents(f.read())


def dict_to_envfile(env_vars, fpath):
    with open(fpath, 'w') as f:
        for k, v in sorted(env_vars.items()):
            print('{0}={1}'.format(k, v), file=f)


def parse_env(src):
    if os.path.isdir(src):
        return envdir_to_dict(src)
    elif os.path.isfile(src):
        return envfile_to_dict(src)
    else:
        raise IOError("Source environment file/dir {0!r} doesn't exist!".format(src))


def convert_to_envfile(src, dest):
    dict_to_envfile(parse_env(src), dest)


def convert_to_envdir(src, dest):
    dict_to_envdir(parse_env(src), dest)


@click.group()
@click.version_option()
def main():
    pass


@main.command()
@click.argument('src', type=click.Path(exists=True))
@click.argument('dest', type=click.Path())
def convert(src, dest):
    if os.path.isdir(src) and (os.path.isfile(dest) or not os.path.exists(dest)):
        convert_to_envfile(src, dest)
    elif os.path.isfile(src) and (os.path.isdir(dest) or not os.path.exists(dest)):
        convert_to_envdir(src, dest)
    else:
        raise IOError("src and dest cannot both be files or both directories.")
    return 0

if __name__ == '__main__':
    main()

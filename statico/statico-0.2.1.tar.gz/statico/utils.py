# -*- coding: utf-8 -*-
"""
    statico.utils
    -------------
    Defines utility functions
    :license: MIT, see LICENSE for more details.
"""
import sys
import shutil
import datetime
from pathlib import Path
from github3 import GitHub, GitHubError


if sys.version_info < (3,):
    import codecs

    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    def u(x):
        return x

def copy_directory(src, dest):
    """
    Copies a directory to a destination
    :param src:  str    The source
    :param dest: str    The destination
    :return:
    """
    try:
        shutil.copytree(src, dest)
    except shutil.Error as e:
        return 'Directory not copied. Error: ' + format(e)
    except OSError as e:
        return 'Directory not copied. Error: ' + format(e)

    return None


def get_mtime(f):
    """
    Get modification time of a given file
    :param f:
    :return:
    """
    return f.stat().st_mtime


def sorted_list_dir(path):
    """
    Returns a sorted list of directories under a given path
    :param path:
    :return:
    """
    p = Path(path)
    paths = [x for x in p.iterdir()]
    return sorted(paths, key=get_mtime, reverse=True)


def validate_date(date_text):
    """
    Checks if a string is a date (in ISO format)
    :param date_text:
    :return:
    """
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False

    return True


def get_gh_repos(user, repo_count):
    """
    Get a user's repositories with a limit
    :param user:
    :param repo_count:
    :return:
    """
    repos = None
    if user and repo_count:
        try:
            gh = GitHub()
            repo_limit = int(repo_count) if repo_count else 5
            repos = list(map(lambda r: r.repository, list(gh.search_repositories(
                'user:' + user, sort='updated'))[:repo_limit]))
        except GitHubError:
            repos = None

    return repos


def parse_metadata(fp):
    """
    Parses metadata from source files
    :param fp:
    :return:
    """
    found_open = False
    found_close = False
    rest = []
    data = {}

    for line in fp:
        line = line.strip()

        if line.startswith('---') and not found_open:
            found_open = True
        elif line.startswith('---') and found_open:
            found_close = True
        elif found_open and not found_close:
            parts = line.split(':', 1)
            attr = parts[0].strip()
            value = parts[1].strip()

            if validate_date(value):
                data[attr] = datetime.datetime.strptime(
                    value, '%Y-%m-%d').strftime('%B %d, %Y')
                data['date_iso'] = value
            else:
                data[attr] = value
        else:  # Found close
            rest.append(line)

    return rest, data

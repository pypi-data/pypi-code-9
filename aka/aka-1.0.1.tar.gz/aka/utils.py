"""
Copyright (C) 2015 Mattias Ugelvik
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import contextlib
import tempfile
import pathlib
import sys
import os


def expand_stuff(string):
    return os.path.expandvars(os.path.expanduser(string))


def find_duplicates(iterable):
    dups, seen = set(), set()
    for item in iterable:
        if item in seen:
            dups.add(item)
        seen.add(item)
    return dups


@contextlib.contextmanager
def temporary_directory():
    """
    Make a temporary directory. Will remove it afterwards, if it is empty.
    """
    temp_dir = tempfile.mkdtemp(prefix="aka_")
    try:
        yield temp_dir
    finally:
        try:
            os.rmdir(temp_dir)
        except OSError as e:
            print("LOST FILES IN TEMP DIR: {!r}".format(temp_dir), file=sys.stderr)


def prompt_user(prompt, alternatives, default=None, callbacks=dict(), file=sys.stdout):
    while True:
        print(prompt ,file=file, end="")
        response = input().lower()
        if response in alternatives:
            return response
        elif response in callbacks:
            callbacks[response]()
            continue
        elif default and response == "":
            return default
        
        print("Sorry, you must choose one: {!r}".format(alternatives), file=file)


def yes_no_prompt(prompt, default=True):
    """ Returns True if the user responds "yes", False otherwise """
    return prompt_user(
        "{} {}: ".format(prompt, "[Y/n]" if default else "[N/y]"),
        alternatives={"y", "yes", "n", "no"},
        default="y" if default else "n") in {"y", "yes"}
                           

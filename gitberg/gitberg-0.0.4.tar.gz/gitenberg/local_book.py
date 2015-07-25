#!/usr/bin/env python
# encoding: utf-8
""" An object for describing a book repo on a local filesystem """

import semver
import sh

class LocalBook(object):
    def __init__(self, path):
        self.path = path

    def find_book_file(self):
        # TODO: or summary.asciidoc
        return "{}/{}".format(self.path, 'book.asciidoc')

    def get_version(self):
        book_file_path = self.find_book_file()
        line = sh.head(book_file_path)[2]
        if not line.startswith('v'):
            raise  # version line not found
        else:
            return line[1:]

class BookVersion(object):
    def __init__(self, version_str):
        self.version = version_str

    def get_next_patch(self):
        return semver.bump_patch(self.version)

    def get_asciidoc_str(self):
        return "v{0}".format(self.get_next_patch)



        # TODO: find latest git tag
        # TODO: compare them, fail if not matched?
        # TODO: create _next_ tag

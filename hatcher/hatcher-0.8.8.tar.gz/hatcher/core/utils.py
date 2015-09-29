import hashlib
import os
import re

from requests.utils import default_user_agent as requests_user_agent

from okonomiyaki import file_formats
from okonomiyaki.versions import EnpkgVersion

import hatcher


_R_RUNTIME = re.compile("""
    ^(?P<language>[\w]+)_runtime
    _
    (?P<version>[^_]+)
    _
    (?P<build_system_version>[^_]+)
    _
    (?P<platform>[^_]+)
    _
    (?P<build>\d+)
    \.
    (?P<extension>.+$)
    """, re.VERBOSE)


def python_tag_name(tag):
    if tag is None:
        return 'none'
    return tag


class RuntimeMetadata(object):
    _PYTHON_VERSION_TO_PYTHON_TAG = {
        "3.4": "cp34",
        "3.3": "cp33",
        "3.2": "cp32",
        "3.1": "cp31",
        "3.0": "cp30",
        "2.7": "cp27",
        "2.6": "cp26",
        "2.5": "cp25",
    }
    _VERSION_PREFIX_RE = re.compile(r'^(?P<version>\d+\.\d+)\.\d+$')

    def __init__(self, language, version, build, platform,
                 build_system_version, file_format, path):
        self.language = language
        self.version = version
        self.build = build
        self.platform = platform
        self.build_system_version = build_system_version
        self.file_format = file_format
        self._sha256 = None
        self.path = path

    @property
    def full_version(self):
        return '{0}-{1}'.format(self.version, self.build)

    @property
    def python_tag(self):
        match = self._VERSION_PREFIX_RE.match(self.version)
        if match is None:
            raise ValueError(
                'Unrecognized Python version: {0!r}'.format(self.version))
        version_prefix = match.group('version')
        if version_prefix not in self._PYTHON_VERSION_TO_PYTHON_TAG:
            raise ValueError(
                'Unsupported Python version: {0!r}'.format(self.version))
        return self._PYTHON_VERSION_TO_PYTHON_TAG[version_prefix]

    @property
    def filename(self):
        return os.path.basename(self.path)

    @property
    def sha256(self):
        if self._sha256 is None:
            self._sha256 = compute_sha256(self.path)
        return self._sha256

    @classmethod
    def from_file(cls, path, platform=None):
        basename = os.path.basename(path)
        m = _R_RUNTIME.match(basename)
        if m is None:
            raise ValueError('Invalid format for {0}'.format(path))
        attrs = m.groupdict()
        attrs['file_format'] = attrs.pop('extension')
        attrs['build'] = int(attrs['build'])
        return cls(path=path, **attrs)


class EggMetadata(object):

    def __init__(self, metadata, path):
        self._egg_metadata = metadata
        self._sha256 = None
        self.path = path

    @property
    def full_version(self):
        return str(self._egg_metadata.version)

    @property
    def python_tag(self):
        return self._egg_metadata.python_tag_string

    @property
    def name(self):
        return self._egg_metadata.egg_basename

    @property
    def sha256(self):
        if self._sha256 is None:
            self._sha256 = compute_sha256(self.path)
        return self._sha256

    @classmethod
    def from_file(cls, path):
        metadata = file_formats.EggMetadata.from_egg(path)
        return cls(metadata, path)


class _SorterMixin(object):

    def __init__(self, key):
        self.key = key

    def _assert_can_compare(self, other):
        cls = type(self)
        if not isinstance(other, cls):
            msg = "Cannot compare {0!r} and {1!r}"
            raise TypeError(msg.format(cls, type(other)))

    def __eq__(self, other):
        self._assert_can_compare(other)
        return self.key == other.key

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        self._assert_can_compare(other)
        return self.key < other.key

    def __le__(self, other):
        return not (self > other)

    def __gt__(self, other):
        self._assert_can_compare(other)
        return self.key > other.key

    def __ge__(self, other):
        return not (self < other)

    def __hash__(self):
        return hash(self.key)


class AppSorter(_SorterMixin):

    def __init__(self, name, version, python_tag):
        self._name = name
        self._version = version
        self._python_tag = python_tag

        comparable_version = EnpkgVersion.from_string(version)

        key = (name.lower(), comparable_version, python_tag)
        super(AppSorter, self).__init__(key)

    def __repr__(self):
        return '{0}({1!r}, {2!r}, {3!r})'.format(
            type(self).__name__, self._name, self._version, self._python_tag)


class EggNameSorter(_SorterMixin):

    def __init__(self, egg_file_name):
        self._egg_file_name = egg_file_name
        egg_name, upstream, build = file_formats.split_egg_name(egg_file_name)
        comparable_version = EnpkgVersion.from_upstream_and_build(
            upstream, build)

        _, extension = os.path.splitext(egg_file_name)

        key = (egg_name, comparable_version, extension)
        super(EggNameSorter, self).__init__(key)

    def __repr__(self):
        return '{0}({1!r})'.format(type(self).__name__, self._egg_file_name)


def _hash_file(hasher, filename, block_size):
    with open(filename, "rb") as fp:
        while True:
            data = fp.read(block_size)
            if data == b"":
                break
            hasher.update(data)
    return hasher.hexdigest()


def compute_sha256(filename, block_size=16384):
    return _hash_file(hashlib.sha256(), filename, block_size)


def compute_md5(filename, block_size=16384):
    return _hash_file(hashlib.md5(), filename, block_size)


def hatcher_user_agent():
    return 'hatcher/{0} {1}'.format(
        hatcher.__version__, requests_user_agent())

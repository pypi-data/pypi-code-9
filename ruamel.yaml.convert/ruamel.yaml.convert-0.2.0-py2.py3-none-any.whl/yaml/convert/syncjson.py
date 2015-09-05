# encode: utf-8
"""
SyncJSON provides basic routines to synchronise JSON and YAML data
"""

from __future__ import print_function

__all__ = ['SyncJSON', 'SyncJSONException', 'datetime_to_time']

import os
import sys
import datetime
from glob import glob
import hashlib

import ruamel.yaml
from ruamel.yaml.comments import CommentedMap
from ruamel.yaml.scalarstring import PreservedScalarString

if sys.version_info < (3,):
    string_types = basestring,
else:
    string_types = str,
if sys.version_info < (2, 7):
    import simplejson as json
else:
    import json


class SyncJSONException(BaseException):
    pass


class SyncJSON(object):
    def __init__(self):
        self._load_json_with_yaml = False

    def json_yaml_all(self, src_dir, target_dir=None, json_pattern=None):
        """target_dir equals src_dir if not given
        json_pattern allows selecting specfic files
        """
        self._src_dir = src_dir
        self._target_dir = target_dir if target_dir is not None else src_dir
        self._json = "*.json" if json_pattern is None else json_pattern
        for file_name in glob(os.path.join(self._src_dir, self._json)):
            base_name_no_ext = os.path.splitext(os.path.basename(file_name))[0]
            yaml_name = os.path.join(self._target_dir, base_name_no_ext) + \
                '.yaml'
            self.json_yaml(file_name, yaml_name)

    def json_yaml(self, json_name, yaml_name):
        """convert a single file from json to yaml

        overload/replace the individual steps, most likely json_yaml_adapt

        """
        self.json_yaml_save(
            yaml_name,
            self.json_yaml_adapt(
                self.json_yaml_load(json_name)
            )
        )
        self.json_yaml_touch(json_name, yaml_name)

    def json_yaml_load(self, json_name):
        """
        don't load with RoundTripLoader here to keep order of keys, it will also give you
        the often unwanted flow style for everything
        """
        return json.load(open(json_name), object_pairs_hook=CommentedMap)

    def json_yaml_adapt(self, data):
        if isinstance(data, dict):
            for k in data:
                v = data[k]
                if isinstance(v, string_types):
                    if '\n' in v:
                        data[k] = PreservedScalarString(v)
                        continue
        elif isinstance(data, list):
            pass
        return data

    def json_yaml_save(self, yaml_name, data):
        ruamel.yaml.dump(
            data,
            open(yaml_name, 'w'),
            Dumper=ruamel.yaml.RoundTripDumper,
            allow_unicode=True
        )

    def json_yaml_touch(self, json_name, yaml_name):
        t = os.path.getmtime(json_name)
        os.utime(yaml_name, (t, t))

    def yaml_json(self, yaml_name, json_name):
        """convert a single file from json to yaml

        overload/replace the individual steps, most likely yaml_json_adapt

        """
        self.yaml_json_save(
            json_name,
            self.yaml_json_adapt(
                self.yaml_json_load(yaml_name)
            )
        )
        self.yaml_json_touch(yaml_name, json_name)

    def yaml_json_load(self, yaml_name):
        return ruamel.yaml.load(open(yaml_name), Loader=ruamel.yaml.SafeLoader)

    def yaml_json_adapt(self, data):
        if isinstance(data, dict):
            for k in data:
                v = data[k]
                if isinstance(v, datetime.date):
                    data[k] = data[k].strftime('%Y-%m-%d')
                elif isinstance(v, datetime.datetime):
                    data[k] = data[k].strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(data, list):
            pass
        return data

    def yaml_json_save(self, json_name, data):
        json.dump(data, open(json_name, 'w'), indent=2, sort_keys=True)

    def yaml_json_touch(self, yaml_name, json_name):
        t = os.path.getmtime(yaml_name)
        os.utime(json_name, (t, t))

    def equal_all(self, src_dir, target_dir=None, json_pattern=None):
        """target_dir equals src_dir if not given.
        json_pattern allows selecting specfic files
        """
        different = []
        self._src_dir = src_dir
        self._target_dir = target_dir if target_dir is not None else src_dir
        self._json = "*.json" if json_pattern is None else json_pattern
        for file_name in glob(os.path.join(self._src_dir, self._json)):
            yaml_name = repext(file_name, '.yaml', target_dir)
            if not self.equal(file_name, yaml_name):
                different.append(file_name)
        if not different:
            return
        raise SyncJSONException(different)

    def equal(self, json_name, yaml_name):
        """load json and yaml data and compare after adapting yaml data"""
        json_data = json.load(open(json_name))
        yaml_data = ruamel.yaml.load(open(yaml_name),
                                     Loader=ruamel.yaml.SafeLoader)
        yaml_data = self.yaml_json_adapt(yaml_data)
        if json_data != yaml_data:
            for k in json_data:
                if json_data[k] != yaml_data[k]:
                    print(k)
        return json_data == yaml_data

    def sync(self, json_path=None, yaml_path=None,
             json_pattern=None, yaml_pattern=None,
             last_synced=None):
        """target_dir equals src_dir if not given
            json_pattern allows selecting specfic files
            """
        # print('calling sync2', json_path, yaml_path, last_synced)
        assert last_synced is not None
        if json_path is None:
            assert yaml_path is not None
            json_path = yaml_path
        elif yaml_path is None:
            yaml_path = json_path

        if json_pattern is None:
            json_pattern = "*.json"
        if yaml_pattern is None:
            yaml_pattern = '*.yaml'

        json_files = [fn for fn in glob(os.path.join(json_path, json_pattern))]
        yaml_files = [fn for fn in glob(os.path.join(yaml_path, yaml_pattern))]

        # lists of files to convert are created first, as none will be synced
        # if there are files that were touched on both the json and yaml side
        j2y = []
        y2j = []
        both = []

        for fn in json_files[:]:
            yfn = repext(fn, '.yaml', yaml_path)
            if yfn not in yaml_files:
                j2y.append((fn, yfn))
                json_files.remove(fn)
        for fn in yaml_files[:]:
            jfn = repext(fn, '.json', json_path)
            if jfn not in json_files:
                y2j.append((fn, jfn))
                yaml_files.remove(fn)
        # json_files and yaml_files should now have the same list of files
        assert len(json_files) == len(yaml_files)
        for full_json in json_files[:]:
            full_yaml = repext(full_json, '.yaml', yaml_path)
            assert full_yaml in yaml_files
            if os.path.getmtime(full_json) < last_synced:
                if os.path.getmtime(full_yaml) > last_synced:
                    y2j.append((full_yaml, full_json))
            else:
                if os.path.getmtime(full_yaml) <= last_synced:
                    j2y.append((full_json, full_yaml))
                else:
                    both.append((full_json, full_yaml))
        if both:
            raise SyncJSONException('Both changed: {0}'.format(both))
        for jfn, yfn in j2y:
            self.json_yaml(jfn, yfn)
        for yfn, jfn in y2j:
            self.yaml_json(yfn, jfn)

    def split(self, combine_name, yaml_path):
        file_names = []
        with open(combine_name) as cfp:
            file_name = None
            sha = None
            data = ''
            for idx, line in enumerate(cfp):
                if line == '...\n' or line == '---\n':
                    if file_name:
                        changed = False
                        full_path = os.path.join(yaml_path, file_name)
                        if not os.path.exists(full_path):
                            changed = True
                        elif hashlib.sha256(data.encode('utf-8')).hexdigest() != sha:
                            changed = True
                        if changed:
                            file_names.append(file_name)
                            d = ruamel.yaml.load(data, Loader=ruamel.yaml.RoundTripLoader)
                            with open(full_path, 'w') as fp:
                                ruamel.yaml.dump(
                                    d, fp,
                                    Dumper=ruamel.yaml.RoundTripDumper,
                                    allow_unicode=True,
                                )
                    file_name = None
                    sha = None
                    data = ''
                    continue
                if file_name is None and line.startswith("# file: "):
                    file_name = line.split(': ', 1)[1].strip()
                    continue
                if sha is None and line.startswith("# sha256: "):
                    sha = line.split(': ', 1)[1].strip()
                    continue
                data += line
        return file_names

    def combine(self, combine_name, yaml_path, yaml_pattern=None):
        """
        this combines the yaml files in a single file separated by
        ---
        # file:  ....
        # sha256: ....
        and ending in a line with '...'
        """
        if yaml_pattern is None:
            yaml_pattern = '*.yaml'
        yaml_files = [fn for fn in sorted(glob(os.path.join(yaml_path, yaml_pattern)))]
        with open(combine_name, 'w') as cfp:
            for file_name in yaml_files:
                if os.path.abspath(combine_name) == os.path.abspath(file_name):
                    continue   # don't want to include combine file itself
                cfp.write('---\n# file:   {0}\n'.format(os.path.basename(file_name)))
                # appending data to cftp would be quicker, but this checks if
                # everything read as YAML to begin with (and drops '---')
                with open(file_name) as fp:
                    d = fp.read()
                    cfp.write("# sha256: {0}\n".format(hashlib.sha256(
                        d.encode('utf-8')).hexdigest()))
                    d = ruamel.yaml.load(
                        open(file_name),
                        Loader=ruamel.yaml.RoundTripLoader)
                ruamel.yaml.dump(d, cfp,
                                 Dumper=ruamel.yaml.RoundTripDumper,
                                 allow_unicode=True)
            cfp.write('...\n')


def repext(fn, ext, path=None):
    """replace extension on fn with ext, replace path if provided"""
    if path:
        fn = os.path.basename(fn)
    base = os.path.splitext(fn)[0]
    if ext:
        if ext[0] != '.':
            ext = '.' + ext
        base += ext
    if path:
        base = os.path.join(path, base)
    return base


def datetime_to_time(dt):
    """routine to convert datetimestamp accurately to time, e.g. for comparison to
    os.path.getmtime()
    """
    # using time.mktime(dt.timetuple()) loses the microseconds
    dt -= datetime.datetime.utcfromtimestamp(0)
    if sys.version_info < (2, 7):
        return ((86400*dt.days + dt.seconds)*1000000 + dt.microseconds) / 1e6
    return dt.total_seconds()

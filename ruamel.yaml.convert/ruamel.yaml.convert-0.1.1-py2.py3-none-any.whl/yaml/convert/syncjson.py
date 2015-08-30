
from __future__ import print_function
__all__ = ['SyncJSON', 'SyncJSONException']

import os
from glob import glob
import json

import ruamel.yaml
from ruamel.yaml.comments import CommentedMap


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
        if self._load_json_with_yaml:
            raise NotImplementedError
        else:
            data = json.load(open(json_name))
        d = CommentedMap()
        for k in sorted(data):
            d[k] = data[k]
        ruamel.yaml.dump(
            d,
            open(yaml_name, 'w'),
            Dumper=ruamel.yaml.RoundTripDumper,
            allow_unicode=True
        )

    def yaml_json(self, yaml_name, json_name):
        data = ruamel.yaml.load(open(yaml_name),
                                Loader=ruamel.yaml.SafeLoader)
        json.dump(data, open(json_name, 'w'), indent=2, sort_keys=True)

    def equal_all(self, src_dir, target_dir=None, json_pattern=None):
        """target_dir equals src_dir if not given
            json_pattern allows selecting specfic files
            """
        different = []
        self._src_dir = src_dir
        self._target_dir = target_dir if target_dir is not None else src_dir
        self._json = "*.json" if json_pattern is None else json_pattern
        for file_name in glob(os.path.join(self._src_dir, self._json)):
            base_name_no_ext = os.path.splitext(os.path.basename(file_name))[0]
            yaml_name = os.path.join(self._target_dir, base_name_no_ext) + \
                '.yaml'
            if not self.equal(file_name, yaml_name):
                different.append(file_name)
        if not different:
            return
        raise SyncJSONException(different)

    def equal(self, json_name, yaml_name):
        json_data = json.load(open(json_name))
        yaml_data = ruamel.yaml.load(open(yaml_name),
                                     Loader=ruamel.yaml.SafeLoader)
        return json_data == yaml_data

    def sync(self, src_dir, target_dir=None, json_pattern=None,
             last_synced=None):
        """target_dir equals src_dir if not given
            json_pattern allows selecting specfic files
            """
        assert last_synced is not None
        self._src_dir = src_dir
        self._target_dir = target_dir if target_dir is not None else src_dir
        self._json = "*.json" if json_pattern is None else json_pattern
        todo_json_yaml = []
        todo_yaml_json = []
        both_changed = []
        for json_name in glob(os.path.join(self._src_dir, self._json)):
            base_name_no_ext = os.path.splitext(os.path.basename(json_name))[0]
            yaml_name = os.path.join(self._target_dir, base_name_no_ext) + \
                '.yaml'
            if os.path.getmtime(json_name) < last_synced:
                if os.path.getmtime(yaml_name) < last_synced:
                    continue    # both older than last sync
                todo_yaml_json.append((yaml_name, json_name))
            else:
                if os.path.getmtime(yaml_name) > last_synced:
                    # yuck, both newer than last sync
                    both_changed.append((json_name, yaml_name))
                else:
                    todo_json_yaml.append((json_name, yaml_name))
        if both_changed:
            raise SyncJSONException('Both changed: {0}'.format(both_changed))
        for fns in todo_json_yaml:
            self.json_yaml(*fns)
        for fns in todo_yaml_json:
            self.yaml_json(*fns)

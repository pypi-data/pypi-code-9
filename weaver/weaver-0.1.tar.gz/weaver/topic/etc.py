import json
from os.path import join
from fabric.api import *
from weaver.utils import _

# === Helpers
def load_json(fname):
    _file = open(fname)
    _schema = json.load(_file)
    return _schema

@task
def json_cmp(expected, actual):
    """
    Takes two json files and shows difference between two
    """
    def _json_cmp(path, data):
        with open(path, "w") as fh:
            out = json.dumps(data, indent = 0, sort_keys =
                True).replace("\\","")
            fh.write(out)
    json1 = load_json(expected)
    json2 = load_json(actual)
    expected_out = "/tmp/test_expected.json"
    actual_out = "/tmp/test_result.json"
    _json_cmp(expected_out, json1)
    _json_cmp(actual_out, json2)
    env.run(_("vimdiff {expected_out} {actual_out}"))

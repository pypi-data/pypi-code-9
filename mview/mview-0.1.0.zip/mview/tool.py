__author__ = 'Zhichao HAN'


import os
import tempfile
import subprocess

import pandas as pd


def show_by_tool(data, exec_=None, verbose=False):
    import mview
    if exec_ is None:
        exec_ = mview.config.get('executor')
    assert type(data) == pd.DataFrame

    fh, filename = tempfile.mkstemp(suffix='.csv')
    os.close(fh)
    data.to_csv(filename)
    if len(exec_) > 0:
        cmd = '%s %s' % (exec_, filename)
    else:
        cmd = filename
    if verbose:
        print cmd
    assert subprocess.check_call(cmd, shell=True) == 0
    os.remove(filename)
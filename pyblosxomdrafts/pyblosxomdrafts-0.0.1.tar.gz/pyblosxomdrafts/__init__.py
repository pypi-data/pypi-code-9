__author__      = "Sean Hammond pyblosxomdrafts at seanh dot cc"
__version__     = "0.1"
__url__         = "https://github.com/seanh/pyblosxomdrafts"
__description__ = ("A Pyblosxom plugin that lets you save draft entries")


import os

from Pyblosxom import tools


def verify_installation(request):
    return True


def cb_prepare(args):
    data = args['request'].get_data()
    # Do show drafts on their own permalink pages.
    if data['bl_type'] == 'file':
        return

    # Filter drafts out on non-permalink pages.
    data['entry_list'] = [
        e for e in data['entry_list']
        if 'drafts' not in e.get_metadata('absolute_path').split(os.path.sep)]

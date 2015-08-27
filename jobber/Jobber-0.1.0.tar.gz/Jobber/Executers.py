import os
from . import LocalJobExecuter, DRMAAJobExecuter

__author__ = 'rodak'
executers = {"local": LocalJobExecuter.DRMAAJobActor,
             "drmaa": DRMAAJobExecuter.DRMAAJobActor}

try:
    from sys import path
    path.append(os.path.join(os.path.expanduser("~"), ".jobber"))
    from executers import local_executers
    if not isinstance(local_executers, dict):
        raise Exception("local_executers should be a dictionary not a %s" % str(type(local_executers)))
    executers = executers.update(local_executers)
except ImportError:
    pass

# execfile(os.path.dirname(os.path.realpath(__file__))+"/executers.py")
# execfile("./executers.py")


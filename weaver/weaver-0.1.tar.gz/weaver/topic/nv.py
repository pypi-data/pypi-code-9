import glob
from os.path import join
from weaver import get_service_name

from fabric.api import *

# === CONF
NV_PATH = "/Users/kevinlin/Dropbox/Apps/NV"
PROJECT_PREFIX = 'p'
GLUE_TASK = 'todo.tt'

class Config(object):
    config = {}

@task
def tt(project):
    """
    Get tasks for project
    """
    sr = env.service_registry[get_service_name(__file__)]
    nv_path = sr.get('nv_path')
    project_prefix = sr.get('project_prefix')
    glue_task = sr.get('glue_task')

    name = ".".join([PROJECT_PREFIX, project, GLUE_TASK])
    path = join(NV_PATH, name)
    tasks = glob.glob(path + ".[0-9][0-9.-]-*")
    clean_tasks = []
    #TODO:use regex
    for t in tasks:
        clean_tasks.append(t[t.index('--') + 2:t.index('.txt')])
    print(clean_tasks)
    return clean_tasks


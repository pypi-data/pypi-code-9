from os.path import join

from weaver import ServiceRegistry
from weaver import helpers
from weaver.contrib.noah import config, utils as nutils
from weaver.contrib.noah.node import Node, Edge
from weaver.utils import _
from fabric.api import *

SR = ServiceRegistry.get_service_registry()
SR.register("noah", config.config)
SERVICE_NAME = 'noah'

__all__ = ["ls", "clean", "graph"]

def conf():
    domain = helpers.get_domain('stage')
    service = helpers.get_service()
    return SR.get_thread_config(service, [domain])

@task
def ls():
    root = conf()['NV_ROOT']
    print(root)
    local(_("ls {root}"))

@task
def clean():
    """
    Clean bad files from noah
    """
    root = conf()['NV_ROOT']
    all_files = nutils.get_all_files(root)
    get_empty_files(root, all_files)

@task
def graph():
    """
    Build graph
    """
    node_root = conf()['NODE_ROOT']
    print _build_graph(node_root)

#TODO: implement max_depth
def _build_graph(start_node, max_depth = None):
    Q = []
    visited = set()
    graph = Node(start_node)
    depth = 0

    fh = get_node(start_node)
    links = nutils.get_all_links(fh)
    visited.add(start_node)
    for l in links:
        Q.append(Edge(start_node, l))

    acc = 0
    while Q:
        prev, cur = Q.pop(0)
        graph.add_edge(Edge(prev, cur))
        print("prev: %s, cur: %s" % (prev, cur))

        if cur not in visited:
            visited.add(cur)
            try:
                fh = get_node(cur)
                links = nutils.get_all_links(fh)
            except IOError:
                links = []
            Q.extend([Edge(cur, l) for l in links])
        acc += 1

        if acc >= 3:
            break
    return graph


# --- Helpers
def get_empty_files(root, fnames):
    """
    Include empty files and files w/only the frontmatter
    """
    for fname in fnames:
        path = join(root, fname)
        f, b = nutils.split_frontmatter_and_body(open(path))
        if not b:
            print("%s is empty" % fname)

def get_node(name):
    """
    Args:
        name of node (no extensions)
    Throws:
        IOError
    """
    root = conf()['NV_ROOT']
    path = join(root, name + '.txt')
    return open(path)

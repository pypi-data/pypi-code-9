from pprint import pprint
from fabric.api import *
from weaver.utils import _
from weaver import helpers

# --- Helpers
def is_prod(stage):
    return stage.lower() == 'prod'

def is_desktop(stage):
    return stage.lower() == 'desktop'

def get_service_name(_file):
    """
    Service name is basename of file without file suffix
    """
    return os.path.basename(_file).replace(".pyc","").replace(".py","")

# --- Meta Tasks

def _local(*args, **kwargs):
    #TODO: make this configurable
    local("source ~/.zshrc")
    local(*args, **kwargs)

# --- Tasks

@task
def domain(name,value):
    """ set a domain """
    env.domain[name] = value

@task
def stage(stage):
    """ Set the stage """
    env.stage = stage
    #domain('stage', stage)

@task
def region(region):
    env.region = region

@task
def service(service):
    """
    Initializes service.
    Looks in the service registry and initializes it with current env
    """
    env.service_registry.initialize_service(service)
    meta = env.service_registry.meta
    config = env.service_registry.config
    #NEXT:lazy loading of services
    env.service_registry.register(service, config, meta)
    env._service_config = env.service_registry.get_thread_config(service,
            helpers.get_stage(), helpers.get_region())

@task
def debug(pdb=False):
    """
    Print out env information
    """
    pprint(env)
    if getattr(env, 'service', None):
        conf = env.service_registry.get_conf(env.service)
        pprint(conf)
    if pdb:
        import pdb; pdb.set_trace()

@task
def _eval(cmd):
    """ dangerous: execute a arbitrary cmd """
    eval(cmd)

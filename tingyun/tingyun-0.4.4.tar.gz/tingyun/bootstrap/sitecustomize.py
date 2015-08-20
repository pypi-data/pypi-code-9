import os
import sys
import imp
from tingyun.admin.start_log import log_bootstrap
from tingyun.api.mapper import ENV_CONFIG_FILE

log_bootstrap('Ting Yun Bootstrap = %s' % __file__)
log_bootstrap('working_directory = %r' % os.getcwd())
 
# manual load the customize module, just avoid the python module system return something cached when pythonpath changed
boot_directory = os.path.dirname(__file__)
root_directory = os.path.dirname(boot_directory)

log_bootstrap("root dir is: %s" % boot_directory)

path = list(sys.path)
if boot_directory in path:
    del path[path.index(boot_directory)]
 
try:
    (filename, pathname, description) = imp.find_module('sitecustomize', path)
except ImportError:
    pass
else:
    imp.load_module('sitecustomize', filename, pathname, description)
 
# just for verify the tingyun-admin is run in same version python interpreter with multiple process,
# avoid python application start sub process run in different python version, because pythonpath is changed, this file
# always loaded.
expected_python_prefix = os.environ.get('TINGYUN_PYTHON_PREFIX')
actual_python_prefix = os.path.normpath(sys.prefix)
expected_python_version = os.environ.get('TINGYUN_PYTHON_VERSION')
actual_python_version = '.'.join(map(str, sys.version_info[:2]))
 
python_prefix_matches = expected_python_prefix == actual_python_prefix
python_version_matches = expected_python_version == actual_python_version


log_bootstrap("expected_python_prefix == actual_python_prefix = %s" % python_prefix_matches)
log_bootstrap("expected_python_version == actual_python_version = %s" % python_version_matches)

if python_prefix_matches and python_version_matches:
    config_file = os.environ.get(ENV_CONFIG_FILE, None)
    log_bootstrap("get the config file: %s" % config_file, close=True)

    if config_file is not None:
        # When installed as an egg with buildout, the root directory for
        # packages is not listed in sys.path and scripts instead set it
        # after Python has started up. This will cause importing of
        # 'tingyun' module to fail.
   
        if root_directory not in sys.path:
            sys.path.insert(0, root_directory)
   
        import tingyun.agent
   
        # Finally initialize the agent.
        tingyun.agent.initialize(config_file=config_file)
#
"""
Make arguments local urls


"""
import os,sys
import shlex
import string
import subprocess
from module_env import BaseEnvironment, ModuleEnvironmentError

class ScriptEnvironment(BaseEnvironment):
    """Run an external script for environment prep
    """
    name       = "Local"

    def __init__(self, runner, **kw):
        super(ScriptEnvironment, self).__init__(runner, **kw)
        
    def process_config(self, runner):
        """Runs before the normal command but after read the config"""
        


        
    def setup_environment(self, runner):
        'read the mex inputs and map all bisque urls to local files'

        runner.log ("Execute setup '%s' in %s" % (" ".join (self.script + ['setup']), os.getcwd()))
        if subprocess.call(self.script + ['setup'])!=0:
            raise ModuleEnvironmentError("Error during setup")
        
    def teardown_environment(self, runner):
        'read the outputs  map all local files to bisque urls'
        runner.log ("Execute teardown '%s' in %s" % (" ".join(self.script+['teardown']), os.getcwd()))
        if subprocess.call(self.script + ['teardown'])!= 0:
            raise ModuleEnvironmentError("Error during teardown")
            

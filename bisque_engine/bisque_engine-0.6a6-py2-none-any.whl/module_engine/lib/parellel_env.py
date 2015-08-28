#
"""
Prepare for a multiple execution evironment

"""
import os,sys
import shlex
import string
import subprocess
from module_env import BaseEnvironment, ModuleEnvironmentError

class ParallelEnvironment(BaseEnvironment):
    """Run an external script for environment prep
    """
    name       = "_Parallel"

    def __init__(self, runner, **kw):
        super(ScriptEnvironment, self).__init__(runner, **kw)
        runner.check_multirun = True
        
    def process_config(self, runner):
        """Runs before the normal command but after read the config"""

        #Fetch the mex and look for multiple runs

        runner.process_submexes(

        
        
    def setup_environment(self, runner):
        'determine using  parallel mex and process elements'
        runner.log ("Execute setup '%s' in %s" % (" ".join (self.script + ['setup']), os.getcwd()))
        
    def teardown_environment(self, runner):
        'determine if useing paralellel mex and close all'
        runner.log ("Execute teardown '%s' in %s" % (" ".join(self.script+['teardown']), os.getcwd()))
            

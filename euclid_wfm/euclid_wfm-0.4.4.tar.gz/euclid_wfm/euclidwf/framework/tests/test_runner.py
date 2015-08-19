'''
Created on Jun 25, 2015

@author: martin.melchior
'''
import tempfile
from inspect import isfunction
import os
import sys
import unittest

from twisted.internet import defer
from twisted.python.failure import Failure
from pydron.dataflow.graph import Graph

from euclidwf.framework.configuration import DRM_CONFIGURE, DRM_SUBMIT,\
    DRM_CHECKSTATUS, DRM_CLEANUP, DRM_CHECKSTATUS_TIME, DRM_CHECKSTATUS_TIMEOUT,\
    DRM_PROTOCOL, WS_PROTOCOL, WS_ROOT, LOCALCACHE, WFM_PROXYFCTS, WFM_PKGDEFS,\
    WFM_SCRIPTS
from euclidwf.framework.context import CONTEXT
from euclidwf.framework.drm_access import JOB_EXECUTING, JOB_COMPLETED, JOB_ERROR
from euclidwf.framework.runner import PipelineExecution, RUNID, REPORT, PIPELINE,\
    SUBMITTED, STATUS, CONFIG, INPUTS, OUTPUTS
from euclidwf.utilities.cmd_executor import AbstractCmdExecutor


class TestRunner(unittest.TestCase):

    def setUp(self):
        # config
        self.config = _testconfig()
        # input data dict
        self.inputs = {'workdir' : 'testdir', 'a' : 'a.xml', 'b' : 'b.xml', 'logdir' : 'logs'}
        workdir=os.path.join(self.config[WS_ROOT], self.inputs['workdir'])
        os.makedirs(workdir)
        with open(os.path.join(workdir,self.inputs['a']),'w') as filea:
            filea.write("Dummy file for input a.")
        with open(os.path.join(workdir,self.inputs['b']),'w') as fileb:
            fileb.write("Dummy file for input b.")
        # script
        self.script = 'testpipeline.py'
        with open(os.path.join(self.config[WFM_SCRIPTS],self.script),'w') as pipelinefile:
            pipelinefile.write(TESTSCRIPT)
        
        # create the packagefile
        with open(os.path.join(self.config[WFM_PKGDEFS],'testpkg.py'),'w') as pkgfile:
            pkgfile.write(TESTPKG)


    def test_initialize(self):
        execution = PipelineExecution("1", self.script, self.inputs, self.config)
        execution.initialize()
        self.assertTrue(execution.proxyfcts_exist())
        self.assertTrue(self.config[WFM_SCRIPTS] in sys.path)
        self.assertTrue(self.config[WFM_PROXYFCTS] in sys.path)
        self.assertTrue(execution.pipeline and isfunction(execution.pipeline))
        self.assertIsInstance(execution.dataflow, Graph)
        self.assertEquals(1,len(execution.dataflow.get_all_ticks()))
        self.assertTrue(execution.data[CONTEXT])
        self.assertTrue(execution.traverser)
        
        
    def test_start_success(self):
        execution = PipelineExecution("1", self.script, self.inputs, self.config)
        execution.initialize()
        test_executor=TestCmdExecutor(self.config, "1", False, 0, False, JOB_COMPLETED)
        execution.callbacks._cmd_executor=test_executor
        execution.start()
        self.assertTrue(execution.outputs)
        self.assertEquals('test_exec/c.xml', execution.outputs['c'])
        self.assertEquals(1, len(execution.report))
        self.assertEquals(JOB_COMPLETED, execution.report[0]['status'])
        self.assertEquals('1', execution.report[0]['tick'])
        self.assertEquals('1', execution.report[0]['pid'])
        self.assertEquals('test_exec', execution.report[0]['path'])
        
        result_dict=PipelineExecution.todict(execution)
        self.assertEquals("1",result_dict[RUNID]) 
        self.assertTrue(result_dict[CONFIG])
        self.assertEquals("COMPLETED",result_dict[STATUS])
        self.assertTrue(result_dict[SUBMITTED])
        self.assertEquals("testpipeline",result_dict[PIPELINE]['name'])
        self.assertTrue(result_dict[REPORT])
        self.assertTrue(result_dict[INPUTS])
        self.assertTrue(result_dict[OUTPUTS])
            

    def test_start_error(self):
        execution = PipelineExecution("1", self.script, self.inputs, self.config)
        execution.initialize()
        test_executor=TestCmdExecutor(self.config, "1", False, 0, False, JOB_ERROR)
        execution.callbacks._cmd_executor=test_executor
        execution.start()
        self.assertFalse(execution.outputs)
        self.assertEquals(1, len(execution.report))
        self.assertEquals(JOB_ERROR, execution.report[0]['status'])
        self.assertEquals('1', execution.report[0]['tick'])
        self.assertEquals('1', execution.report[0]['pid'])
        self.assertEquals('test_exec', execution.report[0]['path'])
    

    def test_start_failed_submit(self):
        execution = PipelineExecution("1", self.script, self.inputs, self.config)
        execution.initialize()
        test_executor=TestCmdExecutor(self.config, "1", True, 0, False, JOB_ERROR)
        execution.callbacks._cmd_executor=test_executor
        execution.start()
        self.assertFalse(execution.outputs)
        self.assertEquals(1, len(execution.report))
        self.assertEquals('n/a', execution.report[0]['status'])
        self.assertEquals('1', execution.report[0]['tick'])
        self.assertEquals('n/a', execution.report[0]['pid'])
        self.assertEquals('test_exec', execution.report[0]['path'])
        self.assertTrue(execution.stacktrace)


def _testconfig():
    config={}
    tmpdir=tempfile.mkdtemp()
    config[DRM_CONFIGURE]="configure"
    config[DRM_SUBMIT]="submit"
    config[DRM_CHECKSTATUS]="checkstatus"
    config[DRM_CLEANUP]="cleanup"

    config[DRM_CHECKSTATUS_TIME]=10
    config[DRM_CHECKSTATUS_TIMEOUT]=100000000

    config[DRM_PROTOCOL]="local"

    config[WS_PROTOCOL]="file"
    config[WS_ROOT]=os.path.join(tmpdir,"workspace")
    config[LOCALCACHE]=os.path.join(tmpdir,"localcache")

    config[WFM_PROXYFCTS]=os.path.join(tmpdir,"code","proxyfcts")
    config[WFM_PKGDEFS]=os.path.join(tmpdir,"code","pkgdefs")
    config[WFM_SCRIPTS]=os.path.join(tmpdir,"code","scripts")
    
    os.makedirs(config[WS_ROOT])    
    os.makedirs(config[LOCALCACHE])
    os.makedirs(config[WFM_PROXYFCTS])
    os.makedirs(config[WFM_PKGDEFS])
    os.makedirs(config[WFM_SCRIPTS])

    return config


TESTPKG='''
from euclidwf.framework.taskdefs import Package, Executable, Input, Output, ComputingResources

euclid_spe_test=Package("testpkg", executables=[
    Executable("test_exec",
       inputs=[Input("a"), Input("b")], 
       outputs=[Output("c")],
       resources=ComputingResources(num_cores=1, ram=1.0, walltime=0.0001)
    )])

'''

TESTSCRIPT='''
from euclidwf.framework.workflow_dsl import pipeline
from proxy_functions_testpkg import test_exec

@pipeline(outputs=('c'))        
def testpipeline(a,b):
    return test_exec(a=a,b=b)
'''

class TestCmdExecutor(AbstractCmdExecutor):

    def __init__(self, config, pid, fail_submit, numofchecks, fail_check, final_status):
        self.config=config
        self.cachedir=config[LOCALCACHE]
        self.pid=pid
        self.submit_process=self._get_submit_process(fail_submit)
        self.checkstatus_process_pending=self._get_checkstatus(JOB_EXECUTING, fail_check)
        self.checkstatus_process_final=self._get_checkstatus(final_status, fail_check)
        self.checked=0
        self.numofchecks=numofchecks
        
            
    def _get_submit_process(self, fail):
        if not fail:
            return MockProcess("job_id=%s"%self.pid, "", None)
        else:
            return MockProcess("job_id=%s"%self.pid, "Exception occurred.", Failure(ValueError("Exception occurred")))


    def _get_checkstatus(self, status, fail):
        if not fail:
            return MockProcess("status=%s"%status, "", None)
        else:
            return MockProcess("status=%s"%status, "Exception occurred.", Failure(ValueError("Exception occurred")))


    def execute(self, command):
        cmd0=command[0]
        if cmd0.startswith('submit'):
            return self._handle_submit(command)
        elif cmd0.startswith('checkstatus'):
            return self._handle_checkstatus(command)

    def _handle_checkstatus(self, cmdArray):
        self.checked+=1
        d=defer.Deferred()
        if self.checked<=self.numofchecks:
            d.callback(self.checkstatus_process_pending)
        else:
            d.callback(self.checkstatus_process_final)
        return d            


    def _handle_submit(self, cmdArray):
        taskname=cmdArray[1][len("--task="):]
        workdir=cmdArray[2][len("--workdir="):]
        inputs=cmdArray[3][len("--inputs="):]
        outputs=eval(cmdArray[4][len("--outputs="):])
        logdir=cmdArray[5][len("--logdir="):]
        outputfilepath=os.path.join(workdir, outputs['c'])
        os.makedirs(os.path.dirname(outputfilepath))
        with open(outputfilepath, 'w') as outputfile:
            outputfile.write("%s\n"%taskname)
            outputfile.write("%s\n"%workdir)
            outputfile.write("%s\n"%inputs)
            outputfile.write("%s\n"%logdir)
        d = defer.Deferred()
        d.callback(self.submit_process)
        return d
        

class MockProcess():
    
    def __init__(self, stdoutmsg, stderrmsg, reason):
        self.stdout=MockResponse(stdoutmsg, None)
        self.stderr=MockResponse(stderrmsg, None)
        self.exited=MockResponse(None, reason)
        
        
class MockResponse():
    
    def __init__(self, response, reason):
        self.response=response
        self.reason=reason
        
    def add_callback(self, method):
        method(self.response)

    def next_event(self):
        return self.reason

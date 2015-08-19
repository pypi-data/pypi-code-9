'''
Created on Apr 16, 2015

@author: martin.melchior
'''

import datetime
from enum import Enum
import logging
import os
import sys

from pydron.dataflow import graph
from pydron.interpreter.traverser import Traverser

from euclidwf.framework import context
from euclidwf.framework.configuration import WFM_PROXYFCTS, WFM_SCRIPTS, WFM_PKGDEFS
from euclidwf.framework.context import CONTEXT, serializable, WORKDIR, LOGDIR
from euclidwf.framework.graph_builder import build_graph
from euclidwf.framework.node_callbacks import NodeCallbacks
from euclidwf.framework.workflow_dsl import load_pipeline_from_file
from euclidwf.utilities.error_handling import PipelineFrameworkError
from euclidwf.generators.proxy_functions_generator import generate_proxyfcts
import traceback

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


RUNID='runid'
STATUS='status'
CONFIG='config'
SUBMITTED='submitted'
PIPELINE='pipeline'
REPORT='report'
INPUTS='inputs'
OUTPUTS='outputs'
ERRORLOG='errlog'


class ExecStatus(Enum):
    NEW = 1
    EXECUTING = 2
    FAILED = 3
    CANCELLED = 4
    COMPLETED = 5

    def __str__(self):
        return self.name

    @classmethod
    def fromstring(cls, s):
        return getattr(cls, s.upper(), None)


class PipelineExecution():
    """
    Object to keep a reference to all information needed to perform a pipeline run,
    to launch and check status of the pipeline run and to inspect the reports on the results.
    """
    def __init__(self, runid, script, inputs, config, status=ExecStatus.NEW):
        self.runid=runid
        self.script=script
        self.data=inputs
        self.config=config
        self.status=status
        self.outputs=None
        self.report=None
        self.stacktrace=None
        self.created=datetime.datetime.now()
        
        
    def initialize(self):
        '''
        First, configures PYTHONPATH so that the pipeline specification can be parsed.
        Then, loads pipeline and creates the design time graph.
        Finally, it prepares all for executing the pipeline by creating a runtime context
        and instantiating a graph traverser. 
        '''
        if not self.proxyfcts_exist():
            generate_proxyfcts(self.config[WFM_PKGDEFS], self.config[WFM_PROXYFCTS])
        add_to_path([self.config[WFM_SCRIPTS], self.config[WFM_PROXYFCTS]])
        self.path_to_script=os.path.join(self.config[WFM_SCRIPTS],self.script)
        self.pipeline=load_pipeline_from_file(self.path_to_script)  
        
        # build the design time dataflow graph
        self.dataflow = build_graph(self.pipeline)   
        
        # initialize the context
        self.data[CONTEXT]=context.create_context(self.data, self.config)
        
        # instantiate the traverser
        self.callbacks=NodeCallbacks(self.config)
        self.traverser=Traverser(self.callbacks.schedule_refinement, self.callbacks.submit_task)
        
        
    def proxyfcts_exist(self):
        return os.path.exists(self.config[WFM_PROXYFCTS]) and os.listdir(self.config[WFM_PROXYFCTS])
        
        
    def start(self):
        self.status=ExecStatus.EXECUTING
        d = self.traverser.execute(self.dataflow, self.data)
            
        def finalize(outputs):
            self.status=ExecStatus.COMPLETED
            aliases=self.dataflow.get_task_properties(graph.FINAL_TICK)['aliases']
            self.outputs={}
            for _name,_alias in aliases.iteritems():
                self.outputs[_alias]=outputs[_name]
            self.report=summary(self.traverser.get_graph())
            
        def failed(reason):
            self.status=ExecStatus.FAILED
            self.report=summary(self.traverser.get_graph())
            self.stacktrace=reason.getTraceback()
    
        d.addCallback(finalize)
        d.addErrback(failed)
        return d
   
   
    def get_status(self):
        return self.status
    
   
    def cancel(self):
        raise NotImplementedError("Cancel method not yet implemented.")


    def reset(self): 
        self.cancel()
        self.initialize()
        self.start()

           
    def todict(self):
        try:
            _dict = {RUNID:self.runid, 
                     CONFIG: self.config,
                     STATUS: str(self.status),
                     SUBMITTED: self.created.strftime("%A, %d. %B %Y %I:%M%p"),
                     PIPELINE: 
                        {'name': self.pipeline.func_name,
                         'version':'n/a',
                         'file':self.path_to_script},
                     REPORT:summary(self.traverser.get_graph())  
                    }
            if self.data:
                data = {k:v for k,v in self.data.iteritems() if k != CONTEXT}
                if CONTEXT in self.data.keys():
                    data[CONTEXT]=serializable(self.data[CONTEXT])
                _dict[INPUTS]=data
            if self.outputs:
                self.outputs[WORKDIR]=self.data[WORKDIR]
                self.outputs[LOGDIR]=self.data[LOGDIR]
                _dict[OUTPUTS]=self.outputs
            if self.stacktrace:
                _dict[ERRORLOG]=self.stacktrace
            return _dict
        except:
            _, _, exc_traceback = sys.exc_info()
            exc_msg=repr(traceback.extract_tb(exc_traceback))            
            logger.warn("Exception while dumping run object to dict - stacktrace: \n%s"%exc_msg)
            return None
    
    
    @classmethod
    def fromdict(cls, _dict):
        if RUNID not in _dict.keys():
            raise PipelineFrameworkError("Cannot load PipelineExecution object - runid not defined!")
        runid=_dict[RUNID]
        if PIPELINE not in _dict.keys():
            raise PipelineFrameworkError("Cannot load PipelineExecution object - pipeline script not defined!")
        script=_dict[PIPELINE]
        if CONFIG not in _dict.keys():
            raise PipelineFrameworkError("Cannot load PipelineExecution object - no configuration provided!")
        config=_dict[CONFIG]

        data={}
        if INPUTS in _dict.keys():
            data=_dict[INPUTS]
        if STATUS in _dict.keys():
            status = ExecStatus.fromstring(_dict[STATUS]) if isinstance(_dict[STATUS],str) else _dict[STATUS]
        else:
            status = ExecStatus.NEW
        return PipelineExecution(runid, script, data, config, status)
    

def add_to_path(locations):
    if not locations:
        return
    for loc in locations:
        sys.path.append(loc)


def summary(graph):
    return [summary_entries(tick, graph) for tick in sorted(graph.get_all_ticks())]

        
def summary_entries(tick, graph):
    props = graph.get_task_properties(tick)
    if 'summary' in props.keys() and props['summary'].workdir:
        summary=props['summary']
        path=summary.dfpath
        status=summary.status
        time=summary.lapse_time
        pid=summary.pid
        wd=os.path.join(summary.workdir,path)
        return { 'tick': str(tick), 'path':path, 'pid':pid, 'status':status, 'time':time, 'workdir':wd }
    else:
        return { 'tick': str(tick), 'path':props['path'], 'pid':'n/a', 'status':'n/a', 'time':0.0, 'workdir':'n/a' }
        
